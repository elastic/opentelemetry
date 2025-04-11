---
title: Opinionated defaults
layout: default
nav_order: 6
parent: Setup
grand_parent: EDOT .NET
---

# EDOT .NET opinionated defaults

When using EDOT .NET, Elastic defaults for tracing, metrics and logging are applied. These defaults are designed
to provide a faster getting started experience by automatically enabling data collection from telemetry signals without
requiring as much up-front code as the upstream OpenTelemetry SDK. This has the positive side effect of reducing the
boilerplate code you must maintain in your application. These defaults should be satisfactory for most applications
but may be overridden for advanced use cases.

## Defaults for all signals

When using any of the following registration extension methods:

- `IHostApplicationBuilder.AddElasticOpenTelemetry`
- `IServiceCollection.AddElasticOpenTelemetry`
- `IOpenTelemetryBuilder.WithElasticDefaults`

EDOT .NET enables:

- Observation of all signals (tracing, metrics and logging)
- OTLP exporter for all signals

When sending data to an Elastic Observability backend, OTLP via the EDOT Collector is recommended for
compatibility and is required for full support. EDOT .NET enables OTLP over gRPC as the default for all signals.
This behaviour can be disabled using [configuration](./../configuration).

All signals are configured to apply EDOT .NET defaults for resource attributes via the `ResourceBuilder`.

### Controlling defaults for each signal

For discrete control of the signals where Elastic defaults apply, consider using one of the
signal-specific extension methods for the `IOpenTelemetryBuilder`.

- `WithElasticTracing`
- `WithElasticMetrics`
- `WithElasticLogging`

For example, you might choose to use the OpenTelemetry SDK but only enable tracing with Elastic
defaults using the following registration code.

```csharp
using OpenTelemetry;

builder.Services.AddOpenTelemetry()
   .WithElasticTracing();
```

The preceding code:

1. Imports the required types from the `OpenTelemetry` namespace.
1. Registers the OpenTelemetry SDK for the application using `AddOpenTelemetry`.
1. Adds Elastic defaults for tracing (see below). This doesn't apply Elastic defaults for logging or metrics.

## Defaults for resource attributes

The following attributes are added in all scenarios (NuGet and zero code installations):

| Attribute                  | Details                                                                     |
| -------------------------- | --------------------------------------------------------------------------- |
| `service.instance.id`      | Set with a random GUID to ensure runtime metrics dashboard can be filtered  |
| `telemetry.distro.name`    | Set as `elastic`                                                            |
| `telemetry.distro.version` | Set as the version of the EDOT .NET                                         |

When using the NuGet installation method, transistive dependencies are added for the following
contrib resource detector packages:

