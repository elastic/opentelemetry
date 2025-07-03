---
navigation_title: Managed OTLP Endpoint
description: Reference documentation for the Elastic Cloud Managed OTLP Endpoint.
applies_to:
  serverless:
    observability: preview
products:
  - id: cloud-serverless
  - id: observability
---

# Elastic Cloud Managed OTLP Endpoint

The {{motlp}} is a managed endpoint for sending OpenTelemetry signals to Elastic Cloud, initially available in {{serverless-full}} only. It provides an endpoint for OpenTelemetry SDKs and Collectors to send telemetry data, with Elastic handling scaling, data processing, and storage.

This endpoint is designed for the following use cases:

* Logs and infrastructure monitoring: Logs forwarded in OTLP format and host and Kubernetes metrics in OTLP format
* APM: Application telemetry in OTLP format

::::{important}
{{motlp}} is not currently available for {{ech}} deployments.
::::

## Differences from the Elastic APM Endpoint

The {{motlp}} ensures that OpenTelemetry data is stored without any schema translation, preserving both OpenTelemetry semantic conventions and resource attributes. It supports ingesting OTLP logs, metrics, and traces in a unified manner, ensuring consistent treatment across all telemetry data.

## Prerequisites

To send data to the {{motlp}}, you need:

* An Elastic Observability Serverless project.
* An {{edot}} or any system that can forward logs, metrics, or traces in OTLP format.

## Find your OTLP Endpoint

To retrieve your {{motlp}} endpoint address and an API key, follow these steps:

   1. In {{ecloud}}, open your Observability project.
   2. Go to **Add data** → **Application** → **OpenTelemetry**.
   3. Select **Managed OTLP Endpoint** in the second step.
   4. Copy the OTLP endpoint configuration value.
   5. Select **Create API Key** to generate an API key.

## Send data in OTLP format

To send data in OTLP format to the {{motlp}}, you need to configure your {{edot}} or any system that can forward logs, metrics, or traces in OTLP format. 

Refer to the [Quickstart guides](/reference/quickstart/index.md) for more information.

## Compatibility

The {{motlp}} does not currently support these features:

* Tail-based sampling (TBS)
* Universal Profiling
