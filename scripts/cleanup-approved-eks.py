"""Execute the separately approved StockPilot Sydney cleanup; never discover delete targets."""

import argparse
import fcntl
import hashlib
import json
import os
import re
import subprocess
import tempfile
import time
import traceback
from datetime import datetime, timezone
from pathlib import Path

REGION = "ap-southeast-2"
CLUSTER = "stockpilot-eks"
APPROVED = {
    "aws_cloudwatch_log_group.eks",
    "aws_eip.nat",
    "aws_eks_access_entry.admin",
    "aws_eks_access_policy_association.admin",
    "aws_eks_addon.ebs",
    "aws_eks_cluster.main",
    "aws_eks_node_group.main",
    "aws_eks_pod_identity_association.ebs",
    "aws_iam_role.cluster",
    "aws_iam_role.ebs",
    "aws_iam_role.nodes",
    "aws_iam_role_policy_attachment.cluster",
    "aws_iam_role_policy_attachment.ebs",
    "aws_internet_gateway.main",
    "aws_nat_gateway.main",
    "aws_route_table.private",
    "aws_route_table.public",
    "aws_vpc.main",
}
APPROVED |= {
    f'aws_eks_addon.network["{name}"]'
    for name in ("coredns", "eks-pod-identity-agent", "kube-proxy", "vpc-cni")
}
APPROVED |= {
    f'aws_iam_role_policy_attachment.nodes["{name}"]'
    for name in (
        "AmazonEC2ContainerRegistryPullOnly",
        "AmazonEKSWorkerNodePolicy",
        "AmazonEKS_CNI_Policy",
    )
}
APPROVED |= {
    f'aws_{kind}.{scope}["{az}"]'
    for kind in ("subnet", "route_table_association")
    for scope in ("public", "private")
    for az in ("a", "b")
}


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def say(message):
    print(datetime.now(timezone.utc).strftime("%H:%M:%SZ"), message, flush=True)


def check_plan(plan):
    require(plan["variables"]["aws_region"]["value"] == REGION, "Plan region changed")
    changes = [
        r
        for r in plan.get("resource_changes", [])
        if r["mode"] == "managed" and r["change"]["actions"] != ["no-op"]
    ]
    require(len(changes) == 33, "Plan must contain the reviewed 33 changes")
    require({r["address"] for r in changes} == APPROVED, "Plan scope changed")
    require(
        all(r["change"]["actions"] == ["delete"] for r in changes),
        "Plan contains creates or updates",
    )
    require(
        all(r["provider_name"] == "registry.terraform.io/hashicorp/aws" for r in changes),
        "Unexpected provider",
    )
    return {r["address"]: r["change"]["before"] for r in changes}


