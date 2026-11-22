# Availability exercise

Proposed learning target: 99.9% successful valid requests over a rolling 30 days.
A valid event is an HTTP request from a defined population, counted once.
A good event receives the expected 2xx response within the service's latency target.
The error budget is 0.1% of valid events for that same window.

The probe records a few synthetic observations. It does not measure request-based
production availability, enforce a latency objective, or calculate a 30-day SLO.
Use it to reproduce healthy and failing states. A real implementation would need
continuous metrics, request counters, latency histograms, and an alerting backend.
