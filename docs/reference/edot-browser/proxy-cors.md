---
navigation_title: Proxy and CORS
description: Configure a reverse proxy and CORS for EDOT Browser telemetry export.
applies_to:
  stack: ga
  serverless:
    observability: ga
products:
  - id: cloud-serverless
  - id: observability
  - id: edot-sdk
---

# Proxy and CORS configuration

EDOT Browser exports telemetry from the user's browser to an OTLP endpoint. You must put a reverse proxy in front of your OTLP endpoint and configure it for authentication and Cross-Origin Resource Sharing (CORS).

## Why a reverse proxy is required [why-reverse-proxy]

Do not send telemetry directly from the browser to {{product.observability}} with an API key in client-side code. Any credentials in browser code are visible to end users and can be misused. EDOT Browser requires a reverse proxy in front of the OTLP endpoint for these reasons:

- **Authentication**: The EDOT Collector or {{ecloud}} Managed OTLP endpoint expects an `Authorization` header with an API key. The reverse proxy injects the header so the key stays on the server and is not exposed to the browser.
- **Cross-origin requests**: Your web application and the OTLP endpoint often have different origins. Browsers enforce CORS, so without the right headers, export requests are blocked. A reverse proxy on the same origin as your app (or configured to allow it) can add the required CORS headers and handle preflight `OPTIONS` requests.
- **Traffic control**: You can apply rate limiting or other controls at the proxy before traffic reaches the Collector or {{product.observability}}.

For complete examples and security considerations, refer to [OpenTelemetry for Real User Monitoring (RUM)](docs-content://solutions/observability/applications/otel-rum.md).

## Content Security Policy (CSP) [content-security-policy]

If your site uses a Content Security Policy (CSP), add the domain of your reverse proxy or OTLP endpoint to the `connect-src` directive so the browser allows export requests. For example: `connect-src 'self' https://telemetry.example.com`.

## CORS requirements [cors-requirements]

When your web application and the export endpoint have different origins, the browser might block requests unless CORS is configured. Your reverse proxy must:

- Return `Access-Control-Allow-Origin` matching your application origin
- Respond to `OPTIONS` preflight requests with 204
- Include `Authorization` in `Access-Control-Allow-Headers` when using API key authentication

## Example: NGINX reverse proxy [example-nginx]

The following example forwards telemetry from `webapp.example.com` to an EDOT Collector at `collector.example.com`, injects the required `Authorization` header, and handles CORS preflight:

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

## Next steps [next-steps]

- [Install the agent](install-agent.md) and initialize EDOT Browser in your application.
- Refer to [Configure EDOT Browser](configuration.md) for initialization options.
