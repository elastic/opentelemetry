---
navigation_title: Troubleshooting
description: Troubleshoot EDOT Browser telemetry export and common issues.
applies_to:
  stack: ga
  serverless:
    observability: ga
products:
  - id: cloud-serverless
  - id: observability
  - id: edot-sdk
---

# Troubleshooting EDOT Browser

If telemetry doesn't appear in {{product.observability}}, try the following:

- Confirm the `otlpEndpoint` option points to your reverse proxy (not directly to {{product.observability}}) and doesn't include signal paths like `/v1/traces`.
- Check the browser console for network errors or OpenTelemetry-related messages. Cross-Origin Resource Sharing (CORS) errors often mean the reverse proxy is not sending the right `Access-Control-Allow-Origin` or preflight response.
- Ensure the reverse proxy can reach your EDOT Collector or {{ecloud}} Managed OTLP endpoint. To do so, check proxy logs for connection or authorization failures.
- Ensure service name is set and doesn't contain special characters.
- Set `logLevel` to `debug` or `verbose` in the `startBrowserSdk` options to see detailed export and instrumentation output in the console.

If you use a Content Security Policy, ensure the proxy or OTLP endpoint domain is in the `connect-src` directive. For bundler or module resolution errors, refer to [OpenTelemetry for Real User Monitoring (RUM)](docs-content://solutions/observability/applications/otel-rum.md) and the general [OpenTelemetry ingest troubleshooting](docs-content://troubleshoot/ingest/opentelemetry/index.md) docs.

## Next steps [next-steps]

- Refer to [Known limitations](supported-technologies.md#known-limitations) for what is not yet supported.
- Refer to [Set up EDOT Browser](setup.md) for installation and initialization.
- For general OTLP ingest issues, refer to [OpenTelemetry ingest troubleshooting](docs-content://troubleshoot/ingest/opentelemetry/index.md).
