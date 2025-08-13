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

# OpenTelemetry data streams compared to classic APM

The Elastic Distribution of OpenTelemetry (EDOT) stores telemetry data using a storage model optimized for OpenTelemetry signals. When `mapping_mode: otel` is enabled on the Elasticsearch exporter (which is the default setting), EDOT writes logs, traces, and metrics to specialized data streams aligned with OpenTelemetry semantics.

This architecture is designed for scalable observability workloads. It supports dynamic attributes, reduces mapping complexity, and avoids issues like mapping explosions or manual dimension setup.

EDOT uses Elasticsearch’s [Logs data stream (LogsDB)](docs-content://manage-data/data-store/data-streams/logs-data-stream.md) and [Time Series Data Streams (TSDS)](docs-content://manage-data/data-store/data-streams/time-series-data-stream-tsds.md) as storage backends. These are purpose-built to handle the scale and variety of observability data and improve the storage efficiency.

## Logs and traces in LogsDB

Log and trace data is stored in [LogsDB](docs-content://manage-data/data-store/data-streams/logs-data-stream.md), a storage engine optimized for high-ingest, semi-structured observability data. Benefits include:

* Storage efficiency 
* Optimized field handling for dynamic fields (for example, `attributes`)

## Metrics in TSDS

Metric data is stored using Elasticsearch’s [TSDS](docs-content://manage-data/data-store/data-streams/time-series-data-stream-tsds.md). Benefits include:

* Efficient storage using columnar compression  
* Fast aggregations 
* Automatic detection of metric dimensions (no need to manually define `time_series_dimension` in field mappings)

## Query compatibility with classic APM data streams

EDOT is designed to make OpenTelemetry data queryable using many of the same field names as classic APM (ECS-based) data streams. This helps preserve compatibility with existing dashboards, saved searches, and queries.

Query compatibility is achieved through:

* **`passthrough` fields:** Make nested OpenTelemetry fields available at the top level so they can be queried. For example, while the service name is stored at `resource.attributes.service.name`, you can query it as `service.name` (the same field name as the one used in the classic APM data stream).
* **Field aliases:** Map fields with different names in ECS and OpenTelemetry semantic conventions to a common query name to make migration easier.

For example, while OpenTelemetry stores the service name at `resource.attributes.service.name`, you can query it as `service.name` (the same field name used in the classic APM data stream).

### Limitations

Query compatibility is not complete:

* Not all ECS fields have aliases. Some integration-specific fields may require query changes.
* Custom attributes and labels are stored differently.

These differences may require updates to certain queries or visualizations.

Refer to [ECS & OpenTelemetry](ecs://reference/ecs-opentelemetry.md) for details on the available aliases and field mappings.

## Comparison with classic APM data streams

This table highlights key differences between classic Elastic APM data streams and EDOT with `mapping_mode: otel`:

| Feature                   | Classic APM (ECS-based)                                                                                                          | EDOT (`mapping_mode: otel`)                                                                                                          |
|---|---|---|
| Index mode | General-purpose data streams (logs, traces, metrics) <br><br> TSDS is not supported for classic APM. | LogsDB (logs/traces), TSDS (metrics) |
| Mapping style | Nested objects are mapped as structured fields. Some exceptions exist, such as `labels.*` and `numeric_labels.*`, where dots in field names are replaced with underscores. <br><br> ECS supports multiple field types (keyword, long, double, date, boolean, etc.) as defined in the schema. | Native OpenTelemetry fields with `passthrough`, preserving types and structure. |
| Attribute handling | Dynamic mapping. Custom attributes are stored under `labels.*` (strings) or `numeric_labels.*` (numbers); dots in field names are replaced with underscores. <br><br> See [Document examples - classic APM](#classic-apm) | Dynamic mapping with native types under `attributes.*`, preserving dots in field names. <br><br> See [Document examples - EDOT](#edot) |


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