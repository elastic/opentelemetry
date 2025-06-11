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
  - id: edot-sdk
---

# Technologies supported by the EDOT Java Agent

The EDOT Java agent is a [distribution](https://opentelemetry.io/docs/concepts/distributions/) of [OpenTelemetry Java Instrumentation](https://github.com/open-telemetry/opentelemetry-java-instrumentation) agent. It inherits all the [supported](../../compatibility/nomenclature.md) technologies of the OpenTelemetry Java Instrumentation.

## EDOT Collector and Elastic Stack versions

The EDOT Java agent sends data through the OpenTelemetry protocol (OTLP). While OTLP ingest works with later 8.16+ versions of the EDOT Collector, for full support use either [EDOT Collector](../../edot-collector/index.md) versions 9.x or [{{serverless-full}}](docs-content://deploy-manage/deploy/elastic-cloud/serverless.md) for OTLP ingest.

Refer to [EDOT SDKs compatibility](../../compatibility/sdks.md) for support details.

:::{note}
Ingesting data from EDOT SDKs through EDOT Collector 9.x into Elastic Stack versions 8.18+ is supported.
:::

## JVM versions

The EDOT Java agent supports JVM (OpenJDK, OpenJ9) versions 8+. This follows from the [OpenTelemetry supported JMVs](https://github.com/open-telemetry/opentelemetry-java-instrumentation/blob/main/docs/supported-libraries.md#jvms-and-operating-systems).

## Application servers

The EDOT Java agent supports [all the application servers documented by the OpenTelemetry Java agent](https://github.com/open-telemetry/opentelemetry-java-instrumentation/blob/main/docs/supported-libraries.md#application-servers).

## Libraries and Frameworks instrumentations

The EDOT Java agent supports [all the libraries and frameworks documented by the OpenTelemetry Java agent](https://github.com/open-telemetry/opentelemetry-java-instrumentation/blob/main/docs/supported-libraries.md#libraries--frameworks).

Note that [some supported technologies are deactivated by default](https://github.com/open-telemetry/opentelemetry-java-instrumentation/blob/main/docs/supported-libraries.md#disabled-instrumentations) and need explicit configuration to be activated.

The EDOT Java agent also supports technologies listed here that are not available in the [OpenTelemetry Java Instrumentation](https://github.com/open-telemetry/opentelemetry-java-instrumentation).

Refer to the [EDOT Java agent configuration](./configuration.md#configuration-options) for defaults that might differ from the OpenTelemetry Java Instrumentation.

## OpenAI Client instrumentation

The minimum supported version of the OpenAI Java Client is 1.1.0. This instrumentation supports:

* Tracing for requests, including GenAI-specific attributes such as token usage.
* Opt-in logging of OpenAI request and response content payloads.
