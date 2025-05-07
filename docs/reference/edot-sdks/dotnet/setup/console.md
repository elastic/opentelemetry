---
navigation_title: Console applications
applies_to:
  stack:
  serverless:
    observability:
products:
  - cloud-serverless
  - observability
---

# Set up EDOT .NET for console applications

Applications running without a [host](https://learn.microsoft.com/dotnet/core/extensions/generic-host) may initialize
OpenTelemetry manually.

:::{note}
When building console applications, consider using the features provided by
[`Microsoft.Extensions.Hosting`](https://www.nuget.org/packages/microsoft.extensions.hosting) as this enables
dependency injection and logging capabilities.
:::

```csharp
using OpenTelemetry;

using OpenTelemetrySdk sdk = OpenTelemetrySdk.Create(builder => builder
   .WithElasticDefaults());
```

The preceding code:

1. Imports the required types from the `OpenTelemetry` namespace.
1. Creates an instance of the `OpenTelemetrySdk` using its factory `Create` method.
1. Configures the `IOpenTelemetryBuilder` by passing a lambda.
1. Enables EDOT .NET and its [opinionated defaults](./../setup/edot-defaults) by calling `WithElasticDefaults` on the `IOpenTelemetryBuilder`.

:::{warning}
The `using` keyword is applied to the `sdk` variable to define a using declaration, which ensures that the
`OpenTelemetrySdk` instance is disposed of when the application terminates. Disposing of the OpenTelemetry SDK gives the
SDK a chance to flush any telemetry held in memory. Skipping this step may result in data loss.
:::

The above code is sufficient for many applications to achieve a reasonable out-of-the-box experience. The
`IOpenTelemetryBuilder` can be further configured as required within the target application. 

For example, we can observe an additional `ActivitySource` by chaining a call to `WithTracing`,
providing a lambda to configure the `TracerProviderBuilder` to add the name of the additional
`ActivitySource`.

```csharp
using OpenTelemetry;
using OpenTelemetry.Trace;

using OpenTelemetrySdk sdk = OpenTelemetrySdk.Create(builder => builder
   .WithElasticDefaults()
   .WithTracing(t => t.AddSource("MyApp.SourceName")));
```

We can further customise the OpenTelemetry SDK with the other built-in extension methods,
such as `ConfigureResource`.

```csharp
using OpenTelemetry;
using OpenTelemetry.Trace;
using OpenTelemetry.Resources;

using OpenTelemetrySdk sdk = OpenTelemetrySdk.Create(builder => builder
   .WithElasticDefaults()
   .ConfigureResource(r => r.AddService("MyAppName"))
   .WithTracing(t => t.AddSource("MyApp.SourceName")));
```

## Providing configuration

When calling `OpenTelemetrySdk.Create` a dedicated `IServiceCollection` and `IServiceProvider` will be created for the 
SDK and shared by all signals. An `IConfiguration` is created automatically from environment variables. The
recommended method to configure the OpenTelemetry SDK is via environment variables. At a minimum, we should set
the environment variables used to configure the OTLP exporter using any suitable method for your operating system.

```
"OTEL_EXPORTER_OTLP_ENDPOINT" = "https://{MyServerlessEndpoint}.apm.us-east-1.aws.elastic.cloud:443",
"OTEL_EXPORTER_OTLP_HEADERS" = "Authorization=ApiKey {MyEncodedApiKey}"
```

:::{note}
Replace the `{MyServerlessEndpoint}` and `{MyEncodedApiKey}` placeholders above with the values provided
by your Elastic Observability backend.
:::

### Configuring EDOT .NET

Several configuration settings are available to control the additional features offered by EDOT .NET.
These may be configured using environment variables, `IConfiguration` and/or code-based configuration.

See the [configuration](./../configuration) documentation for more details.

As an example, manual code-based configuration can be used to disable the instrumentation assembly scanning
feature.

```csharp
using OpenTelemetry;
using OpenTelemetry.Trace;
using OpenTelemetry.Resources;
using Elastic.OpenTelemetry;

var options = new ElasticOpenTelemetryOptions
{
	SkipInstrumentationAssemblyScanning = true
};

using OpenTelemetrySdk sdk = OpenTelemetrySdk.Create(builder => builder
   .WithElasticDefaults(options)
   .ConfigureResource(r => r.AddService("MyAppName3"))
   .WithTracing(t => t.AddSource("MyApp.SourceName")));
```

The preceding code:

1. Creates an instance of `ElasticOpenTelemetryOptions`
1. Configures `SkipInstrumentationAssemblyScanning` as `true` to disable the assembly scanning feature.
1. Passes the `ElasticOpenTelemetryOptions` from the `options` variable into the `WithElasticDefaults` method.

It's also possible to use `IConfiguration` to control EDOT .NET.

```csharp
using OpenTelemetry;
using OpenTelemetry.Trace;
using OpenTelemetry.Resources;
using Microsoft.Extensions.Configuration;

const string edotPrefix = "Elastic:OpenTelemetry:";

var config = new ConfigurationBuilder()
   .AddJsonFile("appsettings.json")
   .AddInMemoryCollection(new Dictionary<string, string?>()
   {
      [$"{edotPrefix}SkipInstrumentationAssemblyScanning"] = "true",
      [$"{edotPrefix}LogDirectory"] = "C:\\Logs\\MyApp"
   })
   .Build();

using var sdk = OpenTelemetrySdk.Create(builder => builder
   .WithElasticDefaults(config)
   .ConfigureResource(r => r.AddService("MyAppName3"))
   .WithTracing(t => t.AddSource("MyApp.SourceName")));
```

The preceding code:

1. Defines a constant string variable named `edotPrefix` to hold the configuration section prefix.
1. Creates a new `ConfigurationBuilder` to bind configuration values from one or more providers (sources), such as JSON.
1. Calls the `AddJsonFile` method to read configuration from a JSON file named "appsettings.json".
1. Calls the `AddInMemoryCollection` method to add configuration settings from a `Dictionary` of supplied keys and values.
   1. Adds an entry for "SkipInstrumentationAssemblyScanning" prefixed with the correct section name, setting its value to "true."
   1. Adds an entry for "LogDirectory" prefixed with the correct section name, setting its value to "C:\Logs\MyApp".
1. Builds an `IConfigurationRoot` (castable to `IConfiguration`) from the provided sources.
1. Passes the `IConfiguration` from the `config` variable into the `WithElasticDefaults` method.

The example above requires the JSON configuration provider, which can be added as a NuGet package.

```xml
<PackageReference Include="Microsoft.Extensions.Configuration.Json" Version="<LATEST>" />
```

Replace the `<LATEST>` version placeholder with the [latest available package from NuGet.org](https://www.nuget.org/packages/Microsoft.Extensions.Configuration.Json).