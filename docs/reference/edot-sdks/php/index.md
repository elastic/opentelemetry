---
navigation_title: EDOT PHP
description: The Elastic Distribution of OpenTelemetry PHP (EDOT PHP) is a customized version of OpenTelemetry for PHP.
applies_to:
  stack:
  serverless:
    observability:
products:
  - id: cloud-serverless
  - id: observability
  - id: edot-sdk
---

# Elastic Distribution of OpenTelemetry PHP

The {{edot}} (EDOT) PHP is a customized version of [OpenTelemetry for PHP](https://opentelemetry.io/docs/languages/php), configured for the best experience with Elastic Observability. 

Use EDOT PHP to start the OpenTelemetry SDK with your PHP application, and automatically capture tracing data, performance metrics, and logs. Traces, metrics, and logs can be sent to any OpenTelemetry Protocol (OTLP) Collector you choose.

A goal of this distribution is to avoid introducing proprietary concepts in addition to those defined by the wider OpenTelemetry community. For any additional features introduced, Elastic aims at contributing them back to the upstream OpenTelemetry project.

## Features

In addition to all the features of OpenTelemetry PHP, with EDOT PHP you have access to the following:

* SDK improvements and bug fixes contributed by the Elastic team before the changes are available upstream in OpenTelemetry repositories.
* Optional features that can enhance OpenTelemetry data that is being sent to Elastic.
* Elastic-specific processors that ensure optimal compatibility when exporting OpenTelemetry signal data to an Elastic backend like an Elastic Observability deployment.
* Preconfigured collection of tracing and metrics signals, applying some opinionated defaults, such as which sources are collected by default. For example, the OpenTelemetry protocol (OTLP) exporter is enabled by default.
* Built-in support for asynchronous data transmission, reducing request latency
* Out-of-the-box auto-instrumentation — no need to modify your code. EDOT PHP takes care of enabling telemetry collection automatically.
* Additional runtime features such as automatic root span creation, URL grouping, and inferred spans to provide richer and more structured trace data with minimal setup.
* Compatibility with APM Agent Central Configuration to modify the settings of the EDOT PHP agent without having to restart the application.

Follow the step-by-step instructions in [Setup](/reference/edot-sdks/php/setup/index.md) to get started.

## Release notes

For the latest release notes, including known issues, deprecations, and breaking changes, refer to [EDOT PHP release notes](elastic-otel-php://release-notes/index.md)
