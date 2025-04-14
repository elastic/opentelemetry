---
title: Elastic Cloud Serverless
layout: default
nav_order: 2
parent: Quickstart
---

# Quickstart on Elastic Cloud Serverless

The Managed OTLP Endpoint simplifies OpenTelemetry data ingestion. It provides an endpoint for OpenTelemetry SDKs and Collectors to send telemetry data, with Elastic handling scaling, data processing, and storage. The Managed OTLP Endpoint is exclusively for Elastic Cloud users, initially available in Elastic Cloud Serverless only.

This endpoint is designed for the following use cases:

* Logs and Infrastructure Monitoring: Logs forwarded in OTLP format and host and Kubernetes metrics in OTLP format.
* APM: Application telemetry in OTLP format.

## Differences from the existing Elastic APM Endpoint

The Elastic Cloud Managed OTLP Endpoint ensures that OpenTelemetry data is stored without any schema translation, preserving both OpenTelemetry semantic conventions and resource attributes. It supports ingesting OTLP logs, metrics, and traces in a unified manner, ensuring consistent treatment across all telemetry data.

## Prerequisites

* An Elastic Observability Serverless project.
* An Elastic Distribution of OpenTelemetry or any system that can forward logs, metrics, or traces in OTLP format.

## Retrieve connection details for your project

{: .note }
> The following instructions use a managed OTLP endpoint on Elastic Cloud Serverless. This feature is in **Technical Preview** and shouldn't be used in production.

Follow these steps to retrieve the managed OTLP endpoint URL for your Serverless project:

   1. In Elastic Cloud, open your Observability project.
   2. Go to **Add data**, **Application**, **OpenTelemetry**.
   3. Select **Managed OTLP Endpoint** in the second step.
   4. Copy the OTLP endpoint configuration value.
   5. Select **Create API Key** to generate an API key.

## Troubleshoot

### Api Key prefix not found

The following error is due to an improperly formatted API key:

```txt
Exporting failed. Dropping data.
{"kind": "exporter", "data_type": }
"Unauthenticated desc = ApiKey prefix not found"
```

Format your API key as `"Authorization": "ApiKey <api-key-value-here>"` or `"Authorization=ApiKey <api-key>"` depending on whether you're using a Collector or SDK.

### Error: too many requests

The managed endpoint has per-project rate limits in place. If you reach this limit, contact our [support team](https://support.elastic.co).

## Provide feedback

Help improve the Elastic Cloud Managed OTLP Endpoint by sending us feedback in our [discussion forum](https://discuss.elastic.co/c/apm) or [community Slack](https://elasticstack.slack.com/signup).

For EDOT collector feedback, open an issue in the [elastic-agent repository](https://github.com/elastic/elastic-agent/issues).
