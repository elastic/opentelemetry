---
navigation_title: Migration
description: Migrate from the Elastic APM PHP agent to the Elastic Distribution of OpenTelemetry PHP (EDOT PHP).
applies_to:
  stack:
  serverless:
    observability:
products:
  - cloud-serverless
  - observability
  - edot-python
  - apm-php-agent
---

# Migrating to EDOT PHP from the Elastic PHP Agent

Follow these steps to migrate from the legacy Elastic APM PHP agent (`elastic-apm-php`) to the Elastic Distribution of OpenTelemetry PHP (`elastic-otel-php`).

### 1. Uninstall the Elastic APM PHP agent

Remove the previously installed `elastic-apm-php` package:

**Debian/Ubuntu:**

```bash
sudo dpkg -r elastic-apm-php
```

**CentOS/Fedora:**

```bash
sudo rpm -e elastic-apm-php
```

**Alpine Linux:**

```bash
sudo apk del elastic-apm-php
```

applies_to:
  stack:
  serverless:
    observability:
products:
  - cloud-serverless
  - observability
---

### 2. Install EDOT PHP

Download the appropriate package for your system from the [GitHub releases page](https://github.com/elastic/elastic-otel-php/releases).

**Debian/Ubuntu:**

```bash
sudo dpkg -i elastic-otel-php_<version>_amd64.deb
```

**CentOS/Fedora:**

```bash
sudo rpm -ivh elastic-otel-php-<version>-1.x86_64.rpm
```

**Alpine Linux:**

```bash
sudo apk add --allow-untrusted elastic-otel-php-<version>.apk
```

applies_to:
  stack:
  serverless:
    observability:
products:
  - cloud-serverless
  - observability
---

### 3. Update configuration

Switch from `php.ini`-based configuration to environment variables. Below is a common mapping between old and new settings:

| Elastic APM (php.ini)                  | EDOT PHP (environment variable)                              | Description                                    |
| -------------------------------------- | ------------------------------------------------------------ | ---------------------------------------------- |
| `elastic_apm.enabled = 1`              | `ELASTIC_OTEL_ENABLED=true`                                  | Enables EDOT PHP features - enabled by default |
| `elastic_apm.service_name = my-app`    | `OTEL_SERVICE_NAME=my-app`                                   | Defines the logical service name               |
| `elastic_apm.server_url = http://...`  | `OTEL_EXPORTER_OTLP_ENDPOINT=http://localhost:4318`          | Sets OTLP exporter endpoint                    |
| `elastic_apm.secret_token = token123`  | `OTEL_EXPORTER_OTLP_HEADERS="Authorization=Bearer token123"` | Sets auth header for OTLP exporter             |
| `elastic_apm.environment = production` | `OTEL_RESOURCE_ATTRIBUTES=deployment.environment=production` | Adds environment context to exported data      |

:::tip
EDOT PHP does not require changes to your code or Composer configuration — instrumentation works automatically after package installation.
:::

applies_to:
  stack:
  serverless:
    observability:
products:
  - cloud-serverless
  - observability
---

### Full Configuration Mapping: Elastic APM PHP → EDOT PHP

| Elastic APM PHP Option             | EDOT PHP Environment variable equivalent Option                                                                                                                                  | Description                                                                                                                  |
| ---------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------- |
| `api_key`                          | [`OTEL_EXPORTER_OTLP_HEADERS`](https://opentelemetry.io/docs/languages/sdk-configuration/otlp-exporter/#otel_exporter_otlp_headers)                                                    | Set API key via OTLP headers. Example: `Authorization=Bearer <token>`.                                                       |
| `breakdown_metrics`                | ❌                                                                                                                                                                                | No span compression or breakdown-type metric generation (yet).                                                               |
| `capture_errors`                   | ❌                                                                                                                                                                                | No direct equivalent. Handled via standard error handling and inferred spans.                                                |
| `disable_instrumentations`         | [`OTEL_PHP_DISABLED_INSTRUMENTATIONS`](https://opentelemetry.io/docs/languages/php/sdk/#configuration)                                                                    | Comma-separated list of instrumentations to disable.                                                                         |
| `disable_send`                     | ❌                                                                                                                                                                                | No direct option. Could potentially be simulated with custom exporters or filtering processors.                              |
| `enabled`                          | [`ELASTIC_OTEL_ENABLED`](./configuration#general-configuration)                                                                                                               | Enables or disables EDOT PHP instrumentation entirely.                                                                       |
| `environment`                      | [`OTEL_RESOURCE_ATTRIBUTES`](https://opentelemetry.io/docs/languages/sdk-configuration/general/#otel_resource_attributes)                                                        | Add deployment metadata (e.g., `deployment.environment=prod`).                                                               |
| `global_labels`                    | [`OTEL_RESOURCE_ATTRIBUTES`](https://opentelemetry.io/docs/languages/sdk-configuration/general/#otel_resource_attributes)                                                        | Set global key-value pairs for all spans/metrics.                                                                            |
| `log_level`                        | [`OTEL_LOG_LEVEL`](https://opentelemetry.io/docs/specs/otel/configuration/sdk-environment-variables/#general-sdk-configuration), [`ELASTIC_OTEL_LOG_LEVEL_FILE`](./configuration#logging-configuration) | Controls log verbosity globally (`OTEL_LOG_LEVEL`) or per sink (e.g., file, stderr, syslog via `ELASTIC_OTEL_LOG_LEVEL_*`).  |
| `server_url`                       | [`OTEL_EXPORTER_OTLP_ENDPOINT`](https://opentelemetry.io/docs/languages/sdk-configuration/otlp-exporter/#otel_exporter_otlp_endpoint)                                                  | Sets OTLP exporter endpoint. Defaults to `http://localhost:4318`.                                                            |
| `service_name`                     | [`OTEL_SERVICE_NAME`](https://opentelemetry.io/docs/languages/sdk-configuration/general/#otel_service_name)                                                                      | Defines service name for traces/metrics.                                                                                     |
| `transaction_sample_rate`          | [`OTEL_TRACES_SAMPLER_ARG`](https://opentelemetry.io/docs/languages/sdk-configuration/general/#otel_traces_sampler_arg)                                                          | Sampling rate for traces (e.g., `0.25`).                                                                                     |
| `transaction_max_spans`            | ❌                                                                                                                                                                                | No direct support in PHP SDK for limiting spans per transaction.                                                             |
| `span_frames_min_duration`         | [`ELASTIC_OTEL_INFERRED_SPANS_MIN_DURATION`](./configuration#inferred-spans-configuration)                                                                                    | Duration threshold for inferred spans.                                                                                       |
| `sanitize_field_names`             | ❌                                                                                                                                                                                | Not yet supported in EDOT PHP.                                                                                               |
| `verify_server_cert`               | [`ELASTIC_OTEL_VERIFY_SERVER_CERT`](./configuration#asynchronous-data-sending-configuration)                                                                                  | Enable or disable SSL verification when exporting telemetry.                                                                 |
| `transaction_ignore_urls`          | [`OTEL_PHP_EXCLUDED_URLS`](https://opentelemetry.io/docs/languages/php/sdk/#configuration)                                                                                       | A comma-separated list of regex patterns for excluding incoming HTTP URLs from tracing (e.g., `client/.*/info,healthcheck`). |
| `transaction_name_callback`        | ❌                                                                                                                                                                                | No equivalent for callback-based naming; use grouping or manual `setAttribute()`.                                            |
| `log_level_syslog`                 | [`ELASTIC_OTEL_LOG_LEVEL_SYSLOG`](./configuration#logging-configuration)                                                                                                      | Sets syslog sink verbosity.                                                                                                  |
| `log_level_file`                   | [`ELASTIC_OTEL_LOG_LEVEL_FILE`](./configuration#logging-configuration)                                                                                                        | Controls log level for file-based output.                                                                                    |
| `log_level_stderr`                 | [`ELASTIC_OTEL_LOG_LEVEL_STDERR`](./configuration#logging-configuration)                                                                                                      | Controls log level for stderr (recommended in containers).                                                                   |
| `log_file`                         | [`ELASTIC_OTEL_LOG_FILE`](./configuration#logging-configuration)                                                                                                              | Path for log output; supports `%p` (PID) and `%t` (timestamp) placeholders.                                                  |
| `log_feature`                      | [`ELASTIC_OTEL_LOG_FEATURES`](./configuration#logging-configuration)                                                                                                          | Fine-grained feature-based logging configuration.                                                                            |
| `transaction_url_groups`           | [`ELASTIC_OTEL_TRANSACTION_URL_GROUPS`](./configuration#transaction-span-configuration)                                                                                       | Group similar URL paths (e.g., `/user/*`).                                                                                   |
| `inferred_spans_enabled`           | [`ELASTIC_OTEL_INFERRED_SPANS_ENABLED`](./configuration#inferred-spans-configuration)                                                                                         | Enables inferred spans (preview).                                                                                            |
| `inferred_spans_sampling_interval` | [`ELASTIC_OTEL_INFERRED_SPANS_SAMPLING_INTERVAL`](./configuration#inferred-spans-configuration)                                                                               | Sampling frequency for stack traces during inferred spans.                                                                   |
| `inferred_spans_min_duration`      | [`ELASTIC_OTEL_INFERRED_SPANS_MIN_DURATION`](./configuration#inferred-spans-configuration)                                                                                    | Minimum duration of inferred span (used to limit noise).                                                                     |


applies_to:
  stack:
  serverless:
    observability:
products:
  - cloud-serverless
  - observability
---

### 4. Restart your PHP environment

Restart the relevant PHP processes for changes to take effect. This could include:

- PHP-FPM:
  ```bash
  sudo systemctl restart php8.x-fpm
  ```

- Apache:
  ```bash
  sudo systemctl restart apache2
  ```

- CLI scripts:
  ```bash
  php script.php
  ```

applies_to:
  stack:
  serverless:
    observability:
products:
  - cloud-serverless
  - observability
---

✅ You’re now ready to start collecting traces and metrics using OpenTelemetry with Elastic!

## Advantages of EDOT PHP over the Classic Elastic APM Agent

### Fully automatic instrumentation with zero code changes
- No need to modify application code, add Composer packages, or wrap bootstrap files.
- Works out-of-the-box after system package installation.
- No need to register SDK, bootstrap, or start a tracer manually — everything is handled by the agent at the extension level.

### OpenTelemetry standard compliance
- EDOT PHP is built on top of **OpenTelemetry SDK and conventions**, ensuring compatibility with:
  - community tools,
  - vendor-neutral backends,
  - standard propagation formats (`traceparent`, `baggage`),
  - open observability pipelines (e.g., EDOT Collector or OpenTelemetry Collector).

### Modular, extensible architecture
- Based on the OpenTelemetry SDK — you can add custom exporters, processors, and samplers.
- Easy to extend or adapt to advanced use cases (e.g., exporting to multiple backends).

### Better future-proofing and community alignment
- EDOT PHP benefits from:
  - upstream OpenTelemetry improvements,
  - Elastic-specific early bugfixes and features,
  - community-driven instrumentation libraries and patterns.

### Unified telemetry collection (traces + metrics)
- EDOT PHP can be used in environments where **both tracing and metrics** are collected using OpenTelemetry.
- The classic APM agent focuses solely on APM/tracing.
## ⚠️ Limitations Compared to the Elastic APM Agent

- Lack of Span Compression

    The classic Elastic APM agent includes span compression, which merges multiple similar spans (e.g., repeated SQL queries or HTTP calls) into a single composite span to reduce trace noise and overhead.

    EDOT PHP does not currently support span compression. As a result, traces may be more verbose and produce higher cardinality, especially in loop-heavy code.

:::note
For a broader overview of known limitations — including technical constraints related to PHP runtime and extensions — see the [Limitations](./setup/limitations) page.
:::