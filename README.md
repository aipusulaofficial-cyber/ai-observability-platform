# AI Observability Platform

An observability layer for AI workloads that separates telemetry from business outcomes while preserving correlation and operational context.

## Observability model
```text
request / job
   -> correlation context
   -> domain execution
   +-> logs
   +-> metrics
   +-> traces
   +-> health signals
```

Logs, metrics, traces and health endpoints have distinct responsibilities. Telemetry failures must not silently change the business result.

## Contracts
- Correlation context follows the execution boundary.
- Health signals distinguish liveness from readiness where applicable.
- Operational telemetry is structured for diagnosis.
- Domain outcomes remain separate from telemetry transport failures.

## Reliability
The implementation treats missing or failing telemetry backends as an operational concern rather than a reason to manufacture a successful domain result.

## Verification
Contract and failure-path tests validate the observability boundary. CI and security checks are part of the delivery path.

## Evidence
[ARCHITECTURE.md](ARCHITECTURE.md) · [docs/PRINCIPAL-ENGINEERING.md](docs/PRINCIPAL-ENGINEERING.md) · [ADRs](ADRs/)

**Engineering chain:** Code → Contract → Test → Security → Runtime → Observability → Deployment → Evidence.