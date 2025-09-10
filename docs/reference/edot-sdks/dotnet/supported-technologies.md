---
navigation_title: Supported technologies
description: Technologies supported by the Elastic Distribution of OpenTelemetry .NET.
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

# Technologies supported by EDOT .NET SDK

EDOT .NET is a distribution of OpenTelemetry .NET SDK. It inherits all the [supported](/reference/compatibility/nomenclature.md) technologies from the [upstream SDK](https://github.com/open-telemetry/opentelemetry-dotnet).

## EDOT Collector and Elastic Stack versions [dotnet-supported-technologies-edot-collector-and-e]

EDOT .NET sends data through the OpenTelemetry protocol (OTLP). While OTLP ingest works with later 8.16+ versions of the EDOT Collector, for full support use either the [EDOT Collector](/reference/edot-collector/index.md) versions 9.x or [{{serverless-full}}](docs-content://deploy-manage/deploy/elastic-cloud/serverless.md) for OTLP ingest.

:::{note}
Ingesting data from EDOT SDKs through EDOT Collector 9.x into Elastic Stack versions 8.18+ is supported.
:::

Refer to [EDOT SDKs compatibility](/reference/compatibility/sdks.md) for support details.

## .NET Frameworks

This includes the currently supported Microsoft .NET frameworks:

| Framework              | End of support      |
|:---------------------- |:------------------- |
| .NET Framework 4.6.2   | 12th Jan 2027       |
| .NET Framework 4.7     | Not announced       |
| .NET Framework 4.7.1   | Not announced       |
| .NET Framework 4.7.2   | Not announced       |
| .NET Framework 4.8     | Not announced       |
| .NET Framework 4.8.1   | Not announced       |
| .NET 8                 | 10th November 2026  |
| .NET 9                 | 12th May 2026       |
| .NET 10 (preview)¹     | Not announced       |

1. Official support begins once this is released (generally available) in November 2025

For further details, see [Microsoft .NET Framework support dates](https://learn.microsoft.com/lifecycle/products/microsoft-net-framework)
and [.NET Support Policy](https://dotnet.microsoft.com/platform/support/policy).

## Instrumentations [dotnet-supported-technologies-instrumentations]

Instrumentation for .NET can occur in three ways:

1. Built-in OpenTelemetry native instrumentation, where libraries are instrumented using the .NET APIs, requiring no bridging libraries to be observed. Many Microsoft recent libraries implement OpenTelemetry native instrumentation, and many third parties are working on such improvements. When native OTel instrumentation exists, it may be observed directly by the OpenTelemetry SDK (and, by extension, EDOT .NET) by calling `AddSource` to register the `ActivitySource` used by the instrumented code.

2. [Contrib instrumentation](https://github.com/open-telemetry/opentelemetry-dotnet-contrib) packages. These packages bridge existing telemetry from libraries to emit or enrich OpenTelemetry spans and metrics. Some packages have no dependencies and are included with EDOT .NET [by default](/reference/edot-sdks/dotnet/setup/edot-defaults.md). Others, which bring in transitive dependencies, can be added to applications and registered with the OpenTelemetry SDK. EDOT .NET provides an instrumentation assembly scanning feature to register any contrib instrumentation without code changes.

3. Additional instrumentation is available for some components and libraries when using the profiler-based [zero code installation](/reference/edot-sdks/dotnet/setup/zero-code.md), for which  EDOT .NET does not add any additional instrumentation. Find the current list supported in the [.NET zero-code documentation](https://opentelemetry.io/docs/zero-code/dotnet/instrumentations/).

See also the EDOT .NET [opinionated defaults](/reference/edot-sdks/dotnet/setup/edot-defaults.md) for behavior that might differ from the OpenTelemetry NET SDK defaults.

:::{warning}
Instrumentation assembly scanning is not supported for applications using native [AOT](https://learn.microsoft.com/dotnet/core/deploying/native-aot) compilation.
:::

## .NET runtime support

EDOT .NET support all [officially supported](https://dotnet.microsoft.com/en-us/platform/support/policy) versions of [.NET](https://dotnet.microsoft.com/download/dotnet) and
[.NET Framework](https://dotnet.microsoft.com/download/dotnet-framework) (an older Windows-based .NET implementation), except `.NET Framework 3.5`. Due to assembly binding issues introduced by Microsoft, use at least .NET Framework 4.7.2 for best compatibility.

## Exporting data to Elastic

You can export data in the OpenTelemetry-native [OTLP (OpenTelemetry protocol)](https://opentelemetry.io/docs/specs/otlp) format through gRPC and HTTP to self-managed, {{ech}}, or {{serverless-full}} observability.