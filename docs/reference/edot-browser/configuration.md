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

This page explains how to configure EDOT Browser, which settings are supported, and what’s required to start exporting browser telemetry.

EDOT Browser follows OpenTelemetry configuration conventions where possible. Like the upstream OpenTelemetry Browser SDK, it uses explicit configuration at initialization rather than environment variables, which are not available in the browser.

## Configuration model in the browser [configuration-model-in-the-browser]

EDOT Browser runs in your users’ browsers. This has important implications:

- Environment variables exist at build time, when your app is bundled. For example, a bundler replaces `process.env.*` with values. However, the variables are not available at runtime, meaning when the app runs in the browser. You can provide configuration at build time (bundler-defined constants) or at runtime (options passed to the initialization function).
- Never embed secrets in browser configuration.

EDOT Browser does not read `OTEL_*` variables directly. Instead, it accepts configuration values passed explicitly during initialization.

### Common configuration patterns

Typical configuration patterns include:

- Injecting values during build (for example, `process.env.*` replaced by a bundler).
- Passing configuration from a server-rendered page.
- Loading configuration from a global object populated at runtime.

The best approach depends on your application architecture and build tooling.

## Supported configuration settings [supported-configuration-settings]

Configuration is passed as an object to `startBrowserSdk`. The following options are supported:

| Option | Description |
|---|---|
| `serviceName` | Logical name of the frontend service. Defaults to `unknown_service:web` if not set. |
| `serviceVersion` | Version of the application. Optional. |
| `logLevel` | Diagnostic log level (`error`, `warn`, `info`, `debug`, `verbose`). Defaults to `info`. |
| `otlpEndpoint` | Base URL of the OTLP export endpoint (reverse proxy). Do not include signal paths such as `/v1/traces`. Defaults to `http://localhost:4318`. |
| `sampleRate` | Trace sampling ratio (0–1). Defaults to `1` (100%). |
| `resourceAttributes` | Optional resource attributes to attach to telemetry. |
| `exportHeaders` | Headers to send with export requests. Defaults to `{}`. The reverse proxy typically injects `Authorization`; do not put API keys here in browser code. |
| `disabled` | If `true`, the SDK does not start. |
| `configInstrumentations` | Per-instrumentation config. Set `enabled: false` for a key to turn off that instrumentation. |

## Minimal required configuration [minimal-required-configuration]

At a minimum, EDOT Browser requires:

- A service name to identify the frontend application
- An export endpoint that points to a reverse proxy

You can also set a log level, which is recommended during setup.

```js
import { startBrowserSdk } from '@elastic/opentelemetry-browser';

startBrowserSdk({
  serviceName: 'my-web-app',
  otlpEndpoint: 'https://telemetry.example.com',
  logLevel: 'info',
});
```

- `serviceName` identifies the browser application in {{product.observability}}.
- `otlpEndpoint` points to a reverse proxy, not directly to {{product.observability}}.
- `logLevel` controls diagnostic output in the browser console.

## Export endpoint configuration [export-endpoint-configuration]

Configure `otlpEndpoint` to point to a reverse proxy that forwards OTLP traffic to {{product.observability}}. Use the base URL of the proxy only: do not include signal paths such as `/v1/traces`, `/v1/metrics`, or `/v1/logs`. The SDK appends these paths when exporting each signal.

Use a service name that identifies your frontend application and doesn't contain special characters, so that data is correctly categorized in {{product.observability}}.

For details on reverse proxy and authorization, refer to [OpenTelemetry for Real User Monitoring (RUM)](docs-content://solutions/observability/applications/otel-rum.md).

## Logging and diagnostics [logging-and-diagnostics]

EDOT Browser uses the OpenTelemetry diagnostic logger.

To troubleshoot setup issues, increase the log level when calling `startBrowserSdk`:

```js
import { startBrowserSdk } from '@elastic/opentelemetry-browser';

startBrowserSdk({
  serviceName: 'my-web-app',
  otlpEndpoint: 'https://telemetry.example.com',
  logLevel: 'debug',
});
```

Diagnostic logs are written to the browser console. For more information on using debug logging to troubleshoot issues, refer to [Enable debug logging for EDOT SDKs](docs-content://troubleshoot/ingest/opentelemetry/edot-sdks/enable-debug-logging.md) and [Enable debug logging](docs-content://troubleshoot/ingest/opentelemetry/edot-collector/enable-debug-logging.md) (Collector).

## Next steps [next-steps]

- Refer to [Set up EDOT Browser](setup.md) for installation and initialization.
- Refer to [Metrics, traces, and logs](telemetry.md) for what each signal emits and limitations.
- Review [Supported technologies](supported-technologies.md) for browser and instrumentation support.
- Refer to [Troubleshooting](troubleshooting.md) for EDOT Browser–specific issues, or [OpenTelemetry ingest troubleshooting](docs-content://troubleshoot/ingest/opentelemetry/index.md) for general OTLP ingest issues.