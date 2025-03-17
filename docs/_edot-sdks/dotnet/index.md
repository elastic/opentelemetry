---
title: EDOT .NET
layout: default
nav_order: 2
---

# EDOT .NET

The Elastic Distribution of OpenTelemetry .NET (EDOT .NET) provides an extension of the [OpenTelemetry SDK for .NET](https://opentelemetry.io/docs/languages/net).

EDOT .NET makes it easier to get started using OpenTelemetry in your .NET applications through strictly OpenTelemetry native means while also providing a smooth 
and rich out-of-the-box experience with [Elastic Observability](https://www.elastic.co/observability).

> **NOTE**: To learn more about OpenTelemetry distributions in general, visit the [OpenTelemetry documentation](https://opentelemetry.io/docs/concepts/distributions).

The quickest way to get started with EDOT .NET is to follow our [quickstart](./setup/quickstart) guide.

## Features

With EDOT .NET, you have access to all the features of the [OpenTelemetry SDK for .NET](https://github.com/open-telemetry/opentelemetry-dotnet) plus:

* Access to SDK enhancements and bug fixes contributed by the Elastic team _before_ the changes are available upstream in OpenTelemetry repositories.
* Elastic-specific processors that ensure optimal compatibility when exporting OpenTelemetry signal data to an Elastic backend like an Elastic Observability deployment.
* Preconfigured collection of tracing and metrics signals, applying [opinionated defaults](./setup/edot-defaults), such as which instrumentation sources are 
observed by default.
* Ensuring that the OpenTelemetry protocol [(OTLP) exporter](https://opentelemetry.io/docs/specs/otlp) is enabled by default.

### Instrumentation assembly scanning

NOTE: This feature does not function when your application uses the single-file deployment feature.

## .NET runtime support

EDOT .NET support all [officially supported](https://dotnet.microsoft.com/en-us/platform/support/policy) versions of [.NET](https://dotnet.microsoft.com/download/dotnet) and
[.NET Framework](https://dotnet.microsoft.com/download/dotnet-framework)¹ (an older Windows-based .NET implementation), except `.NET Framework 3.5`.

***1.** Due to assembly binding issues introduced by Microsoft, we recommend at least .NET Framework 4.7.2 for best compatibility.*

## Compatibility matrix

Data can be exported in the OpenTelemetry-native [OTLP (OpenTelemetry protocol)](https://opentelemetry.io/docs/specs/otlp) format via gRPC (recommended)
and HTTP to self-managed, Elastic Cloud Hosted or Elastic Cloud Serverless observability backends.

For the best (and supported) experience, we recommend exporting data from EDOT .NET via the [EDOT Collector](./edot-collector/index).

| EDOT .NET version | 8.x      | 9.x      | Serverless |
| ----------------- | -------- | -------- | ---------- |
| 1.0.0             | 8.18.0+¹ | 9.0.0+¹  | 🗸 ²       |

***1.** Via the EDOT Collector.*

***2.** Via the OTel-native ingest endpoint.*