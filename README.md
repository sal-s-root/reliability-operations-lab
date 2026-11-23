# Reliability operations lab

Finite synthetic HTTP checks, an explicit acceptance policy, a controlled local
failure/recovery drill, and runbooks for interpreting observations.

```sh
python3 -m unittest -v
python3 probe.py http://127.0.0.1:8080/healthz --count 5
```

The default requires all samples to succeed. `--max-failure-percent 20` changes
the drill gate; it is not a rolling production SLO. The automated recovery drill
uses only its own loopback server and verifies healthy, stopped, and recovered
states without touching an existing service.

See [SLO assumptions](SLO.md), [investigation procedure](RUNBOOK.md), and the blank
[incident exercise template](INCIDENT-TEMPLATE.md). Actual timestamps and impact
belong in real exercise notes; sample fixtures are not production incident history.
For continuous metrics, dashboards, and tested multi-window alerts, use the
[observability platform](https://github.com/sal-s-root/observability-platform-lab).

## Project history

See [history and scope](HISTORY.md) for the correction of earlier synthetic dates.
