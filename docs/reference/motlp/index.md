---
navigation_title: Managed OTLP Endpoint
description: Reference documentation for the Elastic Cloud Managed OTLP Endpoint.
applies_to:
  serverless:
    observability: ga
    security: ga
  deployment:
    ess: ga
products:
  - id: cloud-serverless
  - id: observability
  - id: edot-collector
---

# Elastic Cloud Managed OTLP Endpoint (mOTLP)

The {{motlp}} allows you to send OpenTelemetry data directly to {{ecloud}} using the OTLP protocol. 

The endpoint adds a resilient ingestion layer that works seamlessly with serverless autoscaling and removes pressure from {{ech}} clusters.

:::{important}
The {{motlp}} endpoint is not available for Elastic [self-managed](docs-content://deploy-manage/deploy/self-managed.md), [ECE](docs-content://deploy-manage/deploy/cloud-enterprise.md), or [ECK](docs-content://deploy-manage/deploy/cloud-on-k8s.md) clusters. To send OTLP data to any of these cluster types, deploy and expose an OTLP-compatible endpoint using the [EDOT Collector as a gateway](elastic-agent://reference/edot-collector/modes.md#edot-collector-as-gateway).
:::

## Prerequisites

To use the {{ecloud}} {{motlp}} you need the following:

- An {{serverless-full}} project or an {{ech}} (ECH) deployment.
- An OTLP-compliant shipper capable of forwarding logs, metrics, or traces in OTLP format. This can include:
  - [OpenTelemetry Collector](elastic-agent://reference/edot-collector/index.md) (EDOT, Contrib, or other distributions)
  - [OpenTelemetry SDKs](/reference/edot-sdks/index.md) (EDOT, upstream, or other distributions)
  - [EDOT Cloud Forwarder](/reference/edot-cloud-forwarder/index.md)
  - Any other forwarder that supports the OTLP protocol.

You don't need APM Server when ingesting data through the Managed OTLP Endpoint. The APM integration (`.apm` endpoint) is a legacy ingest path that only supports traces and translates OTLP telemetry to ECS, whereas {{motlp}} natively ingests OTLP data.

:::{note}
For {{ech}} deployments, {{motlp}} is currently supported in the following AWS regions: ap-southeast-1, ap-northeast-1, ap-south-1, eu-west-1, eu-west-2, us-east-1, us-west-2, us-east-2. 
Support for additional regions and cloud providers is in progress and will be expanded over time. 
:::

## Send data to the Managed OTLP Endpoint

To send data to Elastic through the {{motlp}}, follow the [Send data to the Elastic Cloud Managed OTLP Endpoint](docs-content://solutions/observability/get-started/quickstart-elastic-cloud-otel-endpoint.md) quickstart.

### Find your {{motlp}} endpoint

:::{include} ../_snippets/find-motlp-endpoint.md
:::

### Configure SDKs to send data directly

To configure OpenTelemetry SDKs to send data directly to the {{motlp}}, set the `OTEL_EXPORTER_OTLP_ENDPOINT` and `OTEL_EXPORTER_OTLP_HEADERS` environment variable.

For example:

```bash
export OTEL_EXPORTER_OTLP_ENDPOINT="https://<motlp-endpoint>"
export OTEL_EXPORTER_OTLP_HEADERS="Authorization=ApiKey <key>"
```

### Routing logs to dedicated datasets

You can route logs to dedicated datasets by setting the `data_stream.dataset` attribute to the log record. This attribute is used to route the log to the corresponding dataset.

For example, if you want to route the {{edot-cf}} logs to custom datasets, you can add the following attributes to the log records:

```yaml
processors:
  transform:
    log_statements:
      - set(log.attributes["data_stream.dataset"], "aws.cloudtrail") where log.attributes["aws.cloudtrail.event_id"] != nil
```

You can also set the `OTEL_RESOURCE_ATTRIBUTES` environment variable to set the `data_stream.dataset` attribute for all logs. For example:

```bash
export OTEL_RESOURCE_ATTRIBUTES="data_stream.dataset=app.orders"
```

## Reference architecture

This diagram shows data ingest using {{edot}} and the {{motlp}}:

:::{image} ../images/motlp-reference-architecture.png
:alt: mOTLP Reference architecture
:width: 100%
:::

Telemetry is stored in Elastic in OTLP format, preserving resource attributes and original semantic conventions. If no specific dataset or namespace is provided, the data streams are: `traces-generic.otel-default`, `metrics-generic.otel-default`, and `logs-generic.otel-default`.

For a detailed comparison of how OTel data streams differ from classic Elastic APM data streams, refer to [OTel data streams compared to classic APM](../compatibility/data-streams.md).

## Failure store

```{applies_to}
stack: ga 9.1+
```

The {{motlp}} endpoint is designed to be highly available and resilient. However, there are some scenarios where data might be lost or not sent completely. The [Failure store](docs-content://manage-data/data-store/data-streams/failure-store.md) is a mechanism that allows you to recover from these scenarios.

The Failure store is always enabled for {{motlp}} data streams. This prevents ingest pipeline exceptions and conflicts with data stream mappings. Failed documents are stored in a separate index. You can view the failed documents from the **Data Set Quality** page. Refer to [Data set quality](docs-content://solutions/observability/data-set-quality-monitoring.md).

## Limitations

The following limitations apply when using the {{motlp}}:

* Universal Profiling is not available.
* Only supports histograms with delta temporality. Cumulative histograms are dropped.
* Latency distributions based on histogram values have limited precision due to the fixed boundaries of explicit bucket histograms.
* [Traffic filters](docs-content://deploy-manage/security/ip-filtering-cloud.md) are not yet available on both ECH and Serverless.
* Tail-based sampling (TBS) is not available. The {{motlp}} does not provide centralized hosted sampling. If you need tail-based sampling, configure it on the edge using the [Tail Sampling Processor](https://github.com/open-telemetry/opentelemetry-collector-contrib/tree/main/processor/tailsamplingprocessor) in your OpenTelemetry Collector before sending data to the endpoint.

## Billing

For more information on billing, refer to [Elastic Cloud pricing](https://www.elastic.co/pricing/serverless-observability).
