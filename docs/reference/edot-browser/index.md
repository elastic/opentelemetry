---
navigation_title: EDOT Browser
description: Overview of the Elastic Distribution of OpenTelemetry Browser (EDOT Browser).
applies_to:
  stack:
  serverless:
    observability:
products:
  - id: cloud-serverless
  - id: observability
  - id: edot-sdk
---

# {{edot}} Browser

EDOT Browser is Elastic’s distribution of the OpenTelemetry Browser SDK. It provides a bundled, opinionated setup for collecting traces, metrics, and logs from real user interactions in web applications and exporting that data to {{product.observability}} using the OpenTelemetry Protocol (OTLP).

EDOT Browser is intended for Real User Monitoring (RUM) use cases, where telemetry is collected directly from users’ browsers to understand frontend performance, user interactions, and end-to-end request flows between frontend and backend services.

## What EDOT Browser provides

EDOT Browser is a wrapper around the contrib OpenTelemetry Browser SDK with Elastic-specific packaging and defaults. Its goals are to:

- Provide a single bundle that includes commonly used OpenTelemetry browser components and instrumentations.
- Offer opinionated defaults for collecting browser telemetry, optimized for use with {{product.observability}}.
- Ensure compatibility with Elastic ingest pipelines and data models when exporting OpenTelemetry data.
- Minimize Elastic-specific concepts and contribute improvements contrib where possible.

EDOT Browser collects the following signals:

- **Traces**: For distributed tracing and frontend-to-backend correlation
- **Metrics**: Browser-side performance and runtime metrics
- **Logs**: Using the OpenTelemetry Logs API

## Limitations

EDOT Browser is currently under active development. While the long-term goal is to provide feature parity with classic Elastic {{product.apm}} browser agents, that parity does not yet exist.

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

## EDOT Browser versus classic Elastic {{product.apm}} agents

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

## Browser telemetry and authentication

Because EDOT Browser runs in the user’s browser, it cannot safely embed authentication credentials such as API keys. For this reason, EDOT Browser exports telemetry through a reverse proxy that injects authentication headers before forwarding data to Elastic or an OpenTelemetry Collector.

### Example

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

For full details on the reverse proxy, CORS, CSP, and securing browser telemetry exports, refer to [OpenTelemetry for Real User Monitoring (RUM)](https://www.elastic.co/docs/solutions/observability/applications/otel-rum).

## Next steps

To get started with EDOT Browser:

- Follow the setup instructions in Set up EDOT Browser
- Review configuration options in Configure EDOT Browser
- Refer to Supported technologies for details on browsers and instrumentations