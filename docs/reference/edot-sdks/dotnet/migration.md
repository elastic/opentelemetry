---
navigation_title: Migration
description: Migrate from the Elastic APM .NET agent to the Elastic Distribution of OpenTelemetry .NET (EDOT .NET).
applies_to:
  stack:
  serverless:
    observability:
products:
  - id: cloud-serverless
  - id: observability
  - id: edot-dotnet
  - id: apm-dotnet-agent
---

# Migrate to EDOT .NET from the Elastic APM .NET agent

Compared to the Elastic APM .NET agent, the Elastic Distribution of OpenTelemetry .NET presents a number of advantages:

- No vendor lock-in through standardized concepts, supporting the use of multiple backend vendors or switching between them.
- A single set of application APIs are required to instrument applications.
- A wider pool of knowledge, experience and support is available across the OpenTelemetry community.
- Efficient data collection and advanced data processing opportunities.

While you can use the upstream [OpenTelemetry SDK for .NET](https://github.com/open-telemetry/opentelemetry-dotnet) to directly export data to an Elastic Observability backend, some capabilities of the Elastic tooling might not be able to function as intended. Use the Elastic Distribution of OpenTelemetry (EDOT) language SDK and the [Elastic Distribution of OpenTelemetry collector](../../edot-collector/index.md) for the best experience.

## Migrating from Elastic .NET Agent [migrating-to-edot-net-from-elastic-net-agent]

Follow these steps to migrate from the legacy Elastic APM .NET agent to the Elastic Distribution of OpenTelemetry .NET.

### Manual instrumentation

The Elastic APM Agent supports OTel-native trace instrumentation through its [OpenTelemetry Bridge](https://www.elastic.co/guide/en/apm/agent/dotnet/current/opentelemetry-bridge.html) feature, which is active by default.

The bridge subscribes to instrumentation created using the [`Activity`](https://learn.microsoft.com/dotnet/api/system.diagnostics.activity) API in .NET. An `Activity` represents a unit of work and aligns with the OpenTelemetry "span" concept. The API name is used for historical backward compatibility. The `Activity` API is the recommended approach to introduce tracing when instrumenting applications.

For applications which are instrumented using the [public API](https://www.elastic.co/guide/en/apm/agent/dotnet/current/public-api.html), a recommended first step of the existing APM Agent is to consider migrating instrumentation over to the `Activity` API. For example, in an ASP.NET Core Razor pages application, you might have manually created a child span after the parent transaction for the ASP.NET Core request:

```csharp
using Elastic.Apm.Api;
using Microsoft.AspNetCore.Mvc.RazorPages;

namespace RazorPagesFrontEnd.Pages;

public class IndexModel : PageModel
{
   public async Task OnGet()
   {
      await Elastic.Apm.Agent.Tracer
         .CurrentTransaction.CaptureSpan("Doing stuff", "internal", async span =>
         {
            // represents application work
            await Task.Delay(100);

            // add a custom label to be indexed and made searchable for this span
            span.SetLabel("My label", "A value");
         });
  }
}
```

The preceding code captures, or starts and ends, a span within the current transaction. The span is named `Doing stuff`. The second argument specifies the type of work this span represents, `internal` in this example. Within the async lambda, the work is performed, and a custom label is set.

To convert this to the `Activity` API, first define an `ActivitySource` used to create `Activity` instances (spans). Typically, you have a few, usually just one, of these for application-specific instrumentation. Define a static instance somewhere within your application.

```csharp
public static class Instrumentation
{
   public static readonly ActivitySource ApplicationActivitySource = new("MyAppInstrumentation");
}
```

You can now update the `IndexModel` class to prefer the `Activity` API. Spans created through this API are automatically observed and sent from the APM Agent by the OpenTelemetry bridge.

```csharp
using Microsoft.AspNetCore.Mvc.RazorPages;
using System.Diagnostics;

namespace RazorPagesFrontEnd.Pages;

public class IndexModel : PageModel
{
    public async Task OnGet()
    {
        using var activity = Instrumentation.ApplicationActivitySource
            .StartActivity("Doing stuff");

        await Task.Delay(100);

        activity?.SetTag("My label", "A value");
    }
}
```

This code is equivalent to the previous code snippet, but is now vendor-neutral, preferring the built-in .NET `Activity` API from the `System.Diagnostics` namespace.

The `Activity` class implements `IDisposable`, allowing us to reduce the nesting of code. `StartActivity` is called on the `ActivitySource`, which creates and starts an `Activity`. Starting an `Activity` results in a new span, which may be a child of a parent, if an existing `Activity` is already being tracked. This is handled automatically by the .NET API. The overload in the previous example accepts a name for the `Activity`. You can optionally pass an `ActivityKind`, although this defaults to `ActivityKind.Internal`.

The preceding code uses the `SetTag` method to "activity" variable may be assigned `null`. To reduce instrumentation overhead, `StartActivity` may return `null` if no observers of the `ActivitySource` exist. While the API uses the notion of "tags"; these are functionally equivalent to the OpenTelemetry concept of "attributes. Attributes are used to attach arbitrary information to a span in order to enrich it and provide context when analysing the telemetry data.

### Agent registration

After migrating any manual instrumentation from the Elastic APM Agent public API to the Microsoft `Activity` API, the final step is to switch the observation and export of telemetry signals from the APM Agent to EDOT .NET.

The steps vary by project template. In all cases, you need to add the `Elastic.Opentelemetry` [NuGet package](https://www.nuget.org/packages/Elastic.OpenTelemetry)
to your project:

```xml
<PackageReference Include="Elastic.OpenTelemetry" Version="<LATEST>" />
```

:::{note}
Replace the `<LATEST>` version placeholder with the [latest available package from NuGet.org](https://www.nuget.org/packages/Elastic.OpenTelemetry).
:::

You might also need to install additional instrumentation libraries to observe signals from specific components, such as ASP.NET Core.

```xml
<PackageReference Include="OpenTelemetry.Instrumentation.AspNetCore" Version="<LATEST>" />
```

:::{note}
Replace the `<LATEST>` version placeholder with the [latest available package from NuGet.org](https://www.nuget.org/packages/OpenTelemetry.Instrumentation.AspNetCore).
:::

In an ASP.NET Core application, the APM Agent is likely registered using the `AddAllElasticApm` extension method defined on the `IServiceCollection`.

```csharp
var builder = WebApplication.CreateBuilder(args);
builder.Services.AddAllElasticApm();
```

To switch to using EDOT .NET, replace the preceding code:

```csharp
using OpenTelemetry;

var builder = WebApplication.CreateBuilder(args);

builder.AddElasticOpenTelemetry(b => b
   .WithTracing(t => t.AddSource("MyAppInstrumentation")));
```

The previous snippet adds one additional source to be observed, which matches the name you gave to the `ActivitySource` defined earlier. It also uses the `AddElasticOpenTelemetry` extension method for the `IHostApplicationBuilder`. By default, EDOT .NET is configured to observe the most common instrumentation and export data through OTLP. Refer to [Opinionated defaults](./setup/edot-defaults.md) for more information.

Configuration of the APM Agent is likely to have been achieved using environment variables or by providing settings using the `appsettings.json` file, typical for ASP.NET Core applications:

```json
{
  "ElasticApm": 
    {
      "ServerUrl":  "https://myapmserver:8200",
      "SecretToken":  "apm-server-secret-token",
      "ServiceName": "MyApplication"
    }
}
```

The previous configuration is no longer required and can be replaced with OpenTelemetry SDK settings. At a minimum, provide the endpoint for the export of data and the authorization header used to authenticate.

The OpenTelemetry SDK is generally configured using environment variables. For this application, set the following to be functionally equivalent during the migration of this sample application:

- `OTEL_SERVICE_NAME` = "MyApplication"
- `OTEL_EXPORTER_OTLP_ENDPOINT` = "https://myapmserver:443"
- `OTEL_EXPORTER_OTLP_HEADERS` = "Authorization=Api an_apm_api_key"

The required values for the endpoint and headers can be obtained from your Elastic Observability instance. After you've migrated, you can remove the Elastic APM Agent NuGet from your application.

For more details on registering and configuring EDOT. NET, see the [quickstart](./setup/index.md) documentation.

### Zero-code auto instrumentation

When using the Elastic APM Agent profiler auto-instrumentation functionality, the `elastic_apm_profiler_<version>.zip` must be downloaded and extracted. The following environment variables are configured for the process, service, or IIS application pool.

| Runtime        | Environment variable                | Description                                     |
| -------------- | ----------------------------------- | ----------------------------------------------- |
| .NET Framework | COR_ENABLE_PROFILING                | Instructs the runtime to enable profiling.      |
| .NET Framework | COR_PROFILER                        | Instructs the runtime which profiler to use.    |
| .NET Framework | COR_PROFILER_PATH                   | The location of the profiler.                   |
| .NET           | CORECLR_ENABLE_PROFILING            | Instructs the runtime to enable profiling.      |
| .NET           | CORECLR_PROFILER                    | Instructs the runtime which profiler to use.    |
| .NET           | CORECLR_PROFILER_PATH               | The location of the profiler DLL.               |
| All            | ELASTIC_APM_PROFILER_HOME           | The directory of the extracted profiler.        |
| All            | ELASTIC_APM_PROFILER_INTEGRATIONS   | The location of the ingegrations.yml file.      |
| All            | ELASTIC_APM_SERVER_URL              | The URL of the APM Server.                      |
| All            | ELASTIC_APM_SECRET_TOKEN            | The secret used to authenticate with APM server.|

To switch to the EDOT .NET zero-code auto instrumentation, update the `COR_*` and `CORECLR_*` environment variables to point to the Elastic redistribution of the OpenTelemetry auto-instrumentation profiler.

Follow the steps in [Using EDOT .NET zero-code instrumentation](./setup/zero-code.md) to configure the profiler.

### Limitations

Elastic APM Agent includes several features that are not currently supported when using EDOT .NET. Each of these are being assessed and may be included in contributions to OpenTelemetry or as value-add features of EDOT .NET in future releases.

#### Stacktrace capture

The [stacktrace capture](apm-agent-dotnet://reference/config-stacktrace.md) feature from Elastic APM .NET agent is not currently available in EDOT .NET.

#### Central and dynamic configuration

Currently EDOT .NET does not have an equivalent of the [central configuration feature](docs-content://solutions/observability/apm/apm-agent-central-configuration.md) that the Elastic APM .NET agent supports. 

When using EDOT .NET, all the configurations are static and should be provided to the application with other configurations, such as environment variables.

#### Span compression

EDOT .NET does not implement [span compression](docs-content://solutions/observability/apm/spans.md#apm-spans-span-compression).

## Migrate from the upstream .NET SDK [migrating-to-edot-net-from-the-upstream-opentelemetry-net-sdk]

EDOT .NET require minimal code changes to migrate from the upstream OpenTelemetry SDK for .NET. The distribution [opinionated defaults](./setup/edot-defaults.md) simplify the amount of code required to get started with OpenTelemetry in .NET applications.

In an application which already uses the upstream OpenTelemetry SDK, the following code is an example of how this would be registered and enabled in an ASP.NET Core application.

```csharp
using OpenTelemetry;
using OpenTelemetry.Metrics;
using OpenTelemetry.Resources;
using OpenTelemetry.Trace;

var builder = WebApplication.CreateBuilder(args);

builder.Services.AddOpenTelemetry()
   .ConfigureResource(r => r.AddService("MyServiceName"))
   .WithTracing(t => t
      .AddAspNetCoreInstrumentation()
      .AddHttpClientInstrumentation()
      .AddSource("AppInstrumentation"))
   .WithMetrics(m => m
      .AddAspNetCoreInstrumentation()
      .AddHttpClientInstrumentation())
   .WithLogging()
   .UseOtlpExporter();
```

In the previous code, `AddOpenTelemetry` extension method for the `IServiceCollection` activates the core components. This method returns an `OpenTelemetryBuilder`, which must be further configured to enable tracing, metrics and logging, as well as export through OTLP.

:::{note}
Register each contrib instrumentation library manually when using the SDK.
:::

To get started with the Elastic Distribution of OpenTelemetry .NET, add the `Elastic.OpenTelemetry` [NuGet package](https://www.nuget.org/packages/Elastic.OpenTelemetry)
reference to your project file:

```xml
<PackageReference Include="Elastic.OpenTelemetry" Version="<LATEST>" />
```

:::{note}
Replace the `<LATEST>` version placeholder with the [latest available package from NuGet.org](https://www.nuget.org/packages/Elastic.OpenTelemetry).
:::

EDOT .NET includes a transitive dependency on the OpenTelemetry SDK, so you do not need to add the OpenTelemetry SDK package to your project directly. However, you can explicitly add the OpenTelemetry SDK as a dependency if you want to opt into newer SDK versions.

Due to the EDOT .NET defaults, less code is required to achieve the same instrumentation behavior that the previous code snippet configured for the upstream OpenTelemetry SDK. For example:

```csharp
using OpenTelemetry;

var builder = WebApplication.CreateBuilder(args);

builder.AddElasticOpenTelemetry(b => b
    .WithTracing(t => t.AddSource("AppInstrumentation")));
```

EDOT .NET activates all signals by default, so the registration code is less verbose. EDOT .NET also performs instrumentation assembly scanning to automatically add instrumentation from any contrib libraries that it finds deployed with the application. All that is required is the installation of the relevant instrumentation NuGet packages.

:::{warning}
Instrumentation assembly scanning is not supported for applications using native [AOT](https://learn.microsoft.com/dotnet/core/deploying/native-aot) compilation.
:::

### Zero-code instrumentation

EDOT .NET ships with a lightly modified redistribution of the OpenTelemetry SDK installation script. To instrument a .NET application automatically, download and run the installer script for your operating system from the latest [release](https://github.com/elastic/elastic-otel-dotnet/releases).

Refer to the upstream OpenTelemetry SDK documentation for [.NET zero-code instrumentation](https://opentelemetry.io/docs/zero-code/net) for more examples of using the installation script.