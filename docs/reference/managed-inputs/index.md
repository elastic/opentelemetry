---
navigation_title: Managed inputs
description: Managed inputs are fully managed ingestion endpoints for sending data to Elastic Cloud.
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

Managed inputs are fully managed ingestion endpoints for sending data to {{ecloud}}. Each input exposes a protocol-specific endpoint that buffers data, applies back-pressure, and routes it into {{es}}, so you don't need to run your own ingestion infrastructure.

Managed inputs are the recommended ingestion path for {{ecloud}}. The following managed inputs are available:

| Input | Protocol | Use it to |
| --- | --- | --- |
| [Managed OTLP Endpoint](managed-otlp-endpoint.md) | OpenTelemetry Protocol (OTLP) | Ingest OpenTelemetry logs, metrics, and traces from EDOT collectors and SDKs, the {{edot-cf}}, upstream OpenTelemetry collectors and SDKs, or any OTLP-compliant shipper. |
| [Managed Prometheus Remote Write endpoint](prometheus-remote-write.md) | Prometheus Remote Write v1 (PRW) | Ingest Prometheus metrics into {{es}} time series data streams. |
| [Managed {{es}} _bulk endpoint](elasticsearch-bulk.md) | {{es}} `_bulk` API | Ingest data from `_bulk`-based shippers such as {{product.beats}}, {{product.elastic-agent}}, {{product.logstash}}, and other {{es}}-compatible shippers. |
