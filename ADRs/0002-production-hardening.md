# ADR-0002: Production hardening
FastAPI is the edge contract; OpenTelemetry is initialized at startup; Helm packages Kubernetes; Terraform owns infrastructure inputs; Trivy and CycloneDX gate security and SBOM; Hypothesis and HTTP contracts test the boundary; Locust supplies repeatable load traffic.
Failure handling uses explicit health probes and bounded resources. Production externalizes state, secrets, telemetry collectors and autoscaling.
