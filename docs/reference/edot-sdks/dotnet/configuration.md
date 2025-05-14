---
navigation_title: Configuration
description: Configure the Elastic Distribution of OpenTelemetry .NET (EDOT .NET) to send data to Elastic.
applies_to:
  stack:
  serverless:
    observability:
products:
  - id: cloud-serverless
  - id: observability
  - id: edot-dotnet
---

# Configure the EDOT .NET SDK

Configure the Elastic Distribution of OpenTelemetry .NET (EDOT .NET) to send data to Elastic.

## Configuration methods

Configure the OpenTelemetry SDK using the mechanisms listed in the [OpenTelemetry documentation](https://opentelemetry.io/docs/languages/net/automatic/configuration/),
including:

* Setting [environment variables](#environment-variables).
* Using the [`IConfiguration` integration](#iconfiguration-integration).
* [Manually configuring](#manual-configuration) EDOT .NET.

Configuration options set manually in code take precedence over environment variables, and environment variables take precedence over configuration options set using the `IConfiguration` system.

### Environment variables

You can configure EDOT .NET using environment variables. This is a cross-platform way to configure EDOT .NET and is especially useful in containerized environments.

Environment variables are read at startup and can be used to configure EDOT .NET. For details of the various EDOT-specific options available and their corresponding environment variable names, see [Configuration options](#configuration-options).

All OpenTelemetry environment variables from the upstream SDK may also be used to configure the SDK behavior for features such as resources, samples and exporters.

### IConfiguration integration

In applications that use the [".NET generic host"](https://learn.microsoft.com/dotnet/core/extensions/generic-host), such as [ASP.NET Core](https://learn.microsoft.com/aspnet/core/introduction-to-aspnet-core) and [worker services](https://learn.microsoft.com/dotnet/core/extensions/workers), EDOT .NET can be configured using the `IConfiguration` integration.

When using an `IHostApplicationBuilder` in modern ASP.NET Core applications, the `AddElasticOpenTelemetry` extension method turns on EDOT .NET and configuration from `IHostApplicationBuilder.Configuration` is passed in automatically. For example:

```csharp
var builder = WebApplication.CreateBuilder(args);
// Configuration is automatically bound and can be provided
// via the `appsettings.json` file.
builder.AddElasticOpenTelemetry();
```

By default, at this stage the configuration is populated from the default configuration sources, including the `appsettings.json` file(s) and command-line arguments. You can use these sources to define the configuration for the Elastic Distribution of OpenTelemetry .NET.

For example, you can define the configuration for the Elastic Distribution of OpenTelemetry .NET in the `appsettings.json` file:

```json
{
  "Elastic": {
    "OpenTelemetry": {
      "LogDirectory": "C:\\Logs"
    }
  }
}
```

:::{note}
This example sets the file log directory to `C:\Logs` which activates diagnostic file logging.
:::

Configuration parsed from the `Elastic:OpenTelemetry` section of the `IConfiguration` instance is bound to the `ElasticOpenTelemetryOptions` instance used to configure EDOT .NET.

In situations where the application might not depend on the hosting APIs, but uses the dependency injection APIs instead, an `IConfiguration` instance can be passed in manually. This is usually the case with console applications. For example:

```csharp
var configuration = new ConfigurationBuilder()
    .AddInMemoryCollection(new Dictionary<string, string?>()
    {
        ["Elastic:OpenTelemetry:LogDirectory"] = "C:\\Logs"
    })
    .Build();

var services = new ServiceCollection();
services.AddElasticOpenTelemetry(configuration);
```

To learn more about the Microsoft configuration system, see [Configuration in ASP.NET Core](https://learn.microsoft.com/aspnet/core/fundamentals/configuration).

### Manual configuration

In all other scenarios, you can configure EDOT .NET manually in code.

Create an instance of `ElasticOpenTelemetryOptions` and pass it to an overload of the `WithElasticDefaults` extension methods available on the `IHostApplicationBuilder`, the `IServiceCollection` and the specific signal providers such as `TracerProviderBuilder`.

For example, in traditional console applications, you can configure the Elastic Distribution of OpenTelemetry .NET like this:

```csharp
using OpenTelemetry;
using Elastic.OpenTelemetry;

// Create an instance of `ElasticOpenTelemetryOptions`.
var options = new ElasticOpenTelemetryOptions
{
  // This example sets the file log directory to `C:\Logs`
  // which enables diagnostic file logging.
  FileLogDirectory = "C:\\Logs"
};

// Pass the `ElasticOpenTelemetryOptions` instance to the
// `WithElasticDefaults` extension method for the `IOpenTelemetryBuilder`
//  to configure EDOT .NET.
using var sdk = OpenTelemetrySdk.Create(builder => builder
  .WithElasticDefaults(options));
```

## Configuration options

Because the Elastic Distribution of OpenTelemetry .NET (EDOT .NET) is an extension of the [OpenTelemetry .NET SDK](https://github.com/open-telemetry/opentelemetry-dotnet-instrumentation), it supports both:

* General OpenTelemetry SDK configuration options
* Elastic-specific configuration options that are only available when using EDOT .NET

### OpenTelemetry SDK configuration options

EDOT .NET supports all configuration options listed in the [OpenTelemetry General SDK Configuration documentation](https://opentelemetry.io/docs/languages/sdk-configuration/general/).

### Elastic-specific configuration options

EDOT .NET supports the following Elastic-specific options.

#### `LogDirectory`

* Type: String
* Default: `string.Empty`

A string specifying the output directory where the Elastic Distribution of OpenTelemetry .NET writes diagnostic log files. When not provided, no file logging occurs. Each new .NET process creates a new log file in the specified directory.

| Configuration method | Key |
|---|---|
| Environment variable | `OTEL_DOTNET_AUTO_LOG_DIRECTORY` |
| `IConfiguration` integration | `Elastic:OpenTelemetry:LogDirectory` |

#### `LogLevel`

* Type: String
* Default: `Information`

Sets the logging level for EDOT .NET. Valid options are `Critical`, `Error`, `Warning`, `Information`, `Debug`, `Trace`, and `None`. `None` disables the logging.

| Configuration method | Key |
|---|---|
| Environment variable | `OTEL_LOG_LEVEL` |
| `IConfiguration` integration | `Elastic:OpenTelemetry:LogLevel` |

#### `LogTargets`

* Type: String
* Default: `Information`

A comma-separated list of targets for log output. When global logging is not configured (a log directory or target is not specified) this defaults to `none`. When the instrumented application is running within a container, this defaults to direct logs to `stdout`. Otherwise defaults to `file`.

Valid options are `file`, `stdout` and `none`. `None` disables the logging.

| Configuration method | Key |
|---|---|
| Environment variable | `ELASTIC_OTEL_LOG_TARGETS` |
| `IConfiguration` integration | `Elastic:OpenTelemetry:LogTargets` |

#### `SkipOtlpExporter`

* Type: Bool
* Default: `false`

Allows EDOT .NET to be used with its defaults, but without enabling the export of telemetry data to
an OTLP endpoint. This can be useful when you want to test applications without sending telemetry data.

| Configuration method | Key |
|---|---|
| Environment variable | `ELASTIC_OTEL_SKIP_OTLP_EXPORTER` |
| `IConfiguration` integration | `Elastic:OpenTelemetry:SkipOtlpExporter` |

#### `SkipInstrumentationAssemblyScanning`

* Type: Bool
* Default: `false`

Allows EDOT .NET to be used without the instrumentation assembly scanning feature turned on. This prevents the automatic registration of instrumentation from referenced [OpenTelemetry contrib](https://github.com/open-telemetry/opentelemetry-dotnet-contrib) instrumentation packages.

| Configuration method | Key |
|---|---|
| Environment variable | `ELASTIC_OTEL_SKIP_ASSEMBLY_SCANNING` |
| `IConfiguration` integration | `Elastic:OpenTelemetry:SkipInstrumentationAssemblyScanning` |