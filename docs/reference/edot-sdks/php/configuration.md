---
navigation_title: Configuration
description: Configure the Elastic Distribution of OpenTelemetry PHP (EDOT PHP) to send data to Elastic.
applies_to:
  stack:
  serverless:
    observability:
products:
  - id: cloud-serverless
  - id: observability
  - id: edot-sdk
---

# Configure the EDOT PHP SDK

Learn how to configure the {{edot}} PHP (EDOT PHP) to send data to Elastic.

## Configuration method

You can configure the OpenTelemetry SDK through the mechanisms [documented on the OpenTelemetry website](https://opentelemetry.io/docs/zero-code/php#configuration). EDOT PHP is typically configured with `OTEL_*` environment variables defined by the OpenTelemetry spec. For example:

```bash
export OTEL_EXPORTER_OTLP_ENDPOINT="https://********.cloud.es.io:443/"
```

## Configuration options

Because the {{edot}} PHP is an extension of the OpenTelemetry PHP SDK, it supports:

* [OpenTelemetry configuration options](#opentelemetry-configuration-options)
* [Configuration options only available in EDOT PHP](#options-only-available-in-edot-php)

### OpenTelemetry configuration options

EDOT PHP supports all configuration options listed in the [OpenTelemetry General SDK Configuration documentation](https://opentelemetry.io/docs/languages/sdk-configuration/general/) and [OpenTelemetry PHP SDK](https://opentelemetry.io/docs/languages/php).

The most important OpenTelemetry options you should be aware of include:

| Option(s)                                                                                                                     | Default                 | Accepted values                                 | Description                                                                                                                                                                                                |
| ----------------------------------------------------------------------------------------------------------------------------- | ----------------------- | ----------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [OTEL_EXPORTER_OTLP_ENDPOINT](https://opentelemetry.io/docs/languages/sdk-configuration/otlp-exporter/#otel_exporter_otlp_endpoint) | http://localhost:4318   | URL                                             | Specifies the OTLP endpoint to which telemetry data should be sent.                                                                                                                                        |
| [OTEL_EXPORTER_OTLP_HEADERS](https://opentelemetry.io/docs/languages/sdk-configuration/otlp-exporter/#otel_exporter_otlp_headers)   |                         | string of key-value pairs                       | Key-value pairs to be used as headers (e.g., for authentication) when sending telemetry data via OTLP. Format: `key1=value1,key2=value2`.                                                                  |
| [OTEL_SERVICE_NAME](https://opentelemetry.io/docs/languages/sdk-configuration/general/#otel_service_name)                     | "unknown_service"       | string value                                    | Sets the value of the [service.name](https://opentelemetry.io/docs/specs/semconv/resource/#service) resource attribute.                                                                                    |
| [OTEL_RESOURCE_ATTRIBUTES](https://opentelemetry.io/docs/languages/sdk-configuration/general/#otel_resource_attributes)       |                         | string of key-value pairs                       | Key-value pairs to be used as resource attributes. See [Resource SDK](https://opentelemetry.io/docs/specs/otel/resource/sdk#specifying-resource-information-via-an-environment-variable) for more details. |
| [OTEL_TRACES_SAMPLER](https://opentelemetry.io/docs/languages/sdk-configuration/general/#otel_traces_sampler)                 | "parentbased_always_on" | "always_on", "always_off", "traceidratio", etc. | Determines the sampler used for traces, which controls the amount of data collected and exported.                                                                                                          |
| [OTEL_TRACES_SAMPLER_ARG](https://opentelemetry.io/docs/languages/sdk-configuration/general/#otel_traces_sampler_arg)         |                         | string or number                                | Provides an argument to the configured traces sampler, such as the sampling ratio for `traceidratio` (e.g., `0.25` for 25% sampling).                                                                      |
| [OTEL_LOG_LEVEL](https://opentelemetry.io/docs/specs/otel/configuration/sdk-environment-variables/#general-sdk-configuration)                           | "info"                  | "error", "warn", "info", "debug"                | Sets the verbosity level of the OpenTelemetry SDK’s internal logging. Useful for debugging configuration or troubleshooting instrumentation.                                                               |

For full configuration options of PHP SDK, see the official [OpenTelemetry PHP SDK Configuration documentation](https://opentelemetry.io/docs/languages/php/sdk/#configuration).

### Special considerations

EDOT PHP supports background data transmission (non-blocking export), but only when the exporter is set to `http/protobuf` (OTLP over HTTP), which is the default configuration.
If you change the exporter or the transport protocol, for example to gRPC or another format, telemetry data will be sent synchronously, potentially impacting request latency.

EDOT PHP also sets the `OTEL_PHP_AUTOLOAD_ENABLED` option to `true` by default. This turns on automatic instrumentation without requiring any changes to your application code.
Modifying this option will have no effect: EDOT will override it and enforce it as `true`.

### Options only available in EDOT PHP

In addition to general OpenTelemetry configuration options, there are two kinds of configuration options that are only available in EDOT PHP.

Each option listed in this document that starts with the `ELASTIC_OTEL_` prefix can be set using either an environment variable or the `php.ini` file.

When using the `php.ini` file, replace the `ELASTIC_OTEL_` prefix with `elastic_otel.` and convert the rest of the option name to lowercase, for example:

::::{tab-set}

:::{tab-item} Environment variable
```bash
export ELASTIC_OTEL_ENABLED=true
```
:::

:::{tab-item} php.ini
```ini
elastic_otel.enabled=true
```
:::

::::

`ELASTIC_OTEL_` options that are specific to Elastic and always live in EDOT PHP, meaning they will not be added to upstream, include the following.

#### General configuration

| Option(s)            | Default | Accepted values | Description                                                 |
| -------------------- | ------- | --------------- | ----------------------------------------------------------- |
| ELASTIC_OTEL_ENABLED | true    | true or false   | Enables the automatic bootstrapping of instrumentation code |
| ELASTIC_OTEL_NATIVE_OTLP_SERIALIZER_ENABLED   | true    | true or false   | Enables the native built-in OTLP Protobuf serializer for maximum performance |

#### Asynchronous data sending configuration

| Option(s)                                     | Default | Accepted values                                                                                         | Description                                                                                                                          |
| --------------------------------------------- | ------- | ------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------ |
| ELASTIC_OTEL_ASYNC_TRANSPORT                  | true    | true or false                                                                                           | Use asynchronous (background) transfer of traces, metrics and logs. If false - brings back original OpenTelemetry SDK transfer modes |
| ELASTIC_OTEL_ASYNC_TRANSPORT_SHUTDOWN_TIMEOUT | 30s     | interger number with time duration. Set to 0 to disable the timeout. Optional units: ms (default), s, m | Timeout after which the asynchronous (background) transfer will interrupt data transmission during process termination               |
| ELASTIC_OTEL_MAX_SEND_QUEUE_SIZE              | 2MB     | integer number with optional units: B, MB or GB                                                         | Set the maximum buffer size for asynchronous (background) transfer. It is set per worker process.                                    |
| ELASTIC_OTEL_VERIFY_SERVER_CERT               | true    | true or false                                                                                           | Enables server certificate verification for asynchronous sending                                                                     |

#### Logging configuration

| Option(s)                     | Default | Accepted values                                                                                                                               | Description                                                                                                                                                                                                                                                                                                                      |
| ----------------------------- | ------- | --------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| ELASTIC_OTEL_LOG_FILE         |         | Filesystem path                                                                                                                               | Log file name. You can use the %p placeholder where the process ID will appear in the file name, and %t where the timestamp will appear. Please note that the PHP process must have write permissions for the specified path.                                                                                                    |
| ELASTIC_OTEL_LOG_LEVEL_FILE   | OFF     | OFF, CRITICAL, ERROR, WARNING, INFO, DEBUG, TRACE                                                                                             | Log level for file sink. Set to OFF if you don't want to log to file.                                                                                                                                                                                                                                                            |
| ELASTIC_OTEL_LOG_LEVEL_STDERR | OFF     | OFF, CRITICAL, ERROR, WARNING, INFO, DEBUG, TRACE                                                                                             | Log level for the stderr sink. Set to OFF if you don't want to log to a file. This sink is recommended when running the application in a container.                                                                                                                                                                              |
| ELASTIC_OTEL_LOG_LEVEL_SYSLOG | OFF     | OFF, CRITICAL, ERROR, WARNING, INFO, DEBUG, TRACE                                                                                             | Log level for file sink. Set to OFF if you don't want to log to file. This sink is recommended when you don't have write access to file system.                                                                                                                                                                                  |
| ELASTIC_OTEL_LOG_FEATURES     |         | Comma separated string with FEATURE=LEVEL pairs.<br>Supported features:<br>ALL, MODULE, REQUEST, TRANSPORT, BOOTSTRAP, HOOKS, INSTRUMENTATION | Allows selective setting of log level for features. For example, "ALL=info,TRANSPORT=trace" will result in all other features logging at the info level, while the TRANSPORT feature logs at the trace level. It should be noted that the appropriate log level must be set for the sink - for our example, this would be TRACE. |

#### Transaction span configuration

| Option(s)                                 | Default         | Accepted values                              | Description                                                                                                                                                                    |
| ----------------------------------------- | --------------- | -------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| ELASTIC_OTEL_TRANSACTION_SPAN_ENABLED     | true            | true or false                                | Enables automatic creation of transaction (root) spans for the webserver SAPI. The name of the span will correspond to the request method and path.                            |
| ELASTIC_OTEL_TRANSACTION_SPAN_ENABLED_CLI | true            | true or false                                | Enables automatic creation of transaction (root) spans for the CLI SAPI. The name of the span will correspond to the script name.                                              |
| ELASTIC_OTEL_TRANSACTION_URL_GROUPS       |                 | Comma-separated list of wildcard expressions | Allows grouping multiple URL paths using wildcard expressions, such as `/user/*`. For example, `/user/Alice` and `/user/Bob` will be mapped to the transaction name `/user/*`. |
| <option>                                  | <default value> | <description>                                |

#### Inferred spans configuration

| Option(s)                                      | Default | Accepted values                                                                                 | Description                                                                                                                                                                                                                                                                                                                                |
| ---------------------------------------------- | ------- | ----------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| ELASTIC_OTEL_INFERRED_SPANS_ENABLED            | false   | true or false                                                                                   | Enables the inferred spans feature.                                                                                                                                                                                                                                                                                                        |
| ELASTIC_OTEL_INFERRED_SPANS_REDUCTION_ENABLED  | true    | true or false                                                                                   | If enabled, reduces the number of spans by eliminating preceding frames with the same execution time.                                                                                                                                                                                                                                      |
| ELASTIC_OTEL_INFERRED_SPANS_STACKTRACE_ENABLED | true    | true or false                                                                                   | If enabled, attaches a stack trace to the span metadata.                                                                                                                                                                                                                                                                                   |
| ELASTIC_OTEL_INFERRED_SPANS_SAMPLING_INTERVAL  | 50ms    | interger number with time duration. Optional units: ms (default), s, m. It can't be set to 0.   | The frequency at which stack traces are gathered within a profiling session. The lower you set it, the more accurate the durations will be. This comes at the expense of higher overhead and more spans for potentially irrelevant operations. The minimal duration of a profiling-inferred span is the same as the value of this setting. |
| ELASTIC_OTEL_INFERRED_SPANS_MIN_DURATION       | 0       | interger number with time duration. Optional units: ms (default), s, m. _Disabled if set to 0_. | The minimum duration of an inferred span. Note that the min duration is also implicitly set by the sampling interval. However, increasing the sampling interval also decreases the accuracy of the duration of inferred spans.                                                                                                             |

## Central configuration

APM Agent Central Configuration lets you configure EDOT PHP instances remotely, see [Central configuration docs](/reference/central-configuration.md) for more details.

### Central configuration settings

You can modify the following settings for EDOT PHP through APM Agent Central Configuration:

| Setting | Central configuration name | Type |
|---------|--------------------------|------|
| Logging level | `logging_level` | Dynamic |

Dynamic settings can be changed without having to restart the application.