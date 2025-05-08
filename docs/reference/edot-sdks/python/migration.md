---
navigation_title: Migration
description: Migrate from the Elastic APM Python agent to the Elastic Distribution of OpenTelemetry Python (EDOT Python).
applies_to:
  stack:
  serverless:
    observability:
products:
  - cloud-serverless
  - observability
  - edot-python
  - apm-python-agent
---

# Migrating to EDOT Python from the Elastic APM Python Agent

This guide will highlight the major differences between the [Elastic APM Python agent](https://www.elastic.co/guide/en/apm/agent/python/current/getting-started.html) and the Elastic Distribution of OpenTelemetry Python (EDOT Python).

For step-by-step instructions on setting up EDOT Python refer to [Setup](./setup/index.md).

## We are a distribution

As a distribution of OpenTelemetry, EDOT Python follows certain standards, but there is still some space for innovation.

## EDOT Python principles

### Bold on auto-instrumentation

We have chosen to make auto-instrumentation as simple as possible so you can just focus on your code; we favored an experience that requires minimal changes to your application code. The upstream OpenTelemetry configuration has more options than the distribution requires. Our default configuration is listed [here](https://github.com/elastic/elastic-otel-python?tab=readme-ov-file#configuration).

### Bring your own instrumentation

In EDOT Python we decided to not ship all the available instrumentations in order to accommodate environments where installing more packages than requested may be an issue.
We provide a tool to discover available instrumentations automatically that can be added to your build workflow. See the [Setup](./setup/index#install-the-available-instrumentation).

## Performance overhead

Evaluate the [differences in performance overhead](./overhead) between EDOT Python and Elastic APM Python agent.

## Limitations

### Central and Dynamic configuration

Currently EDOT Python does not have an equivalent of the [central configuration feature](https://www.elastic.co/guide/en/observability/current/apm-agent-configuration.html) that the Elastic APM Python agent supports. When using EDOT Python, all the configurations are static and should be provided to the application with other configurations, e.g. environment variables.

### AWS lambda

At the moment, we are not building a custom lambda layer for our Python distribution. You can refer to the upstream [Lambda Auto-Instrumentation](https://opentelemetry.io/docs/faas/lambda-auto-instrument/).

### Missing instrumentations

Not all instrumentations we have in Elastic APM Python Agent have an OpenTelemetry counterpart. But we may port them if they are requested by users.

At the time of writing these docs, the following libraries are missing an OpenTelemetry instrumentation:
- aiobotocore
- aiomysql
- aiopg
- aioredis
- Azure storage and Azure queue
- Graphene
- httplib2
- pylibmc
- pyodbc
- Sanic
- zlib

### Integration with structured logging

EDOT Python does not have any [structlog integration](https://www.elastic.co/guide/en/apm/agent/python/current/logs.html#structlog) at the moment.

### Span compression

EDOT Python does not implement [span compression](https://www.elastic.co/guide/en/observability/current/apm-data-model-spans.html#apm-spans-span-compression).

### Breakdown metrics

EDOT Python is not sending metrics that power the [Breakdown metrics](https://www.elastic.co/guide/en/apm/guide/current/data-model-metrics.html#_breakdown_metrics).

## Migration steps

- remove any configuration and setup code needed by Elastic APM Python Agent from your application source code.
- migrate any eventual usage of Elastic APM Python Agent API for manual instrumentation with OpenTelemetry API in the application source code.
- follow [setup documentation](setup/index.md) on how to install and configure EDOT Python

## Option reference

This list contains Elastic APM Python agent configuration options that can be migrated to EDOT Python configuration because they have an equivalent in OpenTelemetry:

<!-- keep these sorted -->
* [api_key](#api_key)
* [enabled](#enabled)
* [environment](#environment)
* [global_labels](#global_labels)
* [metrics_interval](#metrics_interval)
* [secret_token](#secret_token)
* [server_url](#server_url)
* [service_name](#service_name)
* [service_version](#service_version)

### `api_key`

The Elastic [`api_key`](https://www.elastic.co/guide/en/apm/agent/python/current/configuration.html#config-api-key) option corresponds to the OpenTelemetry [OTEL_EXPORTER_OTLP_HEADERS](https://opentelemetry.io/docs/concepts/sdk-configuration/otlp-exporter-configuration/#otel_exporter_otlp_headers) option.

For example:`OTEL_EXPORTER_OTLP_HEADERS="Authorization=ApiKey an_api_key"`.

### `enabled`

The Elastic [`enabled`](https://www.elastic.co/guide/en/apm/agent/python/current/configuration.html#config-enabled) option corresponds to the OpenTelemetry [OTEL_SDK_DISABLED](https://opentelemetry.io/docs/specs/otel/configuration/sdk-environment-variables/#general-sdk-configuration) option.

### `environment`

The Elastic [`environment`](https://www.elastic.co/guide/en/apm/agent/python/current/configuration.html#config-environment) option corresponds to setting the `deployment.environment.name` key in [OTEL_RESOURCE_ATTRIBUTES](https://opentelemetry.io/docs/concepts/sdk-configuration/general-sdk-configuration/#otel_resource_attributes).

For example: `OTEL_RESOURCE_ATTRIBUTES=deployment.environment.name=testing`.

### `global_labels`

The Elastic [`global_labels`](https://www.elastic.co/guide/en/apm/agent/python/current/configuration.html#config-global_labels) option corresponds to adding `key=value` comma separated pairs in [OTEL_RESOURCE_ATTRIBUTES](https://opentelemetry.io/docs/concepts/sdk-configuration/general-sdk-configuration/#otel_resource_attributes).

For example: `OTEL_RESOURCE_ATTRIBUTES=alice=first,bob=second`. Such labels will result in labels.key=value attributes on the server, e.g. labels.alice=first

### `metrics_interval`

The Elastic [`metrics_interval`](https://www.elastic.co/guide/en/apm/agent/python/current/configuration.html#config-metrics_interval) corresponds to the OpenTelemetry [OTEL_METRIC_EXPORT_INTERVAL](https://opentelemetry.io/docs/specs/otel/configuration/sdk-environment-variables/#periodic-exporting-metricreader) option.

For example: `OTEL_METRIC_EXPORT_INTERVAL=30000`.

### `secret_token`

The Elastic [`secret_token`](https://www.elastic.co/guide/en/apm/agent/python/current/configuration.html#config-secret-token) option corresponds to the OpenTelemetry [OTEL_EXPORTER_OTLP_HEADERS](https://opentelemetry.io/docs/concepts/sdk-configuration/otlp-exporter-configuration/#otel_exporter_otlp_headers) option.

For example: `OTEL_EXPORTER_OTLP_HEADERS="Authorization=ApiKey an_apm_secret_token"`.

### `server_url`

The Elastic [`server_url`](https://www.elastic.co/guide/en/apm/agent/python/current/configuration.html#config-server-url) option corresponds to the OpenTelemetry [`OTEL_EXPORTER_OTLP_ENDPOINT`](https://opentelemetry.io/docs/concepts/sdk-configuration/otlp-exporter-configuration/#otel_exporter_otlp_endpoint) option.

### `service_name`

The Elastic [`service_name`](https://www.elastic.co/guide/en/apm/agent/python/current/configuration.html#config-service-name) option corresponds to the OpenTelemetry [OTEL_SERVICE_NAME](https://opentelemetry.io/docs/concepts/sdk-configuration/general-sdk-configuration/#otel_service_name) option.

The service name value can also be set using [OTEL_RESOURCE_ATTRIBUTES](https://opentelemetry.io/docs/concepts/sdk-configuration/general-sdk-configuration/#otel_resource_attributes).

For example: `OTEL_RESOURCE_ATTRIBUTES=service.name=myservice`. If `OTEL_SERVICE_NAME` is set, it takes precedence over the resource attribute.

### `service_version`

The Elastic [`service_version`](https://www.elastic.co/guide/en/apm/agent/python/current/configuration.html#config-service-version) option corresponds to setting the `service.version` key in [OTEL_RESOURCE_ATTRIBUTES](https://opentelemetry.io/docs/concepts/sdk-configuration/general-sdk-configuration/#otel_resource_attributes).

For example: `OTEL_RESOURCE_ATTRIBUTES=service.version=1.2.3`.
