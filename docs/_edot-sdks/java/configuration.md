---
title: Configuration
layout: default
nav_order: 2
parent: EDOT Java
---

# Configuring the EDOT Java Agent

The [minimal configuration](#minimal-configuration) section provides a recommended starting point for EDOT Java configuration.

See [configuration options](#configuration-options) for details on the supported configuration options and [configuration methods](#configuration-methods) for how to provide them. 

## Minimal configuration

This configuration is provided using [environment variables](#environment-variables), other [configuration methods](#configuration-methods) are also supported. 

```shell
# service name: mandatory for integration in UI and correlation
OTEL_SERVICE_NAME=my-service

# resource attributes: recommended for integration in UI and correlation, can also include service.name
OTEL_RESOURCE_ATTRIBUTES='service.version=1.0,deployment.environment.name=production'
 
# exporter endpoint: mandatory if not using a local collector accessible on http://localhost:4317
OTEL_EXPORTER_OTLP_ENDPOINT=https://my-otel-collector

# exporter authentication: mandatory if endpoint requires authentication
OTEL_EXPORTER_OTLP_HEADERS='Authorization=ApiKey mySecretApiKey'
```

For authentication, the `OTEL_EXPORTER_OTLP_HEADERS` can also be used with an APM secret token:
```shell
OTEL_EXPORTER_OTLP_HEADERS='Authorization=Bearer mySecretToken'
```

## Configuration options

EDOT Java instrumentation agent is based on OpenTelemetry Java [SDK](https://github.com/open-telemetry/opentelemetry-java) and [Instrumentation](https://github.com/open-telemetry/opentelemetry-java-instrumentation), and thus supports the following
configuration options:
- [OpenTelemetry Java instrumentation configuration options](https://opentelemetry.io/docs/zero-code/java/agent/configuration/)
- [OpenTelemetry Java SDK configuration options](https://opentelemetry.io/docs/languages/java/configuration/)

EDOT Java uses different defaults than the OpenTelemetry Java instrumentation for the following configuration options:

| Option                                                               | EDOT Java default | OpenTelemetry Java agent default                                                                                                             |
|----------------------------------------------------------------------|-------------------|----------------------------------------------------------------------------------------------------------------------------------------------|
| `OTEL_RESOURCE_PROVIDERS_AWS_ENABLED`                                | `true`            | `false` ([docs](https://opentelemetry.io/docs/zero-code/java/agent/configuration/#enable-resource-providers-that-are-disabled-by-default))   |
| `OTEL_RESOURCE_PROVIDERS_GCP_ENABLED`                                | `true`            | `false` ([docs](https://opentelemetry.io/docs/zero-code/java/agent/configuration/#enable-resource-providers-that-are-disabled-by-default))   |
| `OTEL_INSTRUMENTATION_RUNTIME-TELEMETRY_EMIT-EXPERIMENTAL-TELEMETRY` | `true`            | `false` ([docs](https://github.com/open-telemetry/opentelemetry-java-instrumentation/blob/main/instrumentation/runtime-telemetry/README.md)) |
| `OTEL_EXPORTER_OTLP_METRICS_TEMPORALITY_PREFERENCE`                  | `delta` (*)       | `cumulative` ([docs](https://opentelemetry.io/docs/specs/otel/metrics/sdk_exporters/otlp/#additional-environment-variable-configuration))    |

(*) default value set to `delta` only if not already explicitly set.

The EDOT Java instrumentation agent also provides configuration options for each of the [supported features](./features).
This table only contains minimal configuration, see each respective feature for exhaustive configuration options documentation.

| Option                                                 | Default | Feature                                                                                              |
|--------------------------------------------------------|---------|------------------------------------------------------------------------------------------------------|
| `OTEL_INFERRED_SPANS_ENABLED`                          | `false` | [Inferred spans](./features#inferred-spans)                                                          |
| `OTEL_JAVA_EXPERIMENTAL_SPAN_STACKTRACE_MIN_DURATION`  | `5ms`   | [Span stacktrace](./features#span-stacktrace)                                                        |
| `ELASTIC_OTEL_UNIVERSAL_PROFILING_INTEGRATION_ENABLED` | `auto`  | [Elastic Universal profiling integration](./features#elastic-universal-profiling-integration)        |
| `OTEL_INSTRUMENTATION_OPENAI_CLIENT_ENABLED`           | `true`  | [OpenAI client instrumentation](./supported-technologies#openai-client-instrumentation-tech-preview) |

## Configuration methods

Configuration can be provided through multiple [configuration methods](#configuration-methods):

* [Environment variables](#environment-variables)
* [System properties](#system-properties)
* [Properties configuration file](#properties-configuration-file)

Configuration options are applied with the following priorities:

- [environment variables](#system-properties) take precedence over [system properties](#system-properties) and [properties configuration file](#properties-configuration-file).
- [system properties](#system-properties) take precedence on [properties configuration file](#properties-configuration-file).

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
