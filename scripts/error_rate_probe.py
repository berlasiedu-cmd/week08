#!/usr/bin/env python3
"""Probe an HTTP endpoint for a fixed duration and fail if the observed
error rate exceeds a threshold.

Used as an automated deployment gate in the "04 - Deploy to Production"
GitHub Actions workflow (Task 10.3HD): after a new revision is rolled
out, this script tallies HTTP 5xx responses and failed requests against
total requests over a short probing window. A non-zero exit code (error
rate above the threshold) is picked up by the workflow's next step,
which runs `kubectl rollout undo` automatically -- with no person
reading a log or pressing a button.
"""
import argparse
import sys
import time

import requests


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--url", required=True, help="Endpoint to probe")
    parser.add_argument("--duration", type=int, default=30, help="Probe duration in seconds")
    parser.add_argument("--interval", type=float, default=1.0, help="Seconds between requests")
    parser.add_argument("--threshold", type=float, default=0.10, help="Error rate (0-1) that triggers a failure")
    parser.add_argument("--timeout", type=float, default=5.0, help="Per-request timeout in seconds")
    args = parser.parse_args()

    total = 0
    errors = 0
    deadline = time.monotonic() + args.duration

    print(f"Probing {args.url} for {args.duration}s (rollback threshold={args.threshold:.0%})")

    while time.monotonic() < deadline:
        total += 1
        try:
            response = requests.get(args.url, timeout=args.timeout)
            if response.status_code >= 500:
                errors += 1
                print(f"  request {total}: HTTP {response.status_code} (server error)")
            else:
                print(f"  request {total}: HTTP {response.status_code}")
        except requests.RequestException as exc:
            errors += 1
            print(f"  request {total}: request failed ({exc})")

        time.sleep(args.interval)

    error_rate = (errors / total) if total else 1.0
    print(f"\nResult: {errors}/{total} requests failed -> error rate {error_rate:.1%}")

    if error_rate > args.threshold:
        print(f"FAIL: error rate {error_rate:.1%} exceeds threshold {args.threshold:.0%}")
        return 1

    print(f"OK: error rate {error_rate:.1%} is within threshold {args.threshold:.0%}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
