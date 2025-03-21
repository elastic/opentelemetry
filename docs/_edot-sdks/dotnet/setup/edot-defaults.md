---
title: Opinionated defaults
layout: default
nav_order: 6
parent: Setup
grand_parent: EDOT .NET
---

# EDOT .NET opinionated defaults

When using EDOT .NET, you are opted into Elastic defaults for tracing, metrics and logging. These defaults are designed
to provide a quicker getting started experience by automatically enabling data collection from telemetry signals without
requiring as much up-front code as the upstream OpenTelemetry SDK. For most applications, these defaults should be satisfactory.
However, they may be overridden for advanced use cases.

## Defaults for all signals

When using any of the following registration extension methods:

- `IHostApplicationBuilder.AddElasticOpenTelemetry`
- `IServiceCollection.AddElasticOpenTelemetry`
- `IOpenTelemetryBuilder.WithElasticDefaults`

EDOT .NET enables:

- Observation of all signals (tracing, metrics and logging)
- OTLP exporter for all signals

For discrete control of the signals where Elastic defaults apply, consider using one of the
signal-specific extension methods for the `IOpenTelemetryBuilder`.

- `WithElasticTracing`
- `WithElasticMetrics`
- `WithElasticLogging`

For example, you might choose to use the OpenTelemetry SDK but only enable tracing with Elastic
defaults using the following registration code.

```csharp
builder.Services.AddOpenTelemetry()
   .WithElasticTracing();
```

When sending data to an Elastic Observability backend, OTLP via the EDOT Collector is recommended.
EDOT .NET enables OTLP over gRPC as the default for all signals. This behaviour can be disabled using
[configuration](./../configuration).

All signals are configured to apply EDOT .NET defaults for resource attributes via the `ResourceBuilder`.

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
registering them when present.

