---
navigation_title: Migration
description: Migrate from the Elastic APM PHP agent to the Elastic Distribution of OpenTelemetry PHP (EDOT PHP).
applies_to:
  stack:
  serverless:
    observability:
  product:
    edot_php: ga
products:
  - id: cloud-serverless
  - id: observability
  - id: edot-sdk
  - id: apm-agent
---

# Migrate to EDOT PHP from the Elastic APM PHP agent

Compared to the Elastic APM PHP agent, the {{edot}} PHP presents a number of advantages:

- Fully automatic instrumentation with zero code changes. No need to modify application code, add Composer packages, or wrap bootstrap files.
- EDOT PHP is built on top of OpenTelemetry SDK and conventions, ensuring compatibility with community tools, vendor-neutral backends, and so on.
- Modular, extensible architecture based on the OpenTelemetry SDK. You can add custom exporters, processors, and samplers.
- You can use EDOT PHP in environments where both tracing and metrics are collected using OpenTelemetry.

## Migration steps

Follow these steps to migrate from the legacy Elastic APM PHP agent (`elastic-apm-php`) to the {{edot}} PHP (`elastic-otel-php`).

::::::{stepper}

:::::{step} Uninstall the Elastic APM PHP agent

Remove the previously installed `elastic-apm-php` package:

::::{tab-set}

:::{tab-item} Debian/Ubuntu
```bash
sudo dpkg -r elastic-apm-php
```
:::

:::{tab-item} CentOS/Fedora
```bash
sudo rpm -e elastic-apm-php
```
:::

:::{tab-item} Alpine Linux
```bash
sudo apk del elastic-apm-php
```
:::

::::
:::::

:::::{step} Install EDOT PHP

