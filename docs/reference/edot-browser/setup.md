---
navigation_title: Set up
description: Set up the Elastic Distribution of OpenTelemetry Browser (EDOT Browser).
applies_to:
  stack: ga
  serverless:
    observability: ga
products:
  - id: cloud-serverless
  - id: observability
  - id: edot-sdk
---

# Set up EDOT Browser

This guide shows you how to set up the {{edot}} Browser (EDOT Browser) in a web application and export browser telemetry to {{product.observability}}.

EDOT Browser runs directly in users’ browsers. Because of browser security constraints, setup differs from backend OpenTelemetry SDKs, especially for authentication and data export. Review the reverse proxy requirements before you begin.

:::{warning}
Do not run EDOT Browser alongside another {{product.apm}} or RUM agent (including classic Elastic {{product.apm}} browser agents). Multiple agents can cause conflicting instrumentation, duplicate telemetry, or unexpected behavior.
:::

## Prerequisites [prerequisites]

Before you set up EDOT Browser, you need:

- An {{product.observability}} deployment ({{ecloud}} or self-managed)
- An OTLP ingest endpoint ({{ecloud}} Managed OTLP or an EDOT Collector)
- A reverse proxy that accepts telemetry from the browser, injects authentication headers, and forwards data to your OTLP endpoint. You need a reverse proxy because: 
  - API keys cannot be stored in browser code. 
  - The browser and endpoint often have different origins, so CORS must be handled.
  - You can apply rate limiting or other controls at the proxy.

