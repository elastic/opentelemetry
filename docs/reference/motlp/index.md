---
navigation_title: Managed inputs
description: Managed inputs are fully managed ingestion endpoints for sending telemetry to Elastic Cloud.
applies_to:
  serverless:
    observability: ga
    security: ga
  deployment:
    ech: ga
products:
  - id: cloud-serverless
  - id: observability
---

# Managed inputs [managed-inputs]

Managed inputs are fully managed ingestion endpoints for sending telemetry to {{ecloud}}. Each input exposes a protocol-specific endpoint that buffers data, applies back-pressure, and routes it into {{es}}, so you don't need to run your own ingestion infrastructure.

Managed inputs are the recommended ingestion path for {{ecloud}}. The following Managed inputs are available:

| Input | Protocol | Use it to |
| --- | --- | --- |
| [Managed OTLP Endpoint](managed-otlp-endpoint.md) | OpenTelemetry Protocol (OTLP) | Ingest OpenTelemetry logs, metrics, and traces from EDOT or upstream collectors and SDKs. |
| [Managed Prometheus Remote Write Endpoint](prometheus-remote-write.md) | Prometheus Remote Write v1 (PRW) | Ingest Prometheus metrics into {{es}} time series data streams. |
