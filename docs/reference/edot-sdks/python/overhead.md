---
navigation_title: Performance Overhead
description: Performance overhead comparison between EDOT Python and Elastic APM Python Agent.
applies_to:
  stack:
  serverless:
    observability:
products:
  - id: cloud-serverless
  - id: observability
  - id: edot-sdk
---

# Performance overhead

While designed to have minimal performance overhead, the EDOT Java agent, like any instrumentation agent, executes within the application process and thus has a small influence on the application performance. 

This performance overhead depends on the application's technical architecture, its configuration and environment, and the load. These factors are not easy to reproduce on their own, and all applications are different, so it is not possible to provide a simple answer.

## Benchmark 

The following numbers are only provided as indicators, and you should not attempt to extrapolate them. Use them as a framework to evaluate and measure the overhead on your applications.

The following table compares the response times of a sample web application without an agent, with Elastic APM Python Agent and with EDOT Python Agent in two situations: without data loaded and serialized to measure the minimal overhead of agents and with some data loaded and then serialized to provide a more common scenario.

|                                   | No agent  | EDOT Python agent | Elastic APM Python agent |
|-----------------------------------|-----------|-----------------------------|--------------------------|
| No data: Time taken for tests     | 1.277 s   | 2.215 s                     | 2.313 s                  |
| Sample data: Time taken for tests | 4.546 s   | 6.401 s                     | 6.159 s                  |
