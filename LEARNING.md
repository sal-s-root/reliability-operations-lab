# Engineering notes: Operational reliability

## Objective

Connect service checks to repeatable failure drills and an explicit definition of availability.

## Design decisions

- Probe a finite number of times and report each observation with latency and an aggregate sample success rate.
- Use a local HTTP service for a healthy check, an unknown route, and a stopped-listener failure.
- Keep a proposed request-based SLO separate from synthetic sample availability. Provide a blank incident template.

## Verification performed

| Check | Observed result |
|---|---|
| `python3 probe.py http://127.0.0.1:45627/healthz --count 2 --interval 0` | Passed; exit 0 as expected |
| `python3 probe.py http://127.0.0.1:45627/missing --count 1` | Passed; exit 1 as expected |
| `python3 probe.py http://127.0.0.1:45627/healthz --count 1 --timeout 0.2` | Passed; exit 1 as expected |
| `python3 probe.py file:///etc/hosts` | Passed; exit 2 as expected |

## What the evidence establishes

The drill validates local success and failure behavior. It does not establish production uptime, a 30-day SLO, incident experience, or an alert delivery pipeline. DNS resolution can exceed the network timeout.

## Next exercise

Add continuous metrics collection, evaluate alert noise in a lab, and rehearse recovery. Fill incident notes only with observed evidence and real timestamps.
