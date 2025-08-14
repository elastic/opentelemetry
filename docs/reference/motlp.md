---
navigation_title: Managed OTLP Endpoint
description: Reference documentation for the Elastic Cloud Managed OTLP Endpoint.
applies_to:
  serverless:
    observability: preview
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

Telemetry is stored in Elastic in OTLP format, preserving resource attributes and original semantic conventions. If no specific dataset or namespace is provided, the data streams are: `traces-generic.otel-default`, `metrics-generic.otel-default`, and `logs-generic.otel-default`.

You don't need to use APM Server when ingesting data through the Managed OTLP Endpoint. The APM integration (`.apm` endpoint) is a legacy ingest path that only supports traces and translates OTLP telemetry to ECS, whereas {{motlp}} natively ingests OTLP data for logs, metrics, and traces.

## Send data to Elastic

Follow these steps to send data to Elastic using the {{motlp}}.

::::::{stepper}

:::::{step} Check the requirements

To use the {{motlp}} you need the following:

* An Elastic Observability Serverless project. Security projects are not yet supported.
* An OTLP-compliant shipper capable of forwarding logs, metrics, or traces in OTLP format. This can include the OpenTelemetry Collector (EDOT, Contrib, or other distributions), OpenTelemetry SDKs (EDOT, upstream, or other distributions), or any other forwarder that supports the OTLP protocol.

:::::

:::::{step} Locate Your {{motlp}} Endpoint

To retrieve your {{motlp}} endpoint address and an API key, follow these steps:

1. In {{ecloud}}, create an Observability project or open an existing one.
2. Select your project's name and then select **Manage project**.
3. Locate the **Connection alias** and select **Edit**.
4. Copy the **Managed OTLP endpoint** URL.

