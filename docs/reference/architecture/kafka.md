---
navigation_title: Kafka ingest pipelines
description: Use Kafka as a transport buffer in EDOT ingest pipelines for self-managed Elasticsearch or Elastic Cloud Managed OTLP (mOTLP).
applies_to:
  stack:
  serverless:
    observability:
products:
  - id: cloud-serverless
  - id: observability
  - id: edot-collector
---

# Kafka-based ingest pipelines with EDOT [kafka-ingest-pipelines-edot]

Kafka can act as a transport buffer between telemetry sources (applications and edge collectors) and your backend, decoupling production from ingestion. Use this pattern when you need buffering during outages or maintenance, independent scaling of collection and ingestion, or a shared transport layer across environments or networks.

## Reference architectures [reference-architectures]

The following patterns cover self-managed {{es}} and {{ecloud}} (including serverless) using the Managed OTLP endpoint.

### Self-managed (on-prem) {{es}} [self-managed-elasticsearch]

`EDOT SDKs (OTLP) → EDOT Collector (Gateway) → Kafka → EDOT Collector (Consumer) → Elasticsearch`

In this model:
- A Gateway Collector receives OTLP from EDOT SDKs (or upstream SDKs) and exports OTLP payloads to Kafka.
- A Consumer Collector reads OTLP payloads from Kafka and exports to {{es}}.

### {{ecloud}} (Hosted/Serverless) using mOTLP [elastic-cloud-motlp]

`EDOT SDKs (OTLP) → EDOT Collector (Gateway) → Kafka → EDOT Collector (Consumer) → mOTLP`

In this model:
- A Consumer Collector reads OTLP payloads from Kafka and exports to the {{ecloud}} Managed OTLP endpoint (mOTLP) using the OTLP/HTTP exporter.

## Components [components]

These pipelines rely on the following EDOT Collector components:
- `kafkaexporter` to write OTLP payloads to Kafka
- `kafkareceiver` to read OTLP payloads from Kafka

For EDOT, only the `otlp_proto` and `otlp_json` encodings are supported for the Kafka receiver and exporter. Partitioning options (for example, `partition_traces_by_id`) are not supported. Refer to the [EDOT Collector components list](elastic-agent://reference/edot-collector/components.md) for the full list and support notes.

## Example configuration [example-configuration]

The following examples show a minimal split deployment for:
- Gateway Collector (produces to Kafka)
- Consumer Collector (consumes from Kafka and exports to {{es}} or mOTLP)

:::{note}
Use an OTLP encoding on Kafka (for example, `otlp_proto`). Ensure the receiver and exporter use the same encoding and topics.
:::

### Gateway Collector [gateway-collector]

This example receives OTLP and exports to Kafka.

```yaml
receivers:
  otlp:
    protocols:
      grpc:
      http:

exporters:
  kafka:
    brokers: ["kafka1:9092", "kafka2:9092", "kafka3:9092"]
    logs:
      topic: "otel-otlp"
      encoding: otlp_proto
    metrics:
      topic: "otel-otlp"
      encoding: otlp_proto
    traces:
      topic: "otel-otlp"
      encoding: otlp_proto

service:
  pipelines:
    traces:
      receivers: [otlp]
      exporters: [kafka]
    metrics:
      receivers: [otlp]
      exporters: [kafka]
    logs:
      receivers: [otlp]
      exporters: [kafka]
```

### Consumer Collector for self-managed [consumer-collector-self-managed]

This example receives from Kafka and exports to {{es}}.

```yaml
receivers:
  kafka:
    brokers: ["kafka1:9092", "kafka2:9092", "kafka3:9092"]
    logs:
      topics: ["otel-otlp"]
      encoding: otlp_proto
    metrics:
      topics: ["otel-otlp"]
      encoding: otlp_proto
    traces:
      topics: ["otel-otlp"]
      encoding: otlp_proto

exporters:
  elasticsearch:
    endpoints: ["https://elasticsearch.example:9200"]
    api_key: "${ELASTICSEARCH_API_KEY}"

service:
  pipelines:
    traces:
      receivers: [kafka]
      exporters: [elasticsearch]
    metrics:
      receivers: [kafka]
      exporters: [elasticsearch]
    logs:
      receivers: [kafka]
      exporters: [elasticsearch]
```

### Consumer Collector for {{ecloud}} [consumer-collector-motlp]

This example receives from Kafka and exports to {{motlp}}. The {{motlp}} endpoint uses the OTLP/HTTP protocol, so the configuration uses the `otlphttp` exporter to send to the HTTPS endpoint correctly.

```yaml
receivers:
  kafka:
    brokers: ["kafka1:9092", "kafka2:9092", "kafka3:9092"]
    logs:
      topics: ["otel-otlp"]
      encoding: otlp_proto
    metrics:
      topics: ["otel-otlp"]
      encoding: otlp_proto
    traces:
      topics: ["otel-otlp"]
      encoding: otlp_proto

exporters:
  otlphttp:
    endpoint: "${MOTLP_ENDPOINT}"
    headers:
      Authorization: "ApiKey ${MOTLP_API_KEY}"

service:
  pipelines:
    traces:
      receivers: [kafka]
      exporters: [otlphttp]
    metrics:
      receivers: [kafka]
      exporters: [otlphttp]
    logs:
      receivers: [kafka]
      exporters: [otlphttp]
```

## Operational notes [operational-notes]

Monitor backpressure and export failures on both the Gateway and Consumer Collectors. A Kafka buffer can mask downstream ingestion problems until retention is exhausted. To avoid it, size retention and partitions for peak ingest and expected outage windows. 

For {{product.apm}} UI optimizations on self-managed backends, align the backend Collector's mode and processors with the recommended EDOT gateway architecture for your deployment.