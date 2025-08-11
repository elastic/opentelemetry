---
navigation_title: Data streams comparison
description: Learn how EDOT optimizes telemetry storage and query performance in Elastic Observability compared to classic APM.  
applies_to:
  stack:
  serverless:
    observability:
products:
  - id: cloud-serverless
  - id: observability
  - id: edot-collector
  - id: edot-sdk
---

# EDOT data streams compared to classic APM

The Elastic Distribution of OpenTelemetry (EDOT) stores telemetry data using a storage model optimized for OpenTelemetry signals. When `mapping_mode: otel` is enabled on the Elasticsearch exporter (which is the default setting), EDOT writes logs, traces, and metrics to specialized data streams aligned with OpenTelemetry semantics.

This architecture is designed for scalable observability workloads. It supports dynamic attributes, reduces mapping complexity, and avoids issues like mapping explosions or manual dimension setup.

EDOT uses Elasticsearch’s [Logs data stream (LogsDB)](docs-content://manage-data/data-store/data-streams/logs-data-stream.md) and [Time Series Data Streams (TSDS)](docs-content://manage-data/data-store/data-streams/time-series-data-stream-tsds.md) as storage backends. These are purpose-built to handle the scale and variety of observability data and improve the storage efficiency.

### Logs and traces in LogsDB

Log and trace data is stored in [LogsDB](docs-content://manage-data/data-store/data-streams/logs-data-stream.md), a storage engine optimized for high-ingest, semi-structured observability data. Benefits include:

* Optimized field handling for dynamic fields (for example, `attributes`)
* Index sorting for more efficient queries   

### Metrics in TSDS

Metric data is stored using Elasticsearch’s [TSDS](docs-content://manage-data/data-store/data-streams/time-series-data-stream-tsds.md). Benefits include:

* Efficient storage using columnar compression  
* Fast aggregations 
* Automatic detection of metric dimensions (no need to manually define `time_series_dimension` in field mappings)

## Mapping optimizations with `passthrough`

The [`passthrough`](elasticsearch://reference/elasticsearch/mapping-reference/passthrough.md) field type makes EDOT attributes available at the top level, providing query compatibility with ECS-based data streams such as those used by the classic APM.

For example, while the service name is stored at `resource.attributes.service.name`, you can query it as `service.name` (the same field name used in the classic APM data stream). This allows dashboards, saved searches, and queries built for ECS to work with EDOT data without changes.

`passthrough` also works with field aliases to map naming differences between ECS and EDOT semantic conventions. Many fields share the same name and meaning, but when names differ, aliases map them for compatibility to make migration easier. Refer to [ECS & OpenTelemetry](ecs://docs/reference/ecs-opentelemetry.md) for more information.

Key benefits of using the `passthrough` field type include:

* Query compatibility between EDOT and ECS-based data streams  
* Full query support by preserving field types and structure  
* Preventing mapping conflicts by automatically setting `subobjects: false`  
* Supporting dynamic attributes without excessive mapping growth  
* Simplifying TSDS configuration by using the `time_series_dimension` parameter, which applies to all subfields in the `passthrough` object

## Comparison with classic APM data streams

This table highlights key differences between classic Elastic APM data streams and EDOT with `mapping_mode: otel`:

## Comparison with classic APM data streams

| Feature                   | Classic APM (ECS-based)                                                                                                          | EDOT (`mapping_mode: otel`)                                                                                                          |
|---|---|---|
| Index mode | General-purpose indices (logs, traces, metrics) <br><br> TSDS is not supported for classic APM | LogsDB (logs/traces), TSDS (metrics) |
| Mapping style | ECS flattened fields: nested objects are flattened into dotted field names, with all fields stored as `keyword` unless otherwise defined | Native OpenTelemetry fields with `passthrough`, preserving types and structure |
| Attribute handling | Dynamic mapping. Custom attributes stored under `labels.*` (strings) or `numeric_labels.*` (numbers); dots in field names are replaced with underscores <br><br> See [Document examples - classic APM](#classic-apm) | Dynamic mapping with native types under `attributes.*`, preserving dots in field names <br><br> See [Document examples - EDOT](#edot) |
| Query performance | Designed for general-purpose queries; performance depends on mapping complexity and data volume | Similar query performance; LogsDB and TSDS optimize for observability data patterns |
| Metric dimension definition | Manual — requires defining dimensions as fields | Automatic using TSDS — dimensions detected from document fields |

### Document examples

#### Classic APM:

```
labels:
  cart_items: 42
  cart_total_amount: 42.0
```

#### EDOT:

```
attributes:
  cart.items: 42
  cart.total_amount: 42.0
```