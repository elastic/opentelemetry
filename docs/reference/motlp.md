---
navigation_title: Managed OTLP Endpoint
description: Reference documentation for the Elastic Cloud Managed OTLP Endpoint.
applies_to:
  serverless:
    observability: 
products:
  - id: cloud-serverless
  - id: observability
  - id: edot-collector
---

# Elastic Cloud Managed OTLP Endpoint

The {{motlp}} allows you to send OpenTelemetry data directly to {{ecloud}} using the OTLP protocol, with Elastic handling scaling, data processing, and storage. The Managed OTLP endpoint can act like a Gateway Collector, so that you can point your OpenTelemetry SDKs or Collectors to it.

This guide explains how to find your {{motlp}} endpoint, create an API key for authentication, and configure different environments. 

:::{important}
The {{motlp}} endpoint is available on {{serverless-full}} and will soon be supported on {{ech}}. It is not available for self-managed deployments.
:::

## Reference architecture

This diagram shows data ingest using {{edot}} and the {{motlp}}:

:::{image} ./images/motlp-reference-architecture.png
:alt: mOTLP Reference architecture
:width: 100%
:::

For a detailed comparison of how EDOT data streams differ from classic Elastic APM data streams, refer to [EDOT data streams compared to classic APM](../reference/compatibility/data-streams.md).

## Prerequisites

Telemetry is stored in Elastic in OTLP format, preserving resource attributes and original semantic conventions. If no specific dataset or namespace is provided, the data streams are: `traces-generic.otel-default`, `metrics-generic.otel-default`, and `logs-generic.otel-default`.

You don't need to use APM Server when ingesting data through the Managed OTLP Endpoint. The APM integration (`.apm` endpoint) is a legacy ingest path that only supports traces and translates OTLP telemetry to ECS, whereas {{motlp}} natively ingests OTLP data for logs, metrics, and traces.

## Send data to Elastic

To send data to Elastic through the {{motlp}}, follow the [Send data to the Elastic Cloud Managed OTLP Endpoint](docs-content://solutions/observability/get-started/quickstart-elastic-cloud-otel-endpoint.md) quickstart.

### Find your {{motlp}} endpoint

To retrieve your {{motlp}} endpoint address, follow these steps:

1. In Elastic Cloud, create an Observability project or open an existing one.
2. Select your project's name and then select **Manage project**.
3. Locate the Connection alias and select **Edit**.
4. Copy the Managed OTLP endpoint URL.

### Configure SDKs to use the API key

To configure OpenTelemetry SDKs to send data to the {{motlp}}, set the `OTEL_EXPORTER_OTLP_HEADERS` environment variable.

For example:

```bash
export OTEL_EXPORTER_OTLP_HEADERS="Authorization=ApiKey <key>"
```

## Routing logs to dedicated datasets

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

## Failure store

The {{motlp}} endpoint is designed to be highly available and resilient. However, there are some scenarios where data might be lost or not sent completely. The [Failure store](docs-content://manage-data/data-store/data-streams/failure-store.md) is a mechanism that allows you to recover from these scenarios.

The Failure store is always enabled for {{motlp}} data streams. This prevents ingest pipeline exceptions and conflicts with data stream mappings. Failed documents are stored in a separate index. You can view the failed documents from the **Data Set Quality** page. Refer to [Data set quality](docs-content://solutions/observability/data-set-quality-monitoring.md).

## Limitations

The following limitations apply when using the {{motlp}}:

* Tail-based sampling (TBS) is not available.
* Universal Profiling is not available.
* Only supports histograms with delta temporality. Cumulative histograms are dropped.
* Latency distributions based on histogram values have limited precision due to the fixed boundaries of explicit bucket histograms.

## Billing

For more information on billing, refer to [Elastic Cloud pricing](https://www.elastic.co/pricing/serverless-observability).

## Rate limiting

Requests to the {{motlp}} are subject to rate limiting. If you send data at a rate that exceeds the defined limits, your requests will be temporarily rejected.

The rate limit is currently set to 15 MB/s per second, with a burst limit of 30 MB/s per second. As long as your data ingestion rate stays at or below this average, your requests will be accepted.

If send data that exceeds the available rate limit, the {{motlp}} will respond with an HTTP 429 Too Many Requests status code. A log message similar to this will appear in the OpenTelemetry Collector's output:

```json
{
  "code": 8,
  "message": "error exporting items, request to <ingest endpoint> responded with HTTP Status Code 429"
}
```

After your sending rate drops back within the allowed limit, the system will automatically begin accepting requests again.

:::{note}
If you need to increase the rate limit, reach out to Elastic Support.
:::
