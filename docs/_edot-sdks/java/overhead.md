---
title: Performance overhead
layout: default
nav_order: 8
parent: EDOT Java
---

# Performance overhead

While it is designed to and usually have minimal performance overhead, the EDOT Java agent, like any instrumentation agent,
executes within the application process and thus has a small influence on the application performance. 

This extra performance overhead depends on the application's technical architecture, its configuration and environment and 
the load. Those factors are not something that are easy to reproduce on their own, and all applications are different so 
it is impossible to provide a simple answer like "+1% extra CPU time and +100Mb of memory".

The performance overhead on the JVM can be measured by the following high-level metrics:

- application startup time
- application response time, which can be directly perceived by users
- CPU usage
- Garbage collector activity: more memory allocation means more GC activity, thus increasing overall CPU usage and potentially reducing application responsiveness
- Memory usage: how much more memory (heap/non-heap) is needed

While we can't provide generically applicable, accurate numbers about the above, we execute synthetic benchmarks with a sample application
which allows to provide an estimate, comparison between agents and an order of magnitude of the effective overhead.

Those numbers are only provided as indicators, and you should not attempt to extrapolate them. You should however use
them as a framework to evaluate and measure the overhead on your applications.

For example, the application startup overhead going from 5s to 6s (+1s, +20%) does not mean an application having a startup time of
15s will now start in 18s but that you can expect to have about at least one extra second of startup time and the overall
impact remains limited.

The following table compares the *classic Elastic APM Java Agent* with the `EDOT Java Agent` and the same benchmark without an agent.

|                              | no agent  | EDOT Java instrumentation | Elastic APM Java agent |
|------------------------------|-----------|---------------------------|------------------------|
| startup time                 | 5.55 s    | 6.82 s                    | 6.87 s                 |
| request latency (p95)        | 1.96 ms   | 2.06 ms                   | 2.08 ms                |
| total system cpu utilization | 53.82 %   | 54.25 %                   | 56.92 %                |
| total allocated memory       | 21.54 gb  | 26.37 gb                  | 22.15 gb               |
| total GC pauses              | 106 ms    | 123 ms                    | 120 ms                 |
| max heap used                | 436.71 mb | 478.46 mb                 | 573.92 mb              |

The main difference between the two agents is that unlike EDOT, Elastic APM Java agent recycles in-memory data
structures which allows to reduce the overall allocated memory and thus reduces a bit the overhead on the garbage collector.

This difference is also the reason why we observe a difference in the maximum heap usage as more data structures are kept
in-memory when possible and not recycled by the garbage collector. This however does not mean that Elastic APM Java agent _requires_
about 100mb more of memory compared to EDOT, but that when there is no limitation on heap memory usage the agent will
use available memory to minimize memory allocation.

## Optimizing application startup

With EDOT Java, the following resource attribute providers are enabled by default:

- AWS: [`OTEL_RESOURCE_PROVIDERS_AWS_ENABLED`](./configuration#configuration-options) = `true`
- GCP: [`OTEL_RESOURCE_PROVIDERS_GCP_ENABLED`](./configuration#configuration-options) = `true`
- Azure: [`OTEL_RESOURCE_PROVIDERS_AZURE_ENABLED`](./configuration#configuration-options) = `true`

Because those resource attributes providers rely on metadata endpoints, they may require a few HTTP requests.
When the cloud provider is known or none is being used, it might be relevant to selectively disable them by setting
their respective configuration options to `false`.
