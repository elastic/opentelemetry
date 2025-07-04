---
navigation_title: Setup
description: Learn how to set up and configure the Elastic Distribution of OpenTelemetry .NET to instrument your application or service.
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

# Set up the EDOT .NET SDK

Learn how to set up and configure the {{edot}} .NET to instrument your application or service.

## Quickstart guide

EDOT .NET is designed to be straightforward to integrate into your applications. Integration includes applications that have previously used the [OpenTelemetry SDK](https://opentelemetry.io/docs/languages/net/), those that are transitioning from the [Elastic APM Agent](apm-agent-dotnet://reference/index.md) and those introducing observability instrumentation for the first time. When the OpenTelemetry SDK or Elastic APM Agent are already in use, minor code changes are required at the point of registration. Refer to [Migration](/reference/edot-sdks/dotnet/migration.md) for more details.

This quickstart guide documents the introductory steps required to set up OpenTelemetry using EDOT .NET for an ASP.NET Core 
[minimal API](https://learn.microsoft.com/aspnet/core/fundamentals/minimal-apis) application. For detailed, technology-specific steps, see:

* [ASP.NET (.NET Framework)](/reference/edot-sdks/dotnet/setup/aspnet.md)
* [Console applications](/reference/edot-sdks/dotnet/setup/console.md)
* [Worker services](/reference/edot-sdks/dotnet/setup/worker-services.md)
* [Zero code](/reference/edot-sdks/dotnet/setup/zero-code.md)

### Prerequisites

Before getting started:

* Check your .NET SDK version. Before continuing, install a locally supported [.NET SDK version](https://dotnet.microsoft.com/en-us/download/dotnet).
* Create a new ASP.NET Core minimal API project. You need an application to instrument with OpenTelemetry. This quickstart guide uses an ASP.NET Core minimal API project. You can follow along with a new or existing ASP.NET Core application. Refer to the technology-specific documentation for guidance with specific .NET application templates. 
* Set up Elastic Observability. You need somewhere to send the gathered OpenTelemetry data so that it can be viewed and analyzed. This documentation assumes you're using [Elastic Cloud](https://www.elastic.co/cloud) with an [Elastic Observability](https://www.elastic.co/observability) hosted deployment or serverless project. You can use an existing one or set up a new one.

:::{tip}
When using Serverless, use the [{{motlp}}](/reference/motlp.md) for the best experience when using EDOT .NET.
:::

### Installing the NuGet packages

To get started with the {{edot}} .NET, add the `Elastic.OpenTelemetry` [NuGet package](https://www.nuget.org/packages/Elastic.OpenTelemetry)
reference to your project file:

```xml
<PackageReference Include="Elastic.OpenTelemetry" Version="<LATEST>" />
```

:::{note}
Replace the `<LATEST>` version placeholder with the [latest available package from NuGet.org](https://www.nuget.org/packages/Elastic.OpenTelemetry).
:::

EDOT .NET includes a transitive dependency on the OpenTelemetry SDK, so you do not need to add the OpenTelemetry SDK package to your project directly. However,
you can explicitly add the OpenTelemetry SDK as a dependency if you want to opt into newer SDK versions.

#### ASP.NET Core instrumentation

To observe and capture the built-in ASP.NET Core instrumentation, the OpenTelemetry instrumentation for [ASP.NET Core NuGet](https://www.nuget.org/packages/OpenTelemetry.Instrumentation.AspNetCore) package is required. Due to its dependencies, this package is not automatically available when adding `Elastic.OpenTelemetry` to your project.

Manually add the latest version to your project file:

```xml
<PackageReference Include="OpenTelemetry.Instrumentation.AspNetCore" Version="<LATEST>" />
```

:::{note}
Replace the `<LATEST>` version placeholder with the [latest available package from NuGet.org](https://www.nuget.org/packages/OpenTelemetry.Instrumentation.AspNetCore).
:::

The presence of this package is detected by the EDOT instrumentation assembly scanning feature (turned on by default).

### Registering OpenTelemetry with EDOT .NET

To register the OpenTelemetry SDK via EDOT .NET, the recommended approach is to use the extension method available on `IHostApplicationBuilder`. `IHostApplicationBuilder` is the abstraction representing the .NET generic host responsible for managing application startup and lifetime in ASP.NET Core.

```csharp
var builder = WebApplication.CreateBuilder(args);
builder.AddElasticOpenTelemetry();
```

Immediately after creating the WebApplicationBuilder, which implements `IHostApplicationBuilder`, call the `AddElasticOpenTelemetry` method. `AddElasticOpenTelemetry` registers the OpenTelemetry SDK for .NET, applying the Elastic [opinionated defaults](/reference/edot-sdks/dotnet/setup/edot-defaults.md). The Elastic defaults enable tracing, metrics, log signals, and the OTLP exporter.

Additionally, EDOT performs automatic instrumentation assembly scanning to enable the ASP.NET Core instrumentation that we added in the previous step. With the upstream SDK, additional lines of code would be required to register the instrumentation. EDOT .NET aims to simplify the experience of getting started.

### Configure the OpenTelemetry resource attributes

When exporting telemetry data from an application, resource attributes are used to represent metadata about the entity producing the telemetry. While defaults are applied for required attributes such as `service.name`. Explicitly set a descriptive service name to distinguish its data in the Elastic Observability UI.

The OpenTelemetry SDK supports several mechanisms to configure resource attributes. For simple scenarios, the service information can be set programmatically. To achieve this when using EDOT, the `AddElasticOpenTelemetry` method includes an overload accepting an `Action<IOpenTelemetryBuilder>` used to configure the OpenTelemetry SDK through its builder API.

To specify a service name, we can amend the preceding code as follows:

```csharp
builder.AddElasticOpenTelemetry(b => b
  .ConfigureResource(r => r.AddService("MyAppName")));
```

The preceding code requires two additional `using` directives:

```csharp
using OpenTelemetry;
using OpenTelemetry.Resources;
```

Alternatively, the `OTEL_SERVICE_NAME` environment variable can be used to configure the service name. There are two ways to specify this with the OpenTelemetry SDK. Either, as a traditional environment variable, configured before launching the process, or as an entry in the [.NET configuration APIs](https://learn.microsoft.com/dotnet/core/extensions/configuration). These APIs are available and used by default in generic host applications such as ASP.NET Core.

To use `IConfiguration` to specify the service name, create an entry for the key `OTEL_SERVICE_NAME`, with the value representing your preferred service name. Configuring this entry can be achieved through any of the available .NET configuration providers, for example, by creating a configuration entry in the `appsettings.json` file:

```json
{
  "Logging": {
    "LogLevel": {
      "Default": "Information",
      "Microsoft.AspNetCore": "Warning"
    }
  },
  "AllowedHosts": "*",
  "OTEL_SERVICE_NAME": "MyNameFromConfig"
}
```

OpenTelemetry configuration environment variables should be specified as a top-level key/value pair as with the `OTEL_SERVICE_NAME` in the preceding code snippet.

### Configure the OTLP endpoint

The configuration documented so far ensures that when the application starts, the OpenTelemetry SDK is launched with the [EDOT .NET defaults](/reference/edot-sdks/dotnet/setup/edot-defaults.md), activating all signals and exporting telemetry through OTLP. Unless configured otherwise, the OTLP exporter in the SDK defaults to sending data to `localhost` on the default port for OTLP over gRPC, 4317. If you are running a local Collector, this might be sufficient, but in most cases you will need to configure the correct endpoint for exporting telemetry data.

In this quickstart guide, {{serverless-full}} is the backend. The onboarding **Add data** page of Elastic Observability provides the environment variables required to send telemetry data to the Elastic Observability backend. This information includes the endpoint URL and API key that should be used when exporting data. The application must be configured to use the endpoint and authorization header when exporting telemetry data.

As with most OpenTelemetry configuration, you can also configure the endpoint through environment variables, including providing them through application configuration. The values are sensitive and should be secured. Use the [Secret Manager](https://learn.microsoft.com/aspnet/core/security/app-secrets) feature during local development. Once enabled
for your application, add `OTEL_EXPORTER_OTLP_ENDPOINT` and `OTEL_EXPORTER_OTLP_HEADERS` as keys with their respective values.

:::{tip}
Strongly consider using a key/secret store for production environments.
:::

### Instrument application code

EDOT .NET enables the collection of trace, metric, and log signals by default. With no additional configuration, your configured Elastic Observability backend will receive telemetry data from your application at runtime. Development teams are encouraged to enrich the value of telemetry by instrumenting their code to emit application-specific telemetry data such as traces, metrics, and logs. 

In .NET, use the built-in .NET APIs for each signal:

- [Logs](https://learn.microsoft.com/dotnet/core/extensions/logging)
- [Traces](https://learn.microsoft.com/dotnet/core/diagnostics/distributed-tracing-instrumentation-walkthroughs)
- [Metrics](https://learn.microsoft.com/dotnet/core/diagnostics/metrics-instrumentation)

### Next steps

Refer to the technology-specific documentation pages for further details on using EDOT .NET in those application types. The [OpenTelemetry SDK documentation](https://opentelemetry.io/docs/languages/net/getting-started/) provides more examples of working with the .NET SDK.

## Troubleshooting

For help with common setup issues, refer to the [EDOT .NET troubleshooting guide](docs-content://troubleshoot/ingest/opentelemetry/edot-sdks/dotnet/index.md).