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

The Elastic Distribution of OpenTelemetry (EDOT) stores telemetry data using a storage model optimized for OpenTelemetry signals. When `mapping_mode: otel` is enabled, EDOT writes logs, traces, and metrics to specialized data streams aligned with OpenTelemetry semantics to improve efficiency.

This architecture is designed for scalable observability workloads. It supports dynamic attributes, reduces mapping complexity, and avoids issues like mapping explosions or manual dimension setup.

EDOT uses Elasticsearch’s [Logs data stream (LogsDB)](docs-content://manage-data/data-store/data-streams/logs-data-stream.md) and [Time Series Data Streams (TSDS)](docs-content://manage-data/data-store/data-streams/time-series-data-stream-tsds.md) as storage backends. These are purpose-built to handle the scale and variety of observability data.

## Storage architecture

EDOT uses specialized index modes for each type of telemetry signal:

| Signal type | Index mode    | Storage backend |
|-------------|---------------|------------------|
| Logs        | `logsdb`      | LogsDB           |
| Traces      | `logsdb`      | LogsDB           |
| Metrics     | `time_series` | TSDS             |

### Logs and traces in LogsDB

Log and trace data is stored in LogsDB, a storage engine optimized for high-ingest, semi-structured observability data. Benefits include:

* Improved indexing performance for dynamic fields like `attributes`  
* Field-level sorting for more efficient queries  
* Use of the [`passthrough`](#mapping-optimizations-with-passthrough) field type for flexible access without deep nesting  

### Metrics in TSDS

Metric data is stored using Elasticsearch’s TSDS. Benefits include:

* Efficient storage using columnar compression  
* Fast aggregations 
* Automatic detection of metric dimensions (no need to manually define field sets)  

## Mapping optimizations with `passthrough`

OpenTelemetry attributes are stored using the [`passthrough`](elasticsearch://reference/elasticsearch/mapping-reference/passthrough.md) field type, enabling:

* Full query support  
* Dynamic mapping without immediate mapping explosions  
* Simplified query syntax  

Unlike `flattened` fields, which support only keyword-style queries, `passthrough` retains field types and structure, allowing for more expressive queries.

Additionally, the `passthrough` field type includes a `time_series_dimension` parameter, which simplifies the configuration of TSDS for all subfields within the passthrough object. This makes it easier to set up a performant and efficient data stream for your EDOT metrics.

## Storage efficiency

Elasticsearch storage usage depends on the volume and structure of ingested telemetry. EDOT reduces overhead by using:

| Factor               | Impact                                                                 |
|----------------------|------------------------------------------------------------------------|
| Index mode           | LogsDB and TSDS reduce mapping overhead and support efficient compression |
| Schema               | `mapping_mode: otel` avoids ECS-style flattening                          |
| Attribute ingestion  | `passthrough` fields support dynamic attributes with less risk of mapping explosions             |
| Sampling             | Supported natively by EDOT and Elastic APM agents                         |

Elastic compresses telemetry data on ingest. Actual disk usage depends on configuration, sampling, and data shape. [EDOT SDKs](../edot-sdks/index.md) also offer control over emitted data, letting you reduce volume by filtering spans or limiting attributes at the source.

For more details on performance and compression, refer to the [LogsDB](docs-content://manage-data/data-store/data-streams/logs-data-stream.md) and [TSDS](docs-content://manage-data/data-store/data-streams/time-series-data-stream-tsds.md) documentation.

## Comparison with classic APM data streams

This table highlights key differences between classic Elastic APM data streams and EDOT with `mapping_mode: otel`:

| Feature                   | Classic APM (ECS-based)    | EDOT (`mapping_mode: otel`)            |
|---------------------------|-----------------------------|----------------------------------------|
| Index mode                | General-purpose indices     | LogsDB (logs and traces), TSDS (metrics)   |
| Mapping style             | ECS flattened fields        | Native OTel fields and `passthrough`     |
| Attribute control         | Limited                     | Dynamic, flexible                      |
| Query performance         | Comparable                  | Comparable (may improve at scale)      |
| Metric dimension definition | Manual                   | Automatic using TSDS                     |
| Schema flexibility        | Moderate                    | High                                   |