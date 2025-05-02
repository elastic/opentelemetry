---
title: Advanced scenarios
layout: default
nav_order: 5
parent: Setup
grand_parent: EDOT .NET
nav_exclude: true
---

# Advanced scenarios

TODO

## Conditionally enabling signals

TODO

## Native AOT support

## Console applications using Microsoft.Extensions.DependencyInjection

```csharp
using Microsoft.Extensions.DependencyInjection;
using OpenTelemetry;
using OpenTelemetry.Logs;
using OpenTelemetry.Metrics;
using OpenTelemetry.Resources;
using OpenTelemetry.Trace;
using System.Diagnostics;

const string activitySourceName = "MyAppSource";

var services = new ServiceCollection();

var otelBuilder = services.AddElasticOpenTelemetry();

otelBuilder
    .ConfigureResource(r => r.AddService("ConsoleAppService"))
    .WithTracing(t => t.AddSource(activitySourceName));

var sp = services.BuildServiceProvider();

sp.GetService<TracerProvider>();
sp.GetService<MeterProvider>();
sp.GetService<LoggerProvider>();

var activitySource = new ActivitySource(activitySourceName);

using (var activity = activitySource.StartActivity("DoingStuff"))
{
    // Simulated workload
    await Task.Delay(100);
}

Console.ReadKey();
```

