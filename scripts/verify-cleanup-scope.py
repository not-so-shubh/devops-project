"""Ensure cleanup rejects changed plans and never treats AccessDenied as deletion."""

import copy
import importlib.util
import unittest
from pathlib import Path
from unittest.mock import Mock

spec = importlib.util.spec_from_file_location(
    "cleanup", Path(__file__).with_name("cleanup-approved-eks.py")
)
cleanup = importlib.util.module_from_spec(spec)
spec.loader.exec_module(cleanup)


class ScopeTests(unittest.TestCase):
    def setUp(self):
        self.plan = {
            "variables": {"aws_region": {"value": cleanup.REGION}},
            "resource_changes": [
                {
                    "address": address,
                    "mode": "managed",
                    "provider_name": "registry.terraform.io/hashicorp/aws",
                    "change": {"actions": ["delete"], "before": {}},
                }
                for address in sorted(cleanup.APPROVED)
            ],
        }

    def test_exact_approved_plan(self):
        self.assertEqual(len(cleanup.check_plan(self.plan)), 33)

    def test_create_rejected(self):
        self.plan["resource_changes"][0]["change"]["actions"] = ["create"]
        with self.assertRaises(RuntimeError):
            cleanup.check_plan(self.plan)

    def test_other_region_rejected(self):
        self.plan["variables"]["aws_region"]["value"] = "ap-south-1"
        with self.assertRaises(RuntimeError):
            cleanup.check_plan(self.plan)

    def test_extra_resource_rejected(self):
        self.plan["resource_changes"].append(copy.deepcopy(self.plan["resource_changes"][0]))
        with self.assertRaises(RuntimeError):
            cleanup.check_plan(self.plan)

    def test_unrelated_resource_rejected(self):
        self.plan["resource_changes"][0]["address"] = "aws_iam_role.unrelated"
        with self.assertRaises(RuntimeError):
            cleanup.check_plan(self.plan)

    def test_duplicate_resource_rejected(self):
        self.plan["resource_changes"][0]["address"] = self.plan["resource_changes"][1]["address"]
        with self.assertRaises(RuntimeError):
            cleanup.check_plan(self.plan)

    def test_other_provider_rejected(self):
        self.plan["resource_changes"][0]["provider_name"] = "unapproved/provider"
        with self.assertRaises(RuntimeError):
            cleanup.check_plan(self.plan)

    def test_access_denied_is_not_absence(self):
        runner = cleanup.Cleanup.__new__(cleanup.Cleanup)
        runner.aws = Mock(side_effect=RuntimeError("AccessDenied"))
        with self.assertRaisesRegex(RuntimeError, "AccessDenied"):
            runner.absent("ec2", (), {"InvalidVolume.NotFound"})

    def test_confirmed_missing_is_absence(self):
        runner = cleanup.Cleanup.__new__(cleanup.Cleanup)
        runner.aws = Mock(side_effect=RuntimeError("InvalidVolume.NotFound"))
        self.assertTrue(runner.absent("ec2", (), {"InvalidVolume.NotFound"}))

    def test_present_resource_is_not_absence(self):
        runner = cleanup.Cleanup.__new__(cleanup.Cleanup)
        runner.aws = Mock(return_value={"Volumes": [{}]})
        self.assertFalse(runner.absent("ec2", (), {"InvalidVolume.NotFound"}))


if __name__ == "__main__":
    unittest.main(verbosity=2)
