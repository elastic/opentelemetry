---
navigation_title: Metrics, traces, and logs
description: What EDOT Browser emits for each telemetry signal and known limitations.
applies_to:
  stack: ga
  serverless:
    observability: ga
products:
  - id: cloud-serverless
  - id: observability
  - id: edot-sdk
---

# Metrics, traces, and logs

EDOT Browser can export all three OpenTelemetry signals—metrics, traces, and logs—to {{product.observability}} using OTLP. This page describes what is currently emitted for each signal, known limitations of browser-based telemetry, and what is not yet supported.

## Metrics [metrics]

### What EDOT Browser currently emits [metrics-what-is-emitted]

EDOT Browser configures the OpenTelemetry MeterProvider and exports metrics over OTLP when metrics are turned on. The exact set of built-in metrics is still evolving. Metrics might be produced by:

- **Long task instrumentation**: When long task instrumentation is included and turned on, it can report observations related to main-thread blocking (for example long tasks exceeding a threshold). The names and attributes of these metrics depend on the instrumentation implementation.
- **Custom metrics**: Your application can create meters and instruments (counters, histograms, and so on) using the OpenTelemetry Metrics API. EDOT Browser exports those metrics along with any SDK-provided ones.

If you turn on metrics export, ensure your reverse proxy and OTLP endpoint accept the `/v1/metrics` path.

### Known limitations of browser-side metrics [metrics-limitations]

- Metrics are collected in the user’s browser and represent a single session or page. There is no server-side aggregation, each export batch reflects one client’s view.
- Browsers have limited resources. High-cardinality or high-frequency metrics can affect performance and export payload size. Use caution with unbounded attributes (for example user IDs, dynamic URLs) on metrics.
- Metrics are only sent when the SDK exports (for example on an interval or when the page is unloaded). Temporary or single-page sessions might produce few data points.
- Browser environments vary (device, network, extensions). Metric values might be noisier or less consistent than server-side metrics.

:::{note}
Web Vitals (such as Largest Contentful Paint (LCP), First Input Delay (FID), Cumulative Layout Shift (CLS), and related metrics) are not supported in EDOT Browser. There is no built-in Web Vitals instrumentation. If you need Web Vitals or similar Core Web Vitals data, use classic Elastic {{product.apm}} browser agents or a dedicated Web Vitals library.
:::

## Traces [traces]

### What EDOT Browser currently emits [traces-what-is-emitted]

EDOT Browser initializes tracing and registers instrumentations that produce spans:

- Spans for the initial document load and related navigation timing, when the document load instrumentation is included and turned on.
- Each outgoing request using `fetch` or `XMLHttpRequest` is captured as an **`external.http`** span with attributes such as URL, HTTP method, and status code. These spans represent the client-side portion of the request.
- Spans for user actions such as "click" and "submit". These interaction spans group the subsequent work (for example `external.http` requests) so you can attribute frontend and backend activity to a specific user action in {{product.observability}}.

When your backend is instrumented with OpenTelemetry and trace context (trace ID, span ID) is propagated in HTTP headers, the browser’s `external.http` span and the backend spans appear in the same trace, giving you end-to-end visibility in Discover and Service Maps. Refer to [What to expect in Kibana](setup.md#what-to-expect-in-kibana) for how these traces appear in the Observability app.

### Known limitations of browser-side traces [traces-limitations]

- Frontend-to-backend trace continuity depends on your backend and HTTP client propagating the W3C Trace Context headers. If propagation is not configured, browser and backend spans appear as separate traces.
- Only requests that go through the instrumented `fetch` and `XMLHttpRequest` APIs are captured. Requests made by other mechanisms (for example some third-party scripts, WebSockets, or non-instrumented clients) do not produce spans unless you add custom instrumentation.
- Sampling is applied in the browser. High traffic can lead to large trace volume, so configure sampling or export options appropriately.
- Traces are tied to the page and session. Cross-tab or cross-origin flows might not form a single trace unless you implement custom context propagation.

:::{note}
Full feature parity with classic Elastic {{product.apm}} RUM agents for tracing (for example, certain automatic instrumentations or span types) is not yet available.
:::

## Logs [logs]

### What EDOT Browser currently emits [logs-what-is-emitted]

EDOT Browser supports the OpenTelemetry Logs API. When the LoggerProvider is configured and logs are exported using OTLP:

- **Application logs**: Your application code can obtain a logger from the OpenTelemetry API and emit log records (severity, body, attributes). EDOT Browser exports these records to your configured endpoint on the `/v1/logs` path.
- **Resource and context**: Log records are associated with the same resource (for example service name) and can optionally be linked to the active trace context, so you can correlate logs with traces in {{product.observability}}.

There is no requirement to use logs. If you do not create log records or do not configure log export, no log data is sent.

### Known limitations of browser-side logs [logs-limitations]

- Logs are buffered in the browser and sent on the export cycle. High log volume can increase memory use and export payload size, and might affect page performance. Prefer sampling or severity filtering for noisy logs.
- As with metrics, logs reflect a single client session. You do not get centralized log aggregation in the browser, that happens in {{product.observability}} after export.
- Logs that are not exported before the user navigates away or closes the tab might be lost unless the SDK supports a reliable flush (for example on `beforeunload`). Be aware that some log data might not reach the backend in edge cases.

:::{note}
Automatic capture of `console` methods (for example `console.log`, `console.error`) is not provided by EDOT Browser. To send logs to {{product.observability}}, you must use the OpenTelemetry Logs API from your application code. Automatic console instrumentation might be considered in the future.
:::

## Next steps [next-steps]

- Refer to [Set up EDOT Browser](setup.md) for installation and export configuration.
- Refer to [What to expect in {{kib}}](setup.md#what-to-expect-in-kibana) for how traces appear in the Observability app.
- Refer to [Supported technologies](supported-technologies.md) for included instrumentations and [Configure EDOT Browser](configuration.md) for turning signals and instrumentations on or off.
