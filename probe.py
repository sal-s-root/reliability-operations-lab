#!/usr/bin/env python3
"""Run a finite HTTP availability drill; JSON lines are observations, not incidents."""
import argparse
import json
import math
import time
import urllib.request

def probe(url, timeout):
    start = time.monotonic()
    try:
        with urllib.request.urlopen(url, timeout=timeout) as response:
            status = response.status
        result = {"ok": 200 <= status < 300, "status": status}
    except (OSError, ValueError) as error:
        result = {"ok": False, "error": str(error)}
    result["latency_ms"] = round((time.monotonic() - start) * 1000, 2)
    return result

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("url")
    parser.add_argument("--count", type=int, default=5)
    parser.add_argument("--interval", type=float, default=1)
    parser.add_argument("--timeout", type=float, default=2)
    parser.add_argument("--max-failure-percent", type=float, default=0)
    args = parser.parse_args()
    if not math.isfinite(args.max_failure_percent) or not 0 <= args.max_failure_percent <= 100:
        parser.error("max-failure-percent must be finite and between 0 and 100")
    if not 1 <= args.count <= 1000:
        parser.error("count must be 1-1000")
    if not math.isfinite(args.interval) or args.interval < 0 or not math.isfinite(args.timeout) or args.timeout <= 0:
        parser.error("interval must be finite and nonnegative; timeout finite and positive")
    if not args.url.startswith(("http://", "https://")):
        parser.error("URL must use http or https")
    successes = 0
    for index in range(args.count):
        result = probe(args.url, args.timeout)
        successes += int(result["ok"])
        print(json.dumps({"sample": index + 1, **result}), flush=True)
        if index + 1 < args.count:
            time.sleep(args.interval)
    print(json.dumps({"samples": args.count, "successes": successes,
                      "sample_availability_percent": round(successes / args.count * 100, 2)}))
    return 0 if (args.count - successes) / args.count * 100 <= args.max_failure_percent else 1

if __name__ == "__main__":
    raise SystemExit(main())
