"""Assert a real scrape target and non-empty query results before claiming success."""

import json
import time
import urllib.parse
import urllib.request
from pathlib import Path

base = "http://localhost:9090/api/v1/"


def get(path):
    with urllib.request.urlopen(base + path, timeout=10) as response:
        return json.load(response)


for attempt in range(24):
    targets = get("targets")
    live = [
        t
        for t in targets["data"]["activeTargets"]
        if t.get("labels", {}).get("namespace") == "stockpilot" and t["health"] == "up"
    ]
    data = get(
        "query?"
        + urllib.parse.urlencode(
            {"query": 'sum(rate(stockpilot_http_requests_total{namespace="stockpilot"}[2m]))'}
        )
    )
    result = data["data"]["result"]
    if live and result and float(result[0]["value"][1]) > 0:
        Path("docs/evidence/prometheus-targets.json").write_text(json.dumps(targets, indent=2))
        Path("docs/evidence/prometheus-query.json").write_text(json.dumps(data, indent=2))
        print(
            f"PASS: {len(live)} StockPilot target(s) UP; request rate {result[0]['value'][1]} requests/second"
        )
        break
    time.sleep(5)
else:
    raise SystemExit("No live StockPilot target and populated rate query before deadline")
