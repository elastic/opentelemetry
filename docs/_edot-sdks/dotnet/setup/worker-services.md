---
title: .NET worker services
layout: default
nav_order: 4
parent: Setup
grand_parent: EDOT .NET
---

# Set up EDOT .NET for worker services

When building long-running [worker services](https://learn.microsoft.com/en-us/dotnet/core/extensions/workers)
using the Worker Service template, introducing OpenTelemetry is achieved using the same approach as with ASP.NET Core.
The recommended way to enable EDOT .NET is by calling `AddElasticOpenTelemetry` on the `HostApplicationBuilder`.

```csharp
using Example.WorkerService;

var builder = Host.CreateApplicationBuilder(args);
builder.AddElasticOpenTelemetry();

builder.Services.AddSingleton<QueueReader>();
builder.Services.AddHostedService<Worker>();

var host = builder.Build();
host.Run();
```

The preceding code:

1. Creates a `HostApplicationBuilder` using the `Host.CreateApplicationBuilder` factory method.
1. Enables EDOT .NET by calling `AddElasticOpenTelemetry` on the `HostApplicationBuilder`.
1. Registers application-specific types into the `IServiceCollection`.
1. Builds and runs the `IHost`.

This is the same approach as shown in the [getting started](index) and [ASP.NET Core](aspnetcore) examples
and the same techniques for configuration and usage apply.

## Instrumenting worker services

Let's explore a more complete example, focusing on how instrumentation can be added and
observed for a basic worker service. In this example, we instrument an application designed to
read and process messages from a queue (simulated for simplicity).

In the preceding code, two application types were registered into the dependency injection container.

```csharp
builder.Services.AddSingleton<QueueReader>();
builder.Services.AddHostedService<Worker>();
```

`QueueReader` is a class abstracts the reading of messages from a queue. In this example, it simulates
this by returning a message every five seconds. In a real example, the application would access a
source such as AWS SQS or Azure Service Bus.

```
public class QueueReader
{
   public async IAsyncEnumerable<Message> GetMessages([EnumeratorCancellation] CancellationToken ctx = default)
   {
      while (!ctx.IsCancellationRequested)
      {
         await Task.Delay(TimeSpan.FromSeconds(5), ctx);
         yield return new Message(Guid.NewGuid().ToString());
      }
   }
}
```

