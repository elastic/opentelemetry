---
navigation_title: Migration
description: Migrate from the Elastic APM .NET agent to the Elastic Distribution of OpenTelemetry .NET (EDOT .NET).
applies_to:
  stack:
  serverless:
    observability:
products:
  - cloud-serverless
  - observability
  - edot-dotnet
  - apm-dotnet-agent
---

# Migrating to EDOT .NET

The observability industry is shifting to adopt [OpenTelemetry](https://opentelemetry.io/). At Elastic, we are focused on
contributing to help OpenTelemetry succeed, and OpenTelemetry-native support is being introduced across all Elastic
Observability tooling. OpenTelemetry offers several primary advantages for the industry:

- No vendor lock-in through standardized concepts, supporting the use of multiple backend vendors or switching between them.
- A single set of application APIs are required to instrument applications.
- A wider pool of knowledge, experience and support is available across the OpenTelemetry community.
- Efficient data collection and advanced data processing opportunities.

At Elastic, we believe the responsible choice is to concentrate on enabling and encouraging customers to favor vendor-neutral instrumentation
in their code and reap the benefits of OpenTelemetry. Engineering teams should be preparing to adopt OpenTelemetry and planning
to migrate existing application instrumentation from vendor-specific agents to the standardized OpenTelemetry SDKs.

While the upstream [OpenTelemetry SDK for .NET](https://github.com/open-telemetry/opentelemetry-dotnet) can be used to
directly export data to an Elastic Observability backend (both in Elastic Cloud and on-prem), some capabilities of the
Elastic tooling may not be able to function as intended. For that reason, we provide Elastic distributions that
provide a thin layer over the OpenTelemetry tools to provide our customers with the best compatibility, supportability and features. 
We recommend using the Elastic Distribution of OpenTelemetry (EDOT) language SDK and the 
[Elastic Distribution of OpenTelemetry collector](../../edot-collector/index.md) for the best experience.

This page guides migrating to EDOT .NET from either the existing 
[Elastic APM Agent for .NET](https://www.elastic.co/guide/en/apm/agent/dotnet/current/index.html) or from the upstream
OpenTelemetry SDK.

- [Migrating to EDOT .NET from Elastic .NET Agent](#migrating-to-edot-net-from-elastic-net-agent)
- [Migrating to EDOT .NET from the upstream OpenTelemetry .NET SDK](#migrating-to-edot-net-from-the-upstream-opentelemetry-net-sdk)

## Migrating to EDOT .NET from Elastic .NET Agent [migrating-to-edot-net-from-elastic-net-agent]

### Migrating manual application instrumentation

The Elastic APM Agent supports OTel-native trace instrumentation through its 
[OpenTelemetry Bridge](https://www.elastic.co/guide/en/apm/agent/dotnet/current/opentelemetry-bridge.html) feature which is
enabled by default.

The bridge subscribes to instrumentation created using the [`Activity`](https://learn.microsoft.com/dotnet/api/system.diagnostics.activity) 
API in .NET. An `Activity` represents a unit of work and aligns with the OpenTelemetry "span" concept. The API name is used for historical
backward compatibility. The `Activity` API is the recommended approach to introduce tracing when instrumenting applications.

For applications which are instrumented using the [public API](https://www.elastic.co/guide/en/apm/agent/dotnet/current/public-api.html)
A recommended first step of the existing APM Agent is to consider migrating instrumentation over to the `Activity` API.

For example, in an ASP.NET Core Razor pages application, we may have manually created a child span below
the parent transaction for the ASP.NET Core request:

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

The preceding code captures (starts and ends) a span within the current transaction. The span is named
"Doing stuff". The second argument specifies the type of work this span represents, "internal" in this
example. Within the async lambda, the work is performed, and a custom label is set.

To convert this to the `Activity` API, first define an `ActivitySource` used to create
`Activity` instances (spans). Typically, you have a few (usually just one) of these for application-specific
instrumentation. Define a static instance somewhere within your application.

```csharp
public static class Instrumentation
{
   public static readonly ActivitySource ApplicationActivitySource = new("MyAppInstrumentation");
}
```

The `IndexModel` class can now be updated to prefer the `Activity` API. Spans created through this API
will be automatically observed and sent from the APM Agent by the OpenTelemetry bridge.

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

This code is equivalent to the previous code snippet, but it is now vendor-neutral, preferring the
built-in .NET `Activity` API from the `System.Diagnostics` namespace.

The `Activity` class implements `IDisposable`, allowing us to reduce the nesting of code. `StartActivity`
is called on the `ActivitySource`, which creates and starts an `Activity`. Starting an `Activity` results
in a new span, which may be a child of a parent, if an existing `Activity` is already being tracked. This
is handled automatically by the .NET API. 

The overload we have used accepts a name for the `Activity`, in this example, "Doing stuff". We can
optionally pass an `ActivityKind`, although this defaults to `ActivityKind.Internal`, so we omit that here.

The preceding code uses the `SetTag` method to "activity" variable may be assigned `null`. To reduce instrumentation
overhead, `StartActivity` may return `null` if no observers of the `ActivitySource` exist. While the
API uses the notion of "tags"; these are functionally equivalent to the OpenTelemetry concept of "attributes.
Attributes are used to attach arbitrary information to a span in order to enrich it and provide context when
analysing the telemetry data.

This serves as a brief primer for instrumenting code using the .NET built-in tracing API and the `Activity`
class. Visit the Microsoft documentation for more examples of 
[adding distributed tracing instrumentation](https://learn.microsoft.com/dotnet/core/diagnostics/distributed-tracing-instrumentation-walkthroughs).

### Migrating agent registration

After migrating any manual instrumentation from the Elastic APM Agent public API to the Microsoft `Activity`
API, the final step is to switch the observation and export of telemetry signals from the APM Agent to EDOT .NET.

The precise steps will vary by project template but involve replacing ing the registration of the APM agent. In
all cases, you will need to add the `Elastic.Opentelemetry` [NuGet package](https://www.nuget.org/packages/Elastic.OpenTelemetry)
to your project.

```xml
<PackageReference Include="Elastic.OpenTelemetry" Version="<LATEST>" />
```

:::{note}
Replace the `<LATEST>` version placeholder with the [latest available package from NuGet.org](https://www.nuget.org/packages/Elastic.OpenTelemetry).
:::

You may also need to install additional instrumentation libraries to observe signals from specific components, such as
ASP.NET Core.

```xml
<PackageReference Include="OpenTelemetry.Instrumentation.AspNetCore" Version="<LATEST>" />
```

:::{note}
Replace the `<LATEST>` version placeholder with the [latest available package from NuGet.org](https://www.nuget.org/packages/OpenTelemetry.Instrumentation.AspNetCore).
:::

In an ASP.NET Core application, the APM Agent is likely registered using the `AddAllElasticApm` extension method
defined on the `IServiceCollection`.

```csharp
var builder = WebApplication.CreateBuilder(args);
builder.Services.AddAllElasticApm();
```

To switch to using EDOT .NET, the preceding code should be replaced.

```csharp
using OpenTelemetry;

var builder = WebApplication.CreateBuilder(args);

builder.AddElasticOpenTelemetry(b => b
   .WithTracing(t => t.AddSource("MyAppInstrumentation")));
```

Here, we prefer the `AddElasticOpenTelemetry` extension method for the `IHostApplicationBuilder`.
By default, EDOT .NET is configured to observe the most common instrumentation and export data via OTLP.
See [opinionated defaults](./setup/edot-defaults.md) for more information.

The preceding code snippet adds one additional source to be observed, which matches the name
we gave to the `ActivitySource` defined earlier.

Configuration of the APM Agent is likely to have been achieved using environment variables or by providing settings
using the `appsettings.json` file, typical for ASP.NET Core applications.

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

The above configuration is no longer required and can be replaced with OpenTelemetry SDK settings. At a
minimum, we need to provide the endpoint for the export of data and the authorization header used to
authenticate.

The OpenTelemetry SDK is generally configured using environment variables. For this application, we should
set the following to be functionally equivalent during the migration of this sample application.

- `OTEL_SERVICE_NAME` = "MyApplication"
- `OTEL_EXPORTER_OTLP_ENDPOINT` = "https://myapmserver:443"
- `OTEL_EXPORTER_OTLP_HEADERS` = "Authorization=Api an_apm_api_key"

The required values for the endpoint and headers can be obtained from your Elastic Observability instance.

Once migrated, the Elastic APM Agent NuGet package can be removed from your application.

For more details on registering and configuring EDOT. NET, see the [quickstart](./setup/index.md) documentation.

### Limitations

Elastic APM Agent includes several features that are not currently supported when using EDOT .NET. Each of 
these are being assessed and may be included in contributions to OpenTelemetry or as value-add features of
EDOT .NET in future releases.

- Stacktrace capture
- Central configuration
- Dynamic configuration
- Span compression

### Zero-code auto instrumentation

When using the Elastic APM Agent profiler auto instrumentation functionality, the `elastic_apm_profiler_<version>.zip`
will have been downloaded and extracted. The following environment variables will be configured for the
process, service, or IIS application pool.

| Runtime        | Environment variable                | Description                                     |
| -------------- | ----------------------------------- | ----------------------------------------------- |
| .NET Framework | COR_ENABLE_PROFILING                | Instructs the runtime to enable profiling.      |
| .NET Framework | COR_PROFILER                        | Instructs the runtime which profiler to use.    |
| .NET Framework | COR_PROFILER_PATH                   | The location of the profiler                    |
| .NET           | CORECLR_ENABLE_PROFILING            | Instructs the runtime to enable profiling.      |
| .NET           | CORECLR_PROFILER                    | Instructs the runtime which profiler to use.    |
| .NET           | CORECLR_PROFILER_PATH               | The location of the profiler DLL                |
| All            | ELASTIC_APM_PROFILER_HOME           | The directory of the extracted profiler         |
| All            | ELASTIC_APM_PROFILER_INTEGRATIONS   | The location of the ingegrations.yml file       |
| All            | ELASTIC_APM_SERVER_URL              | The URL of the APM Server                       |
| All            | ELASTIC_APM_SECRET_TOKEN            | The secret used to authenticate with APM server |

To switch to the EDOT .NET zero-code auto instrumentation, the `COR_*` and `CORECLR_*` environment variables must
be updated to point to the Elastic redistribution of the OpenTelemetry autoinstrumentation profiler.

Please follow the steps in [Using EDOT .NET zero-code instrumentation](./setup/zero-code.md) to configure the profiler.

## Migrating to EDOT .NET from the upstream OpenTelemetry .NET SDK [migrating-to-edot-net-from-the-upstream-opentelemetry-net-sdk]

Our design goal for EDOT .NET has been to introduce no new concepts and require minimal code changes to migrate
from the upstream OpenTelemetry SDK for .NET to EDOT .NET as easily as possible. Our [opinionated defaults](./setup/edot-defaults.md)
strive to simplify the amount of code required to get started with OpenTelemetry in .NET applications.

In an application which already uses the upstream OpenTelemetry SDK, the following code is an example of how
this would be registered and enabled in an ASP.NET Core application.

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

In the preceding code, `AddOpenTelemetry` extension method for the `IServiceCollection` is used
to enable the core components. This method returns an `OpenTelemetryBuilder`, which must be further
configured to enable tracing, metrics and logging, as well as export via OTLP.

:::{note}
Each contrib instrumentation library must be registered manually when using the SDK.
:::

To get started with the Elastic Distribution of OpenTelemetry .NET, add the 
`Elastic.OpenTelemetry` [NuGet package](https://www.nuget.org/packages/Elastic.OpenTelemetry)
reference to your project file:

```xml
<PackageReference Include="Elastic.OpenTelemetry" Version="<LATEST>" />
```

:::{note}
Replace the `<LATEST>` version placeholder with the [latest available package from NuGet.org](https://www.nuget.org/packages/Elastic.OpenTelemetry).
:::

EDOT .NET includes a transitive dependency on the OpenTelemetry SDK, so you do not _need_ to add the 
OpenTelemetry SDK package to your project directly. However, you _can_ explicitly add the OpenTelemetry 
SDK as a dependency if you want to opt into newer SDK versions.

Due to the EDOT .NET defaults, less code is required to achieve the same instrumentation behaviour that
the previous code snippet configured for the upstream OpenTelemetry SDK.

```csharp
using OpenTelemetry;

var builder = WebApplication.CreateBuilder(args);

builder.AddElasticOpenTelemetry(b => b
    .WithTracing(t => t.AddSource("AppInstrumentation")));
```

EDOT .NET enables all signals by default, so the registration code is less verbose. EDOT .NET also
performs instrumentation assembly scanning to automatically add instrumentation from any contrib libraries
that it finds deployed with the application. All that is required is the installation of the relevant
instrumentation NuGet packages.

:::{warning}
Instrumentation assembly scanning is not supported for applications using native [AOT](https://learn.microsoft.com/dotnet/core/deploying/native-aot) compilation.
:::

### Zero-code auto instrumentation

EDOT .NET ships with a lightly modified redistribution of the OpenTelemetry SDK installation script.
To instrument a .NET application automatically, download and run the installer script for your operating system
from the latest [release](https://github.com/elastic/elastic-otel-dotnet/releases).

See the upstream OpenTelemetry SDK documentation for [.NET zero-code instrumentation](https://opentelemetry.io/docs/zero-code/net)
for more examples of using the installation script.