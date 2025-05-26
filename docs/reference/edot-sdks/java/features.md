---
navigation_title: Features
description: Explore the features of the Elastic Distribution of OpenTelemetry (EDOT) Java Agent, including inherited OpenTelemetry features and exclusive Elastic enhancements like inferred spans and universal profiling integration.
applies_to:
  stack:
  serverless:
    observability:
products:
  - id: cloud-serverless
  - id: observability
  - id: edot-sdk
---

# Features of the EDOT Java Agent

The EDOT Java agent is a [distribution](https://opentelemetry.io/docs/concepts/distributions/) of [OpenTelemetry Java Instrumentation](https://github.com/open-telemetry/opentelemetry-java-instrumentation) agent. It inherits all the features of the OpenTelemetry Java Instrumentation to capture logs, metrics, and traces.

The EDOT Java agent also provides:

- Exclusive features that are not available in the [OpenTelemetry Java Instrumentation](https://github.com/open-telemetry/opentelemetry-java-instrumentation).
- Features of [OpenTelemetry Java Instrumentation](https://github.com/open-telemetry/opentelemetry-java-instrumentation) with [different default configuration](./configuration.md#configuration-options).

In addition to the features listed, refer to [Supported technologies](./supported-technologies.md).

## Resource attributes

The EDOT Java agent includes the following resource attributes providers from [opentelemetry-java-contrib](https://github.com/open-telemetry/opentelemetry-java-contrib/):

- AWS: [aws-resources](https://github.com/open-telemetry/opentelemetry-java-contrib/tree/main/aws-resources). Turned on by default.
- GCP: [gcp-resources](https://github.com/open-telemetry/opentelemetry-java-contrib/tree/main/gcp-resources). Turned on by default.
- Application server service name detection: [resource-providers](https://github.com/open-telemetry/opentelemetry-java-contrib/tree/main/resource-providers).

## Inferred spans

The EDOT Java agent includes the [Inferred Spans Extension](https://github.com/open-telemetry/opentelemetry-java-contrib/tree/main/inferred-spans) from [opentelemetry-java-contrib](https://github.com/open-telemetry/opentelemetry-java-contrib/). This extension provides the ability to enhance the traces by creating spans from [async-profiler](https://github.com/async-profiler/async-profiler) data without the need of explicit instrumentation of corresponding spans.

This feature is turned off by default and can be activated by setting `OTEL_INFERRED_SPANS_ENABLED` to `true`. Refer to [Inferred-spans](https://github.com/open-telemetry/opentelemetry-java-contrib/tree/main/inferred-spans) documentation for configuration options.

## Span stacktrace

The EDOT Java agent includes the [Span Stacktrace Extension](https://github.com/open-telemetry/opentelemetry-java-contrib/tree/main/span-stacktrace) from [opentelemetry-java-contrib](https://github.com/open-telemetry/opentelemetry-java-contrib/).

This feature is activated by default and allows to capture a stacktrace for spans that have a duration above a threshold. The `OTEL_JAVA_EXPERIMENTAL_SPAN_STACKTRACE_MIN_DURATION` configuration option, which defaults to `5ms`, allows to configure the minimal duration threshold. A negative value turns off the feature.

Refer to [span-stacktrace](https://github.com/open-telemetry/opentelemetry-java-contrib/tree/main/span-stacktrace) for configuration options.

## Runtime metrics

Experimental runtime metrics are turned on by default.

Set `OTEL_INSTRUMENTATION_RUNTIME_TELEMETRY_EMIT_EXPERIMENTAL_TELEMETRY` to `false` to turn them off.

## Metric temporality

{{es}} and {{kib}} work best with metrics provided in delta-temporality. Therefore, the EDOT Java changes the default value of `OTEL_EXPORTER_OTLP_METRICS_TEMPORALITY_PREFERENCE` to `DELTA`. You can override this default if needed, though some provided {{kib}} dashboards will not work correctly if you do it.

## Elastic Universal Profiling integration

[Universal Profiling](https://www.elastic.co/observability/universal-profiling) integration provides the ability to correlate traces with profiling data from the Elastic universal profiler. This feature is turned on by default on supported systems, and turned off otherwise.

Refer to [universal-profiling-integration](https://github.com/elastic/elastic-otel-java/tree/main/universal-profiling-integration) for details and configuration options.
