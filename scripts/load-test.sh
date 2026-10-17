#!/usr/bin/env bash
set -euo pipefail
BASE_URL="${BASE_URL:-http://localhost:3000}"
REQUESTS="${REQUESTS:-120}"
for ((i=0; i<REQUESTS; i++)); do
  curl --fail --silent --show-error "$BASE_URL/api/inventory/stats" >/dev/null
  curl --silent --output /dev/null "$BASE_URL/api/products/2147483647"
  sleep 0.5
done
printf 'Generated %s valid stats requests and %s expected 404s.\n' "$REQUESTS" "$REQUESTS"
