#!/usr/bin/env bash
# Probe one or more HTTP endpoints. Exits non-zero if any fail or exceed the latency budget.
# Usage: ./healthcheck.sh https://api.example.com/health https://web.example.com/health
set -euo pipefail

MAX_MS="${MAX_MS:-800}"
fail=0

for url in "$@"; do
  out=$(curl -s -o /dev/null -w '%{http_code} %{time_total}' --max-time 10 "$url" || echo "000 10")
  code=${out%% *}
  ms=$(awk -v t="${out##* }" 'BEGIN { printf "%d", t * 1000 }')
  if [[ "$code" =~ ^2 ]] && (( ms <= MAX_MS )); then
    printf 'OK    %s  %s  %sms\n' "$code" "$url" "$ms"
  else
    printf 'FAIL  %s  %s  %sms\n' "$code" "$url" "$ms"
    fail=1
  fi
done

exit "$fail"
