---
navigation_title: Supported Technologies
description: Overview of technologies supported by the Elastic Distribution of OpenTelemetry (EDOT) Java Agent, including JVM versions, application servers, frameworks, and LLM instrumentations.
applies_to:
  stack:
  serverless:
    observability:
products:
  - id: cloud-serverless
  - id: observability
  - id: edot-java
---
# Technologies Supported by the EDOT Java Agent

The EDOT Java agent is a [distribution](https://opentelemetry.io/docs/concepts/distributions/) of
[OpenTelemetry Java Instrumentation](https://github.com/open-telemetry/opentelemetry-java-instrumentation) agent, it thus
inherits all the [supported (✅)](../../compatibility/nomenclature.md) technologies of the OpenTelemetry Java Instrumentation.

## EDOT Collector / Elastic Stack versions

The EDOT Java agent sends data via the OpenTelemetry protocol (OTLP). While OTLP ingest works with later 8.16+ versions of the EDOT Collector, for full support it is strongly recommended that you use either [EDOT Collector](../../edot-collector/index.md) versions 9.x or [Elastic Cloud Serverless](https://www.elastic.co/guide/en/serverless/current/intro.html) for OTLP ingest.

See [EDOT SDKs compatibility](../../compatibility/sdks.md) for support details.

:::{note}
> Ingesting data from EDOT SDKs through EDOT Collector 9.x into Elastic Stack versions 8.18+ *is supported*.
:::

## JVM Versions

The EDOT Java agent supports **JVM (OpenJDK, OpenJ9) versions 8+**
This follows from the [OpenTelemetry supported JMVs](https://github.com/open-telemetry/opentelemetry-java-instrumentation/blob/main/docs/supported-libraries.md#jvms-and-operating-systems).

## Application Servers

The EDOT Java agent supports [all the application servers documented by the OpenTelemetry Java agent](https://github.com/open-telemetry/opentelemetry-java-instrumentation/blob/main/docs/supported-libraries.md#application-servers).

## Libraries & Frameworks Instrumentations

The EDOT Java agent supports [all the libraries and frameworks documented by the OpenTelemetry Java agent](https://github.com/open-telemetry/opentelemetry-java-instrumentation/blob/main/docs/supported-libraries.md#libraries--frameworks).

Please note that [some supported technologies are disabled by default](https://github.com/open-telemetry/opentelemetry-java-instrumentation/blob/main/docs/supported-libraries.md#disabled-instrumentations)
and need explicit configuration to be enabled.

The EDOT Java agent also supports technologies listed here that are _not available_ in the [OpenTelemetry Java Instrumentation](https://github.com/open-telemetry/opentelemetry-java-instrumentation).

See also the [EDOT Java agent configuration](./configuration.md#configuration-options) for defaults that might differ from the OpenTelemetry Java Instrumentation.

## LLM instrumentations

### OpenAI Client instrumentation

Instrumentation for the [official OpenAI Java Client](https://github.com/openai/openai-java).
The minimum supported OpenAI Java Client version is 1.1.0.

This instrumentation supports:

* Tracing for requests, including GenAI-specific attributes such as token usage
* Opt-In logging of OpenAI request and response content payloads

Configuration options:

| Option                                                | default                                                       | description                                                                                                                                                                                                                                                                      |
|-------------------------------------------------------|---------------------------------------------------------------|:---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `OTEL_INSTRUMENTATION_OPENAI_CLIENT_ENABLED`          | `true`                                                        | enables or disable OpenAI instrumentation                                                                                                                                                                                                                                        |
| `ELASTIC_OTEL_JAVA_INSTRUMENTATION_GENAI_EMIT_EVENTS` | value of `OTEL_INSTRUMENTATION_GENAI_CAPTURE_MESSAGE_CONTENT` | If set to `true`, the agent will generate log events for OpenAI requests and responses. Potentially sensitive content will only be included if `OTEL_INSTRUMENTATION_GENAI_CAPTURE_MESSAGE_CONTENT` is `true`                                                                    |
| `OTEL_INSTRUMENTATION_GENAI_CAPTURE_MESSAGE_CONTENT`  | `false`                                                       | If set to `true`, enables the capturing of OpenAI request and response content in the log events outputted by the agent.                                                                                                                                                       ↪ |
