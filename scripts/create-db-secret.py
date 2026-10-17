"""Generate a Secret via kubectl stdin, without exposing a password in argv/history."""

import getpass
import json
import subprocess
from urllib.parse import quote

password = getpass.getpass("PostgreSQL password (not logged): ")
if len(password) < 16:
    raise SystemExit("Use at least 16 characters")
username = input("Database user [stockpilot]: ").strip() or "stockpilot"
host = input("Database host [postgres]: ").strip() or "postgres"
url = f"postgresql+psycopg://{quote(username, safe='')}:{quote(password, safe='')}@{host}:5432/stockpilot"
if host != "postgres":
    url += "?sslmode=verify-full"
secret = {
    "apiVersion": "v1",
    "kind": "Secret",
    "metadata": {"name": "stockpilot-db", "namespace": "stockpilot"},
    "type": "Opaque",
    "stringData": {"username": username, "password": password, "database-url": url},
}
# Client-side apply stores another copy in the last-applied annotation; use server-side apply.
subprocess.run(
    ["kubectl", "apply", "--server-side", "-f", "-"],
    input=json.dumps(secret),
    text=True,
    check=True,
)
print("Database Secret applied. Values were not written to disk.")
