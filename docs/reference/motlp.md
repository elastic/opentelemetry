---
navigation_title: Managed OTLP Endpoint
description: Reference documentation for the Elastic Cloud Managed OTLP Endpoint.
applies_to:
  serverless:
    observability:
    security:
  deployment:
    ess: ga
    eck: unavailable
    ece: unavailable
    self: unavailable
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

## Send data to Elastic

To send data to Elastic through the {{motlp}}, follow the [Send data to the Elastic Cloud Managed OTLP Endpoint](docs-content://solutions/observability/get-started/quickstart-elastic-cloud-otel-endpoint.md) quickstart.

### Find your {{motlp}} endpoint

:::{include} _snippets/find-motlp-endpoint.md
:::

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
* [Traffic filters](docs-content://deploy-manage/security/ip-filtering-cloud.md) are not yet available on both ECH and Serverless.

## Billing

For more information on billing, refer to [Elastic Cloud pricing](https://www.elastic.co/pricing/serverless-observability).

## Rate limiting

Requests to the {{motlp}} are subject to rate limiting and throttling. If you send data at a rate that exceeds the limits, your requests might be rejected.

The following rate limits and burst limits apply:

| Deployment type | Rate limit | Burst limit | Dynamic scaling |
|----------------|------------|-------------|-----------------|
| Serverless | 30 MB/s | 60 MB/s | Not available |
| ECH | 1 MB/s (initial) | 2 MB/s (initial) | Yes |

As long as your data ingestion rate stays at or below the rate limit and burst limit, your requests are accepted.

:::{note}
For the {{serverless-full}} trial, the rate limit is reduced to 15 MB/s and the burst limit is 30 MB/s.
:::

### Dynamic rate scaling for {{ech}}

```{applies_to}
ess:
```

For {{ech}} deployments, rate limits can scale up or down dynamically based on backpressure from {{es}}. Every deployment starts with a 1 MB/s rate limit and 2 MB/s burst limit. The system automatically adjusts these limits based on your {{es}} capacity and load patterns. Scaling requires time, so sudden load spikes might still result in temporary rate limiting.

### Exceeding the rate limit

If you send data that exceeds the available limits, the {{motlp}} responds with an HTTP `429` Too Many Requests status code. A log message similar to this appears in the OpenTelemetry Collector's output:

```json
{
  "code": 8,
  "message": "error exporting items, request to <ingest endpoint> responded with HTTP Status Code 429"
}
```

The causes of rate limiting differ by deployment type:

- **{{serverless-full}}**: You exceed the 15 MB/s rate limit or 30 MB/s burst limit.
- **{{ech}}**: You send load spikes that exceed current limits (temporary `429`s) or your {{es}} cluster can't keep up with the load (consistent `429`s).

After your sending rate goes back to the allowed limit, or after the system scales up the rate limit for {{ech}}, requests are automatically accepted again.

### Solutions to rate limiting

The solutions to rate limiting depend on your deployment type:

#### {{ech}} deployments

For {{ech}} deployments, if you're experiencing consistent `429` errors, the primary solution is to increase your {{es}} capacity. Because rate limits are affected by {{es}} backpressure, scaling up your {{es}} cluster reduces backpressure and, over time, increases the ingestion rate for your deployment.

To scale your deployment:

- [Scaling considerations](docs-content://deploy-manage/production-guidance/scaling-considerations.md)
- [Resize deployment](docs-content://deploy-manage/deploy/cloud-enterprise/resize-deployment.md)
- [Autoscaling in ECE and ECH](docs-content://deploy-manage/autoscaling/autoscaling-in-ece-and-ech.md)

Temporary `429`s from load spikes typically resolve on their own as the system scales up, as long as your {{es}} cluster has sufficient capacity.

#### {{serverless-full}} deployments

For {{serverless-full}} projects, you can either decrease data volume or request higher limits.

To increase the rate limit, [contact Elastic Support](docs-content://troubleshoot/ingest/opentelemetry/contact-support.md).
