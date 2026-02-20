---
navigation_title: EDOT Browser
description: Overview of the Elastic Distribution of OpenTelemetry Browser (EDOT Browser).
applies_to:
  stack: ga
  serverless:
    observability: ga
products:
  - id: cloud-serverless
  - id: observability
  - id: edot-sdk
---

# {{edot}} Browser

EDOT Browser is Elastic’s distribution of the OpenTelemetry Browser SDK. It provides a bundled, opinionated setup for collecting traces, metrics, and logs from real user interactions in web applications and exporting that data to {{product.observability}} using the OpenTelemetry Protocol (OTLP).

EDOT Browser is intended for Real User Monitoring (RUM) use cases, where telemetry is collected directly from users’ browsers to understand frontend performance, user interactions, and end-to-end request flows between frontend and backend services.

## What EDOT Browser provides [what-edot-browser-provides]

EDOT Browser is a wrapper around the contrib OpenTelemetry Browser SDK with Elastic-specific packaging and defaults. Its goals are to:

- Provide a single bundle that includes commonly used OpenTelemetry browser components and instrumentations.
- Offer opinionated defaults for collecting browser telemetry, optimized for use with {{product.observability}}.
- Ensure compatibility with Elastic ingest pipelines and data models when exporting OpenTelemetry data.
- Minimize Elastic-specific concepts and contribute improvements to the upstream OpenTelemetry project where possible.

EDOT Browser collects the following signals:

- **Traces**: For distributed tracing and frontend-to-backend correlation
- **Metrics**: Browser-side performance and runtime metrics
- **Logs**: Using the OpenTelemetry Logs API

For what each signal includes, known limitations, and what is not yet supported (such as Web Vitals), refer to [Metrics, traces, and logs](telemetry.md).

## How it works [how-it-works]

EDOT Browser runs in the user's browser as part of your web application. When initialized, it instruments the page and captures telemetry (traces, metrics, logs) from document load, user interactions, and network requests. Data is exported using the OpenTelemetry Protocol (OTLP) over HTTP to an endpoint you configure, typically a reverse proxy that injects authentication and forwards the data to {{product.observability}} or an OpenTelemetry Collector. Because the SDK runs in the browser, it cannot hold credentials; the reverse proxy is responsible for adding API keys or other auth before sending data to {{product.observability}}.

