---
title: Supported Technologies
layout: default
nav_order: 4
parent: EDOT Java
---

# Technologies Supported by the EDOT Java Agent

The EDOT Java agent is a [distribution](https://opentelemetry.io/docs/concepts/distributions/) of
[OpenTelemetry Java Instrumentation](https://github.com/open-telemetry/opentelemetry-java-instrumentation) agent, it thus
inherits all the [supported (✅)](../../compatibility/nomenclature#compatibility--support-nomenclature) technologies of the OpenTelemetry Java Instrumentation:

| Category                 | Compatibility & Support Level  |
|:-------------------------|:------------------------------:|
| [JVMs]                   | ✅                             | 
| [Application Servers]    | ✅                             |
| [Libraries & Frameworks] | ✅                             |

Please note that [some supported technologies are disabled by default](https://github.com/open-telemetry/opentelemetry-java-instrumentation/blob/main/docs/supported-libraries.md#disabled-instrumentations)
and need explicit configuration to be enabled.

The EDOT Java agent also supports technologies listed here that are _not available_ in the [OpenTelemetry Java Instrumentation](https://github.com/open-telemetry/opentelemetry-java-instrumentation).

See also the [EDOT Java agent configuration](./configuration#configuration-options) for defaults that might differ from the OpenTelemetry Java Instrumentation.

## LLM instrumentations

### OpenAI Client instrumentation (tech preview)

Instrumentation for the [official OpenAI Java Client](https://github.com/openai/openai-java).

Note that this instrumentation is currently in **tech preview**, because the OpenAI client itself is still in **beta**.

It supports:

* Tracing for requests, including GenAI-specific attributes such as token usage
* Opt-In logging of OpenAI request and response content payloads

Configuration options:

| Option                                                | default                                                       | description                                                                                                                                                                                                                                                                      |
|-------------------------------------------------------|---------------------------------------------------------------|:---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `OTEL_INSTRUMENTATION_OPENAI_CLIENT_ENABLED`          | `true`                                                        | enables or disable OpenAI instrumentation                                                                                                                                                                                                                                        |
| `ELASTIC_OTEL_JAVA_INSTRUMENTATION_GENAI_EMIT_EVENTS` | value of `OTEL_INSTRUMENTATION_GENAI_CAPTURE_MESSAGE_CONTENT` | If set to `true`, the agent will generate log events for OpenAI requests and responses. Potentially sensitive content will only be included if `OTEL_INSTRUMENTATION_GENAI_CAPTURE_MESSAGE_CONTENT` is `true`                                                                    |
| `OTEL_INSTRUMENTATION_GENAI_CAPTURE_MESSAGE_CONTENT`  | `false`                                                       | If set to `true`, enables the capturing of OpenAI request and response content in the log events outputted by the agent.                                                                                                                                                       ↪ |