For more on OTLP endpoints, reverse proxy configuration, authentication, CORS, and CSP, refer to [OpenTelemetry for Real User Monitoring (RUM)](docs-content://solutions/observability/applications/otel-rum.md).

## Install EDOT Browser [install-edot-browser]

EDOT Browser is distributed as a single bundle that packages the OpenTelemetry Browser SDK with Elastic-specific defaults.

Install EDOT Browser using your package manager:

```bash
# example
npm install @elastic/opentelemetry-browser
```

<!-- TODO: confirm final package name -->

## Initialize EDOT Browser [initialize-edot-browser]

Initialize EDOT Browser as early as possible in your application lifecycle so it can capture initial page loads, user interactions, and network requests.

Initialize it:

- At the top of your application entry point
- In a framework-specific bootstrap location (for example, a React root component, Angular `main.ts`, or a Vue plugin)

A minimal example:

```js
// example
import { initEDOTBrowser } from '@elastic/opentelemetry-browser';

initEDOTBrowser({
  serviceName: 'my-web-app',
  endpoint: 'https://telemetry.example.com', // reverse proxy URL; do not include /v1/traces or other signal paths
});
```

<!-- TODO: update API shape and options once finalized -->

At a minimum, configure:

- The service name used to identify your frontend application
- The export endpoint, which must point to your reverse proxy (not directly to {{product.observability}})

For additional configuration options, refer to [Configure EDOT Browser](configuration.md).

You have successfully initialized EDOT Browser when the SDK loads without errors in the browser console and telemetry begins flowing to your reverse proxy. To confirm data in {{product.observability}}, open the Observability app and check for your service and traces.

## What to expect in {{kib}} [what-to-expect-in-kibana]

After EDOT Browser is sending telemetry to {{product.observability}}, you can inspect traces and spans in the Observability app. The following describes what you see and how to interpret it.

### Spans from browser fetch and XHR [spans-from-fetch-xhr]

Outgoing HTTP requests made with the browser `fetch` API or `XMLHttpRequest` are captured as **`external.http`** spans. Each request to your backend APIs or third-party domains appears as an `external.http` span with attributes such as URL, HTTP method, and status code. These spans represent the client-side portion of the request (time in the browser) and, when your backend is instrumented with OpenTelemetry, link to the corresponding server-side trace using the trace context (trace ID and span ID) propagated in HTTP headers. In the trace view, you see the browser’s `external.http` span as part of the same trace as the backend service spans when propagation is correctly configured.

### User interaction spans and grouping [user-interaction-spans]

EDOT Browser creates user interaction spans for events such as "click" and "submit". These spans represent the user action that triggered subsequent work (for example, a button click that leads to a `fetch` call). In {{kib}}, user interaction spans are used to group related spans: the interaction span is the logical parent or anchor for the cascade of operations that follow (for example, `external.http` requests and any child spans). When you analyze a trace, look for the user interaction span (for example, `userinteraction` or similar) to understand which click or submit caused the associated network and backend activity. This grouping makes it easier to attribute frontend and backend work to specific user actions.

### Frontend-to-backend traces in Discover and Service Maps [frontend-backend-in-discover-and-service-maps]

Traces that start in the browser (from a user interaction) and continue to your backend appear as end-to-end traces in {{product.observability}}:

- **Discover**: When you search or filter by your frontend service name or by trace ID, you see trace documents that include both browser-originated spans (for example, user interaction, `external.http`) and backend service spans, as long as trace context is propagated from the browser to the server. You can inspect the full path of a request from the user action through the frontend to backend services.
- **Service Maps**: Your frontend application appears as a service node. Connections from that node to backend services are derived from the same trace data: when a browser `external.http` span targets a backend that is also instrumented and reported to {{product.observability}}, a dependency link is shown between the frontend and that backend service. This gives you a map of how browser traffic flows to your backend services.

For more on how RUM and distributed traces appear in the Observability app, refer to [User experience (RUM)](docs-content://solutions/observability/applications/user-experience.md).

## How browser telemetry is exported [how-browser-telemetry-is-exported]

EDOT Browser exports telemetry using the OpenTelemetry Protocol (OTLP) over HTTP.

Data flows as follows:

```text
Browser (EDOT Browser)
  → Reverse proxy
    → {{ecloud}} Managed OTLP endpoint
      or EDOT Collector
        → {{product.observability}}
```

The browser sends OTLP data to the reverse proxy endpoint that you configure. The reverse proxy:

- Injects authentication headers (for example, Elastic API keys)
- Handles CORS preflight requests
- Optionally applies rate limiting or traffic controls

## Reverse proxy requirement [reverse-proxy-requirement]

Do not send telemetry directly from the browser to {{product.observability}} using an API key.

Any credentials included in browser code are visible to end users and can be misused. EDOT Browser requires a reverse proxy in front of the OTLP endpoint.

This pattern applies to:

- {{ecloud}} Managed OTLP endpoints
- An EDOT Collector running in gateway mode

### Browser constraints: CSP and CORS [browser-constraints]

If your site uses a Content Security Policy (CSP), add the domain of your reverse proxy or OTLP endpoint to the `connect-src` directive so the browser allows export requests. For example: `connect-src 'self' https://telemetry.example.com`.

If your web application and the export endpoint have different origins, the browser might block requests unless CORS is configured. Your reverse proxy must return `Access-Control-Allow-Origin` matching your application origin, respond to `OPTIONS` preflight requests with 204, and include `Authorization` in `Access-Control-Allow-Headers` when using API key auth. The [overview page](index.md#example-reverse-proxy) includes an NGINX example.

For complete examples and security considerations, refer to [OpenTelemetry for Real User Monitoring (RUM)](docs-content://solutions/observability/applications/otel-rum.md).

## Next steps [next-steps]

After completing setup:

- Refer to [What to expect in {{kib}}](#what-to-expect-in-kibana) above for the span types and views you see (for example, `external.http`, user interaction grouping, Discover and Service Maps).
- Refer to [Metrics, traces, and logs](telemetry.md) for what is emitted for each signal and known limitations.
- Refer to [Configure EDOT Browser](configuration.md) to customize behavior and defaults.
- Review [Supported technologies](supported-technologies.md) for information about browsers and instrumentations.
- Read [User experience (RUM)](docs-content://solutions/observability/applications/user-experience.md) for more on how browser traces appear in the Observability app.