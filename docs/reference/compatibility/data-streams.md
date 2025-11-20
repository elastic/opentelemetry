---
navigation_title: Data streams comparison
description: Learn how EDOT optimizes telemetry storage and query performance in Elastic Observability compared to classic APM and ECS-based integrations. 
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

# OpenTelemetry data streams compared to classic APM and ECS-based integrations

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


## Comparison with classic APM data streams

This table highlights key differences between classic Elastic APM data streams and EDOT with `mapping_mode: otel`:

| Feature                   | Classic APM (ECS-based)                                                                                                          | EDOT (`mapping_mode: otel`)                                                                                                          |
|---|---|---|
| Index mode | General-purpose data streams (logs, traces, metrics) <br><br> TSDS is not supported for classic APM. | LogsDB (logs/traces), TSDS (metrics) |
| Mapping style | Nested objects are mapped as structured fields. Some exceptions exist, such as `labels.*` and `numeric_labels.*`, where dots in field names are replaced with underscores. <br><br> ECS supports multiple field types (keyword, long, double, date, boolean, and so on) as defined in the schema. | Native OpenTelemetry fields with `passthrough`, preserving types and structure. |
| Attribute handling | Dynamic mapping. Custom attributes are stored under `labels.*` (strings) or `numeric_labels.*` (numbers); dots in field names are replaced with underscores. <br><br> See [Document examples - classic APM](#classic-apm) | Dynamic mapping with native types under `attributes.*`, preserving dots in field names. <br><br> See [Document examples - EDOT](#edot) |

### Query compatibility with classic APM data streams

EDOT is designed to make OpenTelemetry data queryable using many of the same field names as classic APM (ECS-based) data streams. This helps preserve compatibility with existing dashboards, saved searches, and queries.

Query compatibility is achieved through:

* **`passthrough` fields:** Make nested OpenTelemetry fields available at the top level so they can be queried. For example, while the service name is stored at `resource.attributes.service.name`, you can query it as `service.name` (the same field name as the one used in the classic APM data stream).
* **Field aliases:** Map fields with different names in ECS and OpenTelemetry semantic conventions to a common query name to make migration easier.

#### Limitations

Query compatibility is not complete:

* Not all ECS fields have aliases. Some integration-specific fields may require query changes.
* Custom attributes and labels are stored differently.

These differences may require updates to certain queries or visualizations.

Refer to [ECS & OpenTelemetry](ecs://reference/ecs-opentelemetry.md) for details on the available aliases and field mappings.


### Document examples

#### Classic APM

```yaml
"@timestamp": "2025-08-14T05:29:43.922Z"
data_stream:
  type: logs
  dataset: apm.app.cart-service
  namespace: default
service:
  name: "cart-service"
host:
  ip: ["127.0.0.1", "0.0.0.0"]
kubernetes:
  namespace: "ecommerce"
labels:
  customer_id: "fc2d1b03-b307-4ae3-a19e-df2804c49fc2"
numeric_labels:
  order_id: 4711
  cart_items: 42
  cart_total_amount: 42.0
message: "Order was successfully created"
log:
  level: INFO
```

#### EDOT

```yaml
"@timestamp": "2025-08-14T05:29:43.922Z"
data_stream:
  type: logs
  dataset: generic.otel
  namespace: default
resource:
  attributes:
    service.name: "cart-service"
    host.ip: ["127.0.0.1", "0.0.0.0"]
    k8s.namespace.name: "ecommerce"
attributes:
  customer.id: "fc2d1b03-b307-4ae3-a19e-df2804c49fc2"
  order.id: 4711
  cart.items: 42
  cart.total_amount: 42.0
body:
  text: "Order was successfully created"
severity_text: INFO
```


## Comparison with ECS-based integrations

While classic APM and EDOT represent two ingestion paths for application telemetry, Elastic’s integrations (for example Nginx, MySQL, Kubernetes) also produce ECS-based data streams for logs, metrics, and events. These use ECS mappings and integration-specific pipelines optimized for their domain.

| Stream type | Typical field layout | Custom attributes / dot notation |
|--------------|----------------------|----------------------------------|
| **Integration ECS-based** | Uses ECS mapping tailored by integration. Custom fields are added under ECS-structured objects or `.custom` objects. Dots in field names are often disallowed or normalized to underscores. | Example: `host.os.name`, `nginx.access.time` rewritten to `nginx_access_time` |
| **EDOT (OTel + passthrough)** | Stores OTel-native nested object structure (`resource.attributes`, `attributes.*`). Uses `passthrough` to expose fields at the top level for query compatibility. | Example: `attributes.cart.items: 42`, `resource.attributes.service.name: "checkout-service"` |

### Integration example (Nginx access logs)

```yaml
"@timestamp": "2025-08-14T12:00:01.123Z"
event:
  dataset: nginx.access
  module: nginx
host:
  name: "web-1"
nginx:
  access:
    request: "/api/v1/items"
    status_code: 200
    bytes_sent: 512
user:
  ip: "203.0.113.45"
```


## Summary of all data stream types

| Feature | Classic APM (ECS-based) | Integration ECS-based streams | EDOT (`mapping_mode: otel`) |
|----------|-------------------------|-------------------------------|-----------------------------|
| **Index mode** | General-purpose data streams (logs, traces, metrics); TSDS not supported | ECS-style data streams (logs, metrics, events) using integrations | LogsDB for logs/traces, TSDS for metrics |
| **Mapping style** | ECS object mappings; nested fields preserved. `labels.*` / `numeric_labels.*` flatten dots. | ECS mappings or integration-altered schemas (flattening, renaming). | OTel-native nested layout with `passthrough`, preserving types and structure. |
| **Attribute handling** | Custom values under `labels.*` / `numeric_labels.*`, dots replaced by underscores. | Integration-specific or prefixed fields. | Custom values under `attributes.*`, dots preserved. |
| **Query compatibility** | Queries target ECS field names (`service.name`, `labels.*`). | Queries assume ECS names; pipelines normalize vendor data. | `passthrough` + aliases allow ECS-style names (such as `service.name`). |
| **Compatibility limits** | N/A | Some integration fields may not align 1:1 with ECS or OTel. | Not all ECS/integration fields have aliases; label vs attribute layout differs. |


## See also

* [ECS and OpenTelemetry schema reference](ecs://reference/ecs-opentelemetry.md)
* [Logs data stream (LogsDB)](docs-content://manage-data/data-store/data-streams/logs-data-stream.md)
* [Time Series Data Stream (TSDS)](docs-content://manage-data/data-store/data-streams/time-series-data-stream-tsds.md)