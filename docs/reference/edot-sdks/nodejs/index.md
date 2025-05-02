---
navigation_title: EDOT Node.js
description: Introduction to the Elastic Distribution of OpenTelemetry Node.js (EDOT Node.js).
---

## EDOT Node.js

The Elastic Distribution of OpenTelemetry Node.js (EDOT Node.js) is a light wrapper around the [OpenTelemetry SDK for Node.js](https://opentelemetry.io/docs/languages/js), preconfigured for the best experience with Elastic Observability. This SDK is fully compatible with the upstream OpenTelemetry SDK and can be used as a drop-in replacement for it. In addition, it provides extra features, such as:

- A single package that includes several OpenTelemetry packages as dependencies, so you only need to install and update a single package (for most use cases). This is similar to OpenTelemetry's `@opentelemetry/auto-instrumentations-node` package.
- The [`@elastic/opentelemetry-instrumentation-openai`](https://github.com/elastic/elastic-otel-node/tree/main/packages/instrumentation-openai#readme) instrumentation for monitoring usage of the OpenAI Node.js client library.
- Additional metrics are collected by default: `process.cpu.*` and `process.memory.*` metrics from the [host-metrics package](https://github.com/open-telemetry/opentelemetry-js-contrib/tree/main/packages/opentelemetry-host-metrics/).

Use EDOT Node.js with your Node.js application to automatically capture distributed tracing data, performance metrics, and logs. EDOT Node.js will automatically instrument [popular modules](./supported-technologies.md#instrumentations) used by your service, and send the data to your configured observability backend.

Follow [the setup instructions](./setup/index.md) to get started.
