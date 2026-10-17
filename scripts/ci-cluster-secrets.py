"""Disposable kind-cluster credentials. Never emit secret values into logs."""

import json
import secrets
import subprocess
from urllib.parse import quote


def apply(obj):
    subprocess.run(
        ["kubectl", "apply", "--server-side", "-f", "-"],
        input=json.dumps(obj),
        text=True,
        check=True,
    )


apply({"apiVersion": "v1", "kind": "Namespace", "metadata": {"name": "monitoring"}})
password = secrets.token_urlsafe(32)
apply(
    {
        "apiVersion": "v1",
        "kind": "Secret",
        "metadata": {"name": "stockpilot-db", "namespace": "stockpilot"},
        "stringData": {
            "username": "stockpilot",
            "password": password,
            "database-url": f"postgresql+psycopg://stockpilot:{quote(password, safe='')}@postgres:5432/stockpilot",
        },
    }
)
password = secrets.token_urlsafe(32)
apply(
    {
        "apiVersion": "v1",
        "kind": "Secret",
        "metadata": {"name": "stockpilot-grafana", "namespace": "monitoring"},
        "stringData": {"admin-user": "admin", "admin-password": password},
    }
)
