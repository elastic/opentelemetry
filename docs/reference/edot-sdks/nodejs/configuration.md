---
navigation_title: Configuration
description: How to configure the Elastic Distribution of OpenTelemetry Node.js (EDOT Node.js) using environment variables.
applies_to:
  stack:
  serverless:
    observability:
products:
  - id: cloud-serverless
  - id: observability
  - id: edot-nodejs
---

# Configuring the EDOT Node.js SDK

The Elastic Distribution of OpenTelemetry Node.js (EDOT Node.js) is configured with environment variables beginning with `OTEL_` or `ELASTIC_OTEL_`. Any `OTEL_*` environment variables behave the same as with the upstream OpenTelemetry SDK. For example, all the OpenTelemetry [General SDK Configuration env vars](https://opentelemetry.io/docs/specs/otel/configuration/sdk-environment-variables/#general-sdk-configuration) are supported. If EDOT Node.js provides a configuration setting specific to the Elastic distribution, it will begin with `ELASTIC_OTEL_`.


## Basic configuration

If not configured, EDOT Node.js will send telemetry data to `http://localhost:4318` with no authentication information, and identify the running service as `unknown_service:node`. Typically a minimal configuration will include

* `OTEL_EXPORTER_OTLP_ENDPOINT`: The full URL of an OpenTelemetry Collector where data will be sent.
* `OTEL_EXPORTER_OTLP_HEADERS`: A comma-separated list of HTTP headers used for exporting data, typically used to set the `Authorization` header with auth information.
* `OTEL_SERVICE_NAME`: The name of your service, used to distinguish telemetry data from other services in your system.

For example, when using an Elastic Cloud Serverless deployment this might be:

```bash
export OTEL_EXPORTER_OTLP_ENDPOINT="https://my-deployment-abc123.ingest.us-west-2.aws.elastic.cloud"
export OTEL_EXPORTER_OTLP_HEADERS="Authorization=ApiKey Zm9vO...mJhcg=="
export OTEL_SERVICE_NAME=my-app
```


## Configuration reference

This section attempts to list all environment variables that can be used to configure EDOT Node.js. Some settings also have a section below discussing behavior that is interesting and/or specific to EDOT Node.js.

:::warning
The behavior of `OTEL_` environment variables are typically defined by upstream OpenTelemetry dependencies of EDOT Node.js. In some cases, these dependencies have a "development" status (`0.x` versions). This means that their behavior can be broken in a minor release of EDOT Node.js.
:::

❇
: Marks settings that are more commonly used.

🔹
: Marks settings with a default value or behavior that differs between EDOT Node.js and upstream OTel JS, or that only exists in EDOT Node.js.

| Name | Notes |
| :--- | :---- |
| `OTEL_SDK_DISABLED` ❇ | [(Ref)][otel-sdk-envvars] Disable the SDK. |
| `OTEL_RESOURCE_ATTRIBUTES` ❇ | [(Ref)][otel-sdk-envvars] Key-value pairs to be used as resource attributes. |
| `OTEL_SERVICE_NAME` ❇ | [(Ref)][otel-sdk-envvars] Set the `service.name` resource attribute. |
| `OTEL_LOG_LEVEL` ❇ | [(Ref)][otel-sdk-envvars] Log level used by the SDK internal logger. Default "info". Use `export OTEL_LOG_LEVEL=verbose` for troubleshooting. One of "all", "verbose", "debug", "info", "warn", "error", "none". |
| `OTEL_PROPAGATORS` | [(Ref)][otel-sdk-envvars] Propagators to use for distributed tracing. Default "tracecontent,baggage". |
| `OTEL_TRACES_SAMPLER` | [(Ref)][otel-sdk-envvars] Sampler to use for traces. Default `parentbased_always_on`. |
| `OTEL_TRACES_SAMPLER_ARG` | [(Ref)][otel-sdk-envvars] Meaning depends on `OTEL_TRACES_SAMPLER`. |
| | |
| `OTEL_EXPORTER_OTLP_ENDPOINT` ❇ | [(Ref)][otel-exporter-envvars] URL to which to send spans, metrics, or logs. Also supports signal-specific `OTEL_EXPORTER_OTLP_{signal}_ENDPOINT`. |
| `OTEL_EXPORTER_OTLP_HEADERS` ❇ | [(Ref)][otel-exporter-envvars] Key-value pairs for headers to be used in HTTP or gRPC requests. Also supports signal-specific `OTEL_EXPORTER_OTLP_{signal}_HEADERS`. |
| `OTEL_EXPORTER_OTLP_PROTOCOL` | [(Ref)][otel-exporter-envvars] OTLP transport protocol. Default `http/protobuf`. One of `http/protobuf`, `grpc`, `http/json`. Also supports signal-specific `OTEL_EXPORTER_OTLP_{signal}_PROTOCOL`. |
| `OTEL_EXPORTER_OTLP_TIMEOUT` | [(Ref)][otel-exporter-envvars] Max time (ms) exporter will way for a batch export. Also supports signal-specific `OTEL_EXPORTER_OTLP_{signal}_TIMEOUT`. |
| `OTEL_EXPORTER_OTLP_COMPRESSION` | [(Ref)][otel-exporter-envvars] Default `gzip`. Also supports signal-specific `OTEL_EXPORTER_OTLP_{signal}_COMPRESSION`. |
| `OTEL_EXPORTER_OTLP_INSECURE` | [(Ref)][otel-exporter-envvars] Whether to disable client transport security for gRPC connections. Default false. Also supports signal-specific `OTEL_EXPORTER_OTLP_{signal}_INSECURE`. |
| `OTEL_EXPORTER_OTLP_CLIENT_KEY` | [(Ref)][otel-exporter-envvars] Client private key for mTLS communication. Also supports signal-specific `OTEL_EXPORTER_OTLP_{signal}_CLIENT_KEY`. |
| `OTEL_EXPORTER_OTLP_CLIENT_CERTIFICATE` | [(Ref)][otel-exporter-envvars] The trusted certificate to use when verifying a server’s TLS credentials. Also supports signal-specific `OTEL_EXPORTER_OTLP_{signal}_CLIENT_CERTIFICATE`. |
| | |
| `OTEL_NODE_RESOURCE_DETECTORS` | [(EDOT Ref)](#otel_node_resource_detectors-details) Comma-separated list of resource detectors to use. |
| `OTEL_NODE_ENABLED_INSTRUMENTATIONS` 🔹 | [(EDOT Ref)](#otel_node_disabledenabled_instrumentations-details) Comma-separated list of instrumentations to enable. |
| `OTEL_NODE_DISABLED_INSTRUMENTATIONS` 🔹 | [(EDOT Ref)](#otel_node_disabledenabled_instrumentations-details) Comma-separated list of instrumentations to disable. |
| | |
| `ELASTIC_OTEL_METRICS_DISABLED` 🔹 | [(EDOT Ref)](#elastic_otel_metrics_disabled-details) Disable any metrics being sent by the SDK. |
| `OTEL_EXPORTER_OTLP_METRICS_TEMPORALITY_PREFERENCE` 🔹 | [(EDOT Ref)](#otel_exporter_otlp_metrics_temporality_preference-details) The metrics exporter's default aggregation `temporality`. Default `delta`. (Note: The upstream OTel default is `cumulative`.) |
| | |
| `OTEL_SEMCONV_STABILITY_OPT_IN` 🔹 | [(EDOT Ref)](#otel_semconv_stability_opt_in-details) Control which HTTP semantic conventions are use by `@opentelemetry/instrumentation-http`. Default 'http'. (Note: The upstream OTel default is an empty value.) |
| | |
| `OTEL_INSTRUMENTATION_GENAI_CAPTURE_MESSAGE_CONTENT` | [(EDOT Ref)](#otel_instrumentation_genai_capture_message_content-details) A boolean to control whether message content should be included in GenAI-related telemetry. |
| | |
| `OTEL_BSP_SCHEDULE_DELAY` | [(Ref)][otel-sdk-envvars-bsp] Duration (ms) between consecutive BatchSpanProcessor exports. Default 5000. |
| `OTEL_BSP_EXPORT_TIMEOUT` | [(Ref)][otel-sdk-envvars-bsp] Maximum allowed time (ms) for BatchSpanProcessor to export. Default 30000. |
| `OTEL_BSP_MAX_QUEUE_SIZE` | [(Ref)][otel-sdk-envvars-bsp] Maximum BatchSpanProcessor queue size. Default 2048. |
| `OTEL_BSP_MAX_EXPORT_BATCH_SIZE` | [(Ref)][otel-sdk-envvars-bsp] Maximum BatchSpanProcessor batch size. Default 512. |
| | |
| `OTEL_BLRP_SCHEDULE_DELAY` | [(Ref)][otel-sdk-envvars-blrp] Duration (ms) between consecutive BatchLogRecordProcessor exports. Default 1000. |
| `OTEL_BLRP_EXPORT_TIMEOUT` | [(Ref)][otel-sdk-envvars-blrp] Maximum allowed time (ms) for BatchLogRecordProcessor to export. Default 30000. |
| `OTEL_BLRP_MAX_QUEUE_SIZE` | [(Ref)][otel-sdk-envvars-blrp] Maximum BatchLogRecordProcessor queue size. Default 2048. |
| `OTEL_BLRP_MAX_EXPORT_BATCH_SIZE` | [(Ref)][otel-sdk-envvars-blrp] Maximum BatchLogRecordProcessor batch size. Default 512. |
| | |
| `OTEL_ATTRIBUTE_VALUE_LENGTH_LIMIT` | [(Ref)][otel-sdk-envvars-attr-limits] Maximum allowed attribute value size. Default: no limit. |
| `OTEL_ATTRIBUTE_COUNT_LIMIT` | [(Ref)][otel-sdk-envvars-attr-limits] Maximum allowed attribute count. Default 128. |
| | |
| `OTEL_SPAN_ATTRIBUTE_VALUE_LENGTH_LIMIT` | [(Ref)][otel-sdk-envvars-span-limits] Max allowed span attribute value size. Default: no limit. |
| `OTEL_SPAN_ATTRIBUTE_COUNT_LIMIT` | [(Ref)][otel-sdk-envvars-span-limits] Max allowed span attribute count. Default 128. |
| `OTEL_SPAN_EVENT_COUNT_LIMIT` | [(Ref)][otel-sdk-envvars-span-limits] Max allowed span event count. Default 128. |
| `OTEL_SPAN_LINK_COUNT_LIMIT` | [(Ref)][otel-sdk-envvars-span-limits] Max allowed span link count. Default 128. |
| `OTEL_EVENT_ATTRIBUTE_COUNT_LIMIT` | [(Ref)][otel-sdk-envvars-span-limits] Max allowed attribute count per span event. Default 128. |
| `OTEL_LINK_ATTRIBUTE_COUNT_LIMIT` | [(Ref)][otel-sdk-envvars-span-limits] Max allowed attribute count per span link. Default 128. |
| | |
| `OTEL_LOGRECORD_ATTRIBUTE_VALUE_LENGTH_LIMIT` | [(Ref)][otel-sdk-envvars-logrecord-limits] Max allowed log record attribute value size. Default: no limit. |
| `OTEL_LOGRECORD_ATTRIBUTE_COUNT_LIMIT` | [(Ref)][otel-sdk-envvars-logrecord-limits] Max allowed log record attribute count. Default 128. |
| | |
| `OTEL_EXPORTER_PROMETHEUS_HOST` | [(Ref)][otel-sdk-envvars-prom] Host used by the Prometheus exporter. Default "localhost". |
| `OTEL_EXPORTER_PROMETHEUS_PORT` | [(Ref)][otel-sdk-envvars-prom] Port used by the Prometheus exporter. Default 9464. |
| | |
| `OTEL_TRACES_EXPORTER` | [(Ref)][otel-sdk-envvars-exp-sel] Trace exporter(s) to use. Default `otlp`. Supports: otlp, console, zipkin, none. |
| `OTEL_METRICS_EXPORTER` | [(Ref)][otel-sdk-envvars-exp-sel] Metrics exporter(s) to use. Default `otlp`. Supports: otlp, console, prometheus, none.|
| `OTEL_LOGS_EXPORTER` | [(Ref)][otel-sdk-envvars-exp-sel] Logs exporter(s) to use. Default `otlp`. Supports: otlp, console, none. |
| | |
| `OTEL_METRICS_EXEMPLAR_FILTER` | [(Ref)][otel-sdk-envvars-metrics] Filter for which measurements can become Exemplars. Default `trace_based`. One of `always_on`, `always_off`, `trace_based`. |
| `OTEL_METRIC_EXPORT_INTERVAL` | [(Ref)][otel-sdk-envvars-metrics] Interval (ms) between consecutive PeriodicExportingMetricReader exports. Default 60000. |
| `OTEL_METRIC_EXPORT_TIMEOUT` | [(Ref)][otel-sdk-envvars-metrics] Max allowed time (ms) for PeriodicExportingMetricReader to export data. Default 30000. |

[otel-sdk-envvars]: https://opentelemetry.io/docs/specs/otel/configuration/sdk-environment-variables/#general-sdk-configuration
[otel-sdk-envvars-bsp]: https://opentelemetry.io/docs/specs/otel/configuration/sdk-environment-variables/#batch-span-processor
[otel-sdk-envvars-blrp]: https://opentelemetry.io/docs/specs/otel/configuration/sdk-environment-variables/#batch-logrecord-processor
[otel-sdk-envvars-attr-limits]: https://opentelemetry.io/docs/specs/otel/configuration/sdk-environment-variables/#attribute-limits
[otel-sdk-envvars-span-limits]: https://opentelemetry.io/docs/specs/otel/configuration/sdk-environment-variables/#span-limits
[otel-sdk-envvars-logrecord-limits]: https://opentelemetry.io/docs/specs/otel/configuration/sdk-environment-variables/#logrecord-limits
[otel-sdk-envvars-prom]: https://opentelemetry.io/docs/specs/otel/configuration/sdk-environment-variables/#prometheus-exporter
[otel-sdk-envvars-exp-sel]: https://opentelemetry.io/docs/specs/otel/configuration/sdk-environment-variables/#exporter-selection
[otel-sdk-envvars-metrics]: https://opentelemetry.io/docs/specs/otel/configuration/sdk-environment-variables/#metrics-sdk-configuration
[otel-exporter-envvars]: https://opentelemetry.io/docs/specs/otel/protocol/exporter/


## EDOT Configuration Details

This section includes additional details on some configuration settings that merit more explanation, or that have behavior that differs in EDOT Node.js when compared to upstream OpenTelemetry JS.


### `OTEL_NODE_RESOURCE_DETECTORS` details [otel_node_resource_detectors-details]

A comma-separated list of named resource detectors to use. EDOT Node.js supports the same set as the upstream [`@opentelemetry/auto-instrumentations-node`](https://github.com/open-telemetry/opentelemetry-js-contrib/blob/main/metapackages/auto-instrumentations-node/README.md#usage-auto-instrumentation):

- `env`
- `host`
- `os`
- `process`
- `serviceinstance`
- `container`
- `alibaba`
- `aws`
- `azure`
- `gcp` - ([temporarily removed](https://github.com/elastic/elastic-otel-node/pull/703))
- `all` - enable all resource detectors (the default)
- `none` - disable resource detection

The "cloud" resource detectors (`alibaba`, `aws`, `azure`, `gcp`) typically make HTTP requests to local metadata services to gather [`cloud.*`](https://opentelemetry.io/docs/specs/semconv/attributes-registry/cloud/) and related resource attributes. If it is important to your application to *not* attempt to gather cloud data on startup, use the following or similar:

```bash
export OTEL_NODE_RESOURCE_DETECTORS=env,host,os,process,serviceinstance,container
```

In addition, EDOT Node.js always includes the [`telemetry.distro.*` resource attributes](https://opentelemetry.io/docs/specs/semconv/attributes-registry/telemetry/).


### `OTEL_NODE_{DISABLED,ENABLED}_INSTRUMENTATIONS` details [otel_node_disabledenabled_instrumentations-details]

`OTEL_NODE_DISABLED_INSTRUMENTATIONS` is a comma-separated list of instrumentation names to disable, from the default set.
`OTEL_NODE_ENABLED_INSTRUMENTATIONS` is a comma-separated list of instrumentation names to enable. Specifying this results in *only* those instrumentations being enabled.

The default set of enabled instrumentations is [the set of included instrumentations](./supported-technologies.md#instrumentations), minus any that are noted as ["disabled by default"](./supported-technologies.md#disabled-instrumentations).

EDOT Node.js handles these settings the same as the upstream [`@opentelemetry/auto-instrumentations-node`](https://github.com/open-telemetry/opentelemetry-js-contrib/blob/main/metapackages/auto-instrumentations-node/README.md#usage-auto-instrumentation), with one addition. In `@opentelemetry/auto-instrumentations-node`, the name of an instrumentation is the name of the package with the `@opentelemetry/instrumentation-` prefix removed -- `cassandra-driver` refers to the instrumentation provided by `@opentelemetry/instrumentation-cassandra`. EDOT Node.js can include instrumentations that do not have this prefix, e.g. `@elastic/opentelemetry-instrumentation-openai`. In these cases, the "name" for the instrumentation is the full package name. For example, to enable only instrumentation for openai, http, fastify, and pino one could use:

```bash
export OTEL_NODE_ENABLED_INSTRUMENTATIONS=http,fastify,pino,@elastic/opentelemetry-instrumentation-openai
```


### `ELASTIC_OTEL_METRICS_DISABLED` details [elastic_otel_metrics_disabled-details]

EDOT Node.js enables the collection and export of metrics by default. If you wish to disable metrics you can by setting the environment variable `ELASTIC_OTEL_METRICS_DISABLED` to the string `true`.

Setting `ELASTIC_OTEL_METRICS_DISABLED=true` is similar to setting `OTEL_METRICS_EXPORTER=none`, in that it ensures no metrics are exported by the SDK. However, this setting will also disable the collection of metrics by the `@opentelemetry/host-metrics` and `@opentelemetry/instrumentation-runtime-node` packages, which can be a minor performace improvement.


### `OTEL_EXPORTER_OTLP_METRICS_TEMPORALITY_PREFERENCE` details [otel_exporter_otlp_metrics_temporality_preference-details]

Elasticsearch and Kibana work best with metrics provided in delta-temporality.
Therefore, the EDOT Node.js changes the default value of `OTEL_EXPORTER_OTLP_METRICS_TEMPORALITY_PREFERENCE` to `delta`.
You can override this default if needed, note though that some provided Kibana dashboards will not work correctly in this case.

Upstream OpenTelemetry defaults the temporality preference to `cumulative`. See https://opentelemetry.io/docs/specs/otel/metrics/sdk_exporters/otlp/#additional-environment-variable-configuration

<!-- TODO: assumes https://github.com/elastic/elastic-otel-node/pull/670 will be merged -->


### `OTEL_SEMCONV_STABILITY_OPT_IN` details [otel_semconv_stability_opt_in-details]

The `OTEL_SEMCONV_STABILITY_OPT_IN` environment variable is defined by OpenTelemetry as the mechanism for user-controlled migration from experimental to stable semantic conventions. Currently it only applies to HTTP semantic conventions. See [the OpenTelemetry HTTP semconv stability migration doc](https://opentelemetry.io/docs/specs/semconv/non-normative/http-migration/) for an introduction.

For Node.js usage, the following instrumentations produce telemetry using HTTP semantic conventions:

- `@opentelemetry/instrumentation-http`: Currently transitioning from old to stable HTTP semantic conventions, via the `OTEL_SEMCONV_STABILITY_OPT_IN` setting.
- `@opentelemetry/instrumentation-undici`: Uses the stable HTTP semantic conventions, because this instrumentation was created after HTTP semconv had stabilized.

EDOT Node.js differs from current upstream OTel JS in that it *defaults `OTEL_SEMCONV_STABILITY_OPT_IN` to `http`*. This means that, by default, all HTTP-related telemetry from EDOT Node.js will use the newer, stable HTTP semantic conventions. (This difference from upstream is expected to be temporary, as upstream `@opentelemetry/instrumentation-http` switches to producing only stable HTTP semantic conventions after its transition period.)


### `OTEL_INSTRUMENTATION_GENAI_CAPTURE_MESSAGE_CONTENT` details [otel_instrumentation_genai_capture_message_content-details]

Set `OTEL_INSTRUMENTATION_GENAI_CAPTURE_MESSAGE_CONTENT` to `true` to
enable capture of content data, such as prompt and completion content, in GenAI telemetry. Currently this applies to the [`@elastic/opentelemetry-instrumentation-openai` instrumentation for the OpenAI Node.js client](https://github.com/elastic/elastic-otel-node/tree/main/packages/instrumentation-openai/#configuration) that is included in EDOT Node.js

The `OTEL_INSTRUMENTATION_GENAI_CAPTURE_MESSAGE_CONTENT` boolean environment variable is a convention established by the OpenTelemetry GenAI SIG. It is referenced in <https://opentelemetry.io/blog/2024/otel-generative-ai/>.
