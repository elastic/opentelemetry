---
navigation_title: Features
description: Explore the features of the Elastic Distribution of OpenTelemetry (EDOT) Java Agent, including inherited OpenTelemetry features and exclusive Elastic enhancements like inferred spans and universal profiling integration.
---
# Features of the EDOT Java Agent

The EDOT Java agent is a [distribution](https://opentelemetry.io/docs/concepts/distributions/) of
[OpenTelemetry Java Instrumentation](https://github.com/open-telemetry/opentelemetry-java-instrumentation) agent, it thus
inherits all the features of the OpenTelemetry Java Instrumentation to capture logs, metrics and traces.

The EDOT Java agent also provides:

- exclusive features that are _not available_ in the [OpenTelemetry Java Instrumentation](https://github.com/open-telemetry/opentelemetry-java-instrumentation)
- features of [OpenTelemetry Java Instrumentation](https://github.com/open-telemetry/opentelemetry-java-instrumentation) with [different default configuration](./configuration#configuration-options)

In addition to the features listed here, see [supported technologies](./supported-technologies) for an overview of the supported technologies.

## Resource attributes

The EDOT Java agent includes the following resource attributes providers from [opentelemetry-java-contrib](https://github.com/open-telemetry/opentelemetry-java-contrib/)
- AWS: [aws-resources](https://github.com/open-telemetry/opentelemetry-java-contrib/tree/main/aws-resources) (_enabled_ by default)
- GCP: [gcp-resources](https://github.com/open-telemetry/opentelemetry-java-contrib/tree/main/gcp-resources) (_enabled_ by default)
- application server service name detection: [resource-providers](https://github.com/open-telemetry/opentelemetry-java-contrib/tree/main/resource-providers)

## Inferred spans

The EDOT Java agent includes the [Inferred Spans Extension](https://github.com/open-telemetry/opentelemetry-java-contrib/tree/main/inferred-spans)
from [opentelemetry-java-contrib](https://github.com/open-telemetry/opentelemetry-java-contrib/).

This extension provides the ability to enhance the traces by creating spans from [async-profiler](https://github.com/async-profiler/async-profiler) data without the need of explicit instrumentation of corresponding spans.

This feature is disabled by default and can be enabled by setting `OTEL_INFERRED_SPANS_ENABLED` to `true`.

See [inferred-spans](https://github.com/open-telemetry/opentelemetry-java-contrib/tree/main/inferred-spans) documentation for configuration options.

## Span stacktrace

The EDOT Java agent includes the [Span Stacktrace Extension](https://github.com/open-telemetry/opentelemetry-java-contrib/tree/main/span-stacktrace)
from [opentelemetry-java-contrib](https://github.com/open-telemetry/opentelemetry-java-contrib/).

This feature is enabled by default and allows to capture a stacktrace for spans that have a duration above a threshold.

The `OTEL_JAVA_EXPERIMENTAL_SPAN_STACKTRACE_MIN_DURATION` configuration option (defaults to `5ms`) allows to configure the minimal duration threshold, a negative value will disable the feature.

See [span-stacktrace](https://github.com/open-telemetry/opentelemetry-java-contrib/tree/main/span-stacktrace) documentation for configuration options.

## Runtime metrics

Experimental runtime metrics are _enabled_ by default.

Set `OTEL_INSTRUMENTATION_RUNTIME_TELEMETRY_EMIT_EXPERIMENTAL_TELEMETRY` to `false` to disable them.

## Metric Temporality

Elasticsearch and Kibana work best with metrics provided in delta-temporality.
Therefore, the EDOT Java changes the default value of `OTEL_EXPORTER_OTLP_METRICS_TEMPORALITY_PREFERENCE` to `DELTA`.
You can override this default if needed, note though that some provided Kibana dashboards will not work correctly in this case.

## Elastic Universal profiling integration

[Universal Profiling](https://www.elastic.co/observability/universal-profiling) integration provides the ability to correlate traces with profiling data from the Elastic universal profiler.

This feature is enabled by default on supported systems, disabled otherwise.

See [universal-profiling-integration](https://github.com/elastic/elastic-otel-java/tree/main/universal-profiling-integration) for details and configuration options.
