---
title: Migration
layout: default
nav_order: 6
parent: EDOT Java
---

# Migrating to EDOT Java from the Elastic Java Agent
 
This documentation describes how to update applications that are currently using the [Elastic APM Java agent](https://www.elastic.co/guide/en/apm/agent/java/current/index.html) to use the Elastic Distribution of OpenTelemetry Java (EDOT Java).

## Advantages of using EDOT Java agent

### OpenTelemetry-native Data

Allows to capture, send, transform and store data in an OpenTelemetry native way. This includes for example the ability to use all features of the OpenTelemetry SDK for manual tracing, data following semantic conventions or ability to use intermediate collectors and processors.

### Broad Coverage of Instrumentation

OpenTelemetry Java Instrumentation provides a [broad coverage of libraries and frameworks](https://github.com/open-telemetry/opentelemetry-java-instrumentation/tree/main/instrumentation).

### Compatible Drop-in Replacement

EDOT Java is a fully compatible drop-in replacement for the upstream OpenTelemetry Java Agent. Hence, there's no vendor lock-in through proprietary instrumentation or agent.

## Limitations

### Supported Java Versions

EDOT Java agent and OpenTelemetry Java instrumentation are only compatible with Java 8 and later.

### Missing Instrumentations

Support for LDAP client instrumentation is not available in EDOT Java, yet.

### Central and Dynamic configuration

Currently EDOT Java does not have an equivalent of the [central configuration feature](https://www.elastic.co/guide/en/observability/current/apm-agent-configuration.html) that the Elastic APM Java agent supports. When using EDOT Java, all the configurations are static and should be provided to the application with other configurations, e.g. environment variables.

### Span compression

EDOT Java does not implement [span compression](https://www.elastic.co/guide/en/observability/current/apm-data-model-spans.html#apm-spans-span-compression).

### Breakdown metrics

EDOT Java is not sending metrics that power the [Breakdown metrics](https://www.elastic.co/guide/en/apm/guide/current/data-model-metrics.html#_breakdown_metrics).

### No remote attach

There is currently no EDOT Java equivalent for starting the agent with the [remote attach](https://www.elastic.co/guide/en/apm/agent/java/current/setup-attach-cli.html) capability. The `-javaagent:` option is the preferred startup mechanism. There is a migration path for starting the agent with [self attach](https://www.elastic.co/guide/en/apm/agent/java/current/setup-attach-api.html), which is to use [runtime attachment](https://github.com/open-telemetry/opentelemetry-java-contrib/blob/main/runtime-attach/README.md).

### Micrometer disabled by default

By default, micrometer instrumentation is disabled and won't capture metrics, enabling requires to set `otel.instrumentation.micrometer.enabled=true`.

## Migration steps

1. **Review all pros/cons of this migration guide** including the [differences in performance overhead](./overhead).
1. **(Optional) Migrate manual instrumentation API:** Usages of the [Elastic APM Agent API](https://www.elastic.co/guide/en/apm/agent/java/current/public-api.html) require migration to OpenTelemetry API:
    - for [Annotation API](https://www.elastic.co/guide/en/apm/agent/java/current/public-api.html#api-annotation) see [OpenTelemetry Annotations](https://opentelemetry.io/docs/zero-code/java/agent/annotations/).
    - for [Transaction API](https://www.elastic.co/guide/en/apm/agent/java/current/public-api.html#api-transaction) see [OpenTelemetry API](https://opentelemetry.io/docs/zero-code/java/agent/api/).

    {: .note}
    Migration of application code using these APIs and annotations is _not strictly required_ when deploying the EDOT agent. If not migrated, the spans, transactions and metrics that were previously explicitly created with those custom API calls and annotations, will no longer be generated. The broader OpenTelemetry instrumentation coverage may replace the need for some or all of these custom code changes.
1. **Replace configuration options** using the [Reference](#option-reference) below, see [Configuration](./configuration) for ways to provide those.
1. **Replace Agent binary** 
    - Remove the `-javaagent:` argument containing [Elastic APM Java agent](https://www.elastic.co/guide/en/apm/agent/java/current/index.html) from the JVM arguments
    - Add `-javaagent:` argument to the JVM arguments to use EDOT Java and restart the application or follow [Kubernetes instructions](./setup/k8s) if applicable

## Option reference

This list contains APM Java agent configuration options that can be migrated to EDOT Java agent configuration because
they have an equivalent in OpenTelemetry:

* [server_url](#server_url)
* [server_urls](#server_urls)
* [secret_token](#secret_token)
* [api_key](#api_key)
* [service_name](#service_name)
* [enabled](#enabled)
* [service_version](#service_version)
* [environment](#environment)
* [global_labels](#global_labels)
* [trace_methods](#trace_methods)

### `server_url`

The Elastic [`server_url`](https://www.elastic.co/guide/en/apm/agent/java/current/config-reporter.html#config-server-url) option corresponds to the OpenTelemetry [`OTEL_EXPORTER_OTLP_ENDPOINT`](https://opentelemetry.io/docs/concepts/sdk-configuration/otlp-exporter-configuration/#otel_exporter_otlp_endpoint) option.

### `server_urls`

The Elastic [`server_urls`](https://www.elastic.co/guide/en/apm/agent/java/current/config-reporter.html#config-server-urls) option has no equivalent OpenTelemetry option - you can only specify one endpoint.

Use [OTEL_EXPORTER_OTLP_ENDPOINT](https://opentelemetry.io/docs/concepts/sdk-configuration/otlp-exporter-configuration/#otel_exporter_otlp_endpoint) instead.

### `secret_token`

The Elastic [`secret_token`](https://www.elastic.co/guide/en/apm/agent/java/current/config-reporter.html#config-secret-token) option corresponds to the OpenTelemetry [OTEL_EXPORTER_OTLP_HEADERS](https://opentelemetry.io/docs/concepts/sdk-configuration/otlp-exporter-configuration/#otel_exporter_otlp_headers) option.

For example: `OTEL_EXPORTER_OTLP_HEADERS="Authorization=Bearer an_apm_secret_token"`.

### `api_key`

The Elastic [`api_key`](https://www.elastic.co/guide/en/apm/agent/java/current/config-reporter.html#config-api-key) option corresponds to the OpenTelemetry [OTEL_EXPORTER_OTLP_HEADERS](https://opentelemetry.io/docs/concepts/sdk-configuration/otlp-exporter-configuration/#otel_exporter_otlp_headers) option.

For example:`OTEL_EXPORTER_OTLP_HEADERS="Authorization=ApiKey an_api_key"`.

### `service_name`

The Elastic [`service_name`](https://www.elastic.co/guide/en/apm/agent/java/current/config-core.html#config-service-name) option corresponds to the OpenTelemetry [OTEL_SERVICE_NAME](https://opentelemetry.io/docs/concepts/sdk-configuration/general-sdk-configuration/#otel_service_name) option.

The service name value can also be set using [OTEL_RESOURCE_ATTRIBUTES](https://opentelemetry.io/docs/concepts/sdk-configuration/general-sdk-configuration/#otel_resource_attributes).

For example: `OTEL_RESOURCE_ATTRIBUTES=service.name=myservice`. If `OTEL_SERVICE_NAME` is set, it takes precedence over the resource attribute.

### `enabled`

The Elastic [`enabled`](https://www.elastic.co/guide/en/apm/agent/java/current/config-core.html#config-enabled) option corresponds to the OpenTelemetry [OTEL_JAVAAGENT_ENABLED](https://opentelemetry.io/docs/zero-code/java/agent/disable/) option.

### `service_version`

The Elastic [`service_version`](https://www.elastic.co/guide/en/apm/agent/java/current/config-core.html#config-service-version) option corresponds to setting the `service.version` key in [OTEL_RESOURCE_ATTRIBUTES](https://opentelemetry.io/docs/concepts/sdk-configuration/general-sdk-configuration/#otel_resource_attributes).

For example: `OTEL_RESOURCE_ATTRIBUTES=service.version=1.2.3`.

### `environment`

The Elastic [`environment`](https://www.elastic.co/guide/en/apm/agent/java/current/config-core.html#config-environment) option corresponds to setting the `deployment.environment` key in [OTEL_RESOURCE_ATTRIBUTES](https://opentelemetry.io/docs/concepts/sdk-configuration/general-sdk-configuration/#otel_resource_attributes).

For example: `OTEL_RESOURCE_ATTRIBUTES=deployment.environment=testing`.

### `global_labels`

The Elastic [`global_labels`](https://www.elastic.co/guide/en/apm/agent/java/current/config-core.html#config-global-labels) option corresponds to adding `key=value` comma separated pairs in [OTEL_RESOURCE_ATTRIBUTES](https://opentelemetry.io/docs/concepts/sdk-configuration/general-sdk-configuration/#otel_resource_attributes).

For example: `OTEL_RESOURCE_ATTRIBUTES=alice=first,bob=second`. Such labels will result in labels.key=value attributes on the server, e.g. labels.alice=first

### `trace_methods`

The Elastic [`trace_methods`] option can be replaced by the [`OTEL_INSTRUMENTATION_METHODS_INCLUDE`](https://opentelemetry.io/docs/zero-code/java/agent/annotations/#creating-spans-around-methods-with-otelinstrumentationmethodsinclude) OpenTelemetry option, however the syntax is different and the ability to use wildcards is more limited.

