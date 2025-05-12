---
navigation_title: EDOT SDKs
description: An overview of the features available in the Elastic Distribution of OpenTelemetry (EDOT) SDKs for various languages.
applies_to:
  stack:
  serverless:
    observability:
products:
  - id: cloud-serverless
  - id: observability
---

# EDOT SDKs Feature Overview

This table provides an overview of the features available in the Elastic Distribution of OpenTelemetry (EDOT) SDKs across different programming languages.

| Feature                       | .NET   | Java   | Node.js | PHP    | Python | Android | iOS    |
| :---------------------------- | :----- | :----- | :------ | :----- | :----- | :------ | :----- |
| **Distributed Tracing**       | ✅ 1.0+ | ✅ 1.0+ | ✅ 1.0+  | ✅ 1.0+ | ✅ 1.0+ | ✅ 1.0+  | ✅ 1.0+ |
| Service Map                   | ✅ 1.0+ | ✅ 1.0+ | ✅ 1.0+  | ✅ 1.0+ | ✅ 1.0+ | ✅ 1.0+  | ✅ v1.0+ |
| Zero-code instrumentation     | ✅ 1.0+ | ✅ 1.0+ | ✅ 1.0+  | ✅ 1.0+ | ✅ 1.0+ | ❌      | ❌      |
| Head-based Sampling         | ✅ 1.0+ | ✅ 1.0+ | ✅ 1.0+  | ✅ 1.0+ | ✅ 1.0+ | ❌      | ✅ v1.0+ |
| Baggage                       | ✅ 1.0+ | ✅ 1.0+ | ✅ 1.0+  | ✅ 1.0+ | ✅ 1.0+ | ❌      | ✅ v1.0+ |
| Inferred Spans                | ❌      | ✅ 1.0+ | ❌      | 𝐓 1.0+ | ❌      | ❌      | ❌      |
| **Logs Collection**           | ✅ 1.0+ | ✅ 1.0+ | 𝐓 1.0+  | ✅ 1.0+ | 𝐓 1.0+ | ✅ 1.0+  | ✅ v1.0+ |
| Logs Correlation              | ✅ 1.0+ | ✅ 1.0+ | 𝐓 1.0+  | ✅ 1.0+ | 𝐓 1.0+ | ✅ 1.0+  | ✅ v1.0+ |
| **Metrics Collection**        | ✅ 1.0+ | ✅ 1.0+ | ✅ 1.0+  | ✅ 1.0+ | ✅ 1.0+ | ✅ 1.0+  | 𝐓 v0.7+ |
| Custom Metrics                | ✅ 1.0+ | ✅ 1.0+ | ✅ 1.0+  | ✅ 1.0+ | ✅ 1.0+ | ✅ 1.0+  | 𝐓 v0.7+ |
| Agent Health Monitoring       | ❌      | ❌      | ❌      | ❌      | ❌      | ❌      | ❌      |
| Runtime Metrics               | ✅ 1.0+ | ✅ 1.0+ | 𝐓 1.0+  | ❌      | ❌      | ❌      | ❌      |
| **Capturing Errors/Exceptions** | ✅ 1.0+ | ✅ 1.0+ | ✅ 1.0+  | ✅ 1.0+ | ✅ 1.0+ | ✅ 1.0+  | ✅ v1.0+ |

**Legend:**

*   ✅ Generally available
*   𝐓 In technical preview
*   ➖ Not applicable
*   ❌ Not available

## Elastic support for EDOT SDKs

Elastic provides technical support for EDOT Language SDKs according to Elastic's [Support Policy](https://www.elastic.co/support_policy). EDOT SDKs are meant to be used in combination with the [EDOT Collector](../edot-collector/index.md) or Elastic's managed OTLP endpoint (on Elastic Cloud Serverless) to ingest data into Elastic solutions from the EDOT SDKs. Other ingestion paths are not officially supported by Elastic.

## License

EDOT SDKs are licensed under the [Apache License, Version 2.0](https://www.apache.org/licenses/LICENSE-2.0).
