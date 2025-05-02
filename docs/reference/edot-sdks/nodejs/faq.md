---
navigation_title: Frequently Asked Questions
description: Frequently asked questions about the Elastic Distribution of OpenTelemetry Node.js (EDOT Node.js).
---

# Frequently Asked Questions on EDOT Node.js

## How to disable the SDK?

Set the `OTEL_SDK_DISABLED` environment variable to `true`, and restart your application.

## How to disable an instrumentation?

Set the [`OTEL_NODE_DISABLED_INSTRUMENTATIONS`](./configuration.md#otel_node_disabledenabled_instrumentations-details) environment variable.

For example, to disable `@opentelemetry/instrumentation-net` and `@opentelemetry/instrumentation-dns`:

```bash
export OTEL_NODE_DISABLED_INSTRUMENTATIONS=dns,net
...
node --import @elastic/opentelemetry-node my-app.js
```

## How to tell if EDOT Node.js is running?

Look for "start Elastic Distribution of OpenTelemetry Node.js" in the application log.

As it is starting, EDOT Node.js always logs (at the "info" level) a preamble to indicate that it has started. For example, it looks like this:

```json
{"name":"elastic-otel-node","level":30,"preamble":true,"distroVersion":"0.7.0","env":{"os":"darwin 24.3.0","arch":"arm64","runtime":"Node.js v18.20.4"},"msg":"start Elastic Distribution of OpenTelemetry Node.js","time":"2025-03-27T22:14:08.288Z"}
...
```

The `distroVersion` field also indicates which version of EDOT Node.js is being used.



