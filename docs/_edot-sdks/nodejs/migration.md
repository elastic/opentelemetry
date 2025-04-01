---
title: Migration
layout: default
nav_order: 5
parent: EDOT Node.js
---

# Migrating to EDOT Node.js from the Elastic Node.js Agent

This documentation describes how to update applications that are currently using the [Elastic APM Node.js agent](https://www.elastic.co/guide/en/apm/agent/nodejs/current/index.html) (npm package `elastic-apm-node`) to use the Elastic Distribution of OpenTelemetry for Node.js (EDOT Node.js, npm package `@elastic/opentelemetry-node`).

## Advantages of using EDOT Node.js agent

### Compatible Drop-in Replacement

The upstream `@opentelemetry/auto-instrumentations-node` package is a vendor-neutral implementation.
EDOT Node.js is a distribution of it and is thus a fully compatible drop-in replacement of the `@opentelemetry/auto-instrumentations-node` package.

### OpenTelemetry-native Data

Allows to capture, send, transform and store data in an OpenTelemetry native way. This includes for example the ability to use all features of the OpenTelemetry SDK for manual tracing, data following semantic conventions or ability to use intermediate collectors and processors.

## Limitations

### Node.js support

EDOT Node.js and OpenTelemetry upstream SDK do support Node.js with versions in the range `^18.19.0 || >=20.6.0`.

### Missing Instrumentations

EDOT Node.js does not yet support instrumentation for AWS Lambda and Azure Functions. However, there are upstream and third-party options based on OpenTelemetry:

- For AWS Lambda use [OpenTelemetry Lambda layers](https://github.com/open-telemetry/opentelemetry-lambda).
- For Azure Functions you can [configure OpenTelemetry](https://learn.microsoft.com/en-us/azure/azure-functions/opentelemetry-howto?tabs=app-insights&pivots=programming-language-javascript).

### Central and Dynamic configuration

Currently EDOT Node.js does not yet have an equivalent of the [central configuration feature](https://www.elastic.co/guide/en/observability/current/apm-agent-configuration.html) that the Elastic APM Node.js agent supports. When using EDOT Node.js, all the configurations are static and should be provided to the application with other configurations, e.g. environment variables.

### Span compression

EDOT Node.js does not implement [span compression](https://www.elastic.co/guide/en/observability/current/apm-data-model-spans.html#apm-spans-span-compression).

## Migration steps

1. **Replace Node.js package**
    - Remove the Elastic APM Node.js Agent package: `npm uninstall elastic-apm-node`
    - Install EDOT Node.js: `npm install --save @elastic/opentelemetry-node`
2. **Remove APM Node.js start method**
    - For services starting the APM Node.js Agent by `require`ing in the code with [require and start](https://www.elastic.co/guide/en/apm/agent/nodejs/current/starting-the-agent.html#start-option-require-and-start) or [require start module](https://www.elastic.co/guide/en/apm/agent/nodejs/current/starting-the-agent.html#start-option-require-start-module) the code should be removed.
    - For services starting with the [`--require` Node.js CLI option](https://www.elastic.co/guide/en/apm/agent/nodejs/current/starting-the-agent.html#start-option-node-require-opt) the option should be removed. If the `--require` option is
    defined in `NODE_OPTIONS` environment variable it should be removed from there.
3. **(Optional) Migrate manual instrumentation API:** If you're using [Elastic APM Node.js Agent API](https://www.elastic.co/guide/en/apm/agent/nodejs/current/api.html) to crate manual transactions and spans you should refactor the code to use `@opentelemetry/api` methods. OpenTelemetry documentaion has several examples of how to [create spans](https://opentelemetry.io/docs/languages/js/instrumentation/#create-spans) manually.
4. **Replace configuration options** using the [Reference](#option-reference) below, see [Configuration](./configuration) for ways to provide those.
5. **Add EDOT Node.js start method:** use Node.js `--import` [option](https://nodejs.org/api/cli.html#--importmodule) when starting your service. You can set it
    - directly as a command option `node --import @elastic/opentelemetry-node service.js`
    - in [NODE_OPTIONS](https://nodejs.org/api/cli.html#node_optionsoptions) environment var `NODE_OPTIONS="--import @elastic/opentelemetry-node" node service.js`

## Option reference

This list contains Elastic APM Node.js agent configuration options that can be migrated to EDOT Node.js SDK configuration because
they have an equivalent in OpenTelemetry:

* [serverUrl](#serverurl)
* [secretToken](#secrettoken)
* [apiKey](#apikey)
* [serviceName](#servicename)
* [active](#active)
* [serviceVersion](#serviceversion)
* [environment](#environment)
* [globalLabels](#globallabels)
* [transactionSampleRate](#transactionsamplerate)
* [logLevel](#loglevel)
* [maxQueueSize](#maxqueuesize)
* [serverTimeout](#servertimeout)
* [apmClientHeaders](#apmclientheaders)
* [disableInstrumentations](#disableinstrumentations)
* [metricsInterval](#metricsinterval)
* [cloudProvider](#cloudprovider)

### `serverUrl`

The Elastic APM Node.js agent [`serverUrl`](https://www.elastic.co/guide/en/apm/agent/nodejs/current/configuration.html#server-url) option corresponds to the OpenTelemetry [`OTEL_EXPORTER_OTLP_ENDPOINT`](https://opentelemetry.io/docs/concepts/sdk-configuration/otlp-exporter-configuration/#otel_exporter_otlp_endpoint) option.

- If using Elastic Cloud Serverless, then set `OTEL_EXPORTER_OTLP_ENDPOINT` to the managed OTLP endpoint URL for your Serverless project, e.g. `export OTEL_EXPORTER_OTLP_ENDPOINT=https://my-prj-a1b2c3.ingest.eu-west-1.aws.elastic.cloud`. See the [Quickstart for Elastic Cloud Serverless](../../quickstart/serverless/).

- If using Elastic Cloud Hosted or Self-managed, then set `OTEL_EXPORTER_OTLP_ENDPOINT` to the endpoint URL of your EDOT Collector. See the [Quickstart for Elastic Cloud Hosted](../../quickstart/ech/hosts_vms) or the [Quickstart for Self-managed](../../quickstart/self-managed/hosts_vms).

### `secretToken`

The Elastic APM Node.js agent [`secretToken`](https://www.elastic.co/guide/en/apm/agent/nodejs/current/configuration.html#secret-token) option corresponds to the OpenTelemetry [OTEL_EXPORTER_OTLP_HEADERS](https://opentelemetry.io/docs/concepts/sdk-configuration/otlp-exporter-configuration/#otel_exporter_otlp_headers) option.

For example: `OTEL_EXPORTER_OTLP_HEADERS="Authorization=Bearer an_apm_secret_token"`.

{: .note}
Secret token usage is discouraged and Elastic recomends the usage of API keys to for authentication.

### `apiKey`

The Elastic APM Node.js agent [`apiKey`](https://www.elastic.co/guide/en/apm/agent/nodejs/current/configuration.html#api-key) option corresponds to the OpenTelemetry [OTEL_EXPORTER_OTLP_HEADERS](https://opentelemetry.io/docs/concepts/sdk-configuration/otlp-exporter-configuration/#otel_exporter_otlp_headers) option.

For example:`OTEL_EXPORTER_OTLP_HEADERS="Authorization=ApiKey an_api_key"`.

### `serviceName`

The Elastic APM Node.js agent [`serviceName`](https://www.elastic.co/guide/en/apm/agent/nodejs/current/configuration.html#service-name) option corresponds to the OpenTelemetry [OTEL_SERVICE_NAME](https://opentelemetry.io/docs/concepts/sdk-configuration/general-sdk-configuration/#otel_service_name) option.

The service name value can also be set using [OTEL_RESOURCE_ATTRIBUTES](https://opentelemetry.io/docs/concepts/sdk-configuration/general-sdk-configuration/#otel_resource_attributes).

For example: `OTEL_RESOURCE_ATTRIBUTES=service.name=myservice`. If `OTEL_SERVICE_NAME` is set, it takes precedence over the resource attribute.

### `active`

The Elastic APM Node.js agent [`active`](https://www.elastic.co/guide/en/apm/agent/nodejs/current/configuration.html#active) option corresponds to the OpenTelemetry [OTEL_SDK_DISABLED](https://opentelemetry.io/docs/specs/otel/configuration/sdk-environment-variables/#general-sdk-configuration) option but it has the opposite meaning. Set the `OTEL_SDK_DISABLED` to `true` if you want to 
deactivate the agent.

For example: `OTEL_SDK_DISABLED=true`.

### `serviceVersion`

The Elastic APM Node.js agent [`serviceVersion`](https://www.elastic.co/guide/en/apm/agent/nodejs/current/configuration.html#service-version) option corresponds to setting the `service.version` key in [OTEL_RESOURCE_ATTRIBUTES](https://opentelemetry.io/docs/concepts/sdk-configuration/general-sdk-configuration/#otel_resource_attributes).

For example: `OTEL_RESOURCE_ATTRIBUTES=service.version=1.2.3`.

### `environment`

The Elastic APM Node.js agent [`environment`](https://www.elastic.co/guide/en/apm/agent/nodejs/current/configuration.html#environment) option corresponds to setting the `deployment.environment` key in [OTEL_RESOURCE_ATTRIBUTES](https://opentelemetry.io/docs/concepts/sdk-configuration/general-sdk-configuration/#otel_resource_attributes).

For example: `OTEL_RESOURCE_ATTRIBUTES=deployment.environment=testing`.

### `globalLabels`

The Elastic APM Node.js agent [`globalLabels`](https://www.elastic.co/guide/en/apm/agent/nodejs/current/configuration.html#global-labels) option corresponds to adding `key=value` comma separated pairs in [OTEL_RESOURCE_ATTRIBUTES](https://opentelemetry.io/docs/concepts/sdk-configuration/general-sdk-configuration/#otel_resource_attributes).

For example: `OTEL_RESOURCE_ATTRIBUTES=alice=first,bob=second`. Such labels will result in labels.key=value attributes on the server, e.g. labels.alice=first

### `transactionSampleRate`

The Elastic APM Node.js agent [`transactionSampleRate`](https://www.elastic.co/guide/en/apm/agent/nodejs/current/configuration.html#transaction-sample-rate) option does not directly correspond to a OpenTelemetry option but the same behaviour can be achieved using `OTEL_TRACES_SAMPLER` and `OTEL_TRACES_SAMPLER_ARG` options. OpenTelemetry Node.js SDK comes with the built-in `TraceIdRatioBased` sampler which accepts an argument for the sample rate.

For example: `OTEL_TRACES_SAMPLER=traceidratio OTEL_TRACES_SAMPLER_ARG=0.25` will sample 25% of the traces your service.

If your serivce may be accessed by other instrumented services and you want to keep the sampling decision to have distrubuted tracing you could use a different sampler that takes into account the sampling decision from the upstream service in distributed traces.

For example: `OTEL_TRACES_SAMPLER=parentbased_traceidratio OTEL_TRACES_SAMPLER_ARG=0.25` will sample 25% of the traces if they start in your service. For traces coming from an upstream service the sampling decision made upstream will be kept.

### `logLevel`

The Elastic APM Node.js agent [`logLevel`](https://www.elastic.co/guide/en/apm/agent/nodejs/current/configuration.html#log-level) option corresponds to the OpenTelemetry [`OTEL_LOG_LEVEL`](https://opentelemetry.io/docs/specs/otel/configuration/sdk-environment-variables/#general-sdk-configuration) option. The possible values change a bit but they represent similar levels. The following
table shows the equivalent values of log levels between `elastic-apm-node` and EDOT Node.js

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

The Elastic APM Node.js agent [`maxQueueSize`](https://www.elastic.co/guide/en/apm/agent/nodejs/current/configuration.html#max-queue-size) option corresponds to a couple of OpenTelemetry options:

- [`OTEL_BSP_MAX_QUEUE_SIZE`](https://opentelemetry.io/docs/specs/otel/configuration/sdk-environment-variables/#batch-span-processor) option to set the queue size for spans.
- [`OTEL_BLRP_MAX_QUEUE_SIZE`](https://opentelemetry.io/docs/specs/otel/configuration/sdk-environment-variables/#batch-span-processor) option to set the queue size for logs.


For example: `OTEL_BSP_MAX_QUEUE_SIZE=2048 OTEL_BLRP_MAX_QUEUE_SIZE=4096`.

### `serverTimeout`

The Elastic APM Node.js agent [`serverTimeout`](https://www.elastic.co/guide/en/apm/agent/nodejs/current/configuration.html#server-timeout) option corresponds to a OpenTelemetry options per signal:

- [`OTEL_BLRP_EXPORT_TIMEOUT`](https://opentelemetry.io/docs/specs/otel/configuration/sdk-environment-variables/#batch-logrecord-processor) option for logs.
- [`OTEL_BSP_EXPORT_TIMEOUT`](https://opentelemetry.io/docs/specs/otel/configuration/sdk-environment-variables/#batch-span-processor) option for spans.
- [`OTEL_METRIC_EXPORT_TIMEOUT`](https://opentelemetry.io/docs/specs/otel/configuration/sdk-environment-variables/#batch-span-processor) option for metrics.

For example: `OTEL_BSP_EXPORT_TIMEOUT=50000 OTEL_BLRP_EXPORT_TIMEOUT=50000 OTEL_METRIC_EXPORT_TIMEOUT=50000`.

### `apmClientHeaders`

The Elastic APM Node.js agent [`apmClientHeaders`](https://www.elastic.co/guide/en/apm/agent/nodejs/current/configuration.html#apm-client-headers) option corresponds to the OpenTelemetry [`OTEL_EXPORTER_OTLP_HEADERS`](https://opentelemetry.io/docs/specs/otel/protocol/exporter/#specifying-headers-via-environment-variables) option.

For example: `OTEL_EXPORTER_OTLP_HEADERS=foo=bar,baz=quux`.

### `disableInstrumentations`

The Elastic APM Node.js agent [`disableInstrumentations`](https://www.elastic.co/guide/en/apm/agent/nodejs/current/configuration.html#apm-client-headers) option corresponds to the EDOT Node.js [`OTEL_NODE_DISABLED_INSTRUMENTATIONS`](https://elastic.github.io/opentelemetry/edot-sdks/nodejs/configuration.html#otel_node_disabledenabled_instrumentations-details) option.

For example: `OTEL_NODE_DISABLED_INSTRUMENTATIONS=express,mysql`.

### `metricsInterval`

The Elastic APM Node.js agent [`metricsInterval`](https://www.elastic.co/guide/en/apm/agent/nodejs/current/configuration.html#metrics-interval) option corresponds to the OpenTelemetry [`OTEL_METRIC_EXPORT_INTERVAL`](https://opentelemetry.io/docs/specs/otel/configuration/sdk-environment-variables/#periodic-exporting-metricreader) option.

For example: `OTEL_METRIC_EXPORT_INTERVAL=30000`.

### `cloudProvider`

The Elastic APM Node.js agent [`cloudProvider`](https://www.elastic.co/guide/en/apm/agent/nodejs/current/configuration.html#cloud-provider) option does not corresponds directly to an OpenTelemetry option but you can get similar behaviour by properly setting [`OTEL_NODE_RESOURCE_DETECTORS`](https://opentelemetry.io/docs/zero-code/js/configuration/#sdk-resource-detector-configuration) option. If you set this option make sure you add along with the cloud detector the non-cloud detectors that apply to your service. For a full list of detectors check [OTEL_NODE_RESOURCE_DETECTORS details](./configuration#otel_node_resource_detectors-details). Not setting this option is the equivalent of `auto`.

For example: `OTEL_NODE_RESOURCE_DETECTORS=os,env,host,process,gcp`. Will make the agent query for GCP metadata only and use other non-cloud detectors to enrich that metadata.

<!-- TODO: Check if possible to migrate `longFieldMaxLenght`. ref: https://github.com/elastic/elastic-otel-node/issues/696-->