- [OpenTelemetry.Resources.Host](https://www.nuget.org/packages/OpenTelemetry.Resources.Host)
- [OpenTelemetry.Resources.ProcessRuntime](https://www.nuget.org/packages/OpenTelemetry.Resources.ProcessRuntime)

The resource detectors are registered on the `ResourceBuilder` to enrich the resource attributes.

### Instrumentation assembly scanning

Instrumentation assembly scanning checks for the presence of the following contrib resource detector packages,
automatically registering them when present.

- [OpenTelemetry.Resources.Container](https://www.nuget.org/packages/OpenTelemetry.Resources.Container)
- [OpenTelemetry.Resources.OperatingSystem](https://www.nuget.org/packages/OpenTelemetry.Resources.OperatingSystem)
- [OpenTelemetry.Resources.Process](https://www.nuget.org/packages/OpenTelemetry.Resources.Process)

{: .warning }
> Instrumentation assembly scanning is not supported for applications using native [AOT](https://learn.microsoft.com/dotnet/core/deploying/native-aot) compilation.

## Defaults for tracing

EDOT .NET applies subtly different defaults depending on the .NET runtime version being targeted.

### HTTP traces

On .NET 9 and newer runtimes, EDOT .NET observes the `System.Net.Http` source to collect traces from the
.NET HTTP APIs. Since .NET 9, the built-in traces are compliant with current semantic conventions. Using
the built-in `System.Net.Http` source is now the recommended choice. If the target application explicitly
depends on the `OpenTelemetry.Instrumentation.Http` package, EDOT .NET assumes it should be
used instead of the built-in source.

{: .note }
When upgrading applications to .NET 9 and newer, consider removing the package reference to `OpenTelemetry.Instrumentation.Http`.

On all other runtimes, when using the NuGet installation method, a transistive dependency is included for the 
[OpenTelemetry.Instrumentation.Http](https://www.nuget.org/packages/OpenTelemetry.Instrumentation.Http)
contrib instrumentation package, which is automatically registered on the `TracerProviderBuilder` via instrumentation assembly scanning.

### gRPC traces

When using the NuGet installation method, a transistive dependency is included for the 
[OpenTelemetry.Instrumentation.GrpcNetClient](https://www.nuget.org/packages/OpenTelemetry.Instrumentation.GrpcNetClient)
contrib instrumentation package.

All scenarios register the gRPC client when instrumentation assembly scanning is supported and enabled.

### SQL client traces

When using the NuGet installation method, a transistive dependency is included for the 
[OpenTelemetry.Instrumentation.SqlClient](https://www.nuget.org/packages/OpenTelemetry.Instrumentation.SqlClient)
contrib instrumentation package.

All scenarios register the SQL client when instrumentation assembly scanning is supported and enabled.

### Additional sources

EDOT .NET observes the `Elastic.Transport` source to collect traces from Elastic client libraries, such as
`Elastic.Clients.Elasticsearch`, which is built upon the [Elastic transport](https://github.com/elastic/elastic-transport-net) layer.

### Instrumentation assembly scanning

Instrumentation assembly scanning checks for the presence of the following contrib instrumentation packages,
registering them when present.

- [OpenTelemetry.Instrumentation.AspNet](https://www.nuget.org/packages/OpenTelemetry.Instrumentation.AspNet)
- [OpenTelemetry.Instrumentation.AspNetCore](https://www.nuget.org/packages/OpenTelemetry.Instrumentation.AspNetCore)
- [OpenTelemetry.Instrumentation.AWS](https://www.nuget.org/packages/OpenTelemetry.Instrumentation.AWS)
- [OpenTelemetry.Instrumentation.ConfluentKafka](https://www.nuget.org/packages/OpenTelemetry.Instrumentation.ConfluentKafka) :
 Instrumentation is registered for both Kafka consumers and producers.
- [OpenTelemetry.Instrumentation.ElasticsearchClient](https://www.nuget.org/packages/OpenTelemetry.Instrumentation.ElasticsearchClient)
- [OpenTelemetry.Instrumentation.EntityFrameworkCore](https://www.nuget.org/packages/OpenTelemetry.Instrumentation.EntityFrameworkCore)
- [OpenTelemetry.Instrumentation.GrpcNetClient](https://www.nuget.org/packages/OpenTelemetry.Instrumentation.GrpcNetClient)
- [OpenTelemetry.Instrumentation.GrpcCore](https://www.nuget.org/packages/OpenTelemetry.Instrumentation.GrpcCore)
- [OpenTelemetry.Instrumentation.Hangfire](https://www.nuget.org/packages/OpenTelemetry.Instrumentation.Hangfire)
- [OpenTelemetry.Instrumentation.Http](https://www.nuget.org/packages/OpenTelemetry.Instrumentation.Http)
- [OpenTelemetry.Instrumentation.Owin](https://www.nuget.org/packages/OpenTelemetry.Instrumentation.Owin)
- [OpenTelemetry.Instrumentation.Quartz](https://www.nuget.org/packages/OpenTelemetry.Instrumentation.Quartz)
- [OpenTelemetry.Instrumentation.ServiceFabricRemoting](https://www.nuget.org/packages/OpenTelemetry.Instrumentation.ServiceFabricRemoting)
- [OpenTelemetry.Instrumentation.SqlClient](https://www.nuget.org/packages/OpenTelemetry.Instrumentation.SqlClient)
- [OpenTelemetry.Instrumentation.StackExchangeRedis](https://www.nuget.org/packages/OpenTelemetry.Instrumentation.StackExchangeRedis)
- [OpenTelemetry.Instrumentation.Wcf](https://www.nuget.org/packages/OpenTelemetry.Instrumentation.Wcf)

{: .warning }
> Instrumentation assembly scanning is not supported for applications using native [AOT](https://learn.microsoft.com/dotnet/core/deploying/native-aot) compilation.

#### ASP.NET Core defaults

To provide a richer experience out-of-the-box, EDOT .NET registers an exception enricher for ASP.NET Core
when using instrumentation assembly scanning.

When an unhandled exception occurs during a request that ASP.NET Core handles, the exception is added as
a span event using the [`AddException`](https://learn.microsoft.com/dotnet/api/system.diagnostics.activity.addexception)
API from `System.Diagnostics`. Span events are stored as logs in the Observability backend and will appear
in the "Errors" UI. Additionally, when the `Exception.Source` property is not null, its value is added as
an attribute `exception.source` on the ASP.NET Core request span.

## Defaults for metrics

EDOT .NET applies subtly different defaults depending on the .NET runtime version being targeted.

### HTTP metrics

On .NET 9 and newer runtimes, EDOT .NET observes the `System.Net.Http` meter to collect metrics from the
.NET HTTP APIs. Since .NET 9, the built-in metrics are compliant with current semantic conventions. Using
the built-in `System.Net.Http` meter is therefore recommended. 

If the target application has an explicit dependency on the `OpenTelemetry.Instrumentation.Http` package, 
EDOT .NET assumes that it should be used instead of the built-in meter. 

{: .note }
When upgrading applications to .NET 9 and newer, consider removing the package reference to `OpenTelemetry.Instrumentation.Http`.

On all other runtimes, when using the NuGet installation method, a transistive dependency is included for the 
[OpenTelemetry.Instrumentation.Http](https://www.nuget.org/packages/OpenTelemetry.Instrumentation.Http)
contrib instrumentation package, which is registered on the `MeterProviderBuilder` via instrumentation assembly scanning.

### Runtime metrics

On .NET 9 and newer runtimes, EDOT .NET observes the `System.Runtime` meter to collect metrics from the
.NET HTTP APIs. Since .NET 9, the built-in traces are compliant with current semantic conventions. Using
the built-in `System.Runtime` meter is therefore recommended. 

If the target application has an explicit dependency on the `OpenTelemetry.Instrumentation.Runtime` package,
EDOT .NET assumes that it should be used instead of the built-in meter.

{: .note }
When upgrading applications to .NET 9 and newer, consider removing the package reference to `OpenTelemetry.Instrumentation.Runtime`.

On all other runtimes, when using the NuGet installation method, a transistive dependency is included for the 
[OpenTelemetry.Instrumentation.Runtime](https://www.nuget.org/packages/OpenTelemetry.Instrumentation.Runtime)
contrib instrumentation package, which is registered on the `MeterProviderBuilder` via instrumentation assembly scanning.

### Process metrics

When using the NuGet installation method, a transistive dependency is included for the 
[OpenTelemetry.Instrumentation.Process](https://www.nuget.org/packages/OpenTelemetry.Instrumentation.Process)
contrib instrumentation package. Process metrics are observed in all scenarios.

### ASP.NET Core metrics

When the target application references the [OpenTelemetry.Instrumentation.AspNetCore](https://www.nuget.org/packages/OpenTelemetry.Instrumentation.AspNetCore)
NuGet package, the following meters are observed by default:

- `Microsoft.AspNetCore.Hosting`
- `Microsoft.AspNetCore.Routing`
- `Microsoft.AspNetCore.Diagnostics`
- `Microsoft.AspNetCore.RateLimiting`
- `Microsoft.AspNetCore.HeaderParsing`
- `Microsoft.AspNetCore.Server.Kestrel`
- `Microsoft.AspNetCore.Http.Connections`

### Additional meters

EDOT .NET observes the `System.Net.NameResolution` meter, to collect metrics from DNS.

### Instrumentation assembly scanning

Instrumentation assembly scanning checks for the presence of the following contrib instrumentation packages,
registering them when present.

- [OpenTelemetry.Instrumentation.AspNet](https://www.nuget.org/packages/OpenTelemetry.Instrumentation.AspNet)
- [OpenTelemetry.Instrumentation.AspNetCore](https://www.nuget.org/packages/OpenTelemetry.Instrumentation.AspNetCore)
- [OpenTelemetry.Instrumentation.AWS](https://www.nuget.org/packages/OpenTelemetry.Instrumentation.AWS)
- [OpenTelemetry.Instrumentation.Cassandra](https://www.nuget.org/packages/OpenTelemetry.Instrumentation.Cassandra)
- [OpenTelemetry.Instrumentation.ConfluentKafka](https://www.nuget.org/packages/OpenTelemetry.Instrumentation.ConfluentKafka) :
  Instrumentation is registered for both Kafka consumers and producers.
- [OpenTelemetry.Instrumentation.EventCounters](https://www.nuget.org/packages/OpenTelemetry.Instrumentation.EventCounters)
- [OpenTelemetry.Instrumentation.Http](https://www.nuget.org/packages/OpenTelemetry.Instrumentation.Http)
- [OpenTelemetry.Instrumentation.Runtime](https://www.nuget.org/packages/OpenTelemetry.Instrumentation.Runtime)
- [OpenTelemetry.Instrumentation.Process](https://www.nuget.org/packages/OpenTelemetry.Instrumentation.Process)

{: .warning }
> Instrumentation assembly scanning is not supported for applications using native [AOT](https://learn.microsoft.com/dotnet/core/deploying/native-aot) compilation.

### Configuration defaults

To ensure the best compatibility of metric data (specifically from the histogram instrument), EDOT .NET
defaults the `TemporalityPreference` configuration setting on `MetricReaderOptions` to use the
`MetricReaderTemporalityPreference.Delta` temporality.

## Defaults for logging

EDOT .NET enables the following options that are not enabled by default when using the upstream
OpenTelemetry SDK.

| Option                   | EDOT .NET default | OpenTelemetry SDK default |
| ------------------------ | ----------------- | ------------------------- |
| IncludeFormattedMessage  | `true`            | `false`                   |
| IncludeScopes            | `false` (Since 1.0.2) *           | `false`                   |

\* Since 1.0.2 `IncludeScopes` is no longer enabled by default. See [troubleshooting](./../troubleshooting/#missing-log-records).
1.0.0 and 1.0.1 default to `true`.

### Instrumentation assembly scanning

Instrumentation assembly scanning is enabled by default and is designed to simplify the registration
code required to configure the OpenTelemetry SDK. Instrumentation assembly scanning uses reflection
to invoke the required registration method for the contrib instrumentation and resource detector packages.

{: .warning }
> It may not be safe to manually call the `AddXyzInstrumentation` method in combination with assembly scanning,
> for all instrumentations. When using EDOT .NET, we strongly recommend you remove the registration of instrumentation
> to avoid overhead and mitigate the potential for duplicated spans. This has a positive side-effect of simplifying the
> code you need to manage.

Alternatively, if you need to configure advanced options when registering instrumentation,
disable instrumentation assembly scanning via [configuration](./../configuration) and prefer manually registering
all instrumentation in your application code.

{: .warning }
> Instrumentation assembly scanning is not supported for applications using native [AOT](https://learn.microsoft.com/dotnet/core/deploying/native-aot) compilation.