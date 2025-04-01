---
title: Migration
layout: default
nav_order: 5
parent: EDOT Node.js
---

# Migrating to EDOT Node.js from the Elastic Node.js Agent

This documentation describes how to update applications that are currently using the [Elastic APM Node.js agent](https://www.elastic.co/guide/en/apm/agent/nodejs/current/index.html) to use the Elastic Distribution of OpenTelemetry for Node.js (EDOT Node.js).

## Advantages of using EDOT Ndode.js agent

### OpenTelemetry-native Data

Allows to capture, send, transform and store data in an OpenTelemetry native way. This includes for example the ability to use all features of the OpenTelemetry SDK for manual tracing, data following semantic conventions or ability to use intermediate collectors and processors.

## Limitations

### Missing Instrumentations

EDOT Node.js does not yet support instrumentation for AWS Lambda and Azure Functions. However, there are upstream and third-party options based on OpenTelemetry:


- For AWS Lambda use [OpenTelemetry Lambda layers](https://github.com/open-telemetry/opentelemetry-lambda).
- For Azure Functions you can [configure OpenTelemetry](https://learn.microsoft.com/en-us/azure/azure-functions/opentelemetry-howto?tabs=app-insights&pivots=programming-language-javascript).

### Central and Dynamic configuration

Currently EDOT Node.js does not yet have an equivalent of the [central configuration feature](https://www.elastic.co/guide/en/observability/current/apm-agent-configuration.html) that the Elastic APM Node.js agent supports. When using EDOT Node.js, all the configurations are static and should be provided to the application with other configurations, e.g. environment variables.

### Span compression

EDOT Node.js does not implement [span compression](https://www.elastic.co/guide/en/observability/current/apm-data-model-spans.html#apm-spans-span-compression).

## Migration steps

1. **Replace Agent Node.js package**
    - Remove Elastic's APM Node.js Agent package by running `npm uninstall --save elastic-apm-node` command in your project.
    - Install EDOT Node.js by runing `npm install --save @elastic/opentelemetry-node` command in your project.
2. **Remove APM Node.js start method**
    - For services starting the APM Node.js Agent by `require`ing in the code with [require and start](https://www.elastic.co/guide/en/apm/agent/nodejs/current/starting-the-agent.html#start-option-require-and-start) or [require start module](https://www.elastic.co/guide/en/apm/agent/nodejs/current/starting-the-agent.html#start-option-require-start-module) the code should be removed.
    - For services starting with [`--require` Node.js CLI option](https://www.elastic.co/guide/en/apm/agent/nodejs/current/starting-the-agent.html#start-option-node-require-opt) the option should be removed. If the `--require` option is
    defined in `NODE_OPTIONS` environment variable it should be removed from there.
    <!-- TODO: add the rest of the methods? -->
3. **(Optional) Migrate manual instrumentation API:** Usages of the [Elastic APM Node.js Agent API](https://www.elastic.co/guide/en/apm/agent/nodejs/current/api.html) require migration to OpenTelemetry API:
    - TODO: explain differences between OTEL & APM? no transactions?
    - TODO: prepare a table of APM API -> OTEL API?
4. **Replace configuration options** using the [Reference](#option-reference) below, see [Configuration](./configuration) for ways to provide those.
5. **Add EDOT Node.js start method** as described in [Setup](./setup/index.html#start-edot-nodejs).

## Option reference

This list contains APM Java agent configuration options that can be migrated to EDOT Node.js agent configuration because
they have an equivalent in OpenTelemetry:

* [serverUrl](#serverUrl)
* [secretToken](#secretToken)
* [apiKey](#apiKey)
* [serviceName](#serviceName)
* [active](#active)
* [serviceVersion](#serviceVersion)
* [environment](#environment)
* [globalLabels](#globalLabels)
* [serverCaCertFile](#serverCaCertFile)
* [transactionSampleRate](#transactionSampleRate)
* [hostname](#hostname)
* [logLevel](#logLevel)
* [maxQueueSize](#maxQueueSize)
* [serverTimeout](#serverTimeout)
* [apmClientHeaders](#apmClientHeaders)
* [disableInstrumentations](#disableInstrumentations)
* [containerId](#containerId)
* [metricsInterval](#metricsInterval)

### `serverUrl`

The Elastic [`serverUrl`](https://www.elastic.co/guide/en/apm/agent/nodejs/current/configuration.html#server-url) option corresponds to the OpenTelemetry [`OTEL_EXPORTER_OTLP_ENDPOINT`](https://opentelemetry.io/docs/concepts/sdk-configuration/otlp-exporter-configuration/#otel_exporter_otlp_endpoint) option.

### `secretToken`

The Elastic [`secretToken`](https://www.elastic.co/guide/en/apm/agent/nodejs/current/configuration.html#secret-token) option corresponds to the OpenTelemetry [OTEL_EXPORTER_OTLP_HEADERS](https://opentelemetry.io/docs/concepts/sdk-configuration/otlp-exporter-configuration/#otel_exporter_otlp_headers) option.

For example: `OTEL_EXPORTER_OTLP_HEADERS="Authorization=Bearer an_apm_secret_token"`.

### `apiKey`

The Elastic [`apiKey`](https://www.elastic.co/guide/en/apm/agent/nodejs/current/configuration.html#api-key) option corresponds to the OpenTelemetry [OTEL_EXPORTER_OTLP_HEADERS](https://opentelemetry.io/docs/concepts/sdk-configuration/otlp-exporter-configuration/#otel_exporter_otlp_headers) option.

For example:`OTEL_EXPORTER_OTLP_HEADERS="Authorization=ApiKey an_api_key"`.

### `serviceName`

The Elastic [`serviceName`](https://www.elastic.co/guide/en/apm/agent/nodejs/current/configuration.html#service-name) option corresponds to the OpenTelemetry [OTEL_SERVICE_NAME](https://opentelemetry.io/docs/concepts/sdk-configuration/general-sdk-configuration/#otel_service_name) option.

The service name value can also be set using [OTEL_RESOURCE_ATTRIBUTES](https://opentelemetry.io/docs/concepts/sdk-configuration/general-sdk-configuration/#otel_resource_attributes).

For example: `OTEL_RESOURCE_ATTRIBUTES=service.name=myservice`. If `OTEL_SERVICE_NAME` is set, it takes precedence over the resource attribute.

### `active`

The Elastic [`active`](https://www.elastic.co/guide/en/apm/agent/nodejs/current/configuration.html#active) option corresponds to the OpenTelemetry [OTEL_SDK_DISABLED](https://opentelemetry.io/docs/specs/otel/configuration/sdk-environment-variables/#general-sdk-configuration) option but it has the opposite meaning. Set the `OTEL_SDK_DISABLED` to `true` if you want to 
deactivate the agent.

For example: `OTEL_SDK_DISABLED=true`.

### `serviceVersion`

The Elastic [`serviceVersion`](https://www.elastic.co/guide/en/apm/agent/nodejs/current/configuration.html#service-version) option corresponds to setting the `service.version` key in [OTEL_RESOURCE_ATTRIBUTES](https://opentelemetry.io/docs/concepts/sdk-configuration/general-sdk-configuration/#otel_resource_attributes).

For example: `OTEL_RESOURCE_ATTRIBUTES=service.version=1.2.3`.

### `environment`

The Elastic [`environment`](https://www.elastic.co/guide/en/apm/agent/nodejs/current/configuration.html#environment) option corresponds to setting the `deployment.environment` key in [OTEL_RESOURCE_ATTRIBUTES](https://opentelemetry.io/docs/concepts/sdk-configuration/general-sdk-configuration/#otel_resource_attributes).

For example: `OTEL_RESOURCE_ATTRIBUTES=deployment.environment=testing`.

### `globalLabels`

The Elastic [`globalLabels`](https://www.elastic.co/guide/en/apm/agent/nodejs/current/configuration.html#global-labels) option corresponds to adding `key=value` comma separated pairs in [OTEL_RESOURCE_ATTRIBUTES](https://opentelemetry.io/docs/concepts/sdk-configuration/general-sdk-configuration/#otel_resource_attributes).

For example: `OTEL_RESOURCE_ATTRIBUTES=alice=first,bob=second`. Such labels will result in labels.key=value attributes on the server, e.g. labels.alice=first

### TODO (double check) `serverCaCertFile`

The Elastic [`serverCaCertFile`](https://www.elastic.co/guide/en/apm/agent/nodejs/current/configuration.html#server-ca-cert-file) option corresponds to the OpenTelemetry [OTEL_EXPORTER_OTLP_CERTIFICATE](https://opentelemetry.io/docs/specs/otel/protocol/exporter/) option. Notice this options can be set specifically for each signal (OTEL_EXPORTER_OTLP_(LOGS|METRICS|TRACES)_CERTIFICATE) and only applies to `grpc` protocol exporter.

For example: `OTEL_EXPORTER_OTLP_CERTIFICATE=./path/to/ca.crt`.

### TODO (double check) `transactionSampleRate`

The Elastic [`transactionSampleRate`](https://www.elastic.co/guide/en/apm/agent/nodejs/current/configuration.html#transaction-sample-rate) option does not directly correspond to a OpenTelemetry option but the same behaviour can be achieved using `OTEL_TRACES_SAMPLER` and `OTEL_TRACES_SAMPLER_ARG` options. OpenTelemetry Node.js SDK comes with the built-in `TraceIdRatioBased` sampler which accepts an argument for the sample rate.

For example: `OTEL_TRACES_SAMPLER=traceidratio OTEL_TRACES_SAMPLER_ARG=0.25`.

### TODO (double check) `hostname`

The Elastic [`hostname`](https://www.elastic.co/guide/en/apm/agent/nodejs/current/configuration.html#service-version) option corresponds to setting the `host.name` key in [OTEL_RESOURCE_ATTRIBUTES](https://opentelemetry.io/docs/concepts/sdk-configuration/general-sdk-configuration/#otel_resource_attributes).

For example: `OTEL_RESOURCE_ATTRIBUTES=host.name=my-host`.

### `logLevel`

The Elastic [`logLevel`](https://www.elastic.co/guide/en/apm/agent/nodejs/current/configuration.html#log-level) option corresponds to the OpenTelemetry [`OTEL_LOG_LEVEL`](https://opentelemetry.io/docs/specs/otel/configuration/sdk-environment-variables/#general-sdk-configuration) option. The possible values change a bit but they represent similar levels. The following
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

The Elastic [`maxQueueSize`](https://www.elastic.co/guide/en/apm/agent/nodejs/current/configuration.html#max-queue-size) option corresponds to the OpenTelemetry [`OTEL_BSP_MAX_QUEUE_SIZE`](https://opentelemetry.io/docs/specs/otel/configuration/sdk-environment-variables/#batch-span-processor) option.

For example: `OTEL_BSP_MAX_QUEUE_SIZE=4096`.

### `serverTimeout`

The Elastic [`serverTimeout`](https://www.elastic.co/guide/en/apm/agent/nodejs/current/configuration.html#server-timeout) option corresponds to the OpenTelemetry [`OTEL_BLRP_EXPORT_TIMEOUT`](https://opentelemetry.io/docs/specs/otel/configuration/sdk-environment-variables/#batch-span-processor) option.

For example: `OTEL_BLRP_EXPORT_TIMEOUT=50000`.

### `apmClientHeaders`

The Elastic [`apmClientHeaders`](https://www.elastic.co/guide/en/apm/agent/nodejs/current/configuration.html#apm-client-headers) option corresponds to the OpenTelemetry [`OTEL_EXPORTER_OTLP_HEADERS`](https://opentelemetry.io/docs/specs/otel/protocol/exporter/#specifying-headers-via-environment-variables) option.

For example: `OTEL_EXPORTER_OTLP_HEADERS=foo=bar,baz=quux`.

### `disableInstrumentations`

The Elastic [`disableInstrumentations`](https://www.elastic.co/guide/en/apm/agent/nodejs/current/configuration.html#apm-client-headers) option corresponds to the EDOT Node.js [`OTEL_NODE_DISABLED_INSTRUMENTATIONS`](https://elastic.github.io/opentelemetry/edot-sdks/nodejs/configuration.html#otel_node_disabledenabled_instrumentations-details) option.

For example: `OTEL_NODE_DISABLED_INSTRUMENTATIONS=express,mysql`.

### TODO (double check) `containerId`

The Elastic [`containerId`](https://www.elastic.co/guide/en/apm/agent/nodejs/current/configuration.html#container-id) option corresponds to setting the `container.id` key in [OTEL_RESOURCE_ATTRIBUTES](https://opentelemetry.io/docs/concepts/sdk-configuration/general-sdk-configuration/#otel_resource_attributes).

For example: `OTEL_RESOURCE_ATTRIBUTES=container.id=my-id`.

### `metricsInterval`

The Elastic [`metricsInterval`](https://www.elastic.co/guide/en/apm/agent/nodejs/current/configuration.html#metrics-interval) option corresponds to the OpenTelemetry [`OTEL_METRIC_EXPORT_INTERVAL`](https://opentelemetry.io/docs/specs/otel/configuration/sdk-environment-variables/#periodic-exporting-metricreader) option.

For example: `OTEL_METRIC_EXPORT_INTERVAL=30000`.

### `cloudProvider`

The Elastic [`cloudProvider`](https://www.elastic.co/guide/en/apm/agent/nodejs/current/configuration.html#cloud-provider) option does not corresponds directly to an OpenTelemetry option but you can get similar behaviour by properly setting [`OTEL_NODE_RESOURCE_DETECTORS`](https://opentelemetry.io/docs/zero-code/js/configuration/#sdk-resource-detector-configuration) option. You have to make sure the
cloud provider is on the list of detectors. Not setting this option is the equivalent of `auto`.

For example: `OTEL_NODE_RESOURCE_DETECTORS=os,env,host,process,gcp`. Will make the agent query for GCP metadata only.



TODO:
https://www.elastic.co/guide/en/apm/agent/nodejs/current/configuration.html#long-field-max-length

is it maybe attr limits on each signal?
https://opentelemetry.io/docs/specs/otel/configuration/sdk-environment-variables/#attribute-limits
https://opentelemetry.io/docs/specs/otel/configuration/sdk-environment-variables/#span-limits
https://opentelemetry.io/docs/specs/otel/configuration/sdk-environment-variables/#logrecord-limits
