---
navigation_title: Metrics
description: Metrics produced by the Elastic Distribution of OpenTelemetry Node.js (EDOT Node.js).
applies_to:
  stack:
  serverless:
    observability:
  product:
    edot_node: ga
products:
  - id: cloud-serverless
  - id: observability
  - id: edot-sdk
---

# Metrics

In the Elastic Distribution of OpenTelemetry for Node.js (EDOT Node.js) the collection of metrics is turned on by default. Refer to the [settings with `METRIC` in the name](./configuration.md) for all options for configuring metric collection.

## Process and runtime metrics

EDOT Node.js gathers metrics from the Node.js process your application is
running using the following packages:

- `@opentelemetry/host-metrics` to gather `process.cpu.*` and `process.memory.*` metrics ([ref](https://github.com/open-telemetry/semantic-conventions/blob/80988c54712ee336cb3a6240b8845e9dfa8c9f49/docs/system/process-metrics.md?plain=1#L22)).
- `@opentelemetry/instrumentation-runtime-node` to gather `nodejs.eventloop.*` ([ref](https://github.com/open-telemetry/semantic-conventions/blob/80988c54712ee336cb3a6240b8845e9dfa8c9f49/model/nodejs/metrics.yaml)) and `v8js.*` ([ref](https://github.com/open-telemetry/semantic-conventions/blob/80988c54712ee336cb3a6240b8845e9dfa8c9f49/model/v8js/metrics.yaml)) metrics.

Process and runtime metrics are useful when you're checking the performance of your instrumented service.
A subset of them are useful to detect issues when doing an overview of the instrumented service. These are:

- `nodejs.eventloop.delay.p50` and `nodejs.eventloop.delay.p90` are the
  50th and 90th [percentiles](https://en.wikipedia.org/wiki/Percentile) of
  the event loop delay. The event loop delay measures the time span between
  the scheduling of a callback and its execution. The bigger the number,
  the more sync work you have in your service blocking the event loop.
- `nodejs.eventloop.utilization` is the utilisation of the event loop reported
  by [`performance.eventLoopUtilization([utilization1[, utilization2]])`](https://nodejs.org/api/perf_hooks.html#performanceeventlooputilizationutilization1-utilization2) which gives
  the percentage of time the event loop is being used (not idle).
- `process.cpu.utilization` is the percentage of time the CPU is running
  the service code. Big values in this metric suggest your service is doing
  compute intensive tasks.
- `process.memory.usage` is the value of [Resident Set Size](https://nodejs.org/api/process.html#processmemoryusagerss) in bytes. It
  measures how much memory the process is allocating.

If your service is instrumented by EDOT Node.js, or by custom instrumentation that includes the packages previously mentioned,
{{kib}} shows them as part of the [service metrics](docs-content://solutions/observability/apm/metrics-ui.md).
