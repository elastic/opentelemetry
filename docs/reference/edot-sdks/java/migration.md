---
navigation_title: Migration
description: Migrate from the Elastic APM Java agent to the Elastic Distribution of OpenTelemetry Java (EDOT Java).
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

# Migrate to EDOT Java from the Elastic APM Java agent

Compared to the Elastic APM Java agent, the Elastic Distribution of OpenTelemetry Java presents a number of advantages:

- Fully automatic instrumentation with zero code changes. No need to modify application code.
- Capture, send, transform, and store data in an OpenTelemetry native way. This includes for example the ability to use all features of the OpenTelemetry SDK for manual tracing, data following semantic conventions, or ability to use intermediate collectors and processors.
- OpenTelemetry Java Instrumentation provides a [broad coverage of libraries, frameworks, and applications](https://github.com/open-telemetry/opentelemetry-java-instrumentation/blob/main/docs/supported-libraries.md).
- EDOT Java is built on top of OpenTelemetry SDK and conventions, ensuring compatibility with community tools, vendor-neutral backends, and so on.

## Migration steps

Follow these steps to migrate from the legacy Elastic APM Java agent to the Elastic Distribution of OpenTelemetry Java.

::::::{stepper}

::::{step} (Optional) Migrate manual instrumentation API

Migrate usages of the [Elastic APM Agent API](apm-agent-java://reference/public-api.md) to OpenTelemetry API:

- For [Annotation API](apm-agent-java://reference/public-api.md#api-annotation), refer to [OpenTelemetry Annotations](https://opentelemetry.io/docs/zero-code/java/agent/annotations/).
- For [Transaction API](apm-agent-java://reference/public-api.md#api-transaction), refer to [OpenTelemetry API](https://opentelemetry.io/docs/zero-code/java/agent/api/).

:::{note}
Migration of application code using these APIs and annotations is not strictly required when deploying the EDOT agent. If not migrated, spans, transactions, and metrics that were previously created with those custom API calls and annotations will no longer be generated. OpenTelemetry instrumentation coverage might replace the need for some or all of these custom code changes.
:::
::::

::::{step} Replace configuration options
Refer to the [Configuration mapping](#configuration-mapping). Refer to [Configuration](./configuration.md) for ways to provide configuration settings.
::::

::::{step} Replace the agent binary

Remove the `-javaagent:` argument that contains the Elastic APM Java agent from the JVM arguments. Then add the `-javaagent:` argument to the JVM arguments to use EDOT Java, and restart the application or follow [Kubernetes instructions](./setup/k8s.md) or [Runtime attach instructions](./setup/runtime-attach.md) if applicable. Refer to [Setup](./setup/index.md).
::::

::::::

## Configuration mapping

The following are Elastic APM Java agent settings that you can migrate to EDOT Java.

### `server_url`

The Elastic [`server_url`](apm-agent-java://reference/config-reporter.md#config-server-url) option corresponds to the OpenTelemetry [`OTEL_EXPORTER_OTLP_ENDPOINT`](https://opentelemetry.io/docs/concepts/sdk-configuration/otlp-exporter-configuration/#otel_exporter_otlp_endpoint) option.

### `server_urls`

The Elastic [`server_urls`](apm-agent-java://reference/config-reporter.md#config-server-urls) option has no equivalent OpenTelemetry option. You can only specify one endpoint.

Use [OTEL_EXPORTER_OTLP_ENDPOINT](https://opentelemetry.io/docs/concepts/sdk-configuration/otlp-exporter-configuration/#otel_exporter_otlp_endpoint) instead.

### `secret_token`

The Elastic [`secret_token`](apm-agent-java://reference/config-reporter.md#config-secret-token) option corresponds to the OpenTelemetry [OTEL_EXPORTER_OTLP_HEADERS](https://opentelemetry.io/docs/concepts/sdk-configuration/otlp-exporter-configuration/#otel_exporter_otlp_headers) option.

For example: `OTEL_EXPORTER_OTLP_HEADERS="Authorization=Bearer an_apm_secret_token"`.

### `api_key`

The Elastic [`api_key`](apm-agent-java://reference/config-reporter.md#config-api-key) option corresponds to the OpenTelemetry [OTEL_EXPORTER_OTLP_HEADERS](https://opentelemetry.io/docs/concepts/sdk-configuration/otlp-exporter-configuration/#otel_exporter_otlp_headers) option.

For example:`OTEL_EXPORTER_OTLP_HEADERS="Authorization=ApiKey an_api_key"`.

### `service_name`

The Elastic [`service_name`](apm-agent-java://reference/config-core.md#config-service-name) option corresponds to the OpenTelemetry [OTEL_SERVICE_NAME](https://opentelemetry.io/docs/concepts/sdk-configuration/general-sdk-configuration/#otel_service_name) option.

The service name value can also be set using [OTEL_RESOURCE_ATTRIBUTES](https://opentelemetry.io/docs/concepts/sdk-configuration/general-sdk-configuration/#otel_resource_attributes).

For example: `OTEL_RESOURCE_ATTRIBUTES=service.name=myservice`. If `OTEL_SERVICE_NAME` is set, it takes precedence over the resource attribute.

### `enabled`

The Elastic [`enabled`](apm-agent-java://reference/config-core.md#config-enabled) option corresponds to the OpenTelemetry [OTEL_JAVAAGENT_ENABLED](https://opentelemetry.io/docs/zero-code/java/agent/disable/) option.

### `service_version`

The Elastic [`service_version`](apm-agent-java://reference/config-core.md#config-service-version) option corresponds to setting the `service.version` key in [OTEL_RESOURCE_ATTRIBUTES](https://opentelemetry.io/docs/concepts/sdk-configuration/general-sdk-configuration/#otel_resource_attributes).

For example: `OTEL_RESOURCE_ATTRIBUTES=service.version=1.2.3`.

### `environment`

The Elastic [`environment`](apm-agent-java://reference/config-core.md#config-environment) option corresponds to setting the `deployment.environment` key in [OTEL_RESOURCE_ATTRIBUTES](https://opentelemetry.io/docs/concepts/sdk-configuration/general-sdk-configuration/#otel_resource_attributes).

For example: `OTEL_RESOURCE_ATTRIBUTES=deployment.environment=testing`.

### `global_labels`

The Elastic [`global_labels`](apm-agent-java://reference/config-core.md#config-global-labels) option corresponds to adding `key=value` comma separated pairs in [OTEL_RESOURCE_ATTRIBUTES](https://opentelemetry.io/docs/concepts/sdk-configuration/general-sdk-configuration/#otel_resource_attributes).

For example: `OTEL_RESOURCE_ATTRIBUTES=alice=first,bob=second`. Such labels will result in labels.key=value attributes on the server, e.g. labels.alice=first

### `trace_methods`

The Elastic [`trace_methods`] option can be replaced by the [`OTEL_INSTRUMENTATION_METHODS_INCLUDE`](https://opentelemetry.io/docs/zero-code/java/agent/annotations/#creating-spans-around-methods-with-otelinstrumentationmethodsinclude) OpenTelemetry option, however the syntax is different and the ability to use wildcards is more limited.

### `capture_jmx_metrics`

The Elastic [`capture_jmx_metrics`](https://www.elastic.co/guide/en/apm/agent/java/current/config-jmx.html#config-capture-jmx-metrics) option can be replaced by 
[OpenTelemetry JMX Insight](https://github.com/open-telemetry/opentelemetry-java-instrumentation/blob/main/instrumentation/jmx-metrics/javaagent/) feature which is included in EDOT Java.

The JMX Insight feature provides the following benefits:

- Ability to define custom metrics using YAML.
- Capturing metrics with pre-defined metrics by using `OTEL_JMX_TARGET_SYSTEM` configuration option.

### `capture_headers`

Replace the Elastic `capture_headers` option with the following options:

- `otel.instrumentation.http.server.capture-request-headers` for HTTP server request
- `otel.instrumentation.http.server.capture-response-headers` for HTTP server response
- `otel.instrumentation.http.client.capture-request-headers` for HTTP client request
- `otel.instrumentation.http.client.capture-response-headers` for HTTP client response
- `otel.instrumentation.messaging.experimental.capture-headers` for messaging

The `capture_headers` option is dynamically adjustable, while the `otel.*` options are statically set by startup and cannot be subsequently adjusted.

### `span_stack_trace_min_duration`

Replace the Elastic `span_stack_trace_min_duration` option with [`OTEL_JAVA_EXPERIMENTAL_SPAN_STACKTRACE_MIN_DURATION`](./features.md#span-stacktrace).

### `disable_instrumentations`

Replace the `disable_instrumentations` option, which allows to selectively disable instrumentation (opt-out), with `OTEL_INSTRUMENTATION_<name>_ENABLED` where `<name>` is the instrumentation name.

See [OpenTelemetry documentation](https://opentelemetry.io/docs/zero-code/java/agent/disable/) for reference and values.

### `enable_instrumentations`

The `enable_instrumentations` option allows to disable all instrumentation enabled by default and selectively enable instrumentation (opt-in) can be replaced with:

- `OTEL_INSTRUMENTATION_COMMON_DEFAULT_ENABLED` = `false` to disable instrumentations enabled by default.
- `OTEL_INSTRUMENTATION_<name>_ENABLED` = `true` where `<name>` is the name of the instrumentation to enable. See [OpenTelemetry documentation](https://opentelemetry.io/docs/zero-code/java/agent/disable/) for reference and values.

### `hostname`

The Elastic [`hostname`](apm-agent-java://reference/config-core.md#config-hostname) option corresponds to setting the `host.name` key in [OTEL_RESOURCE_ATTRIBUTES](https://opentelemetry.io/docs/concepts/sdk-configuration/general-sdk-configuration/#otel_resource_attributes).

For example: `OTEL_RESOURCE_ATTRIBUTES=host.name=myhost`.

### `service_node_name`

The Elastic [`service_node_name`](apm-agent-java://reference/config-core.md#config-service-node-name) option corresponds to setting the `service.instance.id` key in [OTEL_RESOURCE_ATTRIBUTES](https://opentelemetry.io/docs/concepts/sdk-configuration/general-sdk-configuration/#otel_resource_attributes). Warning: by default this is a generated unique ID; if you set this it must be a unique value for each JVM otherwise metric views cannot be correctly aggregated nor disambiguated

For example: `OTEL_RESOURCE_ATTRIBUTES=service.instance.id=myserviceinstance001`.

### `cloud_provider`

The Elastic [`cloud_provider`](apm-agent-java://reference/config-core.md#config-cloud-provider) option corresponds to the per-provider `otel.resource.providers.{provider}.enabled` configuration options.

By default, with EDOT `otel.resource.providers.{provider}.enabled` is set to `true`, this is equivalent to the `cloud_provider` default valuem which is `auto`, or automatically detect cloud providers. Notice that this behavior differs from upstream OpenTelemetry distribution.

When the cloud provider is known, or there is none, turning off the non-relevant providers with `otel.resource.providers.{provider}.enabled = false` allows to [minimize the application startup overhead](./overhead.md#optimizing-application-startup).

## Limitations

The following limitations apply to EDOT Java.

### Supported Java versions

EDOT Java agent and OpenTelemetry Java instrumentation are only compatible with Java 8 and later.

### Missing instrumentations

Support for LDAP client instrumentation is not currently available in EDOT Java.

### Central and dynamic configuration

Currently EDOT Java does not have an equivalent of the [central configuration feature](docs-content://solutions/observability/apm/apm-agent-central-configuration.md) that the Elastic APM Java agent supports. 

When using EDOT Java, all the configurations are static and should be provided to the application with other configurations, such as environment variables.

### Span compression

EDOT Java does not implement [span compression](docs-content://solutions/observability/apm/spans.md#apm-spans-span-compression).

### Breakdown metrics

EDOT Java is not sending metrics that power the [Breakdown metrics](docs-content://solutions/observability/apm/metrics.md#_breakdown_metrics).

### No remote attach

There is currently no EDOT Java equivalent for starting the agent with the [remote attach](apm-agent-java://reference/setup-attach-cli.md) capability. The `-javaagent:` option is the preferred startup mechanism. 

A migration path is available for starting the agent with [self attach](apm-agent-java://reference/setup-attach-api.md), which is to use [runtime attachment](./setup/runtime-attach.md). Some [limitations](./setup/runtime-attach.md#limitations)
apply, and the agent must be started early during application startup.

### Micrometer turned off by default

By default, Micrometer instrumentation is inactive and doesn't capture metrics. To turn it on, use the `otel.instrumentation.micrometer.enabled=true` setting.
