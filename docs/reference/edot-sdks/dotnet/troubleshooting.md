---
navigation_title: Troubleshooting
applies_to:
  stack:
  serverless:
    observability:
products:
  - id: cloud-serverless
  - id: observability
---

# Troubleshooting the EDOT .NET SDK

Use the information in this section to troubleshoot common problems. As a first step, ensure your stack is 
compatible with the [supported technologies](.//supported-technologies.md) for EDOT .NET and the OpenTelemetry SDK.

Don’t worry if you can’t figure out what the problem is; we’re here to help. If you are an existing
Elastic customer with a support contract, please create a ticket in the [Elastic Support portal](https://support.elastic.co/customers/s/login/).
If not, post in the [APM discuss forum](https://discuss.elastic.co/c/apm) or [open a GitHub issue](https://github.com/elastic/elastic-otel-dotnet/issues).

For most problems, such as when no data is received in your Elastic Observability backend, it’s a good idea to first check
the EDOT .NET logs which will provide initialization details and OpenTelemetry SDK events. If you don’t see anything suspicious
 in the EDOT .NET logs (no warning or error), it’s recommended to switch the log level to `Trace` for further investigation.

## Known issues

### Missing log records

The upstream SDK is (currently) [not spec-compliant](https://github.com/open-telemetry/opentelemetry-dotnet/issues/4324) regarding 
the deduplication of attributes when exporting log records. When a log is created within multiple scopes, each scope may store information
using the same logical key. In this situation, attributes will be duplicated in the exported data. This situation is most likely to present when 
logging in to the scope of a request and when the `OpenTelemetryLoggerOptions.IncludeScopes` option is enabled. ASP.NET Core adds the 
`RequestId` to multiple scopes. We therefore recommend not enabling `IncludeScopes` until this is fixed in the SDK. When using the
EDOT Collector or Managed OTLP endpoint in serverless, non-compliant log records will fail to be ingested.

EDOT .NET currently emits a warning if it detects the use of `IncludeScopes` in ASP.NET Core scenarios.

It is also possible for this to occur even when `IncludeScopes` is false. The following code will also result in duplicate
attributes and the potential for lost log records.

```csharp
Logger.LogInformation("Eat your {fruit} {fruit} {fruit}!", "apple", "banana", "mango");
```

To avoid this scenario, ensure each placeholder uses a unique name. e.g.

```csharp
Logger.LogInformation("Eat your {fruit1} {fruit2} {fruit3}!", "apple", "banana", "mango");
```

## Obtaining EDOT .NET diagnostic logs

The Elastic Distribution of OpenTelemetry .NET includes built-in diagnostic logging, which can be directed
to a file, STDOUT and, in common scenarios, an `ILogger` instance. EDOT .NET also observes the built-in diagnostics events
from the upstream OpenTelemetry SDK and includes those in its logging output. The log output may be collected
and used to diagnose issues locally during development and when engaging with Elastic support channels.

## ASP.NET Core (generic host) logging integration

When building applications based on the generic host, such as those created by the [ASP.NET Core](https://learn.microsoft.com/aspnet/core/introduction-to-aspnet-core)
and [worker service](https://learn.microsoft.com/dotnet/core/extensions/workers) templates, the Elastic Distribution
of OpenTelemetry .NET will attempt to automatically register with the built-in logging components when using
the `IHostApplicationBuilder.AddElasticOpenTelemetry` extension method to register EDOT .NET.

```csharp
var builder = WebApplication.CreateBuilder(args);
builder.AddElasticOpenTelemetry();
```

In this scenario, EDOT .NET will attempt to access an available `ILoggerFactory` and create an `ILogger`, logging 
to the event category `Elastic.OpenTelemetry`. This will be registered as the additional logger for the EDOT .NET
diagnostics unless a user-provided `ILogger` has already been configured. This ensures that EDOT .NET and OpenTelemetry
SDK logs are written for the application's configured logging providers. In ASP.NET Core, this includes the console logging
provider and will result in logs such as the following:

```
info: Elastic.OpenTelemetry[0]
      Elastic Distribution of OpenTelemetry (EDOT) .NET: 1.0.0
info: Elastic.OpenTelemetry[0]
      EDOT log file: <disabled>
info: Microsoft.Hosting.Lifetime[14]
      Now listening on: https://localhost:7295
info: Microsoft.Hosting.Lifetime[14]
      Now listening on: http://localhost:5247
info: Microsoft.Hosting.Lifetime[0]
      Application started. Press Ctrl+C to shut down.
info: Microsoft.Hosting.Lifetime[0]
      Hosting environment: Development
```

In the preceding log output, informational level logging is enabled as the default for this application. The
output can be controlled by configuring the log levels.

### Configuring the log level

Logs sent to the integrated `Microsoft.Extensions.Logging` library can be 
[configured](https://learn.microsoft.com/en-us/dotnet/core/extensions/logging?tabs=command-line#configure-logging) in several ways.
A common choice is to use the `appsettings.json` file to configure log-level filters for specific categories.

```json
{
  "Logging": {
    "LogLevel": {
      "Default": "Information",
      "Microsoft.AspNetCore": "Warning",
      "Elastic.OpenTelemetry": "Warning"
    }
  },
  "AllowedHosts": "*"
}
```

In the preceding code, the `Elastic.OpenTelemetry` has been filtered to only emit log entries when they have the
`Warning` log level or a higher severity. This overrides the `Default` configuration of `Information`.

## Enable global file logging

Integrated logging is helpful because it requires little to no setup. The logging infrastructure is not present
by default in some application types, such as console applications. EDOT .NET also offers a global file logging
feature, which is the easiest way to get diagnostics and debug information. File logging is required when engaging
Elastic support where trace logs will be requested.

Specifying at least one of the following environment variables will ensure that EDOT .NET logs into a file

`OTEL_LOG_LEVEL` _(optional)_:
The log level at which the profiler should log. Valid values are

* trace
* debug
* information
* warning
* error
* none

The default value is `information`. More verbose log levels like `trace` and `debug` can affect the runtime
performance of profiler auto instrumentation, so are recommended _only_ for diagnostics purposes.

:::{note}
If `ELASTIC_OTEL_LOG_TARGETS` is not explicitly set to include `file`, global file logging will only 
be enabled when configured with `trace` or `debug`.
:::

`OTEL_DOTNET_AUTO_LOG_DIRECTORY` _(optional)_:
The directory in which to write log files. If unset, defaults to

* `%USERPROFILE%\AppData\Roaming\elastic\elastic-otel-dotnet` on Windows
* `/var/log/elastic/elastic-otel-dotnet` on Linux
* `~/Library/Application Support/elastic/elastic-otel-dotnet` on OSX

> ::::{important}
> The user account under which the profiler process runs must have permission to
> write to the destination log directory. Specifically, ensure that when running
> on IIS, the https://learn.microsoft.com/en-us/iis/manage/configuring-security/application-pool-identities[AppPool identity]
> has write permissions in the target directory.
> ::::

`ELASTIC_OTEL_LOG_TARGETS` _(optional)_:
A semi-colon separated list of targets for profiler logs. Valid values are

* file
* stdout
* none

The default value is `file` if `OTEL_DOTNET_AUTO_LOG_DIRECTORY` is set or `OTEL_LOG_LEVEL` is set to `trace` or `debug`.

## Advanced Troubleshooting

### Diagnosing initialisation (bootstrap) issues

No log file is generated if the EDOT for .NET fails before fully bootstrapping its internal components. In such
circumstances, an additional logger may be provided for diagnostic purposes. Alternatively, the `STDOUT` log target
can be enabled.

#### Providing an additional application logger

An additional `ILogger` that will be used by EDOT .NET to log pre-bootstrap events can be provided by
creating an instance of `ElasticOpenTelemetryOptions`.

```csharp
using Elastic.OpenTelemetry;
using Microsoft.Extensions.Logging;
using OpenTelemetry;

using ILoggerFactory loggerFactory = LoggerFactory.Create(static builder =>
{
   builder
      .AddFilter("Elastic.OpenTelemetry", LogLevel.Trace)
      .AddConsole();
});

Ilogger logger = loggerFactory.CreateLogger("EDOT");

var options = new ElasticOpenTelemetryOptions
{
   AdditionalLogger = logger
};

using var sdk = OpenTelemetrySdk.Create(builder => builder
   .WithElasticDefaults(options));
```

This example adds the console logging provider, but any provider may be included here.
To use this sample code, a dependency on the `Microsoft.Extensions.Logging.Console` 
[NuGet package](https://www.nuget.org/packages/microsoft.extensions.logging.console) is required 

An `ILoggerFactory` is created and configured. In this example,
the `Elastic.OpenTelemetry` category is configured to capture trace logs, which is the most
verbose option. This is the best choice when diagnosing initialisation issues.

The `ILoggerFactory` is used to create an `Ilogger`, which is then assigned to the
`ElasticOpenTelemetryOptions.AdditionalLogger` property. Once the `ElasticOpenTelemetryOptions`
is passed into the `WithElasticDefaults` method, the provided logger can be used to
capture bootstrap logs.

To simplify the preceding code a little, it's also possible to configure the `ElasticOpenTelemetryOptions`
with an `ILoggerFactory` instance that EDOT .NET can use to create its own logger.

```csharp
using var loggerFactory = LoggerFactory.Create(static builder =>
{
   builder
      .AddFilter("Elastic.OpenTelemetry", LogLevel.Debug)
      .AddConsole();
});

var options = new ElasticOpenTelemetryOptions
{
   AdditionalLoggerFactory = loggerFactory
};

using var sdk = OpenTelemetrySdk.Create(builder => builder
   .WithElasticDefaults(options));
```