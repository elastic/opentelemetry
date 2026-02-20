---
navigation_title: Configuration
description: Configure the Elastic Distribution of OpenTelemetry Browser (EDOT Browser).
applies_to:
  stack: ga
  serverless:
    observability: ga
products:
  - id: cloud-serverless
  - id: observability
  - id: edot-sdk
---

# Configure EDOT Browser

This page explains how configuration works in EDOT Browser, which settings are supported, and what’s required to start exporting browser telemetry.

EDOT Browser follows OpenTelemetry configuration conventions where possible, while accounting for the constraints of running in a web browser.

## Configuration model in the browser [configuration-model-in-the-browser]

Unlike backend OpenTelemetry SDKs, EDOT Browser runs in your users’ browsers. This has important implications:

- Environment variables are not available at runtime.
- You must provide configuration at build time (for example, using bundler-defined constants) or at runtime by passing options to an initialization function.
- Never embed secrets in browser configuration.

Because environment variables aren’t available at runtime in the browser, EDOT Browser does not read `OTEL_*` variables directly. Instead, it accepts configuration values passed explicitly during initialization.

### Common configuration patterns

Typical configuration patterns include:

- Injecting values during build (for example, `process.env.*` replaced by a bundler).
- Passing configuration from a server-rendered page.
- Loading configuration from a global object populated at runtime.

The best approach depends on your application architecture and build tooling.

## Supported configuration settings [supported-configuration-settings]

EDOT Browser supports a subset of OpenTelemetry configuration options, plus Elastic-specific extensions.

### OpenTelemetry configuration

EDOT Browser supports a subset of OpenTelemetry SDK configuration options (often associated with `OTEL_*` environment variables in non-browser SDKs).

:::{note}
Some OpenTelemetry options are not applicable in a browser context. Unsupported options are ignored.
:::

Commonly used options include:

| Setting | Description |
|---|---|
| `service.name` | Logical name of the frontend service. Required. |
| `service.version` | Version of the application (optional). |
| `deployment.environment.name` | Environment name (for example, `prod` or `staging`). |
| `OTEL_LOG_LEVEL` | Log level for OpenTelemetry components (`error`, `warn`, `info`, `debug`, `verbose`). |

<!-- TODO: confirm final mapping of supported OpenTelemetry options in EDOT Browser -->

### Elastic-specific configuration

EDOT Browser might expose Elastic-specific configuration options prefixed with `ELASTIC_OTEL_`.

You can use these options to:

- Apply Elastic-specific defaults.
- Ensure compatibility with {{product.observability}}.
- Control optional enhancements.

:::{note}
Elastic-specific configuration options are still evolving. Refer to the configuration reference for the current list of supported settings.
:::

<!-- TODO: document supported ELASTIC_OTEL_* settings once finalized -->

## Minimal required configuration [minimal-required-configuration]

At a minimum, EDOT Browser requires:

- A service name to identify the frontend application
- An export endpoint that points to a reverse proxy

You can also set a log level, which is recommended during setup.

```js
import { initEDOTBrowser } from '@elastic/opentelemetry-browser';

initEDOTBrowser({
  serviceName: 'my-web-app',
  endpoint: 'https://telemetry.example.com',
  logLevel: 'info',
});
```

- `serviceName` identifies the browser application in {{product.observability}}.
- `endpoint` points to a reverse proxy, not directly to {{product.observability}}.
- `logLevel` controls diagnostic output in the browser console.

## Export endpoint configuration [export-endpoint-configuration]

Configure the export endpoint to point to a reverse proxy that forwards OTLP traffic to {{product.observability}}. Use the base URL of the proxy only: do not include signal paths such as `/v1/traces`, `/v1/metrics`, or `/v1/logs` in the endpoint. EDOT Browser adds these paths when exporting each signal.

Do not configure EDOT Browser to send data directly to:

- {{ecloud}} Managed OTLP endpoints
- An EDOT Collector that requires authentication

In a browser, authentication headers and secrets must be injected by the reverse proxy.

Use a service name that identifies your frontend application and does not contain special characters, so that data is correctly categorized in {{product.observability}}.

For details on reverse proxy and auth, refer to [OpenTelemetry for Real User Monitoring (RUM)](docs-content://solutions/observability/applications/otel-rum.md).

## Logging and diagnostics [logging-and-diagnostics]

EDOT Browser uses the OpenTelemetry diagnostic logger.

To troubleshoot setup issues, increase the log level during initialization:

```js
initEDOTBrowser({
  serviceName: 'my-web-app',
  endpoint: 'https://telemetry.example.com',
  logLevel: 'debug',
});
```

Diagnostic logs are written to the browser console.

## Configuration reference [configuration-reference]

The following sections expand as EDOT Browser matures:

- Full list of supported OpenTelemetry options
- Elastic-specific `ELASTIC_OTEL_*` options
- Default values and behavior
- Configuration precedence rules

<!-- TODO: expand configuration reference -->

## Next steps [next-steps]

- Refer to [Set up EDOT Browser](setup.md) for installation and initialization.
- Refer to [Metrics, traces, and logs](telemetry.md) for what each signal emits and limitations.
- Review [Supported technologies](supported-technologies.md) for browser and instrumentation support.
- Refer to [Troubleshooting](supported-technologies.md#troubleshooting) on the Supported technologies page for EDOT Browser–specific issues, or [OpenTelemetry ingest troubleshooting](docs-content://troubleshoot/ingest/opentelemetry/index.md) for general OTLP ingest issues.