In {{product.observability}}, you see **`external.http`** spans for browser fetch and XHR requests, **user interaction** spans (for example, click, submit) that group related frontend and backend activity, and end-to-end traces from the browser to your backend in Discover and Service Maps. For details, refer to [What to expect in Kibana](setup.md#what-to-expect-in-kibana) in the setup guide.

## Limitations [limitations]

EDOT Browser is currently under active development. While the long-term goal is to provide feature parity with classic Elastic {{product.apm}} browser agents, that parity doesn't yet exist.

In particular:

- EDOT Browser is not a drop-in replacement for classic Elastic {{product.apm}} RUM agents.
- There is no supported migration path from classic agents at this time.
- Some features available in classic agents are not yet implemented.
- The exact set of provided instrumentations and defaults might change as development continues.

The following capabilities are not currently available in EDOT Browser:

- Web Vitals instrumentation
- Full feature parity with classic Elastic {{product.apm}} browser agents
- Migration tooling from classic agents

Some of these features might be introduced in the future, potentially through contrib OpenTelemetry contributions.

## EDOT Browser versus classic Elastic {{product.apm}} agents [edot-browser-versus-classic-agents]

Classic Elastic {{product.apm}} browser agents and EDOT Browser serve similar use cases but are built on different architectures.

Classic agents:

- Are Elastic-specific
- Provide mature RUM features out of the box
- Support features not yet available in EDOT Browser

EDOT Browser:

- Is based on OpenTelemetry standards
- Aims to align with contrib OpenTelemetry behavior
- Is still evolving toward feature parity

If you require full feature parity with classic Elastic {{product.apm}} RUM agents today, continue using the classic agents.

## Browser telemetry and authentication [browser-telemetry-and-authentication]

Because EDOT Browser runs in the user’s browser, it cannot safely embed authentication credentials such as API keys. Telemetry must be exported through a reverse proxy that sits between the browser and your OTLP endpoint ({{ecloud}} Managed OTLP or an EDOT Collector). The reverse proxy is required for three reasons:

- **Authentication**: The EDOT Collector or Managed OTLP endpoint expects an `Authorization` header with an API key. Putting that key in browser code would expose it to end users. The reverse proxy injects the header so the key stays on the server.
- **Cross-origin requests**: Your web application and the OTLP endpoint often have different origins. Browsers enforce Cross-Origin Resource Sharing (CORS); without the right headers, export requests are blocked. A reverse proxy on the same origin as your app (or configured to allow it) can add the required CORS headers and handle preflight `OPTIONS` requests.
- **Traffic control**: You can apply rate limiting or other controls at the proxy before traffic reaches the Collector or {{product.observability}}.

:::{warning}
Avoid using EDOT Browser alongside any other {{product.apm}} or RUM agent (including classic Elastic {{product.apm}} browser agents). Running multiple agents can cause conflicting instrumentation, duplicate telemetry, or unexpected behavior.
:::

### Example [example-reverse-proxy]

Example NGINX reverse proxy configuration that forwards telemetry from `webapp.example.com` to an EDOT Collector at `collector.example.com`, injects the required `Authorization` header, and handles CORS preflight:

```nginx
server {
    # Configuration for HTTP/HTTPS goes here
    location / {
        # Take care of preflight requests
        if ($request_method = 'OPTIONS') {
            add_header 'Access-Control-Max-Age' 1728000;
            add_header 'Access-Control-Allow-Origin' 'webapp.example.com' always;
            add_header 'Access-Control-Allow-Headers' 'Accept,Accept-Language,Authorization,Content-Language,Content-Type' always;
            add_header 'Access-Control-Allow-Credentials' 'true' always;
            add_header 'Content-Type' 'text/plain charset=UTF-8';
            add_header 'Content-Length' 0;
            return 204;
        }

        add_header 'Access-Control-Allow-Origin' 'webapp.example.com' always;
        add_header 'Access-Control-Allow-Credentials' 'true' always;
        add_header 'Access-Control-Allow-Headers' 'Accept,Accept-Language,Authorization,Content-Language,Content-Type' always;
        proxy_http_version 1.1;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        # Set the auth header for the Collector here. Follow security best practices
        # for adding secrets (for example Docker secrets, Kubernetes Secrets).
        proxy_set_header Authorization 'ApiKey ...your Elastic API key...';
        proxy_pass https://collector.example.com:4318;
    }
}
```

### Browser constraints [browser-constraints]

If your site uses a Content Security Policy (CSP), add the domain of your OTLP endpoint (or reverse proxy) to the `connect-src` directive so the browser allows export requests. For example: `connect-src 'self' https://telemetry.example.com`.

If your app and the export endpoint have different origins, the browser might block requests unless CORS is correctly configured. The reverse proxy must send `Access-Control-Allow-Origin` matching your application origin, handle `OPTIONS` preflight requests with a 204 response, and include `Authorization` in `Access-Control-Allow-Headers` when using API key authentication. The NGINX example above shows one way to do this.

For more details on reverse proxy setup, CORS, and CSP, refer to [OpenTelemetry for Real User Monitoring (RUM)](docs-content://solutions/observability/applications/otel-rum.md).

## Next steps [next-steps]

To get started with EDOT Browser:

- Follow the setup instructions in [Set up EDOT Browser](setup.md)
- Review configuration options in [Configure EDOT Browser](configuration.md)
- Refer to [Supported technologies](supported-technologies.md) for details on browsers and instrumentations