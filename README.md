# Reliability operations lab

## Purpose

Connect monitoring observations to failure drills, service objectives, and operational documentation.

## Run locally

```sh
python3 probe.py http://127.0.0.1:8080/healthz --count 5
# Start the sibling health API first; see RUNBOOK.md for a failure drill.
```

## Scope and limitations

Synthetic samples are not production SLO evidence. Probe only authorized endpoints; OS DNS resolution can exceed the HTTP timeout.

## Engineering notes

See [LEARNING.md](LEARNING.md) for the design decisions, verification evidence,
and next steps. Never commit credentials, private hostnames, or real incident data.
