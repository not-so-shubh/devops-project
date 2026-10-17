"""Copy only an explicit allowlist of synthetic CI evidence into the repository."""
import json
import os
import shutil
from pathlib import Path

names = set(['pytest-postgres.txt', 'terraform-ci-validate.txt', 'terraform-ci-mock-test.txt', 'compose-ci.txt', 'compose-ci.log', 'compose-smoke.txt', 'metrics.txt', 'frontend-desktop.png', 'frontend-mobile.png', 'kubernetes-ci.txt', 'helm-release-ci.txt', 'hpa-metrics-ci.txt', 'cluster-pods-ci.txt', 'cluster-events-ci.txt', 'migration-ci.log', 'prometheus-targets.json', 'prometheus-query.json', 'grafana-dashboard.png', 'prometheus-targets.png', 'trivy-backend.json', 'trivy-frontend.json'])
destination=Path('docs/evidence')
destination.mkdir(parents=True,exist_ok=True)
written=[]
for source in Path(os.environ['EVIDENCE_DOWNLOAD_DIR']).rglob('*'):
    if source.is_file() and source.name in names:
        shutil.copy2(source,destination/source.name)
        written.append(source.name)
metadata={'source_sha':os.environ['GITHUB_SHA'],'run_id':os.environ['GITHUB_RUN_ID'],
          'run_url':f"https://github.com/{os.environ['GITHUB_REPOSITORY']}/actions/runs/{os.environ['GITHUB_RUN_ID']}",
          'files':sorted(set(written)), 'scope':'Real disposable CI PostgreSQL/Compose/kind evidence; AWS apply/destroy not performed.'}
(destination/'ci-run.json').write_text(json.dumps(metadata,indent=2)+'\n')
print(f'Archived {len(set(written))} allowed evidence files; no credentials or raw browser traces copied.')
