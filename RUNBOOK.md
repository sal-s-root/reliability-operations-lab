# Health endpoint failure drill

1. Start the sibling `containerized-health-api` service on loopback port 8080.
2. Run `python3 probe.py http://127.0.0.1:8080/healthz --count 3`.
3. Stop that lab service and repeat. Expect failures and exit status 1.
4. Restore the service and repeat to verify recovery.
5. Record observed timestamps, symptoms, and evidence in your own drill notes.

For a real alert: confirm customer impact, check recent changes, inspect saturation,
identify a safe mitigation, and verify recovery from the customer path.
Do not restart or delete resources solely because one synthetic check fails.
