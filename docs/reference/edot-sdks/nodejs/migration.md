---
navigation_title: Migration
description: Migrate from the Elastic APM Node.js agent to the Elastic Distribution of OpenTelemetry for Node.js (EDOT Node.js).
applies_to:
  stack:
  serverless:
    observability:
  product:
    edot_node: ga
products:
  - id: cloud-serverless
  - id: observability
  - id: edot-sdk
  - id: apm-agent
---

# Migrate to EDOT Node.js from the Elastic APM Node.js agent

Compared to the Elastic APM Node.js agent, the {{edot}} Node.js presents a number of advantages:

- Fully automatic instrumentation with zero code changes. No need to modify application code.
- EDOT Node.js is built on top of OpenTelemetry SDK and conventions, ensuring compatibility with community tools, vendor-neutral backends, and so on.
- Modular, extensible architecture based on the OpenTelemetry SDK. You can add custom exporters, processors, and samplers.
- You can use EDOT Node.js in environments where both tracing and metrics are collected using OpenTelemetry.


## Migration steps

Follow these steps to migrate from the legacy Elastic APM PHP agent (`elastic-apm-node`) to the {{edot}} PHP (`@elastic/opentelemetry-node`).

::::::{stepper}

::::{step} Replace the Node.js package

Remove the Elastic APM Node.js Agent package and install EDOT Node.js:

```sh
npm uninstall elastic-apm-node
npm install --save @elastic/opentelemetry-node
```

::::

::::{step} Remove APM Node.js start method

