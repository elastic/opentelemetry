---
navigation_title: Supported technologies
description: Supported browsers, instrumentations, and known differences in EDOT Browser.
applies_to:
  stack: ga
  serverless:
    observability: ga
products:
  - id: cloud-serverless
  - id: observability
  - id: edot-sdk
---

# Supported technologies

This page lists:

- Supported browser versions
- Included instrumentations and their default behavior
- Differences between EDOT Browser and contrib OpenTelemetry JS

## Supported browsers [supported-browsers]

EDOT Browser is designed to run in modern evergreen browsers.

| Browser | Supported versions |
|----------|--------------------|
| Chrome   | TODO |
| Edge     | TODO |
| Firefox  | TODO |
| Safari   | TODO |

:::{note}
Internet Explorer is not supported.
:::

### Browser requirements

At a minimum, the runtime environment must support:

- ES2018 (or later) language features
- `fetch` API
- `Promise`
- `Performance` and `PerformanceObserver` APIs

<!-- TODO: confirm exact language target and polyfill expectations -->

If your application targets older browsers, you might need to provide polyfills. EDOT Browser does not ship with built-in polyfills.

## Included instrumentations [included-instrumentations]

EDOT Browser bundles a curated set of OpenTelemetry JS instrumentations suitable for browser environments.

The following table lists instrumentations that are currently included:

| Instrumentation | Included | On by default | Notes |
|-----------------|----------|-------------------|-------|
| Document load   | TODO     | TODO              | TODO |
| Fetch           | TODO     | TODO              | TODO |
| XMLHttpRequest  | TODO     | TODO              | TODO |
| User interaction| TODO     | TODO              | TODO |
| Long tasks      | TODO     | TODO              | TODO |

<!-- TODO: replace with actual instrumentation package names and behavior -->

### Default behavior

By default, EDOT Browser:

- Initializes tracing
- Registers included instrumentations
- Configures an OTLP exporter
- Applies Elastic-specific defaults (for example, resource detection or attribute normalization)

<!-- TODO: document actual defaults once finalized -->

You can turn off or override instrumentations during initialization if needed.

<!-- TODO: document customization API once stable -->

## Differences from contrib OpenTelemetry JS [differences-from-upstream]

EDOT Browser builds on top of contrib OpenTelemetry JS, but introduces several differences to simplify setup and align with {{product.observability}}.

### Configuration model

- EDOT Browser doesn't read environment variables at runtime.
- Configuration must be passed explicitly during initialization.
- Elastic-specific configuration options might be available.

### Export behavior

- EDOT Browser expects telemetry to be sent to a reverse proxy.
- Direct export to authenticated OTLP endpoints is not supported in the browser.
- Authentication headers must be injected by infrastructure outside the browser.

### Defaults and opinionated setup

Compared to contrib OpenTelemetry JS:

- EDOT Browser provides a simplified initialization API.
- A curated set of instrumentations is preconfigured.
- Sensible defaults are applied for Elastic ingestion.

<!-- TODO: add concrete comparison once API stabilizes -->

### Scope limitations

Some contrib OpenTelemetry JS features are not available or are intentionally unsupported in EDOT Browser due to browser constraints.

These might include:

- Environment-based configuration
- Certain resource detectors
- Node.js-specific instrumentation

<!-- TODO: enumerate unsupported features explicitly -->

## Version compatibility [version-compatibility]

| Component | Version |
|----------|---------|
| OpenTelemetry JS API | TODO |
| OpenTelemetry JS SDK | TODO |

<!-- TODO: document compatibility matrix once versioning strategy is defined -->

## Known limitations [known-limitations]

When using EDOT Browser with {{product.observability}}, be aware of the following:

- API key authentication requires a reverse proxy; credentials cannot be stored in the browser.
- Metrics from browser-based RUM might have more limited utility than backend metrics, depending on your use case.
- Some OpenTelemetry browser instrumentations are still experimental. Behavior might change.
- Monitor the performance impact on the browser when using multiple instrumentations, especially on lower-end devices.

## Troubleshooting [troubleshooting]

If telemetry does not appear in {{product.observability}}:

- Confirm the export endpoint points to your reverse proxy (not directly to {{product.observability}}) and doesn't include signal paths like `/v1/traces`.
- Check the browser console for network errors or OpenTelemetry-related messages. Cross-Origin Resource Sharing (CORS) errors often mean the reverse proxy is not sending the right `Access-Control-Allow-Origin` or preflight response.
- Ensure the reverse proxy can reach your EDOT Collector or {{ecloud}} Managed OTLP endpoint; check proxy logs for connection or auth failures.
- Ensure service name is set and doesn't contain special characters.
- Set the log level to `debug` or `verbose` during initialization to check the detailed export and instrumentation output in the console.

If you use a Content Security Policy, ensure the proxy or OTLP endpoint domain is in the `connect-src` directive. For bundler or module resolution errors, refer to [OpenTelemetry for Real User Monitoring (RUM)](docs-content://solutions/observability/applications/otel-rum.md) and the general [OpenTelemetry ingest troubleshooting](docs-content://troubleshoot/ingest/opentelemetry/index.md) docs.

## Next steps [next-steps]

- Refer to [Set up EDOT Browser](setup.md) to get started.
- Refer to [Metrics, traces, and logs](telemetry.md) for what is emitted per signal and what is not yet supported.
- Review [Configuration](configuration.md) to customize behavior.
- Refer to [Known limitations](#known-limitations) and [Troubleshooting](#troubleshooting) above for EDOT Browser–specific guidance, or [OpenTelemetry ingest troubleshooting](docs-content://troubleshoot/ingest/opentelemetry/index.md) for general OTLP ingest issues.