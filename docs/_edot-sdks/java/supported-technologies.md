---
title: Supported Technologies
layout: default
nav_order: 4
parent: EDOT Java
---

# Technologies Supported by the EDOT Java Agent

The EDOT Java agent is a [distribution](https://opentelemetry.io/docs/concepts/distributions/) of
[OpenTelemetry Java Instrumentation](https://github.com/open-telemetry/opentelemetry-java-instrumentation) agent, it thus
inherits all the [supported technologies of the OpenTelemetry Java Instrumentation](https://github.com/open-telemetry/opentelemetry-java-instrumentation/blob/main/docs/supported-libraries.md).

Please note that [some supported technologies are disabled by default](https://github.com/open-telemetry/opentelemetry-java-instrumentation/blob/main/docs/supported-libraries.md#disabled-instrumentations)
and need explicit configuration to be enabled.

The EDOT Java agent also supports technologies listed here that are _not available_ in the [OpenTelemetry Java Instrumentation](https://github.com/open-telemetry/opentelemetry-java-instrumentation).

See also the [EDOT Java agent features](./features) for defaults that might differ from the OpenTelemetry Java Instrumentation.

## OpenAI Client instrumentation (tech preview)

Instrumentation for the [official OpenAI Java Client](https://github.com/openai/openai-java).

Note that this instrumentation is currently in **tech preview**, because the OpenAI client itself is still in **beta**.

It supports:

* Tracing for requests, including GenAI-specific attributes such as token usage
* Opt-In logging of OpenAI request and response content payloads
