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

EDOT Browser runs directly in users' browsers. Because of browser security constraints, authentication and data export require a reverse proxy. When your OTLP endpoint is available ({{ecloud}} Managed OTLP or an EDOT Collector), do the following:

- [Install the agent](install-agent.md): Add EDOT Browser to your application (package or bundle) and initialize it.
- [Configure proxy and CORS](proxy-cors.md): Set up a reverse proxy in front of your OTLP endpoint and configure CORS so the browser can export telemetry securely.

:::{note}
Do not run EDOT Browser alongside another {{product.apm}} or RUM agent (including classic Elastic {{product.apm}} browser agents). Multiple agents can cause conflicting instrumentation, duplicate telemetry, or unexpected behavior.
:::

## Prerequisites [prerequisites]

Before you set up EDOT Browser, you need:

- An {{product.observability}} deployment ({{ecloud}} or self-managed)
- An OTLP ingest endpoint ({{ecloud}} Managed OTLP or an EDOT Collector)

## How browser telemetry is exported [how-browser-telemetry-is-exported]

EDOT Browser exports telemetry using the OpenTelemetry Protocol (OTLP) over HTTP. Data flows as follows:

**Browser (EDOT Browser) → Reverse proxy → {{ecloud}} Managed OTLP endpoint or EDOT Collector → {{product.observability}}**

The browser sends OTLP data to the reverse proxy endpoint that you configure.

## What to expect in {{kib}} [what-to-expect-in-kibana]

After EDOT Browser is sending telemetry to {{product.observability}}, you can inspect traces and spans in the Observability app. The following describes what you see and how to interpret it.

### Spans from browser fetch and XHR [spans-from-fetch-xhr]

Outgoing HTTP requests made with the browser `fetch` API or `XMLHttpRequest` are captured as `external.http` spans. Each request to your backend APIs or third-party domains appears as an `external.http` span with attributes such as URL, HTTP method, and status code. These spans represent the client-side portion of the request (time in the browser) and, when your backend is instrumented with EDOT, link to the corresponding server-side trace using the trace context (trace ID and span ID) propagated in HTTP headers. In the trace view, you see the browser's `external.http` span as part of the same trace as the backend service spans when propagation is correctly configured.

### User interaction spans and grouping [user-interaction-spans]

EDOT Browser creates user interaction spans for events such as "click" and "submit". These spans represent the user action that triggered subsequent work (for example, a button click that leads to a `fetch` call). In {{kib}}, user interaction spans are used to group related spans: the interaction span is the logical parent or anchor for the cascade of operations that follow (for example, `external.http` requests and any child spans). When you analyze a trace, look for the user interaction span (for example, `userinteraction` or similar) to understand which click or submit caused the associated network and backend activity. This grouping makes it easier to attribute frontend and backend work to specific user actions.

### Frontend-to-backend traces in Discover and Service Maps [frontend-backend-in-discover-and-service-maps]

Traces that start in the browser (from a user interaction) and continue to your backend appear as end-to-end traces in {{product.observability}}:

- **Discover**: When you search or filter by your frontend service name or by trace ID, you see trace documents that include both browser-originated spans (for example, user interaction, `external.http`) and backend service spans, as long as trace context is propagated from the browser to the server. You can inspect the full path of a request from the user action through the frontend to backend services.
- **Service Maps**: Your frontend application appears as a service node. Connections from that node to backend services are derived from the same trace data: when a browser `external.http` span targets a backend that is also instrumented and reported to {{product.observability}}, a dependency link is shown between the frontend and that backend service. This gives you a map of how browser traffic flows to your backend services.

For more on how RUM and distributed traces appear in the Observability app, refer to [User experience (RUM)](docs-content://solutions/observability/applications/user-experience.md).

## Next steps [next-steps]

After completing setup:

- Refer to [Install the agent](install-agent.md) and [Proxy and CORS](proxy-cors.md) for installation and proxy configuration.
- Refer to [Configure EDOT Browser](configuration.md) to customize behavior and defaults.
- Refer to [Metrics, traces, and logs](telemetry.md) for what is emitted for each signal and known limitations.
- Review [Supported technologies](supported-technologies.md) for information about browsers, bundlers, and instrumentations.
- If telemetry doesn't appear, refer to [Troubleshooting](troubleshooting.md).