Download the appropriate package for your system from the [GitHub releases page](https://github.com/elastic/elastic-otel-php/releases).

::::{tab-set}

:::{tab-item} Debian/Ubuntu
```bash
sudo dpkg -i elastic-otel-php_<version>_amd64.deb
```
:::

:::{tab-item} CentOS/Fedora
```bash
sudo rpm -ivh elastic-otel-php-<version>-1.x86_64.rpm
```
:::

:::{tab-item} Alpine Linux
```bash
sudo apk add --allow-untrusted elastic-otel-php-<version>.apk
```
:::

::::
:::::

:::::{step} Update configuration

Switch from `php.ini`-based configuration to environment variables. The following is a common mapping between old and new settings:

| Elastic APM (php.ini)                  | EDOT PHP (environment variable)                              | Description                                    |
| -------------------------------------- | ------------------------------------------------------------ | ---------------------------------------------- |
| `elastic_apm.enabled = 1`              | `ELASTIC_OTEL_ENABLED=true`                                  | Enables EDOT PHP features - enabled by default |
| `elastic_apm.service_name = my-app`    | `OTEL_SERVICE_NAME=my-app`                                   | Defines the logical service name               |
| `elastic_apm.server_url = http://...`  | `OTEL_EXPORTER_OTLP_ENDPOINT=http://localhost:4318`          | Sets OTLP exporter endpoint                    |
| `elastic_apm.secret_token = token123`  | `OTEL_EXPORTER_OTLP_HEADERS="Authorization=Bearer token123"` | Sets auth header for OTLP exporter             |
| `elastic_apm.environment = production` | `OTEL_RESOURCE_ATTRIBUTES=deployment.environment=production` | Adds environment context to exported data      |

::::{tip}
EDOT PHP does not require changes to your code or Composer configuration — instrumentation works automatically after package installation.
::::
:::::                                                                    |

:::::{step} Restart your PHP environment

Restart the relevant PHP processes for changes to take effect. This might include:

::::{tab-set}

:::{tab-item} PHP-FPM
```bash
sudo systemctl restart php8.x-fpm
```
:::

:::{tab-item} Apache
```bash
sudo systemctl restart apache2
```
:::

:::{tab-item} CLI scripts
```bash
php script.php
```
:::

::::
:::::
::::::

## Configuration mapping

The following are Elastic APM PHP agent settings that you can migrate to EDOT PHP.

| Elastic APM PHP Option             | EDOT PHP Environment variable equivalent Option                                                                                                                                  | Description                                                                                                                  |
| ---------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------- |
| `api_key`                          | [`OTEL_EXPORTER_OTLP_HEADERS`](https://opentelemetry.io/docs/languages/sdk-configuration/otlp-exporter/#otel_exporter_otlp_headers)                                                    | Set API key via OTLP headers. Example: `Authorization=Bearer <token>`.                                                       |
| `breakdown_metrics`                | Not available                                                                                                                                                                                | No span compression or breakdown-type metric generation (yet).                                                               |
| `capture_errors`                   | Not available                                                                                                                                                                                | No direct equivalent. Handled via standard error handling and inferred spans.                                                |
| `disable_instrumentations`         | [`OTEL_PHP_DISABLED_INSTRUMENTATIONS`](https://opentelemetry.io/docs/languages/php/sdk/#configuration)                                                                    | Comma-separated list of instrumentations to disable.                                                                         |
| `disable_send`                     | Not available                                                                                                                                                                                | No direct option. Could potentially be simulated with custom exporters or filtering processors.                              |
| `enabled`                          | [`ELASTIC_OTEL_ENABLED`](/reference/edot-sdks/php/configuration.md#general-configuration)                                                                                                               | Enables or disables EDOT PHP instrumentation entirely.                                                                       |
| `environment`                      | [`OTEL_RESOURCE_ATTRIBUTES`](https://opentelemetry.io/docs/languages/sdk-configuration/general/#otel_resource_attributes)                                                        | Add deployment metadata (e.g., `deployment.environment=prod`).                                                               |
| `global_labels`                    | [`OTEL_RESOURCE_ATTRIBUTES`](https://opentelemetry.io/docs/languages/sdk-configuration/general/#otel_resource_attributes)                                                        | Set global key-value pairs for all spans/metrics.                                                                            |
| `log_level`                        | [`OTEL_LOG_LEVEL`](https://opentelemetry.io/docs/specs/otel/configuration/sdk-environment-variables/#general-sdk-configuration), [`ELASTIC_OTEL_LOG_LEVEL_FILE`](/reference/edot-sdks/php/configuration.md#logging-configuration) | Controls log verbosity globally (`OTEL_LOG_LEVEL`) or per sink (e.g., file, stderr, syslog via `ELASTIC_OTEL_LOG_LEVEL_*`).  |
| `server_url`                       | [`OTEL_EXPORTER_OTLP_ENDPOINT`](https://opentelemetry.io/docs/languages/sdk-configuration/otlp-exporter/#otel_exporter_otlp_endpoint)                                                  | Sets OTLP exporter endpoint. Defaults to `http://localhost:4318`.                                                            |
| `service_name`                     | [`OTEL_SERVICE_NAME`](https://opentelemetry.io/docs/languages/sdk-configuration/general/#otel_service_name)                                                                      | Defines service name for traces/metrics.                                                                                     |
| `transaction_sample_rate`          | [`OTEL_TRACES_SAMPLER_ARG`](https://opentelemetry.io/docs/languages/sdk-configuration/general/#otel_traces_sampler_arg)                                                          | Sampling rate for traces (e.g., `0.25`).                                                                                     |
| `transaction_max_spans`            | Not available                                                                                                                                                                                | No direct support in PHP SDK for limiting spans per transaction.                                                             |
| `span_frames_min_duration`         | [`ELASTIC_OTEL_INFERRED_SPANS_MIN_DURATION`](/reference/edot-sdks/php/configuration.md#inferred-spans-configuration)                                                                                    | Duration threshold for inferred spans.                                                                                       |
| `sanitize_field_names`             | Not available                                                                                                                                                                                | Not yet supported in EDOT PHP.                                                                                               |
| `verify_server_cert`               | [`ELASTIC_OTEL_VERIFY_SERVER_CERT`](/reference/edot-sdks/php/configuration.md#asynchronous-data-sending-configuration)                                                                                  | Enable or disable SSL verification when exporting telemetry.                                                                 |
| `transaction_ignore_urls`          | [`OTEL_PHP_EXCLUDED_URLS`](https://opentelemetry.io/docs/languages/php/sdk/#configuration)                                                                                       | A comma-separated list of regex patterns for excluding incoming HTTP URLs from tracing (e.g., `client/.*/info,healthcheck`). |
| `transaction_name_callback`        | Not available                                                                                                                                                                                | No equivalent for callback-based naming; use grouping or manual `setAttribute()`.                                            |
| `log_level_syslog`                 | [`ELASTIC_OTEL_LOG_LEVEL_SYSLOG`](/reference/edot-sdks/php/configuration.md#logging-configuration)                                                                                                      | Sets syslog sink verbosity.                                                                                                  |
| `log_level_file`                   | [`ELASTIC_OTEL_LOG_LEVEL_FILE`](/reference/edot-sdks/php/configuration.md#logging-configuration)                                                                                                        | Controls log level for file-based output.                                                                                    |
| `log_level_stderr`                 | [`ELASTIC_OTEL_LOG_LEVEL_STDERR`](/reference/edot-sdks/php/configuration.md#logging-configuration)                                                                                                      | Controls log level for stderr (recommended in containers).                                                                   |
| `log_file`                         | [`ELASTIC_OTEL_LOG_FILE`](/reference/edot-sdks/php/configuration.md#logging-configuration)                                                                                                              | Path for log output; supports `%p` (PID) and `%t` (timestamp) placeholders.                                                  |
| `log_feature`                      | [`ELASTIC_OTEL_LOG_FEATURES`](/reference/edot-sdks/php/configuration.md#logging-configuration)                                                                                                          | Fine-grained feature-based logging configuration.                                                                            |
| `transaction_url_groups`           | [`ELASTIC_OTEL_TRANSACTION_URL_GROUPS`](/reference/edot-sdks/php/configuration.md#transaction-span-configuration)                                                                                       | Group similar URL paths (e.g., `/user/*`).                                                                                   |
| `inferred_spans_enabled`           | [`ELASTIC_OTEL_INFERRED_SPANS_ENABLED`](/reference/edot-sdks/php/configuration.md#inferred-spans-configuration)                                                                                         | Enables inferred spans (preview).                                                                                            |
| `inferred_spans_sampling_interval` | [`ELASTIC_OTEL_INFERRED_SPANS_SAMPLING_INTERVAL`](/reference/edot-sdks/php/configuration.md#inferred-spans-configuration)                                                                               | Sampling frequency for stack traces during inferred spans.                                                                   |
| `inferred_spans_min_duration`      | [`ELASTIC_OTEL_INFERRED_SPANS_MIN_DURATION`](/reference/edot-sdks/php/configuration.md#inferred-spans-configuration)                                                                                    | Minimum duration of inferred span (used to limit noise). 

## Limitations

The following limitations apply to EDOT PHP:

- Lack of span compression: The classic Elastic APM agent includes span compression, which merges multiple similar spans. EDOT PHP doesn't currently support span compression. As a result, traces may be more verbose and produce higher cardinality, especially in loop-heavy code.

:::{note}
For a broader overview of known limitations — including technical constraints related to PHP runtime and extensions, refer to [Limitations](/reference/edot-sdks/php/setup/limitations.md).
:::