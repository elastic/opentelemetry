---
title: Supported Technologies
layout: default
nav_order: 3
parent: EDOT Java
---

# Technologies Supported by the EDOT Java Agent

The EDOT Java agent is a [distribution](https://opentelemetry.io/docs/concepts/distributions/) of
[OpenTelemetry Java Instrumentation](https://github.com/open-telemetry/opentelemetry-java-instrumentation) agent, it thus
inherits all the [supported technologies of the OpenTelemetry Java Instrumentation](https://github.com/open-telemetry/opentelemetry-java-instrumentation/blob/main/docs/supported-libraries.md).

Please note that [some supported technologies are disabled by default](https://github.com/open-telemetry/opentelemetry-java-instrumentation/blob/main/docs/supported-libraries.md#disabled-instrumentations)
and need explicit configuration to be enabled.

The EDOT Java agent also provides exclusive features that are _not available_ in the [OpenTelemetry Java Instrumentation](https://github.com/open-telemetry/opentelemetry-java-instrumentation)
or are provided but with different default configuration.

## Resource attributes

The EDOT Java agent includes the following resource attributes providers from [opentelemetry-java-contrib](https://github.com/open-telemetry/opentelemetry-java-contrib/)
- AWS: [aws-resources](https://github.com/open-telemetry/opentelemetry-java-contrib/tree/main/aws-resources) (_enabled_ by default)
- GCP: [gcp-resources](https://github.com/open-telemetry/opentelemetry-java-contrib/tree/main/gcp-resources) (_enabled_ by default)
- application server service name detection: [resource-providers](https://github.com/open-telemetry/opentelemetry-java-contrib/tree/main/resource-providers)

## Inferred spans

The EDOT Java agent includes the [Inferred Spans Extension](https://github.com/open-telemetry/opentelemetry-java-contrib/tree/main/inferred-spans)
from [opentelemetry-java-contrib](https://github.com/open-telemetry/opentelemetry-java-contrib/).

This extension provides the ability to enhance the traces by creating spans from [async-profiler](https://github.com/async-profiler/async-profiler) data.

This feature is disabled by default and can be enabled by setting `OTEL_INFERRED_SPANS_ENABLED` to `true`.

See [inferred-spans](https://github.com/open-telemetry/opentelemetry-java-contrib/tree/main/inferred-spans) documentation for configuration options.

## Span stacktrace

The EDOT Java agent includes the [Span Stacktrace Extension](https://github.com/open-telemetry/opentelemetry-java-contrib/tree/main/span-stacktrace)
from [opentelemetry-java-contrib](https://github.com/open-telemetry/opentelemetry-java-contrib/).

This feature is enabled by default and allows to capture a stacktrace for spans that have a duration above a threshold (default 5ms).

See [span-stacktrace](https://github.com/open-telemetry/opentelemetry-java-contrib/tree/main/span-stacktrace) documentation for configuration options.

## Runtime metrics

Experimental runtime metrics are _enabled_ by default.

Set `otel.instrumentation.runtime-telemetry.emit-experimental-telemetry` to `false` to disable them.

## OpenAI Client instrumentation (tech preview)

Instrumentation for the [official OpenAI Java Client](https://github.com/openai/openai-java).

Note that this instrumentation is currently in **tech preview**, because the OpenAI client itself is still in **beta**.

It supports:

* Tracing for requests, including GenAI-specific attributes such as token usage
* Opt-In logging of OpenAI request and response content payloads

## Elastic Universal profiling integration

Universal profiling integration provides the ability to correlate traces with profiling data from the Elastic universal profiler.

This feature is enabled by default on supported systems, disabled otherwise.

See [universal-profiling-integration](https://github.com/elastic/elastic-otel-java/tree/main/universal-profiling-integration) for details and configuration options.