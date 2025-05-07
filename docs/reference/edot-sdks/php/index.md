---
navigation_title: EDOT PHP
description: The Elastic Distribution of OpenTelemetry PHP (EDOT PHP) is a customized version of OpenTelemetry for PHP.
applies_to:
  stack:
  serverless:
    observability:
products:
  - cloud-serverless
  - observability
---

# Elastic Distribution of OpenTelemetry PHP

The Elastic Distribution of OpenTelemetry PHP (EDOT PHP) is a customized version of [OpenTelemetry for PHP](https://opentelemetry.io/docs/languages/php).
EDOT PHP makes it easier to get started using OpenTelemetry in your PHP applications through strictly OpenTelemetry native means, while also providing a smooth and rich out of the box experience with [Elastic Observability](https://www.elastic.co/observability). It's an explicit goal of this distribution to introduce **no new concepts** in addition to those defined by the wider OpenTelemetry community.

With EDOT PHP you have access to all the features of the OpenTelemetry PHP agent plus:

* Access to SDK improvements and bug fixes contributed by the Elastic team _before_ the changes are available upstream in OpenTelemetry repositories.
* Access to optional features that can enhance OpenTelemetry data that is being sent to Elastic.
* Elastic-specific processors that ensure optimal compatibility when exporting OpenTelemetry signal data to an Elastic backend like an Elastic Observability deployment.
* Preconfigured collection of tracing and metrics signals, applying some opinionated defaults, such as which sources are collected by default.
* Ensuring that the OpenTelemetry protocol (OTLP) exporter is enabled by default.
* Built-in support for **asynchronous data transmission**, reducing request latency
* Out-of-the-box auto-instrumentation — no need to modify your code. EDOT PHP takes care of enabling telemetry collection automatically.
* Additional runtime features such as **automatic root span creation**, **URL grouping**, and **inferred spans** to provide richer and more structured trace data with minimal setup.

**Ready to try out EDOT PHP?** Follow the step-by-step instructions in [Get started](./setup/index.md).
