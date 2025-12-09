---
navigation_title: Data streams
description: Learn how EDOT stores traces, metrics, and logs in Elasticsearch. Understand OTel-native and ECS-compatible storage modes, exporter behavior, and differences between Managed OTLP Endpoint and local EDOT gateways.
applies_to:
  stack:
  serverless:
    observability:
products:
  - id: cloud-serverless
  - id: observability
  - id: edot-collector
---

# EDOT data streams

{{edot}} writes telemetry data to two types of data stream schemas in {{es}}:

- OTel-native data streams (default)
- ECS-compatible data streams (for backwards compatibility with {{product.apm}})

This page provides a practical reference for which data streams EDOT uses, exporter behavior, and storage engines. For a detailed comparison of OTel data streams with classic {{product.apm}} and ECS-based integrations, refer to [OTel data streams compared to classic {{product.apm}}](./compatibility/data-streams.md).

To learn how to route OpenTelemetry (OTel) signals to custom data streams, refer to [Data stream routing](docs-content://solutions/observability/apm/opentelemetry/data-stream-routing.md).

## Exporter behavior: `otel` and `ecs`

EDOT may use two {{es}} exporters:

- `otel`: sends data to OTel-native data streams  
- `ecs`: sends data to ECS-compatible data streams  

The `ecs` exporter ensures compatibility with legacy {{product.apm}} data formats.

## Data streams used by a local deployment

When EDOT runs as a [local gateway or Collector](/reference/architecture/index.md), it writes telemetry data to different data streams depending on the storage mode and exporter configuration:

### OTel-native mode

This is the default mode. When ingesting standard OTel signals, EDOT writes to:

| Signal | Data stream |
|--------|-------------|
| Traces | `traces-otel-*` |
| Metrics | `metrics-otel-*` (TSDB-backed using `mode: time_series`) |
| Logs | `logs-otel-*` |
| Aggregated service destination metrics | `metrics-service_destination.[1m\|10m\|60m].otel-*` |

These streams follow OTel naming conventions and field structures.

### ECS-compatible mode

When the `ecs` exporter is enabled, or when ingesting data from {{product.apm}} agents using `elasticapmintake`, EDOT writes to:

- `traces-apm-*`
- `traces-apm.sampled-*`
- `metrics-apm.internal-*`
- `metrics-apm.*-*`
- `metrics-apm.service_destination.[interval]-*`
- `logs-apm.error-*`
- `logs-apm.app.*-*`

These match legacy {{product.apm-server}} behavior.

## Managed OTLP Endpoint

The {{motlp}} follows the same stream selection logic as local EDOT deployments:

- OTel-native streams for standard OTel telemetry  
- ECS-compatible streams for {{product.apm}}-formatted events  

The main difference is that {{motlp}} is a managed cloud service that handles ingestion and storage, whereas local EDOT deployments require you to manage the Collector infrastructure yourself. Ingest and storage behavior remain consistent between both approaches.

To customize which data streams your telemetry is routed to, you can use [data stream routing](docs-content://solutions/observability/apm/opentelemetry/data-stream-routing.md) with `data_stream.dataset` and `data_stream.namespace` attributes. For information about how resource attributes map to ECS fields and affect data storage, refer to [Attributes and labels](docs-content://solutions/observability/apm/opentelemetry/attributes.md).

## Field duplication

You may notice fields like:

- `resource.attributes.service.name`
- `service.name`

These are not true duplicates. Here's why:

- OTel defines attributes at multiple levels (for example: resource, span).
- EDOT stores resource attributes under `resource.attributes.*`, according to OTel specifications.
- {{kib}} dashboards and {{product.apm}} UI rely on ECS-style top-level fields like `service.name`.

For more information about how resource attributes are mapped to ECS fields and stored, refer to [Attributes and labels](docs-content://solutions/observability/apm/opentelemetry/attributes.md).

To bridge these models, EDOT aliases or copies key fields so that:

- Dashboards continue to function  
- Filters and searches behave consistently  
- OTel structure remains intact for downstream compatibility  

This duplication is intentional.

## Storage engines used by EDOT

| Data type | Storage engine |
|-----------|----------------|
| Metrics   | TSDB (`mode: time_series`) |
| Logs      | LogsDB |
| Traces    | Standard time-series model |

EDOT uses the same index templates and mappings as the rest of the Observability solution.