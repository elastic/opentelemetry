---
title: Migration
layout: default
nav_order: 6
parent: EDOT Java
---

# Migrating to EDOT Java from the Elastic Java Agent
 
This documentation describes how to update applications using the [Elastic APM Java agent](https://www.elastic.co/guide/en/apm/agent/java/current/index.html) to use the Elastic Distribution of OpenTelemetry Java (EDOT Java).

## Advantages of using EDOT Java agent

TODO

## Limitations

TODO

## Migration steps

- remove the `-javaagent:` argument containing [Elastic APM Java agent]([Elastic APM Java agent](https://www.elastic.co/guide/en/apm/agent/java/current/index.html) from the JVM arguments
- replace configuration options using [reference](#option-reference) below, see [configuration](./configuration) for ways to provide those.
- add `-javaagent:` argument to the JVM arguments to use EDOT Java agent.

## Option reference

This list contains APM Java agent configuration options that can be migrated to EDOT Java agent configuration.

* [server_url](#server_url)
* [server_urls](#server_urls)
* [secret_token](#secret_token)
* [api_key](#api_key)
* [service_name](#service_name)
* [enabled](#enabled)
* [service_version](#service_version)
* [environment](#environment)
* [global_labels](#global_labels)

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

The Elastic [`enabled`](https://www.elastic.co/guide/en/apm/agent/java/current/config-core.html#config-enabled) option corresponds to the OpenTelemetry [OTEL_JAVAAGENT_ENABLED](https://opentelemetry.io/docs/languages/java/automatic/agent-config/#suppressing-specific-auto-instrumentation) option.

### `service_version`

The Elastic [`service_version`](https://www.elastic.co/guide/en/apm/agent/java/current/config-core.html#config-service-version) option corresponds to setting the `service.version` key in [OTEL_RESOURCE_ATTRIBUTES](https://opentelemetry.io/docs/concepts/sdk-configuration/general-sdk-configuration/#otel_resource_attributes).

For example: `OTEL_RESOURCE_ATTRIBUTES=service.version=1.2.3`.

### `environment`

The Elastic [`environment`](https://www.elastic.co/guide/en/apm/agent/java/current/config-core.html#config-environment) option corresponds to setting the `deployment.environment` key in [OTEL_RESOURCE_ATTRIBUTES](https://opentelemetry.io/docs/concepts/sdk-configuration/general-sdk-configuration/#otel_resource_attributes).

For example: `OTEL_RESOURCE_ATTRIBUTES=deployment.environment=testing`.

### `global_labels`

The Elastic [`global_labels`](https://www.elastic.co/guide/en/apm/agent/java/current/config-core.html#config-global-labels) option corresponds to adding `key=value` comma separated pairs in [OTEL_RESOURCE_ATTRIBUTES](https://opentelemetry.io/docs/concepts/sdk-configuration/general-sdk-configuration/#otel_resource_attributes).

For example: `OTEL_RESOURCE_ATTRIBUTES=alice=first,bob=second`. Such labels will result in labels.key=value attributes on the server, e.g. labels.alice=first

