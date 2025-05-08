---
navigation_title: Performance Overhead
description: Performance overhead comparison between EDOT Python and Elastic APM Python Agent.
applies_to:
  stack:
  serverless:
    observability:
products:
  - cloud-serverless
  - observability
  - edot-python
---

# Performance Overhead

Every instrumentation agent comes with performance overhead for your application. How much really depends on your application and on the instrumentations used.

While we can't provide generically applicable, accurate numbers about the performance overhead, here you can find some measurement taken
from a sample web application which allows to provide a comparison between agents and an order of magnitude of the effective overhead.

Those numbers are only provided as indicators, and you should not attempt to extrapolate them. You should however use
them as a framework to evaluate and measure the overhead on your applications.

The following table compares the response times of a sample web application without an agent, with Elastic APM Python Agent and with EDOT Python Agent in two situations: without data loaded and serialized to measure the minimal overhead of agents and with some data loaded and then serialized to provide a more common scenario.

|                                   | No agent  | EDOT Python agent | Elastic APM Python agent |
|-----------------------------------|-----------|-----------------------------|--------------------------|
| No data: Time taken for tests     | 1.277 s   | 2.215 s                     | 2.313 s                  |
| Sample data: Time taken for tests | 4.546 s   | 6.401 s                     | 6.159 s                  |