- [OpenTelemetry.Resources.Container](https://www.nuget.org/packages/OpenTelemetry.Resources.Container)
- [OpenTelemetry.Resources.OperatingSystem](https://www.nuget.org/packages/OpenTelemetry.Resources.OperatingSystem)
- [OpenTelemetry.Resources.Process](https://www.nuget.org/packages/OpenTelemetry.Resources.Process)

> **NOTE**: Instrumentation assembly scanning is not supported when publishing using native AOT.

## Defaults for tracing

EDOT .NET applies subtly different defaults depending on the .NET runtime version being targeted.

### HTTP traces

On .NET 9 and newer runtimes, EDOT .NET observes the `System.Net.Http` source to collect traces from the
.NET HTTP APIs. Since .NET 9, the built-in traces are compliant with current semantic conventions. Using
the built-in `System.Net.Http` source is therefore recommended. If the target application explicitly depends on the `OpenTelemetry.Instrumentation.Http` package, EDOT .NET assumes it should be
used instead of the built-in source. When upgrading applications to .NET 9 and newer, consider removing the
package reference to `OpenTelemetry.Instrumentation.Http`.

On all other runtimes, when using the NuGet installation method, a transistive dependency is included for the 
[OpenTelemetry.Instrumentation.Http](https://www.nuget.org/packages/OpenTelemetry.Instrumentation.Http)
contrib instrumentation package, which is registered on the `TracerProviderBuilder`. 

### gRPC traces

When using the NuGet installation method, a transistive dependency is included for the 
[OpenTelemetry.Instrumentation.GrpcNetClient](https://www.nuget.org/packages/OpenTelemetry.Instrumentation.GrpcNetClient)
contrib instrumentation package.

All scenarios register The gRPC client instrumentation on the `TracerProviderBuilder`. 

### SQL client traces

When using the NuGet installation method, a transistive dependency is included for the 
[OpenTelemetry.Instrumentation.SqlClient](https://www.nuget.org/packages/OpenTelemetry.Instrumentation.SqlClient)
contrib instrumentation package. The SQL client instrumentation is registered in all scenarios, except when 
the target application has been compiled for native AOT.

### Additional sources

EDOT .NET observes the `Elastic.Transport` source to collect traces from Elastic client libraries, such as
`Elastic.Clients.Elasticsearch`, which is built upon the transport layer.

### Instrumentation assembly scanning

Instrumentation assembly scanning checks for the presence of the following contrib instrumentation packages,
registering them when present.

- [OpenTelemetry.Instrumentation.AspNet](https://www.nuget.org/packages/OpenTelemetry.Instrumentation.AspNet)
- [OpenTelemetry.Instrumentation.AspNetCore](https://www.nuget.org/packages/OpenTelemetry.Instrumentation.AspNetCore)
- [OpenTelemetry.Instrumentation.AWS](https://www.nuget.org/packages/OpenTelemetry.Instrumentation.AWS)
- [OpenTelemetry.Instrumentation.ConfluentKafka](https://www.nuget.org/packages/OpenTelemetry.Instrumentation.ConfluentKafka) :
 Instrumentation is registered for both Kafka consumers and producers.
- [OpenTelemetry.Instrumentation.EntityFrameworkCore](https://www.nuget.org/packages/OpenTelemetry.Instrumentation.EntityFrameworkCore)
- [OpenTelemetry.Instrumentation.GrpcCore](https://www.nuget.org/packages/OpenTelemetry.Instrumentation.GrpcCore)
- [OpenTelemetry.Instrumentation.Hangfire](https://www.nuget.org/packages/OpenTelemetry.Instrumentation.Hangfire)
- [OpenTelemetry.Instrumentation.ElasticsearchClient](https://www.nuget.org/packages/OpenTelemetry.Instrumentation.ElasticsearchClient)
- [OpenTelemetry.Instrumentation.Owin](https://www.nuget.org/packages/OpenTelemetry.Instrumentation.Owin)
- [OpenTelemetry.Instrumentation.Quartz](https://www.nuget.org/packages/OpenTelemetry.Instrumentation.Quartz)
- [OpenTelemetry.Instrumentation.ServiceFabricRemoting](https://www.nuget.org/packages/OpenTelemetry.Instrumentation.ServiceFabricRemoting)
- [OpenTelemetry.Instrumentation.StackExchangeRedis](https://www.nuget.org/packages/OpenTelemetry.Instrumentation.StackExchangeRedis)
- [OpenTelemetry.Instrumentation.Wcf](https://www.nuget.org/packages/OpenTelemetry.Instrumentation.Wcf)

> **NOTE**: Instrumentation assembly scanning is not supported when publishing using native AOT.

## Defaults for metrics

EDOT .NET applies subtly different defaults depending on the .NET runtime version being targeted.

### HTTP metrics

On .NET 9 and newer runtimes, EDOT .NET observes the `System.Net.Http` meter to collect metrics from the
.NET HTTP APIs. Since .NET 9, the built-in metrics are compliant with current semantic conventions. Using
the built-in `System.Net.Http` meter is therefore recommended. 

If the target application has an explicit dependency on the `OpenTelemetry.Instrumentation.Http` package, 
EDOT .NET assumes that it should be used instead of the built-in meter. When upgrading applications to .NET 9
and newer, consider removing the package reference to `OpenTelemetry.Instrumentation.Http`.

On all other runtimes, when using the NuGet installation method, a transistive dependency is included for the 
[OpenTelemetry.Instrumentation.Http](https://www.nuget.org/packages/OpenTelemetry.Instrumentation.Http)
contrib instrumentation package, which is registered on the `TracerProviderBuilder`. 

### Runtime metrics

On .NET 9 and newer runtimes, EDOT .NET observes the `System.Runtime` meter to collect metrics from the
.NET HTTP APIs. Since .NET 9, the built-in traces are compliant with current semantic conventions. Using
the built-in `System.Runtime` meter is therefore recommended. 

If the target application has an explicit dependency on the `OpenTelemetry.Instrumentation.Runtime` package,
EDOT .NET assumes that it should be used instead of the built-in meter. When upgrading applications to .NET 9
and newer, consider removing the package reference to `OpenTelemetry.Instrumentation.Runtime`.

On all other runtimes, when using the NuGet installation method, a transistive dependency is included for the 
[OpenTelemetry.Instrumentation.Runtime](https://www.nuget.org/packages/OpenTelemetry.Instrumentation.Runtime)
contrib instrumentation package, which is registered on the `MeterProviderBuilder`. 

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

> **NOTE**: Instrumentation assembly scanning is not supported when publishing using native AOT.

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
| IncludeScopes            | `true`            | `false`                   |

### Instrumentation assembly scanning

Instrumentation assembly scanning is enabled by default and is designed to simplify the registration
code required to configure the OpenTelemetry SDK. Instrumentation assembly scanning uses reflection
to invoke the required registration method for the contrib instrumentation and resource detector packages.

> **IMPORTANT**: Sometimes, it may be safe to manually call the `AddXyzInstrumentation` method,
but that is not guaranteed. When using EDOT .NET, we strongly recommend you remove the registration of
instrumentation to avoid overhead and mitigate the potential for duplicated spans. This has a positive
side-effect of simplifying the code you need to manage.

> **NOTE**: Instrumentation assembly scanning is not supported when publishing using native AOT.

Instrumentation assembly scanning can be disabled via [configuration](./../configuration).