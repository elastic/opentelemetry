---
navigation_title: Set up
description: Set up the Elastic Distribution of OpenTelemetry Browser (EDOT Browser).
applies_to:
  stack:
  serverless:
    observability:
products:
  - id: cloud-serverless
  - id: observability
  - id: edot-sdk
---

# Set up EDOT Browser

This guide shows you how to set up the {{edot}} Browser (EDOT Browser) in a web application and export browser telemetry to {{product.observability}}.

EDOT Browser runs directly in users’ browsers. Because of browser security constraints, setup differs from backend OpenTelemetry SDKs, especially for authentication and data export. Review the reverse proxy requirements before you begin.

## Prerequisites

Before you set up EDOT Browser, you need:

- An {{product.observability}} deployment ({{ecloud}} or self-managed)
- An OTLP ingest endpoint ({{ecloud}} Managed OTLP or an EDOT Collector)
- A reverse proxy that:
  - Accepts telemetry from the browser
  - Injects authentication headers
  - Forwards data to Elastic

For information about OTLP endpoints, reverse proxy configuration, authentication, CORS, and CSP, refer to OpenTelemetry for Real User Monitoring (RUM).

## Install EDOT Browser

EDOT Browser is distributed as a single bundle that packages the OpenTelemetry Browser SDK with Elastic-specific defaults.

Install EDOT Browser using your package manager:

```bash
# example
npm install @elastic/opentelemetry-browser
```

<!-- TODO: confirm final package name -->

## Initialize EDOT Browser

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
  endpoint: 'https://telemetry.example.com', // reverse proxy URL
});
```

<!-- TODO: update API shape and options once finalized -->

At a minimum, configure:

- The service name used to identify your frontend application
- The export endpoint, which must point to your reverse proxy (not directly to Elastic)

For additional configuration options, refer to Configure EDOT Browser.

## How browser telemetry is exported

EDOT Browser exports telemetry using the OpenTelemetry Protocol (OTLP) over HTTP.

Data flows as follows:

```
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

## Reverse proxy requirement

Do not send telemetry directly from the browser to Elastic using an API key.

Any credentials included in browser code are visible to end users and can be misused. EDOT Browser requires a reverse proxy in front of the OTLP endpoint.

This pattern applies to:

- {{ecloud}} Managed OTLP endpoints
- An EDOT Collector running in gateway mode

For complete examples and security considerations, refer to OpenTelemetry for Real User Monitoring (RUM).

## Next steps

After completing setup:

- See Configure EDOT Browser to customize behavior and defaults
- Review Supported technologies for information about browsers and instrumentations
- Read What to expect in Elastic to understand how browser traces appear in Discover and Service Maps