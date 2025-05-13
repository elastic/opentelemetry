---
navigation_title: .NET worker services
description: Learn how to instrument .NET worker services for Elastic Observability using the Elastic Distribution of OpenTelemetry .NET.
applies_to:
  stack:
  serverless:
    observability:
products:
  - id: cloud-serverless
  - id: observability
  - id: edot-dotnet
---

# Set up EDOT .NET for worker services

When building long-running [worker services](https://learn.microsoft.com/en-us/dotnet/core/extensions/workers) using the Worker Service template, OpenTelemetry is introduced using the same approach as for ASP.NET Core. The recommended way to turn on EDOT .NET is by calling `AddElasticOpenTelemetry` on the `HostApplicationBuilder`.

```csharp
using Example.WorkerService;

var builder = Host.CreateApplicationBuilder(args);
builder.AddElasticOpenTelemetry();

builder.Services.AddSingleton<QueueReader>();
builder.Services.AddHostedService<Worker>();

var host = builder.Build();
host.Run();
```

The previous code:

1. Creates a `HostApplicationBuilder` using the `Host.CreateApplicationBuilder` factory method.
2. Turns on EDOT .NET by calling `AddElasticOpenTelemetry` on the `HostApplicationBuilder`.
3. Registers application-specific types into the `IServiceCollection`.
4. Builds and runs the `IHost` to execute the application workload.

Because the worker service template is based on the generic host, shared with ASP.NET Core applications, this is the same approach as shown in the [getting started](index.md) and the same techniques for configuration and usage apply.

## Instrument worker services

Consider an application designed to read and process messages from a queue (simulated for simplicity). In the preceding code, two application types were registered into the dependency injection container:

```csharp
builder.Services.AddSingleton<QueueReader>();
builder.Services.AddHostedService<Worker>();
```

`QueueReader` is a class that abstracts the reading of messages from a queue. This example simulates this by returning a message every five seconds. In practice, an actual application would receive messages from a source such as AWS SQS or Azure Service Bus.

```csharp
using System.Runtime.CompilerServices;

namespace Example.WorkerService;

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

The previous code:

1. Defines a `GetMessages` method, returning an `IAsyncEnumerable<Message>`.
2. The while loop continues until it is cancelled.
3. It simulates receiving a message from a queue, in this case, yielding one every five seconds.

For this example, the `Message` type is a simple record class exposing an `Id` property.

```csharp
namespace Example.WorkerService;

public record class Message(string Id) {}
```

The main work takes place inside a `BackgroundService`.

```csharp
namespace Example.WorkerService;

public class Worker : BackgroundService
{
   private readonly ILogger<Worker> _logger;
   private readonly QueueReader _queueReader;

   private static readonly Random Random = new();

   public Worker(ILogger<Worker> logger, QueueReader queueReader)
   {
      _logger = logger;
      _queueReader = queueReader;
   }

   protected override async Task ExecuteAsync(CancellationToken stoppingToken)
   {
      await foreach (var message in _queueReader.GetMessages().WithCancellation(stoppingToken))
      {
         var success = await ProcessMessageAsync(message);

         if (!success)
         {
            _logger.LogError("Unable to process message {Id}", message.Id);
         }
      }
   }

   private static async Task<bool> ProcessMessageAsync(Message message)
   {
      await Task.Delay(Random.Next(100, 300)); // simulate processing
      return Random.Next(10) < 8; // simulate 80% success
   }
}
```

The previous code:

1. Accepts an `ILogger` and `QueueReader` in the constructor, provided by dependency injection.
2. Implements a long-running work loop in `ExecuteAsync`.
3. Within the loop, it waits for a message to be made available by the `QueueReader` before processing it.
4. `ProcessMessageAsync` provides a dummy processing implementation which fails occasionally.
5. The code is currently instrumented with logging, recording an error for messages it fails to process.

In the remaining part of this example, we'll introduce tracing and metrics instrumentation for this 
application.

At the beginning of the `Worker` class, we'll define some static and constant fields.

```csharp
public const string DiagnosticName = "Elastic.Processor";

private static readonly ActivitySource ActivitySource = new(DiagnosticName);
private static readonly Meter Meter = new(DiagnosticName);
private static readonly Counter<int> MessagesReadCounter = Meter.CreateCounter<int>("elastic.processor.messages_read");
```

These lines of code require two additional using directives:

```csharp
using System.Diagnostics;
using System.Diagnostics.Metrics;
```

The previous code:

1. Adds the 'DiagnosticName' field to define a unique name used for this application's telemetry signals that 
we'll later use to observe them. 
2. Creates a static `ActivitySource`, which will be the source for `Activity` instances used for trace
instrumentation. It uses the name defined in the 'DiagnosticName' constant field.
3. Creates a static `Meter`, which will be the source for metrics. It also uses the name defined in the 
'DiagnosticName' constant field.
4. Creates a `Counter<int>` stored in the field 'MessagesReadCounter'. This instrument has the name 
'elastic.processor.messages_read'. 

The naming of custom metrics is a decision left to organizations. As a good practice, the name is prefixed with a unique identifier for the metric owner and uses dot notation to provide a concise yet meaningful name.

The final step is to record telemetry when processing messages. We'll amend the `ExecuteAsync` method to add instrumentation.

```csharp
protected override async Task ExecuteAsync(CancellationToken stoppingToken)
{
   await foreach (var message in _queueReader.GetMessages().WithCancellation(stoppingToken))
   {
      using var activity = ActivitySource.StartActivity("Process message", ActivityKind.Internal);

      activity?.SetTag("elastic.message.id", message.Id);

      if (MessagesReadCounter.Enabled)
         MessagesReadCounter.Add(1);

      var success = await ProcessMessageAsync(message);

      if (!success)
      {
         _logger.LogError("Unable to process message {Id}", message.Id);
         activity?.SetStatus(ActivityStatusCode.Error);
      }
   }
}
```

The previous code:

1. Starts an `Activity` using `ActivitySource.StartActivity`. As a reminder, an activity in .NET is a "span" in OpenTelemetry terminology. The activity is given a name and optionally an `ActivityKind`.
2. The message ID is added as a tag (attribute in OpenTelemetry parlance) using the `SetTag` method. The null conditional operator `activity?` is used when calling methods on the `Activity`, which might be null if unobserved.
3. The code also increments the counter stored in the 'MessagesReadCounter' field.
4. After processing the message, if processing fails, we use `SetStatus` to identify that there was an error.

With the instrumentation in place, we need to make a final change to our 'Program.cs' file to configure OpenTelemetry to observe our new instrumentation.

```csharp
builder.AddElasticOpenTelemetry(b => b
   .WithTracing(t => t.AddSource(Worker.DiagnosticName))
   .WithMetrics(m => m.AddMeter(Worker.DiagnosticName)));
```

The previous code:

1. Configures tracing using `WithTracing` to add the diagnostic name as a source for trace telemetry we wish to collect and export. The `AddSource` method is called on the builder to configure this.
2. Configures metrics using `WithMetrics` to add the diagnostic name as a meter for metrics telemetry we wish to collect and export. The `AddMeter` method is called on the builder to configure this.

With these changes in place, this sample application is now instrumented, and for each message processed, a span will be created and exported. We also increment a metric for which the value will be periodically sent. EDOT .NET configures the delta temporality [by default](../setup/edot-defaults.md), so each exported value for the counter will be the count since the last export.