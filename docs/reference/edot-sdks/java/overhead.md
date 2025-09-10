---
navigation_title: Performance overhead
description: This page details the expected performance impact when instrumenting Java applications with the Elastic Distribution of OpenTelemetry SDK, including benchmarks and optimization tips.
applies_to:
  stack:
  serverless:
    observability:
  product:
    edot_java: ga
products:
  - id: cloud-serverless
  - id: observability
  - id: edot-sdk
---

# Performance overhead of the EDOT SDK for Java

This page details the expected performance impact when instrumenting Java applications with the Elastic Distribution of OpenTelemetry SDK, including benchmarks and optimization tips.

While designed to have minimal performance overhead, the EDOT Java agent, like any instrumentation agent, executes within the application process and thus has a small influence on the application performance. 

This performance overhead depends on the application's technical architecture, its configuration and environment, and the load. These factors are not easy to reproduce on their own, and all applications are different, so it is not possible to provide a simple answer.

You can measure the performance overhead on the JVM by using the following high-level metrics:

- Application startup time
- Application response time, which can be directly perceived by users
- CPU usage
- Garbage collector activity: more memory allocation means more GC activity, thus increasing overall CPU usage and potentially reducing application responsiveness
- Memory usage: how much more memory (heap/non-heap) is needed

## Benchmark

While Elastic can't provide generically applicable, accurate numbers about the impact on the previous metrics, synthetic benchmarks are executed with a sample application, which allows to provide an estimate and comparison between agents. Those numbers are only provided as indicators: use them as a framework to evaluate and measure the overhead on your applications.

For example, the application startup overhead going from 5s to 6s (+1s, +20%) does not mean an application having a startup time of 15s will now start in 18s but that you can expect to have about at least one extra second of startup time and the overall impact remains limited.

The following table compares the classic Elastic APM Java Agent with the EDOT Java Agent and the same benchmark without an agent.

|                              | No agent  | EDOT Java instrumentation | Elastic APM Java agent |
|------------------------------|-----------|---------------------------|------------------------|
| Startup time                 | 5.55 s    | 6.82 s                    | 6.87 s                 |
| Request latency (p95)        | 1.96 ms   | 2.06 ms                   | 2.08 ms                |
| Total system cpu utilization | 53.82 %   | 54.25 %                   | 56.92 %                |
| Total allocated memory       | 21.54 gb  | 26.37 gb                  | 22.15 gb               |
| Total GC pauses              | 106 ms    | 123 ms                    | 120 ms                 |
| Max heap used                | 436.71 mb | 478.46 mb                 | 573.92 mb              |

The main difference between the two agents is that, unlike EDOT, Elastic APM Java agent recycles in-memory data structures which allows to reduce the overall allocated memory and thus reduces a bit the overhead on the garbage collector.

This difference is also the reason why we observe a difference in the maximum heap usage as more data structures are kept in-memory when possible and not recycled by the garbage collector. This, however, does not mean that Elastic APM Java agent requires about 100mb more of memory compared to EDOT, but that when there is no limitation on heap memory usage the agent will use available memory to minimize memory allocation.

## Optimizing application startup

With EDOT Java, the following resource attribute providers are enabled by default:

- AWS: [`OTEL_RESOURCE_PROVIDERS_AWS_ENABLED`](/reference/edot-sdks/java/configuration.md#configuration-options) = `true`
- GCP: [`OTEL_RESOURCE_PROVIDERS_GCP_ENABLED`](/reference/edot-sdks/java/configuration.md#configuration-options) = `true`
- Azure: [`OTEL_RESOURCE_PROVIDERS_AZURE_ENABLED`](/reference/edot-sdks/java/configuration.md#configuration-options) = `true`

Because those resource attributes providers rely on metadata endpoints, they might require a few HTTP requests. When the cloud provider is known or none is being used, it might be relevant to selectively turn them off by setting their respective configuration options to `false`.

Also, each activated instrumentation adds instrumentation overhead. You can control this by applying one of the following strategies:

- [Turn off instrumentations selectively](https://opentelemetry.io/docs/zero-code/java/agent/disable/#suppressing-specific-agent-instrumentation).
- [Turn off all instrumentations and selectively turn on the ones you need](https://opentelemetry.io/docs/zero-code/java/agent/disable/#enable-only-specific-instrumentation).

Note that some instrumentation relies on other instrumentation to function properly. When selectively turning on instrumentations, make sure to turn on the transitive instrumentation dependencies too.
