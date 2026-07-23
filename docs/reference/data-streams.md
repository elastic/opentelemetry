---
navigation_title: Data streams
description: Learn how {{edot}} stores OpenTelemetry signals in Elasticsearch. Understand OTel-native and ECS-compatible data streams, exporter behavior, storage engines, and how to configure data retention.
applies_to:
  stack:
  serverless:
    observability:
products:
  - id: cloud-serverless
  - id: observability
  - id: edot-collector
---

# {{edot}} data streams

{{edot}} writes telemetry data to two types of data stream schemas in {{es}}:

- OTel-native data streams (default)
- ECS-compatible data streams (for backwards compatibility with {{product.apm}})

This page provides a practical reference for which data streams {{edot}} uses, exporter behavior, storage engines, and how to configure data retention. For a detailed comparison of OTel data streams with classic {{product.apm}} and ECS-based integrations, refer to [OTel data streams compared to classic {{product.apm}}](./compatibility/data-streams.md).

To learn how to route OpenTelemetry (OTel) signals to custom data streams, refer to [Data stream routing](docs-content://solutions/observability/apm/opentelemetry/data-stream-routing.md).

## Exporter behavior

{{edot}} uses the `otel` exporter by default, which sends data to OTel-native data streams. For backwards compatibility with legacy {{product.apm}} data formats, {{edot}} can also use the `ecs` exporter, which sends data to ECS-compatible data streams.

## Data streams used by a local deployment

When {{edot}} runs as a [local gateway or Collector](/reference/architecture/index.md), it writes telemetry data to different data streams depending on the exporter configuration and data source:

### OTel-native mode

This is the default mode. When ingesting standard OTel signals, {{edot}} writes to:

| Signal | Data stream |
|--------|-------------|
| Traces | `traces-*.otel-*` |
| Metrics | `metrics-*.otel-*` (TSDB-backed using `mode: time_series`) |
| Logs | `logs-*.otel-*` |
| Aggregated metrics | `metrics-*.[1m\|10m\|60m].otel-*` |

These streams follow OTel naming conventions and field structures.

### ECS-compatible data streams

When ingesting data from {{product.apm}} agents using the `elasticapmintake` receiver, {{edot}} automatically routes data to ECS-compatible data streams. The `elasticapmintake` receiver determines the destination data stream and internally uses ECS-compatible formatting for compatibility with legacy {{product.apm-server}} behavior. 

:::{note}
The `elasticapmintake` receiver is intended for migration use cases from classic {{product.apm}} agents. For new deployments, we recommend using OTel SDKs with the default OTel-native data streams.
:::

When the `ecs` exporter is explicitly enabled, {{edot}} writes to:

- `traces-apm-*`
- `metrics-apm.internal-*`
- `metrics-apm.*-*`
- `metrics-apm.*.[interval]-*`
- `logs-apm.error-*`
- `logs-apm.app.*-*`

These match legacy {{product.apm-server}} behavior.

## Managed OTLP Endpoint

The {{motlp}} follows the same stream selection logic as local {{edot}} deployments:

- OTel-native streams for standard OTel telemetry  
- ECS-compatible streams for {{product.apm}}-formatted events  

The main difference is that {{motlp}} is a managed cloud service that handles ingestion and storage, whereas local {{edot}} deployments require you to manage the Collector infrastructure yourself. Ingest and storage behavior remain consistent between both approaches.

To customize which data streams your telemetry is routed to, you can use [data stream routing](docs-content://solutions/observability/apm/opentelemetry/data-stream-routing.md) with `data_stream.dataset` and `data_stream.namespace` attributes.

## Field duplication

You may notice fields like:

- `resource.attributes.service.name`
- `service.name`

These are not true duplicates. Here's why:

- OTel defines attributes at multiple levels (for example: resource, span).
- {{edot}} stores resource attributes under `resource.attributes.*`, according to OTel specifications.
- {{kib}} dashboards and {{product.apm}} UI rely on ECS-style top-level fields like `service.name`.

For more information about how resource attributes are mapped to ECS fields and stored, refer to [Attributes and labels](docs-content://solutions/observability/apm/opentelemetry/attributes.md).

{{edot}} uses two mechanisms to bridge these models:

1. **Passthrough fields**: When fields are propagated from `resource.attributes` to top level (also for `scope.attributes` and `attributes`), {{edot}} uses passthrough fields with no storage overhead.

2. **Field copying**: {{edot}} performs some copying for specific fields for enrichment and compatibility purposes. This copying is separate from the passthrough mechanism. For example, conditionally copying `span.id` to `transaction.id`.

These mechanisms ensure that:

- Dashboards continue to function  
- Filters and searches behave consistently  
- OTel structure remains intact for downstream compatibility  

This duplication is intentional.

## Storage engines

The storage engine used by {{edot}} depends on which data stream the data is sent to. Different data streams use different index templates, and the index templates determine which storage engine is used.

For example:
- When {{edot}} sends to OTel-native data streams (using the `otel` exporter), the data uses the storage engines configured for those data streams.
- When {{edot}} sends to ECS-compatible data streams (using `elasticapmintake` or the `ecs` exporter), the data uses the storage engines configured for those data streams.

{{edot}} uses the same index templates and mappings as the rest of the Observability solution.

## Data stream lifecycle and retention

{{edot}} data streams have no default retention period. Backing indices roll over when they reach 50 GB or 30 days old, but data is not automatically deleted unless you configure a delete phase.

### {{ech}} and self-managed deployments

OTel-native {{edot}} data streams use the built-in ILM policies `logs`, `metrics`, and `traces@lifecycle`, as set by the `logs@settings`, `metrics@tsdb-settings`, and `traces@settings` component templates that the OTel index templates compose in {{es}}. To customize retention without modifying those managed policies, create a `@custom` component template for the relevant signal type:

| Signal | Component template |
|--------|--------------------|
| Logs   | `logs-otel@custom` |
| Metrics | `metrics-otel@custom` |
| Traces | `traces-otel@custom` |

When created, these component templates are automatically picked up by the corresponding OTel index template. For step-by-step instructions, refer to [Customize built-in ILM policies](docs-content://manage-data/lifecycle/index-lifecycle-management/tutorial-customize-built-in-policies.md).

### {{serverless-full}}

Use [Data Stream Lifecycle (DSL)](docs-content://manage-data/lifecycle/data-stream.md) to configure retention. Configuration is the same as for any other {{es}} data stream.