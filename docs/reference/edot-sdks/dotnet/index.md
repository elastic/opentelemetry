---
navigation_title: EDOT .NET
description: The Elastic Distribution of OpenTelemetry (EDOT) .NET provides an extension of the OpenTelemetry SDK for .NET, configured for the best experience with Elastic Observability. 
applies_to:
  stack:
  serverless:
    observability:
  product:
    edot_dotnet: ga
products:
  - id: cloud-serverless
  - id: observability
  - id: edot-sdk

---

# Elastic Distribution of OpenTelemetry .NET

The {{edot}} (EDOT) .NET provides an extension of the [OpenTelemetry SDK for .NET](https://opentelemetry.io/docs/languages/net), configured for the best experience with Elastic Observability. 

Use EDOT .NET to start the OpenTelemetry SDK with your .NET application, and automatically capture tracing data, performance metrics, and logs. Traces, metrics, and logs can be sent to any OpenTelemetry Protocol (OTLP) Collector you choose.

A goal of this distribution is to avoid introducing proprietary concepts in addition to those defined by the wider OpenTelemetry community. For any additional features introduced, Elastic aims at contributing them back to the contrib OpenTelemetry project.

## Features [edot-sdks-dotnet-features]

In addition to all the features of OpenTelemetry .NET, with EDOT .NET you have access to the following:

* Improvements and bug fixes contributed by the Elastic team before the changes are available in contrib OpenTelemetry repositories.
* Optional features that can enhance OpenTelemetry data that is being sent to Elastic.
* Elastic-specific processors that ensure optimal compatibility when exporting OpenTelemetry signal data to an Elastic backend like an Elastic Observability deployment.
* Preconfigured collection of tracing and metrics signals, applying some opinionated defaults, such as which sources are collected by default. For example, the OpenTelemetry protocol [(OTLP) exporter](https://opentelemetry.io/docs/specs/otlp) is enabled by default.
* Instrumentation assembly scanning to automatically enable instrumentation from installed contrib NuGet packages.

Follow the step-by-step instructions in [Setup](/reference/edot-sdks/dotnet/setup/index.md) to get started.

## Release notes [edot-sdks-dotnet-release-notes]

For the latest release notes, including known issues, deprecations, and breaking changes, refer to [EDOT .NET release notes](elastic-otel-dotnet://release-notes/index.md)