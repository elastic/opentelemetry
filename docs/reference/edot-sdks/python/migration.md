---
navigation_title: Migration
description: Migrate from the Elastic APM Python agent to the Elastic Distribution of OpenTelemetry Python (EDOT Python).
applies_to:
  stack:
  serverless:
    observability:
products:
  - id: cloud-serverless
  - id: observability
  - id: edot-sdk
  - id: apm-agent
---

# Migrate to EDOT Python from the Elastic APM Python agent

Learn the differences between the [Elastic APM Python agent](apm-agent-python://reference/index.md) and the {{edot}} Python (EDOT Python).

Follow the steps to migrate your instrumentation and settings. For step-by-step instructions on setting up EDOT Python refer to [Setup](./setup/index.md).

## Migration steps

Follow these steps to migrate:

1. Remove any configuration and setup code needed by Elastic APM Python Agent from your application source code.
2. Migrate any usage of Elastic APM Python Agent API to manual instrumentation with OpenTelemetry API in the application source code.
3. Follow the [setup documentation](setup/index.md) on to install and configure EDOT Python.

## Configuration mapping

The following are Elastic APM Python agent settings that you can migrate to EDOT Python.

### `api_key`

The Elastic [`api_key`](apm-agent-python://reference/configuration.md#config-api-key) option corresponds to the OpenTelemetry [OTEL_EXPORTER_OTLP_HEADERS](https://opentelemetry.io/docs/concepts/sdk-configuration/otlp-exporter-configuration/#otel_exporter_otlp_headers) option.

For example: `OTEL_EXPORTER_OTLP_HEADERS="Authorization=ApiKey an_api_key"`.

### `enabled`

The Elastic [`enabled`](apm-agent-python://reference/configuration.md#config-enabled) option corresponds to the OpenTelemetry [OTEL_SDK_DISABLED](https://opentelemetry.io/docs/specs/otel/configuration/sdk-environment-variables/#general-sdk-configuration) option.

### `environment`

The Elastic [`environment`](apm-agent-python://reference/configuration.md#config-environment) option corresponds to setting the `deployment.environment.name` key in [OTEL_RESOURCE_ATTRIBUTES](https://opentelemetry.io/docs/concepts/sdk-configuration/general-sdk-configuration/#otel_resource_attributes).

For example: `OTEL_RESOURCE_ATTRIBUTES=deployment.environment.name=testing`.

### `global_labels`

The Elastic [`global_labels`](apm-agent-python://reference/configuration.md#config-global_labels) option corresponds to adding `key=value` comma separated pairs in [OTEL_RESOURCE_ATTRIBUTES](https://opentelemetry.io/docs/concepts/sdk-configuration/general-sdk-configuration/#otel_resource_attributes).

For example: `OTEL_RESOURCE_ATTRIBUTES=alice=first,bob=second`. Such labels will result in labels.key=value attributes on the server, e.g. labels.alice=first

### `metrics_interval`

The Elastic [`metrics_interval`](apm-agent-python://reference/configuration.md#config-metrics_interval) corresponds to the OpenTelemetry [OTEL_METRIC_EXPORT_INTERVAL](https://opentelemetry.io/docs/specs/otel/configuration/sdk-environment-variables/#periodic-exporting-metricreader) option.

For example: `OTEL_METRIC_EXPORT_INTERVAL=30000`.

### `secret_token`

The Elastic [`secret_token`](apm-agent-python://reference/configuration.md#config-secret-token) option corresponds to the OpenTelemetry [OTEL_EXPORTER_OTLP_HEADERS](https://opentelemetry.io/docs/concepts/sdk-configuration/otlp-exporter-configuration/#otel_exporter_otlp_headers) option.

For example: `OTEL_EXPORTER_OTLP_HEADERS="Authorization=ApiKey an_apm_secret_token"`.

### `server_url`

The Elastic [`server_url`](apm-agent-python://reference/configuration.md#config-server-url) option corresponds to the OpenTelemetry [`OTEL_EXPORTER_OTLP_ENDPOINT`](https://opentelemetry.io/docs/concepts/sdk-configuration/otlp-exporter-configuration/#otel_exporter_otlp_endpoint) option.

### `service_name`

The Elastic [`service_name`](apm-agent-python://reference/configuration.md#config-service-name) option corresponds to the OpenTelemetry [OTEL_SERVICE_NAME](https://opentelemetry.io/docs/concepts/sdk-configuration/general-sdk-configuration/#otel_service_name) option.

You can also set the service name using [OTEL_RESOURCE_ATTRIBUTES](https://opentelemetry.io/docs/concepts/sdk-configuration/general-sdk-configuration/#otel_resource_attributes).

For example: `OTEL_RESOURCE_ATTRIBUTES=service.name=myservice`. If `OTEL_SERVICE_NAME` is set, it takes precedence over the resource attribute.

### `service_version`

The Elastic [`service_version`](apm-agent-python://reference/configuration.md#config-service-version) option corresponds to setting the `service.version` key in [OTEL_RESOURCE_ATTRIBUTES](https://opentelemetry.io/docs/concepts/sdk-configuration/general-sdk-configuration/#otel_resource_attributes).

For example: `OTEL_RESOURCE_ATTRIBUTES=service.version=1.2.3`.

## Performance overhead

Evaluate the [differences in performance overhead](./overhead.md) between EDOT Python and Elastic APM Python agent.

## Limitations

The following limitations apply when migrating to EDOT Python.

### Central and dynamic configuration

You can manage EDOT Python configurations through the [central configuration feature](docs-content://solutions/observability/apm/apm-agent-central-configuration.md) in the Applications UI.

Refer to [Central configuration](../../central-configuration.md) for more information.

### AWS Lambda

A custom lambda layer for the {{edot}} Python is not currently available. Refer to the upstream [Lambda Auto-Instrumentation](https://opentelemetry.io/docs/faas/lambda-auto-instrument/).

### Missing instrumentations

The following libraries are currently missing an OpenTelemetry equivalent:

- Azure storage and Azure queue
- `aiobotocore`
- `aiomysql`
- `aiopg`
- `aioredis`
- `Graphene`
- `httplib2`
- `pylibmc`
- `pyodbc`
- `Sanic`
- `zlib`

### Integration with structured logging

EDOT Python lacks a [structlog integration](apm-agent-python://reference/logs.md#structlog) at the moment.

### Span compression

EDOT Python does not implement [span compression](docs-content://solutions/observability/apm/spans.md#apm-spans-span-compression).

### Breakdown metrics

EDOT Python is not sending metrics that power the [Breakdown metrics](docs-content://solutions/observability/apm/metrics.md#_breakdown_metrics).