% ## commented out until mOTLP on ECH is available
% ### Elastic Cloud on Elasticsearch ({{ech}})
% 1. Open your deployment in the Elastic Cloud console.
% 2. Navigate to **Integrations** and find **OpenTelemetry** or **Managed OTLP**.
% 3. Copy the endpoint URL shown.
% ## Self-Managed
% For self-managed environments, you can deploy and expose an OTLP-compatible endpoint using the EDOT Collector as a gateway. Refer to [EDOT deployment docs](https://www.elastic.co/docs/reference/opentelemetry/edot-collector/modes#edot-collector-as-gateway).
%
% :::{note}
% Please reach out to support, and then Engineering can look into increasing it based on the license tier or for experimentation purposes.
% :::

:::::

:::::{step} Create an API key

Generate an API key with appropriate ingest privileges to authenticate OTLP traffic:

1. In {{ecloud}}, go to **Manage project** → **API Keys**.
2. Select **Create API Key**.
3. Name the key. For example, `otlp-client`.
4. Edit the optional security settings.
5. Select **Create API Key**.
6. Copy the key to the clipboard.

Add this key to your final API key string. For example:

```
Authorization: ApiKey <your-api-key>
```

:::{important}
The API key copied from Kibana does not include the `ApiKey` scheme. Always prepend `ApiKey ` before using it in your configuration or encoding it for Kubernetes secrets. For example:

  - Correct: `Authorization: ApiKey abc123`
  - Incorrect: `Authorization: abc123`
:::

:::::

:::::{step} Send data to the {{motlp}}

The final step is to use the {{motlp}} endpoint and your Elastic API key to send data to {{ecloud}}.

::::{tab-set}

:::{tab-item} OpenTelemetry Collector example
To send data to the {{motlp}} from the {{edot}} Collector or the upstream Collector, configure the `otlp` exporter:

```yaml
exporters:
  otlp:
    endpoint: https://<motlp-endpoint>
    headers:
      Authorization: ApiKey <your-api-key>
```

Set the API key as an environment variable or directly in the configuration as shown in the example.
:::

:::{tab-item} OpenTelemetry SDK example
To send data to the {{motlp}} from {{edot}} SDKs or upstream SDKs, set the following variables in your application's environment:

```bash
export OTEL_EXPORTER_OTLP_ENDPOINT="https://<motlp-endpoint>"
export OTEL_EXPORTER_OTLP_HEADERS="Authorization=ApiKey <your-api-key>"
```

Avoid extra spaces in the header. For Python SDKs replace any spaces with `%20`. For example:

```
OTEL_EXPORTER_OTLP_HEADERS=Authorization=ApiKey%20<your-api-key>`
```
:::

:::{tab-item} Kubernetes example
You can store your API key in a Kubernetes secret and reference it in your OTLP exporter configuration. This is more secure than hardcoding credentials.

The API key from Kibana does not include the `ApiKey` scheme. You must prepend `ApiKey ` before storing it. 

For example, if your API key from Kibana is `abc123`, run:

```bash
kubectl create secret generic otlp-api-key \
  --namespace=default \
  --from-literal=api-key="ApiKey abc123"
```

Mount the secret as an environment variable or file, then reference it in your OTLP exporter configuration:

```yaml
exporters:
  otlp:
    endpoint: https://<motlp-endpoint>
    headers:
      Authorization: ${API_KEY}
```

And in your deployment spec:

```yaml
env:
  - name: API_KEY
    valueFrom:
      secretKeyRef:
        name: otlp-api-key
        key: api-key
```

:::{important}
When creating a Kubernetes secret, always encode the full string in Base64, including the scheme (for example, `ApiKey abc123`).
:::
:::

::::

:::::

::::::

## Rate limiting

Requests to the {{motlp}} are subject to rate limiting. If you send data at a rate that exceeds the defined limits, your requests will be temporarily rejected.

The rate limit is currently set to 15 MiB per second, with a burst limit of 30 MiB per second. As long as your data ingestion rate stays at or below this average, your requests will be accepted.

If send data that exceeds the available rate limit, the {{motlp}} will respond with an HTTP 429 Too Many Requests status code. A log message similar to this will appear in the OpenTelemetry Collector's output:

```json
{
  "code": 8,
  "message": "error exporting items, request to <ingest endpoint> responded with HTTP Status Code 429"
}
```

Once your sending rate drops back within the allowed limit, the system will automatically begin accepting requests again.

:::{note}
If you need to increase the rate limit, reach out to Elastic Support.
:::

## Failure store

The {{motlp}} endpoint is designed to be highly available and resilient. However, there are some scenarios where data might be lost or not sent completely. The [Failure store](docs-content://manage-data/data-store/data-streams/failure-store.md) is a mechanism that allows you to recover from these scenarios.

The Failure store is always enabled for {{motlp}} data streams. This prevents ingest pipeline exceptions and conflicts with data stream mappings. Failed documents are stored in a separate index. You can view the failed documents from the **Data Set Quality** page. Refer to [Data set quality](docs-content://solutions/observability/data-set-quality-monitoring.md).

## Routing logs to dedicated datasets

You can route logs to dedicated datasets by setting the `data_stream.dataset` attribute to the log record. This attribute is used to route the log to the corresponding dataset.

For example, if you want to route the {{edot-cf}} logs to custom datasets, you can add the following attributes to the log records:

```yaml
processors:
  transform:
    - set(attributes["data_stream.dataset"], "aws.cloudtrail") where attributes["aws.cloudtrail.event_id"] != nil
    - set(attributes["data_stream.dataset"], "aws.vpc-flow-logs") where attributes["aws.vpc.flow.log.version"] != nil
```

## Limitations

The following limitations apply when using the {{motlp}}:

* Tail-based sampling (TBS) is not available.
* Universal Profiling is not available.
* Only supports histograms with delta temporality. Cumulative histograms are dropped.
* Latency distributions based on histogram values have limited precision due to the fixed boundaries of explicit bucket histograms.

## Billing

For more information on billing, refer to [Elastic Cloud pricing](https://www.elastic.co/pricing/serverless-observability).
