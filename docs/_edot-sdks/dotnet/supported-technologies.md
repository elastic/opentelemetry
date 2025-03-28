---
title: Supported Technologies
layout: default
nav_order: 3
parent: EDOT .NET
---

# Technologies Supported by EDOT .NET SDK

EDOT .NET is a distribution of OpenTelemetry .NET SDK, it thus inherits all the supported technologies
from the [upstream SDK](https://github.com/open-telemetry/opentelemetry-dotnet).

## .NET Frameworks

This includes the currently supported Microsoft .NET frameworks:

| Framework              | End of support      |
|:---------------------- |:------------------- |
| .NET Framework 4.6.2   | 12th Jan 2027       |
| .NET Framework 4.7     | _Not announced_     |
| .NET Framework 4.7.1   | _Not announced_     |
| .NET Framework 4.7.2   | _Not announced_     |
| .NET Framework 4.8     | _Not announced_     |
| .NET Framework 4.8.1   | _Not announced_     |
| .NET 8                 | 10th November 2026  |
| .NET 9                 | 12th May 2026       |
| .NET 10 (preview)¹     | _Not announced_     |

1. Official support begins once this is released (generally available) in November 2025

For further details, see [Microsoft .NET Framework support dates](https://learn.microsoft.com/lifecycle/products/microsoft-net-framework)
and [.NET Support Policy](https://dotnet.microsoft.com/platform/support/policy).

## Instrumentations

Instrumentation for .NET can occur in three main ways:

1. Built-in OpenTelemetry native instrumentation (the end goal for OpenTelemetry),
where libraries are instrumented using the .NET APIs, requiring no bridging libraries to
be observed. Many Microsoft recent libraries implement OpenTelemetry native instrumentation, and many third parties 
are working on such improvements. When native OTel instrumentation
exists, it may be observed directly by the OpenTelemetry SDK (and, by extension, EDOT .NET) by calling
`AddSource` to register the `ActivitySource` used by the instrumented code.
1. [Contrib instrumentation](https://github.com/open-telemetry/opentelemetry-dotnet-contrib) packages.
These packages "bridge" existing telemetry from libraries to emit or enrich OpenTelemetry spans and metrics.
Some packages have no dependencies and are included with EDOT .NET [by default](./setup/edot-defaults).
Others, which bring in transitive dependencies, can be added to applications and registered with the 
OpenTelemetry SDK. EDOT .NET provides an instrumentation assembly scanning feature to register any contrib instrumentation without code changes.
1. Additional instrumentation is available for some components and libraries when using the
profiler-based [zero code installation](./setup/zero-code), for which  EDOT .NET does not add any additional
instrumentation. The current list supported upstream can be found in the 
[.NET zero-code documentation](https://opentelemetry.io/docs/zero-code/dotnet/instrumentations/).

See also the EDOT .NET [opinionated defaults](./setup/edot-defaults) for behaviour that might differ from the
OpenTelemetry NET SDK defaults.