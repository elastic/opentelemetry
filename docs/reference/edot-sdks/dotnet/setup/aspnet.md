---
navigation_title: ASP.NET
applies_to:
  stack:
  serverless:
---

# Set up EDOT .NET for ASP.NET applications on .NET Framework

EDOT .NET can be used with ASP.NET applications by registering the OpenTelemetry SDK TelemetryHttpModule.

## Installing the NuGet packages

To get started with the Elastic Distribution of OpenTelemetry .NET, add the `Elastic.OpenTelemetry` [NuGet package](https://www.nuget.org/packages/Elastic.OpenTelemetry)
reference to your project file:

```xml
<PackageReference Include="Elastic.OpenTelemetry" Version="<LATEST>" />
```

:::{note}
Replace the `<LATEST>` version placeholder with the [latest available package from NuGet.org](https://www.nuget.org/packages/Elastic.OpenTelemetry).
:::

EDOT .NET includes a transitive dependency on the OpenTelemetry SDK, so you do not _need_ to add the OpenTelemetry SDK package to your project directly. However,
you _can_ explicitly add the OpenTelemetry SDK as a dependency if you want to opt into newer SDK versions.

For ASP.NET applications, you will also need to install the contrib instrumentation library. Add the 
`OpenTelemetry.Instrumentation.AspNet` [NuGet package](https://www.nuget.org/packages/OpenTelemetry.Instrumentation.AspNet)
reference to your project file:

```xml
<PackageReference Include="OpenTelemetry.Instrumentation.AspNet" Version="<LATEST>" />
```

:::{note}
Replace the `<LATEST>` version placeholder with the [latest available package from NuGet.org](https://www.nuget.org/packages/Elastic.OpenTelemetry).
:::

:::{note}
If you use the Visual Studio NuGet Package Manager or the .NET CLI to install this package, you will need to allow pre-release
package versions.
:::

## Modify web.config

Next, modify your `Web.Config` file to add a required HttpModule:

```xml
<system.webServer>
   <modules>
      <add
         name="TelemetryHttpModule"
         type="OpenTelemetry.Instrumentation.AspNet.TelemetryHttpModule,
               OpenTelemetry.Instrumentation.AspNet.TelemetryHttpModule"
         preCondition="integratedMode,managedHandler" />
   </modules>
</system.webServer>
```

## Register the EDOT .NET and OpenTelemetry SDK

Finally, initialize ASP.NET instrumentation in your `Global.asax.cs` file along with other OpenTelemetry initialization:

```csharp
using OpenTelemetry;
using OpenTelemetry.Resources;
using System.Web;
using System.Web.Http;
using System.Web.Mvc;
using System.Web.Optimization;
using System.Web.Routing;

namespace AspNetFramework
{
   public class WebApiApplication : HttpApplication
   {
      private OpenTelemetrySdk _sdk;

      protected void Application_Start()
      {
         _sdk = OpenTelemetrySdk.Create(builder => builder
           .WithElasticDefaults()
           .ConfigureResource(r => r.AddService("MyClassicAspNetApp")));

         AreaRegistration.RegisterAllAreas();
         GlobalConfiguration.Configure(WebApiConfig.Register);
         FilterConfig.RegisterGlobalFilters(GlobalFilters.Filters);
         RouteConfig.RegisterRoutes(RouteTable.Routes);
         BundleConfig.RegisterBundles(BundleTable.Bundles);
      }

      protected void Application_End()
      {
         _sdk?.Dispose();
      }
    }
}
```

The preceding code:

1. Imports the required types from the `OpenTelemetry` namespace.
1. Creates an instance of the `OpenTelemetrySdk` using its factory `Create` method.
1. Configures the `IOpenTelemetryBuilder` by passing a lambda.
1. Enables EDOT .NET and its [opinionated defaults](./../setup/edot-defaults) by calling `WithElasticDefaults` on the `IOpenTelemetryBuilder`.
1. Calls `ConfigureResource` to configure the name for the service.

By default, EDOT .NET uses instrumentation assembly scanning and will detect the `OpenTelemetry.Instrumentation.AspNet`
instrumentation, registering it with the OpenTelemetry SDK. Traces for ASP.NET requests will automatically be observed
and exported over OTLP without further configuration.

## Configure environment variables

When calling `OpenTelemetrySdk.Create` a dedicated `IServiceCollection` and `IServiceProvider` will be created for the 
SDK and shared by all signals. An `IConfiguration` is created automatically from environment variables. The
recommended method to configure the OpenTelemetry SDK is via environment variables. At a minimum, we should set
the environment variables used to configure the OTLP exporter using any suitable method for your operating system.

```
"OTEL_EXPORTER_OTLP_ENDPOINT" = "https://{MyServerlessEndpoint}.apm.us-east-1.aws.elastic.cloud:443",
"OTEL_EXPORTER_OTLP_HEADERS" = "Authorization=ApiKey {MyEncodedApiKey}"
```

## Advanced ASP.NET configuration

For further advice on configuring OpenTelemetry in ASP.NET application visit the 
[OpenTelemetry documentation](https://opentelemetry.io/docs/languages/dotnet/netframework/).