class Cleanup:
    def __init__(self, review, backup_hash):
        self.review = review.resolve()
        self.root = Path(__file__).resolve().parents[1]
        self.backup_hash = backup_hash
        self.env = os.environ.copy()
        self.env.update(AWS_REGION=REGION, AWS_DEFAULT_REGION=REGION, AWS_PAGER="")
        self.env["PATH"] = str(Path.home() / ".local/bin") + ":" + self.env["PATH"]
        self.env["TF_DATA_DIR"] = tempfile.mkdtemp(prefix="stockpilot-cleanup-tf-")

    def call(self, *args):
        result = subprocess.run(args, env=self.env, text=True, capture_output=True)
        if result.returncode:
            with (self.review / "command-errors.log").open("a") as stream:
                stream.write(repr(args) + "\n" + result.stdout + result.stderr + "\n")
            match = re.search(r"An error occurred \(([^)]+)\)", result.stderr)
            code = match.group(1) if match else "CommandFailed"
            raise RuntimeError(code)
        return result.stdout

    def aws(self, service, *args):
        return json.loads(
            self.call(
                "aws",
                service,
                *args,
                "--region",
                REGION,
                "--output",
                "json",
                "--cli-connect-timeout",
                "10",
                "--cli-read-timeout",
                "60",
            )
        )

    def kube(self, *args):
        return json.loads(self.call("kubectl", "--request-timeout=30s", *args, "-o", "json"))

    def absent(self, service, args, missing_codes):
        try:
            self.aws(service, *args)
        except RuntimeError as error:
            if str(error) in missing_codes:
                return True
            raise
        return False

    def wait(self, predicate, label, seconds=600):
        deadline = time.monotonic() + seconds
        while time.monotonic() < deadline:
            if predicate():
                say("PASS: " + label)
                return
            say("Waiting: " + label)
            time.sleep(10)
        raise RuntimeError("Timed out: " + label + "; no force deletion attempted")

    def terraform(self, *args):
        return ("terraform", "-chdir=" + str(self.root / "terraform"), *args)

    def logged(self, label, *args):
        say(label)
        with (self.review / "cleanup-commands.log").open("a") as stream:
            process = subprocess.Popen(args, env=self.env, stdout=stream, stderr=stream)
            while True:
                try:
                    code = process.wait(timeout=20)
                    break
                except subprocess.TimeoutExpired:
                    say("In progress: " + label)
        require(code == 0, label + " failed; inspect private cleanup-commands.log")

    def run(self):
        require(
            self.review.is_relative_to(Path.home() / "stockpilot-private-backups"),
            "Review directory must be in the private backup directory",
        )
        lock = (self.review / "cleanup.lock").open("a")
        fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        require(
            not (self.review / "cleanup-summary.json").exists(),
            "Cleanup already completed",
        )
        assets = json.loads((self.review / "cleanup-assets.json").read_text())
        saved_plan = self.review / "aws-cleanup-review.tfplan"
        require(assets["region"] == REGION, "Asset region changed")
        require(digest(saved_plan) == assets["destroy_plan_sha256"], "Saved plan changed")
        require(
            digest(self.review / "stockpilot.dump") == self.backup_hash,
            "Backup changed",
        )
        self.logged(
            "Initialize locked Terraform provider",
            *self.terraform("init", "-input=false", "-lockfile=readonly"),
        )
        plan = json.loads(self.call(*self.terraform("show", "-json", str(saved_plan))))
        before = check_plan(plan)
        identity = self.aws("sts", "get-caller-identity")
        require(
            plan["variables"]["admin_principal_arn"]["value"].split(":")[4] == identity["Account"],
            "AWS account changed",
        )
        require(before["aws_vpc.main"]["id"] == assets["vpc_id"], "VPC changed")
        require(before["aws_vpc.main"]["cidr_block"] == "10.42.0.0/16", "VPC scope changed")
        for address, name in (
            ("cluster", "cluster"),
            ("nodes", "nodes"),
            ("ebs", "ebs-csi"),
        ):
            require(
                before["aws_iam_role." + address]["name"] == CLUSTER + "-" + name,
                "IAM role scope changed",
            )
        cluster = self.aws("eks", "describe-cluster", "--name", CLUSTER)["cluster"]
        require(
            cluster["arn"] == before["aws_eks_cluster.main"]["arn"],
            "Cluster identity changed",
        )
        require(
            cluster["resourcesVpcConfig"]["vpcId"] == assets["vpc_id"],
            "Cluster VPC changed",
        )
        require(
            self.call("kubectl", "config", "current-context").strip() == cluster["arn"],
            "kubectl context changed",
        )
        claims = self.kube("get", "pvc", "-A")["items"]
        require(len(claims) == 1, "Unexpected persistent data in this cluster")
        claim = claims[0]
        require(claim["metadata"]["namespace"] == "stockpilot", "Unexpected claim namespace")
        require(claim["metadata"]["uid"] == assets["pvc_uid"], "Database claim changed")
        require(
            claim["metadata"]["name"] == assets["pvc_name"],
            "Database claim name changed",
        )
        pv = self.kube("get", "pv", assets["pv_name"])
        require(pv["spec"]["claimRef"]["uid"] == assets["pvc_uid"], "Volume binding changed")
        require(
            pv["spec"]["csi"]["volumeHandle"] == assets["volume_id"],
            "Database volume changed",
        )
        require(
            pv["spec"]["persistentVolumeReclaimPolicy"] == "Delete",
            "Reclaim policy changed",
        )
        volume = self.aws("ec2", "describe-volumes", "--volume-ids", assets["volume_id"])[
            "Volumes"
        ][0]
        require(volume["Size"] == 5 and assets["volume_gib"] == 5, "Database size changed")
        service = self.kube("get", "svc", "traefik", "-n", "ingress-system")
        require(
            service["metadata"]["uid"] == assets["ingress_service_uid"],
            "Ingress service changed",
        )
        lbs = self.aws("elb", "describe-load-balancers")["LoadBalancerDescriptions"]
        lbs = [lb for lb in lbs if lb.get("VPCId") == assets["vpc_id"]]
        require(
            len(lbs) == 1 and lbs[0]["LoadBalancerName"] == assets["classic_load_balancer_name"],
            "Load balancer scope changed",
        )
        require(
            service["status"]["loadBalancer"]["ingress"] == [{"hostname": lbs[0]["DNSName"]}],
            "Ingress endpoint changed",
        )
        modern = self.aws("elbv2", "describe-load-balancers")["LoadBalancers"]
        require(
            not any(lb.get("VpcId") == assets["vpc_id"] for lb in modern),
            "Unexpected additional load balancer",
        )
        group = self.aws(
            "eks",
            "describe-nodegroup",
            "--cluster-name",
            CLUSTER,
            "--nodegroup-name",
            "operations",
        )["nodegroup"]
        asg_names = [x["name"] for x in group["resources"]["autoScalingGroups"]]
        require(len(asg_names) == 1, "Unexpected worker group scope")
        asgs = self.aws(
            "autoscaling",
            "describe-auto-scaling-groups",
            "--auto-scaling-group-names",
            *asg_names,
        )["AutoScalingGroups"]
        instance_ids = [x["InstanceId"] for g in asgs for x in g["Instances"]]
        require(len(instance_ids) == 2, "Unexpected worker count")
        reservations = self.aws("ec2", "describe-instances", "--instance-ids", *instance_ids)[
            "Reservations"
        ]
        roots = []
        for reservation in reservations:
            for instance in reservation["Instances"]:
                require(instance["VpcId"] == assets["vpc_id"], "Worker VPC changed")
                root = next(
                    x["Ebs"]
                    for x in instance["BlockDeviceMappings"]
                    if x["DeviceName"] == instance["RootDeviceName"]
                )
                require(root["DeleteOnTermination"], "Worker root disk would be retained")
                roots.append(root["VolumeId"])
        require(len(roots) == 2, "Unexpected root disk count")
        (self.review / "cleanup-before.json").write_text(
            json.dumps(
                {
                    "assets": assets,
                    "worker_ids": instance_ids,
                    "root_volume_ids": roots,
                    "asg_names": asg_names,
                },
                indent=2,
            )
            + "\n"
        )
        (self.review / "state-before-cleanup.json").write_text(
            self.call(*self.terraform("state", "pull"))
        )
        say("PASS: approved plan, account, backup and all live resource identities match")

        for release, namespace in (
            ("traefik", "ingress-system"),
            ("stockpilot", "stockpilot"),
        ):
            self.logged(
                "Remove " + release,
                "helm",
                "uninstall",
                release,
                "-n",
                namespace,
                "--wait",
                "--timeout",
                "10m",
            )
        current = self.kube("get", "pvc", assets["pvc_name"], "-n", "stockpilot")
        require(
            current["metadata"]["uid"] == assets["pvc_uid"],
            "Claim changed before deletion",
        )
        self.logged(
            "Delete approved database claim",
            "kubectl",
            "delete",
            "pvc",
            assets["pvc_name"],
            "-n",
            "stockpilot",
            "--wait=true",
            "--timeout=5m",
        )
        lb_args = (
            "describe-load-balancers",
            "--load-balancer-names",
            assets["classic_load_balancer_name"],
        )
        self.wait(
            lambda: self.absent(
                "elb",
                lb_args,
                {"LoadBalancerNotFound", "LoadBalancerNotFoundException"},
            ),
            "ingress load balancer deleted",
        )
        volume_args = ("describe-volumes", "--volume-ids", assets["volume_id"])
        self.wait(
            lambda: self.absent("ec2", volume_args, {"InvalidVolume.NotFound"}),
            "database EBS volume deleted",
        )
        for release, namespace in (
            ("monitoring", "monitoring"),
            ("metrics-server", "kube-system"),
        ):
            self.logged(
                "Remove " + release,
                "helm",
                "uninstall",
                release,
                "-n",
                namespace,
                "--wait",
                "--timeout",
                "5m",
            )
        require(
            digest(saved_plan) == assets["destroy_plan_sha256"],
            "Saved plan changed before apply",
        )
        self.logged(
            "Apply approved 33-resource destruction plan",
            *self.terraform("apply", "-input=false", "-no-color", str(saved_plan)),
        )

        require(
            not self.call(*self.terraform("state", "list")).strip(),
            "Terraform state is not empty",
        )
        require(
            self.absent(
                "eks",
                ("describe-cluster", "--name", CLUSTER),
                {"ResourceNotFoundException"},
            ),
            "Cluster still exists",
        )
        require(
            self.absent(
                "ec2",
                ("describe-vpcs", "--vpc-ids", assets["vpc_id"]),
                {"InvalidVpcID.NotFound"},
            ),
            "VPC still exists",
        )
        require(
            self.absent(
                "ec2",
                ("describe-addresses", "--allocation-ids", before["aws_eip.nat"]["id"]),
                {"InvalidAllocationID.NotFound"},
            ),
            "Elastic IP still exists",
        )
        require(
            not self.aws(
                "autoscaling",
                "describe-auto-scaling-groups",
                "--auto-scaling-group-names",
                *asg_names,
            )["AutoScalingGroups"],
            "Worker ASG remains",
        )
        for volume_id in [assets["volume_id"], *roots]:
            self.wait(
                lambda vid=volume_id: self.absent(
                    "ec2",
                    ("describe-volumes", "--volume-ids", vid),
                    {"InvalidVolume.NotFound"},
                ),
                "approved EBS disk absent",
                300,
            )
        try:
            remaining = self.aws("ec2", "describe-instances", "--instance-ids", *instance_ids)[
                "Reservations"
            ]
            require(
                all(i["State"]["Name"] == "terminated" for r in remaining for i in r["Instances"]),
                "Worker instance still active",
            )
        except RuntimeError as error:
            if str(error) != "InvalidInstanceID.NotFound":
                raise
        for key in ("cluster", "nodes", "ebs"):
            require(
                self.absent(
                    "iam",
                    ("get-role", "--role-name", before["aws_iam_role." + key]["name"]),
                    {"NoSuchEntity"},
                ),
                "Project IAM role remains",
            )
        logs = self.aws(
            "logs",
            "describe-log-groups",
            "--log-group-name-prefix",
            before["aws_cloudwatch_log_group.eks"]["name"],
        )["logGroups"]
        require(
            not any(
                x["logGroupName"] == before["aws_cloudwatch_log_group.eks"]["name"] for x in logs
            ),
            "Cluster log group remains",
        )
        require(
            not self.aws(
                "ec2",
                "describe-network-interfaces",
                "--filters",
                "Name=vpc-id,Values=" + assets["vpc_id"],
            )["NetworkInterfaces"],
            "Project network interface remains",
        )
        nat = self.aws(
            "ec2",
            "describe-nat-gateways",
            "--filter",
            "Name=vpc-id,Values=" + assets["vpc_id"],
        )["NatGateways"]
        require(all(x["State"] == "deleted" for x in nat), "NAT gateway remains")
        require(
            self.absent(
                "elb",
                lb_args,
                {"LoadBalancerNotFound", "LoadBalancerNotFoundException"},
            ),
            "Ingress load balancer remains",
        )
        summary = {
            "status": "PASS",
            "completed_utc": datetime.now(timezone.utc).isoformat(),
            "region": REGION,
            "terraform_managed_resources_destroyed": 33,
            "terraform_state_empty": True,
            "cluster_deleted": True,
            "worker_instances_terminated": 2,
            "approved_ebs_disks_deleted": 3,
            "load_balancer_deleted": True,
            "vpc_deleted": True,
            "nat_gateway_deleted": True,
            "elastic_ip_released": True,
            "project_iam_roles_deleted": 3,
            "cluster_log_group_deleted": True,
            "project_network_interfaces_remaining": 0,
            "database_backup_sha256": self.backup_hash,
        }
        (self.review / "cleanup-summary.json").write_text(json.dumps(summary, indent=2) + "\n")
        say("CLEANUP VERIFIED")
        print(json.dumps(summary, indent=2), flush=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--review-dir", type=Path, required=True)
    parser.add_argument("--backup-sha256", required=True)
    parser.add_argument("--execute-approved", action="store_true", required=True)
    args = parser.parse_args()
    os.umask(0o077)
    try:
        Cleanup(args.review_dir, args.backup_sha256).run()
    except Exception as error:
        if args.review_dir.is_dir():
            (args.review_dir / "cleanup-error.log").write_text(traceback.format_exc())
        say("CLEANUP STOPPED: " + str(error))
        say("Keep private logs. Do not start a second cleanup; send this status for recovery.")
        raise SystemExit(1) from None


if __name__ == "__main__":
    main()
