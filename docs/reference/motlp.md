---
navigation_title: Managed OTLP Endpoint
description: Reference documentation for the Elastic Cloud Managed OTLP Endpoint.
applies_to:
  serverless:
    observability:
  deployment:
    ess: preview 9.2
products:
  - id: cloud-serverless
  - id: observability
  - id: edot-collector
---

# Elastic Cloud Managed OTLP Endpoint

The {{motlp}} allows you to send OpenTelemetry data directly to {{ecloud}} using the OTLP protocol, with Elastic handling scaling, data processing, and storage. The Managed OTLP endpoint can act like a Gateway Collector, so that you can point your OpenTelemetry SDKs or Collectors to it.

:::{important}
The {{motlp}} endpoint is not available for Elastic [self-managed](docs-content://deploy-manage/deploy/self-managed.md), [ECE](docs-content://deploy-manage/deploy/cloud-enterprise.md) or [ECK](docs-content://deploy-manage/deploy/cloud-on-k8s.md) clusters. To send OTLP data to any of these cluster types, deploy and expose an OTLP-compatible endpoint using the EDOT Collector as a gateway. Refer to [EDOT deployment docs](elastic-agent://reference/edot-collector/modes.md#edot-collector-as-gateway) for more information.
:::

## Reference architecture

This diagram shows data ingest using {{edot}} and the {{motlp}}:

:::{image} ./images/motlp-reference-architecture.png
:alt: mOTLP Reference architecture
:width: 100%
:::

Telemetry is stored in Elastic in OTLP format, preserving resource attributes and original semantic conventions. If no specific dataset or namespace is provided, the data streams are: `traces-generic.otel-default`, `metrics-generic.otel-default`, and `logs-generic.otel-default`.

For a detailed comparison of how OTel data streams differ from classic Elastic APM data streams, refer to [OTel data streams compared to classic APM](./compatibility/data-streams.md).

## Prerequisites

To use the {{ecloud}} {{motlp}} you need the following:

- An {{serverless-full}} project or an {{ech}} (ECH) deployment. Security projects are not yet supported.
- An OTLP-compliant shipper capable of forwarding logs, metrics, or traces in OTLP format. This can include:
  - [OpenTelemetry Collector](elastic-agent://reference/edot-collector/index.md) (EDOT, Contrib, or other distributions)
  - [OpenTelemetry SDKs](/reference/edot-sdks/index.md) (EDOT, upstream, or other distributions)
  - [EDOT Cloud Forwarder](/reference/edot-cloud-forwarder/index.md)
  - Any other forwarder that supports the OTLP protocol.

:::{note}
You don't need APM Server when ingesting data through the Managed OTLP Endpoint. The APM integration (`.apm` endpoint) is a legacy ingest path that only supports traces and translates OTLP telemetry to ECS, whereas {{motlp}} natively ingests OTLP data for logs, metrics, and traces.
:::

## Send data to Elastic

To send data to Elastic through the {{motlp}}, follow the [Send data to the Elastic Cloud Managed OTLP Endpoint](docs-content://solutions/observability/get-started/quickstart-elastic-cloud-otel-endpoint.md) quickstart.

### Find your {{motlp}} endpoint

To retrieve your {{motlp}} endpoint address, follow these steps:

::::{applies-switch}

:::{applies-item} serverless:
1. In {{ecloud}}, create an Observability project or open an existing one.
2. Select your project's name and then select **Manage project**.
3. Locate the **Connection alias** and select **Edit**.
4. Copy the **Managed OTLP endpoint** URL.
:::

:::{applies-item} ess: preview 9.2
1. Open your deployment in the Elastic Cloud console.
2. Navigate to **Integrations** and find **OpenTelemetry** or **Managed OTLP**.
3. Copy the endpoint URL shown.
:::

::::

### Configure SDKs to send data directly

To configure OpenTelemetry SDKs to send data directly to the {{motlp}}, set the `OTEL_EXPORTER_OTLP_ENDPOINT` and `OTEL_EXPORTER_OTLP_HEADERS` environment variable.

For example:

```bash
export OTEL_EXPORTER_OTLP_ENDPOINT="https://<motlp-endpoint>"
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

Requests to the {{motlp}} are subject to rate limiting and throttling. If you exceed your {{es}} capacity in {{ech}}, or send data at a rate that exceeds the limits, your requests might be rejected.

The following rate limits and burst limits apply:

| Deployment type | Rate limit | Burst limit |
|----------------|------------|-------------|
| Serverless | 15 MB/s | 30 MB/s |
% | ECH | MB/s | MB/s |

As long as your data ingestion rate stays at or below the rate limit and burst limit, your requests are accepted.

### Exceeding the rate limit

If you send data that exceeds the available limits, the {{motlp}} responds with an HTTP `429` Too Many Requests status code. A log message similar to this appears in the OpenTelemetry Collector's output:

```json
{
  "code": 8,
  "message": "error exporting items, request to <ingest endpoint> responded with HTTP Status Code 429"
}
```

After your sending rate goes back to the allowed limit, the system automatically begins accepting requests again.

### Solutions to rate limiting

Depending on the reason for the rate limiting, you can either increase your {{es}} capacity or request higher limits.

#### Increase your {{es}} capacity

If data intake exceeds the capacity of {{es}} in your {{ech}} deployment, you might get rate limiting errors. To solve this issue, scale or resize your deployment:

- [Scaling considerations](docs-content://deploy-manage/production-guidance/scaling-considerations.md)
- [Resize deployment](docs-content://deploy-manage/deploy/cloud-enterprise/resize-deployment.md)
- [Autoscaling in ECE and ECH](docs-content://deploy-manage/autoscaling/autoscaling-in-ece-and-ech.md)

#### Request higher limits

If rate limiting is not caused by {{es}} capacity or you're on {{serverless-full}}, you can either decrease data volume or request higher limits.

To increase the rate limit, [reach out to Elastic Support](docs-content://troubleshoot/ingest/opentelemetry/contact-support.md).
