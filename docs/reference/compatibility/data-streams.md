---
navigation_title: Data streams comparison
description: Learn how {{edot}} optimizes telemetry storage and query performance in {{product.observability}} compared to classic APM and ECS-based integrations. 
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

# OpenTelemetry data streams compared to classic {{product.apm}} and ECS-based integrations

{{edot}} stores telemetry data using a storage model optimized for OpenTelemetry signals. When `mapping_mode: otel` is enabled on the {{es}} exporter (which is the default setting), {{edot}} writes logs, traces, and metrics to specialized data streams aligned with OpenTelemetry specifications.

This architecture is designed for scalable observability workloads. It supports dynamic attributes, reduces mapping complexity, and avoids issues like mapping explosions or manual dimension setup.

{{edot}} uses {{es}}'s [Logs data stream (LogsDB)](docs-content://manage-data/data-store/data-streams/logs-data-stream.md) and [Time Series Data Streams (TSDS)](docs-content://manage-data/data-store/data-streams/time-series-data-stream-tsds.md) as storage backends. These are purpose-built to handle the scale and variety of observability data and improve the storage efficiency.

This page provides a detailed comparison of {{edot}} data streams with classic {{product.apm}} and ECS-based integrations. For a practical reference on which data streams {{edot}} uses, exporter behavior, and storage engines, see [{{edot}} data streams](../data-streams.md).

## Logs and traces in LogsDB

