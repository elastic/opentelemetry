---
navigation_title: Configuration
description: Learn how to configure the Elastic Distribution of OpenTelemetry (EDOT) Java Agent, including minimal setup, configuration options, and methods like environment variables and system properties.
applies_to:
  stack:
  serverless:
    observability:
  product:
    edot_java: ga
products:
  - id: cloud-serverless
  - id: observability
  - id: edot-sdk
---

# Configure the EDOT Java agent

The [minimal configuration](#minimal-configuration) section provides a recommended starting point for EDOT Java configuration.

See [configuration options](#configuration-options) for details on the supported configuration options and [configuration methods](#configuration-methods) for how to provide them.

:::{note} 
[Declarative configuration](https://opentelemetry.io/docs/specs/otel/configuration/sdk-environment-variables/#declarative-configuration) is not supported. Using it deactivates many agent features.
:::

## Minimal configuration

This configuration is provided using [environment variables](#environment-variables), other [configuration methods](#configuration-methods) are also supported.

```sh
# service name: mandatory for integration in UI and correlation
OTEL_SERVICE_NAME=my-service

# resource attributes: recommended for integration in UI and correlation, can also include service.name
OTEL_RESOURCE_ATTRIBUTES='service.version=1.0,deployment.environment.name=production'

# exporter endpoint: mandatory if not using a local Collector accessible on http://localhost:4317
OTEL_EXPORTER_OTLP_ENDPOINT=https://my-otel-collector

# exporter authentication: mandatory if endpoint requires authentication
OTEL_EXPORTER_OTLP_HEADERS='Authorization=ApiKey mySecretApiKey'
```

For authentication, the `OTEL_EXPORTER_OTLP_HEADERS` can also be used with an APM secret token:
```sh
OTEL_EXPORTER_OTLP_HEADERS='Authorization=Bearer mySecretToken'
```

## Configuration options

EDOT Java instrumentation agent is based on OpenTelemetry Java [SDK](https://github.com/open-telemetry/opentelemetry-java) and [Instrumentation](https://github.com/open-telemetry/opentelemetry-java-instrumentation), and thus supports the following
configuration options:
- [OpenTelemetry Java instrumentation configuration options](https://opentelemetry.io/docs/zero-code/java/agent/configuration/)
- [OpenTelemetry Java SDK configuration options](https://opentelemetry.io/docs/languages/java/configuration/)

EDOT Java uses different defaults than the OpenTelemetry Java instrumentation for the following configuration options:

| Option                                                               | EDOT Java default | OpenTelemetry Java agent default                                                                                                             | EDOT Java version |
|----------------------------------------------------------------------|-------------------|----------------------------------------------------------------------------------------------------------------------------------------------|-------------------|
| `OTEL_RESOURCE_PROVIDERS_AWS_ENABLED`                                | `true`            | `false` ([docs](https://opentelemetry.io/docs/zero-code/java/agent/configuration/#enable-resource-providers-that-are-disabled-by-default))   | 1.0.0+            |
| `OTEL_RESOURCE_PROVIDERS_GCP_ENABLED`                                | `true`            | `false` ([docs](https://opentelemetry.io/docs/zero-code/java/agent/configuration/#enable-resource-providers-that-are-disabled-by-default))   | 1.0.0+            |
| `OTEL_RESOURCE_PROVIDERS_AZURE_ENABLED`                              | `true`            | `false` ([docs](https://opentelemetry.io/docs/zero-code/java/agent/configuration/#enable-resource-providers-that-are-disabled-by-default))   | 1.4.0+            |
| `OTEL_INSTRUMENTATION_RUNTIME-TELEMETRY_EMIT-EXPERIMENTAL-TELEMETRY` | `true`            | `false` ([docs](https://github.com/open-telemetry/opentelemetry-java-instrumentation/blob/main/instrumentation/runtime-telemetry/README.md)) | 1.4.0+            |
| `OTEL_EXPORTER_OTLP_METRICS_TEMPORALITY_PREFERENCE`                  | `delta` (*)       | `cumulative` ([docs](https://opentelemetry.io/docs/specs/otel/metrics/sdk_exporters/otlp/#additional-environment-variable-configuration))    | 1.0.0+            |

(*) default value set to `delta` only if not already explicitly set.

The EDOT Java instrumentation agent also provides configuration options for each of the [supported features](/reference/edot-sdks/java/features.md).
This table only contains minimal configuration, see each respective feature for exhaustive configuration options documentation.

| Option                                                 | Default | Feature                                                                                                                  | EDOT Java version |
|--------------------------------------------------------|---------|--------------------------------------------------------------------------------------------------------------------------|-------------------|
| `OTEL_INFERRED_SPANS_ENABLED`                          | `false` | [Inferred spans](/reference/edot-sdks/java/features.md#inferred-spans)                                                   | 1.0.0+            |
| `OTEL_JAVA_EXPERIMENTAL_SPAN_STACKTRACE_MIN_DURATION`  | `5ms`   | [Span stacktrace](/reference/edot-sdks/java/features.md#span-stacktrace)                                                 | 1.0.0+            |
| `ELASTIC_OTEL_UNIVERSAL_PROFILING_INTEGRATION_ENABLED` | `auto`  | [Elastic Universal profiling integration](/reference/edot-sdks/java/features.md#elastic-universal-profiling-integration) | 1.0.0+            |
| `OTEL_INSTRUMENTATION_OPENAI_CLIENT_ENABLED`           | `true`  | [OpenAI client instrumentation](/reference/edot-sdks/java/supported-technologies.md#openai-client-instrumentation)       | 1.4.0+            |
| `ELASTIC_OTEL_JAVAAGENT_LOG_LEVEL`                     | `INFO`  | [Agent logging](#agent-logging)                                                                                          | 1.5.0+            |
| `ELASTIC_OTEL_VERIFY_SERVER_CERT`                      | `true`  | [Exporter certificate verification](#exporter-certificate-verification)                                                  | 1.5.0+            |

## OpenAI Client settings

The following settings are available:

| Option                                                | default                                                       | description                                                                                                                                                                                                                                                                      |
|-------------------------------------------------------|---------------------------------------------------------------|:---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `OTEL_INSTRUMENTATION_OPENAI_CLIENT_ENABLED`          | `true`                                                        | enables or disable OpenAI instrumentation                                                                                                                                                                                                                                        |
| `ELASTIC_OTEL_JAVA_INSTRUMENTATION_GENAI_EMIT_EVENTS` | value of `OTEL_INSTRUMENTATION_GENAI_CAPTURE_MESSAGE_CONTENT` | If set to `true`, the agent will generate log events for OpenAI requests and responses. Potentially sensitive content will only be included if `OTEL_INSTRUMENTATION_GENAI_CAPTURE_MESSAGE_CONTENT` is `true`                                                                    |
| `OTEL_INSTRUMENTATION_GENAI_CAPTURE_MESSAGE_CONTENT`  | `false`                                                       | If set to `true`, enables the capturing of OpenAI request and response content in the log events outputted by the agent.                                                                                                                                                       ↪ |


## Configuration methods

Configuration can be provided through multiple [configuration methods](#configuration-methods):

* [Environment variables](#environment-variables)
* [System properties](#system-properties)
* [Properties configuration file](#properties-configuration-file)

Configuration options are applied with the following priorities:

- [environment variables](#system-properties) take precedence over [system properties](#system-properties) and [properties configuration file](#properties-configuration-file).
- [system properties](#system-properties) take precedence on [properties configuration file](#properties-configuration-file).

:::{important}
[Declarative configuration](https://opentelemetry.io/docs/specs/otel/configuration/#declarative-configuration) is not supported.
:::

### Environment variables

Environment variables provide a cross-platform way to configure EDOT Java and is especially useful in containerized environments.

Define environment variables before starting the JVM:

```sh
export OTEL_SERVICE_NAME=my-service
java ...
```

### System properties

These configuration options can be seen by anything that can see the executed command-line.

Define system properties at the JVM start, usually on the command-line:

```sh
java -Dotel.service.name=my-service ...
```

When modifying the JVM command line options is not possible, using the `JAVA_TOOL_OPTIONS` environment variable could
be used to provide the system properties, for example:

```sh
export JAVA_TOOL_OPTIONS='-Dotel.service.name=my-service'
```

### Properties configuration file

EDOT Java can be configured using a java properties configuration file.

Before starting the JVM, create and populate the configuration file and specify where to find it:

```sh
echo otel.service.name=my-service > my.properties
java -Dotel.javaagent.configuration-file=my.properties ...
```

## Agent logging

The EDOT Java agent provides the ability to control the agent log verbosity by setting the log level with the `ELASTIC_OTEL_JAVAAGENT_LOG_LEVEL` configuration option (`INFO` by default).

The following log levels are supported: `TRACE`, `DEBUG`, `INFO`, `WARN`, `ERROR`, `FATAL` and `OFF`.

For [troubleshooting](docs-content://troubleshoot/ingest/opentelemetry/edot-sdks/java/index.md#agent-debug-logging), the `ELASTIC_OTEL_JAVAAGENT_LOG_LEVEL=DEBUG` is a recommended alternative to `OTEL_JAVAAGENT_DEBUG=true` as it provides span information in JSON format.

This feature relies on the `OTEL_JAVAAGENT_LOGGING` configuration option to be set to `elastic` (default), the `simple` value from upstream is not supported.

Setting `OTEL_JAVAAGENT_LOGGING=none` or `ELASTIC_OTEL_JAVAAGENT_LOG_LEVEL=OFF` disables agent logging feature.

Setting `OTEL_JAVAAGENT_LOGGING=application` will disable EDOT agent logging feature and attempt to use the application logger.
As [documented here in the upstream documentation](https://opentelemetry.io/docs/zero-code/java/agent/configuration/#java-agent-logging-output),
support for this depends on the application and logging libraries used.

## Exporter certificate verification

The EDOT Java agent provides the ability to toggle the exporter endpoint certificate verification with the `ELASTIC_OTEL_VERIFY_SERVER_CERT` configuration option (`true` by default).

When the endpoint certificate is not trusted by the JVM where the agent runs, the common symptom is security-related exceptions with the following message: `unable to find valid certification path to requested target`.

This is common in the following scenarios:
- When endpoint uses a self-signed certificate not trusted by the JVM
- When the certificate authority used by the endpoint certificate is not trusted by the JVM

One solution is to add the certificate or certificate authority to the JVM trust store, which requires modifying the JVM trust store.

If trust store modification is not possible or not practical, for example when troubleshooting or working with a local deployment, certificate verification can be disabled by setting `ELASTIC_OTEL_VERIFY_SERVER_CERT` to `false`. This however need to be evaluated carefully as it lowers the communication security and could allow for man-in-the-middle attacks where the data could be intercepted between the agent and the collector endpoint.