For services starting the APM Node.js Agent by using `require()` with the [require and start](apm-agent-nodejs://reference/starting-agent.md#start-option-require-and-start) or [require start module](apm-agent-nodejs://reference/starting-agent.md#start-option-require-start-module) methods, the `require('elastic-apm-node')`, remove the code.

For services starting with the [`--require` Node.js CLI option](apm-agent-nodejs://reference/starting-agent.md#start-option-node-require-opt), remove the option. If the `--require` option is defined in `NODE_OPTIONS` environment variable, remove it there.

::::

::::{step} (Optional) Migrate manual instrumentation API
If you're using the [Elastic APM Node.js Agent API](apm-agent-nodejs://reference/api.md) to create manual transactions and spans you should refactor the code to use `@opentelemetry/api` methods. OpenTelemetry documentation has several examples of how to [create spans](https://opentelemetry.io/docs/languages/js/instrumentation/#create-spans) manually.
::::

::::{step} Replace configuration options
Refer to the [Configuration mapping](#configuration-mapping). Refer to [Configuration](/reference/edot-sdks/nodejs/configuration.md) for details on EDOT Node.js configuration.
::::

::::{step} Add EDOT Node.js start method

Use the [Node.js `--import` option](https://nodejs.org/api/cli.html#--importmodule) to start EDOT Node.js with your service.

Set it on the command-line using `node --import @elastic/opentelemetry-node service.js` or in the [`NODE_OPTIONS` environment variable](https://nodejs.org/api/cli.html#node_optionsoptions): `NODE_OPTIONS="--import @elastic/opentelemetry-node" node service.js`.
::::

::::::

## Configuration mapping

This list contains Elastic APM Node.js agent configuration options that can be migrated to EDOT Node.js SDK configuration because they have an equivalent in OpenTelemetry.

### `serverUrl`

The Elastic APM Node.js agent [`serverUrl`](apm-agent-nodejs://reference/configuration.md#server-url) option corresponds to the OpenTelemetry [`OTEL_EXPORTER_OTLP_ENDPOINT`](https://opentelemetry.io/docs/concepts/sdk-configuration/otlp-exporter-configuration/#otel_exporter_otlp_endpoint) option.

- If using {{serverless-full}}, set `OTEL_EXPORTER_OTLP_ENDPOINT` to the [{{motlp}}](/reference/motlp.md) URL for your Serverless project. For example, `OTEL_EXPORTER_OTLP_ENDPOINT=https://my-prj-a1b2c3.ingest.eu-west-1.aws.elastic.cloud`. Refer to the [Quickstart for {{serverless-full}}](/reference/quickstart/serverless/index.md).

- If using {{ech}} or Self-managed, set `OTEL_EXPORTER_OTLP_ENDPOINT` to the endpoint URL of your EDOT Collector. Refer to the [Quickstart for {{ech}}](/reference/quickstart/ech/hosts_vms.md) or the [Quickstart for Self-managed](/reference/quickstart/self-managed/hosts_vms.md).

### `secretToken`

The Elastic APM Node.js agent [`secretToken`](apm-agent-nodejs://reference/configuration.md#secret-token) option corresponds to setting the `Authorization` header in the OpenTelemetry [OTEL_EXPORTER_OTLP_HEADERS](https://opentelemetry.io/docs/concepts/sdk-configuration/otlp-exporter-configuration/#otel_exporter_otlp_headers) option.

For example: `OTEL_EXPORTER_OTLP_HEADERS="Authorization=Bearer an_apm_secret_token"`.

:::{note}
Secret token usage is discouraged. Use API keys for authentication.
:::

### `apiKey`

The Elastic APM Node.js agent [`apiKey`](apm-agent-nodejs://reference/configuration.md#api-key) option corresponds to setting the `Authorization` header in the OpenTelemetry [OTEL_EXPORTER_OTLP_HEADERS](https://opentelemetry.io/docs/concepts/sdk-configuration/otlp-exporter-configuration/#otel_exporter_otlp_headers) option.

For example:`OTEL_EXPORTER_OTLP_HEADERS="Authorization=ApiKey an_api_key"`.

### `serviceName`

The Elastic APM Node.js agent [`serviceName`](apm-agent-nodejs://reference/configuration.md#service-name) option corresponds to the OpenTelemetry [OTEL_SERVICE_NAME](https://opentelemetry.io/docs/concepts/sdk-configuration/general-sdk-configuration/#otel_service_name) option.

You can also set the service name using [OTEL_RESOURCE_ATTRIBUTES](https://opentelemetry.io/docs/concepts/sdk-configuration/general-sdk-configuration/#otel_resource_attributes). For example: `OTEL_RESOURCE_ATTRIBUTES=service.name=myservice`. A value in `OTEL_SERVICE_NAME` takes precedence over a `service.name` value in `OTEL_RESOURCE_ATTRIBUTES`.

### `active`

The Elastic APM Node.js agent [`active`](apm-agent-nodejs://reference/configuration.md#active) option corresponds to the OpenTelemetry [OTEL_SDK_DISABLED](https://opentelemetry.io/docs/specs/otel/configuration/sdk-environment-variables/#general-sdk-configuration) option but it has the opposite meaning. 

Set the `OTEL_SDK_DISABLED` to `true` if you want to deactivate the agent. For example: `OTEL_SDK_DISABLED=true`.

### `serviceVersion`

The Elastic APM Node.js agent [`serviceVersion`](apm-agent-nodejs://reference/configuration.md#service-version) option corresponds to setting the `service.version` key in [OTEL_RESOURCE_ATTRIBUTES](https://opentelemetry.io/docs/concepts/sdk-configuration/general-sdk-configuration/#otel_resource_attributes).

For example: `OTEL_RESOURCE_ATTRIBUTES=service.version=1.2.3`.

### `environment`

The Elastic APM Node.js agent [`environment`](apm-agent-nodejs://reference/configuration.md#environment) option corresponds to setting the `deployment.environment` key in [OTEL_RESOURCE_ATTRIBUTES](https://opentelemetry.io/docs/concepts/sdk-configuration/general-sdk-configuration/#otel_resource_attributes).

For example: `OTEL_RESOURCE_ATTRIBUTES=deployment.environment=testing`.

### `globalLabels`

The Elastic APM Node.js agent [`globalLabels`](apm-agent-nodejs://reference/configuration.md#global-labels) option corresponds to adding `key=value` comma separated pairs in [OTEL_RESOURCE_ATTRIBUTES](https://opentelemetry.io/docs/concepts/sdk-configuration/general-sdk-configuration/#otel_resource_attributes).

For example: `OTEL_RESOURCE_ATTRIBUTES=alice=first,bob=second`. Such labels will result in labels.key=value attributes on the server. For example, `labels.alice=first`.

### `transactionSampleRate`

The Elastic APM Node.js agent [`transactionSampleRate`](apm-agent-nodejs://reference/configuration.md#transaction-sample-rate) corresponds to the OpenTelemetry `OTEL_TRACES_SAMPLER` and `OTEL_TRACES_SAMPLER_ARG` options. 

For example, for the equivalent of `transactionSampleRate: '0.25'` use `OTEL_TRACES_SAMPLER=parentbased_traceidratio OTEL_TRACES_SAMPLER_ARG=0.25`.

### `logLevel`

The Elastic APM Node.js agent [`logLevel`](apm-agent-nodejs://reference/configuration.md#log-level) option corresponds to the OpenTelemetry [`OTEL_LOG_LEVEL`](https://opentelemetry.io/docs/specs/otel/configuration/sdk-environment-variables/#general-sdk-configuration) option. 

The following table shows the equivalent values of log levels between `elastic-apm-node` and EDOT Node.js.

| ELASTIC_APM_LOG_LEVEL | OTEL_LOG_LEVEL |
| --------------------- | -------------- |
| `off`                 | `none`         |
| `error`               | `error`        |
| `warn`                | `warn`         |
| `info`                | `info`         |
| `debug`               | `debug`        |
| `trace`               | `verbose`      |
| `trace`               | `all`          |

### `maxQueueSize`

The Elastic APM Node.js agent [`maxQueueSize`](apm-agent-nodejs://reference/configuration.md#max-queue-size) option corresponds to a couple of OpenTelemetry options:

- [`OTEL_BSP_MAX_QUEUE_SIZE`](https://opentelemetry.io/docs/specs/otel/configuration/sdk-environment-variables/#batch-span-processor) option to set the queue size for spans.
- [`OTEL_BLRP_MAX_QUEUE_SIZE`](https://opentelemetry.io/docs/specs/otel/configuration/sdk-environment-variables/#batch-span-processor) option to set the queue size for logs.


For example: `OTEL_BSP_MAX_QUEUE_SIZE=2048 OTEL_BLRP_MAX_QUEUE_SIZE=4096`.

### `serverTimeout`

The Elastic APM Node.js agent [`serverTimeout`](apm-agent-nodejs://reference/configuration.md#server-timeout) option corresponds to a OpenTelemetry options per signal:

- [`OTEL_BLRP_EXPORT_TIMEOUT`](https://opentelemetry.io/docs/specs/otel/configuration/sdk-environment-variables/#batch-logrecord-processor) option for logs.
- [`OTEL_BSP_EXPORT_TIMEOUT`](https://opentelemetry.io/docs/specs/otel/configuration/sdk-environment-variables/#batch-span-processor) option for spans.
- [`OTEL_METRIC_EXPORT_TIMEOUT`](https://opentelemetry.io/docs/specs/otel/configuration/sdk-environment-variables/#batch-span-processor) option for metrics.

For example: `OTEL_BSP_EXPORT_TIMEOUT=50000 OTEL_BLRP_EXPORT_TIMEOUT=50000 OTEL_METRIC_EXPORT_TIMEOUT=50000`.

### `apmClientHeaders`

The Elastic APM Node.js agent [`apmClientHeaders`](apm-agent-nodejs://reference/configuration.md#apm-client-headers) option corresponds to the OpenTelemetry [`OTEL_EXPORTER_OTLP_HEADERS`](https://opentelemetry.io/docs/specs/otel/protocol/exporter/#specifying-headers-via-environment-variables) option.

For example: `OTEL_EXPORTER_OTLP_HEADERS=foo=bar,baz=quux`.

### `disableInstrumentations`

The Elastic APM Node.js agent [`disableInstrumentations`](apm-agent-nodejs://reference/configuration.md#apm-client-headers) option corresponds to the EDOT Node.js [`OTEL_NODE_DISABLED_INSTRUMENTATIONS`](/reference/edot-sdks/nodejs/configuration.md#otel_node_disabledenabled_instrumentations-details) option.

For example: `OTEL_NODE_DISABLED_INSTRUMENTATIONS=express,mysql`.

### `metricsInterval`

The Elastic APM Node.js agent [`metricsInterval`](apm-agent-nodejs://reference/configuration.md#metrics-interval) option corresponds to the OpenTelemetry [`OTEL_METRIC_EXPORT_INTERVAL`](https://opentelemetry.io/docs/specs/otel/configuration/sdk-environment-variables/#periodic-exporting-metricreader) option.

For example: `OTEL_METRIC_EXPORT_INTERVAL=30000`.

### `cloudProvider`

The Elastic APM Node.js agent [`cloudProvider`](apm-agent-nodejs://reference/configuration.md#cloud-provider) option does not corresponds directly to an OpenTelemetry option but you can get similar behavior by properly setting [`OTEL_NODE_RESOURCE_DETECTORS`](https://opentelemetry.io/docs/zero-code/js/configuration/#sdk-resource-detector-configuration) option. If you set this option make sure you add along with the cloud detector the non-cloud detectors that apply to your service. For a full list of detectors check [OTEL_NODE_RESOURCE_DETECTORS details](/reference/edot-sdks/nodejs/configuration.md#otel_node_resource_detectors-details). Not setting this option is the equivalent of `auto`.

For example: `OTEL_NODE_RESOURCE_DETECTORS=os,env,host,serviceinstance,process,aws` will make the agent query for AWS metadata only and use other non-cloud detectors to enrich that metadata.

## Limitations

The following limitations apply to EDOT Node.js.

### Supported Node.js versions

EDOT Node.js and OpenTelemetry upstream SDK support Node.js versions in the range `^18.19.0 || >=20.6.0`. Elastic APM Node.js works with Node.js versions `>=14.17.0`, though with limited support for Node.js 14 and 16 given that those major versions of Node.js are out of long-term support.

### Missing instrumentations

EDOT Node.js doesn't currently support instrumentation for AWS Lambda and Azure Functions. However, there are upstream and third-party options based on OpenTelemetry:

- For AWS Lambda use [OpenTelemetry Lambda layers](https://github.com/open-telemetry/opentelemetry-lambda).
- For Azure Functions you can [configure OpenTelemetry](https://learn.microsoft.com/en-us/azure/azure-functions/opentelemetry-howto?tabs=app-insights&pivots=programming-language-javascript).

### Central configuration

Currently EDOT Node.js does not yet have an equivalent of the [central configuration feature](docs-content://solutions/observability/apm/apm-agent-central-configuration.md) that the Elastic APM Node.js agent supports. When using EDOT Node.js, all the configurations are static and must be provided to the application as environment variables.

### Span compression

EDOT Node.js does not implement [span compression](docs-content://solutions/observability/apm/spans.md#apm-spans-span-compression).