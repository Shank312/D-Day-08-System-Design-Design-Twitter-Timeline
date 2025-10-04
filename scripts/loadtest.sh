

#!/usr/bin/env bash
set -euo pipefail
echo "Running k6 home timeline test..."
k6 run loadtest/k6-home-timeline.js || true
echo "Running Locust..."
locust -f loadtest/locustfile.py --headless -u 100 -r 10 -t 1m || true