Log and trace data is stored in [LogsDB](docs-content://manage-data/data-store/data-streams/logs-data-stream.md), a storage engine optimized for high-ingest, semi-structured observability data. Benefits include:

* Storage efficiency 
* Optimized field handling for dynamic fields (for example, `attributes`)

## Metrics in TSDS

Metric data is stored using {{es}}'s [TSDS](docs-content://manage-data/data-store/data-streams/time-series-data-stream-tsds.md). Benefits include:

* Efficient storage using columnar compression  
* Fast aggregations 
* Automatic detection of metric dimensions (no need to manually define `time_series_dimension` in field mappings)


## Comparison with classic {{product.apm}} data streams [comparison-with-classic-apm-data-streams]

This table highlights key differences between classic {{product.apm}} data streams and {{edot}} with `mapping_mode: otel`:

| Feature                   | Classic {{product.apm}} (ECS-based)                                                                                                          | {{edot}} (`mapping_mode: otel`)                                                                                                          |
|---|---|---|
| Index mode | General-purpose data streams (logs, traces, metrics) <br><br> TSDS is not supported for classic {{product.apm}}. | LogsDB (logs/traces), TSDS (metrics) |
| Mapping style | Nested objects are mapped as structured fields. Some exceptions exist, such as `labels.*` and `numeric_labels.*`, where dots in field names are replaced with underscores. <br><br> ECS supports multiple field types (keyword, long, double, date, boolean, and so on) as defined in the schema. | Native OpenTelemetry fields with `passthrough`, preserving types and structure. |
| Attribute handling | Dynamic mapping. Custom attributes are stored under `labels.*` (strings) or `numeric_labels.*` (numbers); dots in field names are replaced with underscores. <br><br> See [Document examples - classic {{product.apm}}](#classic-apm) | Dynamic mapping with native types under `attributes.*`, preserving dots in field names. <br><br> See [Document examples - {{edot}}](#edot) |

### Query compatibility with classic {{product.apm}} data streams

{{edot}} is designed to make OpenTelemetry data queryable using many of the same field names as classic {{product.apm}} (ECS-based) data streams. This helps preserve compatibility with existing dashboards, saved searches, and queries.

Query compatibility is achieved through:

* **`passthrough` fields:** Make nested OpenTelemetry fields available at the top level so they can be queried. For example, while the service name is stored at `resource.attributes.service.name`, you can query it as `service.name` (the same field name as the one used in the classic {{product.apm}} data stream).
* **Field aliases:** Map fields with different names in ECS and OpenTelemetry semantic conventions to a common query name to make migration easier.

#### Limitations

Query compatibility is not complete:

* Not all ECS fields have aliases. Some integration-specific fields may require query changes.
* Custom attributes and labels are stored differently.

These differences may require updates to certain queries or visualizations.

Refer to [ECS & OpenTelemetry](ecs://reference/ecs-opentelemetry.md) for details on the available aliases and field mappings.


### Document examples

#### Classic {{product.apm}} [classic-apm]

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

#### {{edot}} [edot]

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

While classic {{product.apm}} and {{edot}} represent two ingestion paths for application telemetry, Elastic's integrations (for example Nginx, MySQL, Kubernetes) also produce ECS-based data streams for logs, metrics, and events. These use ECS mappings and integration-specific pipelines optimized for their domain.

| Stream type | Typical field layout | Custom attributes / dot notation |
|--------------|----------------------|----------------------------------|
| **Integration ECS-based** | Uses ECS mapping tailored by integration. Custom fields are added under ECS-structured objects or `.custom` objects. Dots in field names are often disallowed or normalized to underscores. | Example: `host.os.name`, `nginx.access.time` rewritten to `nginx_access_time` |
| **{{edot}} (OTel + passthrough)** | Stores OTel-native nested object structure (`resource.attributes.*`, `attributes.*`). Uses `passthrough` to expose fields at the top level for query compatibility. | Example: `attributes.cart.items: 42`, `resource.attributes.service.name: "checkout-service"` |

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

| Feature | Classic {{product.apm}} (ECS-based) | Integration ECS-based streams | {{edot}} (`mapping_mode: otel`) |
|----------|-------------------------|-------------------------------|-----------------------------|
| **Index mode** | General-purpose data streams (logs, traces, metrics); TSDS not supported | ECS-style data streams (logs, metrics, events) using integrations | LogsDB for logs/traces, TSDS for metrics |
| **Mapping style** | ECS object mappings; nested fields preserved. `labels.*` / `numeric_labels.*` flatten dots. | ECS mappings or integration-altered schemas (flattening, renaming). | OTel-native nested layout with `passthrough`, preserving types and structure. |
| **Attribute handling** | Custom values under `labels.*` / `numeric_labels.*`, dots replaced by underscores. | Integration-specific or prefixed fields. | Custom values under `attributes.*`, dots preserved. |
| **Query compatibility** | Queries target ECS field names (`service.name`, `labels.*`). | Queries assume ECS names; pipelines normalize vendor data. | `passthrough` + aliases allow ECS-style names (such as `service.name`). |
| **Compatibility limits** | N/A | Some integration fields may not align 1:1 with ECS or OTel. | Not all ECS/integration fields have aliases; label vs attribute layout differs. |


## The `event.ingested` field [event-ingested]

OTel-native data streams don't populate [`event.ingested`](ecs://reference/ecs-event.md), the ECS field that records when a document was indexed.

On ECS-based integration data streams, `event.ingested` is set by the `.fleet_final_pipeline-1` ingest pipeline, which {{product.fleet}} attaches as `index.final_pipeline` to the data streams it manages. The `logs-otel@template` and `metrics-otel@template` index templates don't compose a `final_pipeline`, so nothing sets `event.ingested` on `logs-*.otel-*` or `metrics-*.otel-*` data streams.

:::{note}
Refer to [elastic/elasticsearch#100324](https://github.com/elastic/elasticsearch/issues/100324) for the open request to expose `event.ingested` as a data stream setting.
:::

### Impact on detection rules

Elastic Security prebuilt detection rules that use `event.ingested` as their timestamp override, such as the External Alerts rule, report a `partial failure` execution status when their index patterns match OTel-native data streams:

```txt
The following indices are missing the timestamp override field "event.ingested"
```

The rule still runs and falls back to `@timestamp`, but it loses the protection against ingest lag that the timestamp override provides. Documents indexed later than the rule's lookback window can be missed.

### Populate `event.ingested` on OTel log data streams

`logs-otel@template` composes `logs@settings`, which sets `index.default_pipeline` to `logs@default-pipeline`. That pipeline calls the `logs@custom` ingest pipeline if it exists, which gives you an upgrade-safe extension point.

Create `logs@custom` to route OTel datasets to a dedicated pipeline:

```console
PUT _ingest/pipeline/logs@custom
{
  "processors": [
    {
      "pipeline": {
        "name": "logs-otel@custom",
        "ignore_missing_pipeline": true,
        "if": "$('data_stream.dataset', 'null').endsWith('.otel')"
      }
    }
  ]
}
```

Then create `logs-otel@custom` to set the field:

```console
PUT _ingest/pipeline/logs-otel@custom
{
  "field_access_pattern": "flexible",
  "processors": [
    {
      "set": {
        "field": "attributes.event.ingested",
        "value": "{{{_ingest.timestamp}}}",
        "override": false
      }
    }
  ]
}
```

Keep the following in mind:

* Set the field as `attributes.event.ingested`. Because `attributes` is a `passthrough` object in `logs-otel@mappings`, the field is then queryable under the bare name `event.ingested`.
* {applies_to}`stack: ga 9.2+` {applies_to}`serverless: ga` `field_access_pattern` must be `flexible` to write a dotted field name into a `passthrough` object. Refer to [field access pattern](docs-content://manage-data/ingest/transform-enrich/ingest-pipelines.md#access-source-pattern-flexible).
* You don't need to declare the field mapping. `ecs@mappings`, which `logs-otel@template` composes, has an `ecs_date` dynamic template matching `*.ingested`, so the field is mapped as `date`.

`metrics-otel@template` composes `metrics@tsdb-settings`, which doesn't set a `default_pipeline`, so there's no equivalent extension point for `metrics-*.otel-*` data streams.

### Streams

The `logs@custom` pipeline doesn't apply to [Streams](docs-content://solutions/observability/streams/streams.md). {{kib}} generates its own index template for wired streams that composes only `<ancestor>@stream.layer` component templates and sets `default_pipeline` to `<stream>@stream.processing`, so `logs@settings` and `logs@custom` aren't part of the composition.

For a wired stream, add a [`set` processor](docs-content://solutions/observability/streams/processors/set.md) to a child stream. Root wired streams can't hold custom processing.

```json
{
  "action": "set",
  "to": "attributes.event.ingested",
  "copy_from": "_ingest.timestamp",
  "override": false
}
```

Keep the following in mind:

* Use `copy_from`. The [Streamlang](docs-content://solutions/observability/streams/streamlang.md) `set` action rejects Mustache template syntax in `value`, and the `manual_ingest_pipeline` action isn't allowed in wired streams.
* The `to` value must be prefixed with `attributes.`. The bare field name is rejected.
* Wired streams are `dynamic: false`, so you must also [declare](docs-content://solutions/observability/streams/map-fields.md) `event.ingested` as a `date` field on the stream. Otherwise the value is stored but not indexed.

## See also

* [ECS and OpenTelemetry schema reference](ecs://reference/ecs-opentelemetry.md)
* [Logs data stream (LogsDB)](docs-content://manage-data/data-store/data-streams/logs-data-stream.md)
* [Time Series Data Stream (TSDS)](docs-content://manage-data/data-store/data-streams/time-series-data-stream-tsds.md)
