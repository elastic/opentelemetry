---
navigation_title: Console applications
description: Learn how to instrument console applications using the Elastic Distribution of OpenTelemetry .NET.
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

# Set up EDOT .NET for console applications

You can instrument console applications using the {{edot}} .NET. Applications running without a [host](https://learn.microsoft.com/dotnet/core/extensions/generic-host) can initialize OpenTelemetry manually. For example:

```csharp
using OpenTelemetry;

using OpenTelemetrySdk sdk = OpenTelemetrySdk.Create(builder => builder
   .WithElasticDefaults());
```

The preceding code:

1. Imports the required types from the `OpenTelemetry` namespace.
2. Creates an instance of the `OpenTelemetrySdk` using its factory `Create` method.
3. Configures the `IOpenTelemetryBuilder` by passing a lambda.
4. Enables EDOT .NET and its [opinionated defaults](edot-defaults.md) by calling `WithElasticDefaults` on the `IOpenTelemetryBuilder`.

When building console applications, consider using the features provided by [`Microsoft.Extensions.Hosting`](https://www.nuget.org/packages/microsoft.extensions.hosting) as this turns on dependency injection and logging capabilities.

:::{warning}
The `using` keyword is applied to the `sdk` variable to define a using declaration, which ensures that the `OpenTelemetrySdk` instance is disposed of when the application terminates. Disposing of the OpenTelemetry SDK gives the SDK a chance to flush any telemetry held in memory. Skipping this step may result in data loss.
:::

The previous code is sufficient for many applications to achieve a reasonable out-of-the-box experience. The `IOpenTelemetryBuilder` can be further configured as required within the target application. 

For example, you can observe an additional `ActivitySource` by chaining a call to `WithTracing`, providing a lambda to configure the `TracerProviderBuilder` to add the name of the additional `ActivitySource`.

```csharp
using OpenTelemetry;
using OpenTelemetry.Trace;

using OpenTelemetrySdk sdk = OpenTelemetrySdk.Create(builder => builder
   .WithElasticDefaults()
   .WithTracing(t => t.AddSource("MyApp.SourceName")));
```

You can further customize the OpenTelemetry SDK with the other built-in extension methods, such as `ConfigureResource`.

```csharp
using OpenTelemetry;
using OpenTelemetry.Trace;
using OpenTelemetry.Resources;

using OpenTelemetrySdk sdk = OpenTelemetrySdk.Create(builder => builder
   .WithElasticDefaults()
   .ConfigureResource(r => r.AddService("MyAppName"))
   .WithTracing(t => t.AddSource("MyApp.SourceName")));
```

## Provide configuration values

When calling `OpenTelemetrySdk.Create` a dedicated `IServiceCollection` and `IServiceProvider` is created for the  SDK and shared by all signals. An `IConfiguration` is created automatically from environment variables. The recommended method to configure the OpenTelemetry SDK is via environment variables. At a minimum, set the environment variables used to configure the OTLP exporter using any suitable method for your operating system.

```
"OTEL_EXPORTER_OTLP_ENDPOINT" = "https://{MyServerlessEndpoint}.apm.us-east-1.aws.elastic.cloud:443",
"OTEL_EXPORTER_OTLP_HEADERS" = "Authorization=ApiKey {MyEncodedApiKey}"
```

Replace the `{MyServerlessEndpoint}` and `{MyEncodedApiKey}` placeholders above with the values provided by your Elastic Observability backend.

### Configure EDOT .NET

Several configuration settings are available to control the additional features offered by EDOT .NET. These might be configured using environment variables, `IConfiguration` and/or code-based configuration. Refer to [Configuration](/reference/edot-sdks/dotnet/configuration.md) documentation for more details.

As an example, manual code-based configuration can be used to disable the instrumentation assembly scanning feature.

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

1. Creates an instance of `ElasticOpenTelemetryOptions`.
2. Configures `SkipInstrumentationAssemblyScanning` as `true` to disable the assembly scanning feature.
3. Passes the `ElasticOpenTelemetryOptions` from the `options` variable into the `WithElasticDefaults` method.

You can also use `IConfiguration` to control EDOT .NET.

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
2. Creates a new `ConfigurationBuilder` to bind configuration values from one or more providers (sources), such as JSON.
3. Calls the `AddJsonFile` method to read configuration from a JSON file named "appsettings.json".
4. Calls the `AddInMemoryCollection` method to add configuration settings from a `Dictionary` of supplied keys and values.
   1. Adds an entry for "SkipInstrumentationAssemblyScanning" prefixed with the correct section name, setting its value to "true."
   2. Adds an entry for "LogDirectory" prefixed with the correct section name, setting its value to "C:\Logs\MyApp".
5. Builds an `IConfigurationRoot` (castable to `IConfiguration`) from the provided sources.
6. Passes the `IConfiguration` from the `config` variable into the `WithElasticDefaults` method.

The previous example requires the JSON configuration provider, which you an add as a NuGet package.

```xml
<PackageReference Include="Microsoft.Extensions.Configuration.Json" Version="<LATEST>" />
```

Replace the `<LATEST>` version placeholder with the [latest available package from NuGet.org](https://www.nuget.org/packages/Microsoft.Extensions.Configuration.Json).