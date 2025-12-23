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
  - id: edot-sdk
---

# EDOT SDKs 

The {{edot}} (EDOT) SDKs are production-ready, customized distributions of [OpenTelemetry](https://opentelemetry.io/) language SDKs, specifically optimized for seamless integration with {{product.observability}}. EDOT SDKs provide a comprehensive observability solution that automatically captures distributed traces, metrics, and logs from your applications with minimal configuration.

While maintaining full compatibility with the OpenTelemetry specification, EDOT SDKs provide improvements and bug fixes from Elastic before they become available in contrib OpenTelemetry repositories.

## Supported languages

EDOT SDKs are available for the following programming languages and platforms:

* [.NET](elastic-otel-dotnet://reference/edot-dotnet/index.md)
* [Java](elastic-otel-java://reference/edot-java/index.md)
* [Node](elastic-otel-node://reference/edot-node/index.md)
* [PHP](elastic-otel-php://reference/edot-php/index.md)
* [Python](elastic-otel-python://reference/edot-python/index.md)
* [Android](apm-agent-android://reference/edot-android/index.md)
* [iOS](apm-agent-ios://reference/edot-ios/index.md)

## Feature overview

This table provides an overview of the features available in the {{edot}} (EDOT) SDKs across different programming languages.

% start:edot-features

| Feature | .NET | Java | Node.js | PHP | Python | Android | iOS |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **[Distributed tracing](https://opentelemetry.io/docs/concepts/signals/traces/)** | ✅ 1.0+ | ✅ 1.0+ | ✅ 1.0+ | ✅ 1.0+ | ✅ 1.0+ | ✅ 1.0+ | ✅ 1.0+ | 
| [Service map](docs-content://solutions/observability/apm/service-map.md) | ✅ 1.0+ | ✅ 1.0+ | ✅ 1.0+ | ✅ 1.0+ | ✅ 1.0+ | ✅ 1.0+ | ✅ v1.0+ | 
| [Zero-code instrumentation](https://opentelemetry.io/docs/concepts/instrumentation/zero-code/) | ✅ 1.0+ | ✅ 1.0+ | ✅ 1.0+ | ✅ 1.0+ | ✅ 1.0+ | ❌  | ❌  | 
| [Head-based sampling](https://opentelemetry.io/docs/concepts/sampling/#head-sampling) | ✅ 1.0+ | ✅ 1.0+ | ✅ 1.0+ | ✅ 1.0+ | ✅ 1.0+ | ✅ 1.1+ | ✅ v1.0+ | 
| [Baggage](https://opentelemetry.io/docs/concepts/signals/baggage/) | ✅ 1.0+ | ✅ 1.0+ | ✅ 1.0+ | ✅ 1.0+ | ✅ 1.0+ | ❌  | ✅ v1.0+ | 
| Inferred spans | ❌  | ✅ 1.0+ | ❌  | 𝐓 1.0+ | ❌  | ❌  | ❌  | 
| **[Logs collection](https://opentelemetry.io/docs/specs/otel/logs/#opentelemetry-solution)** | ✅ 1.0+ | ✅ 1.0+ | 𝐓 1.0+ | ✅ 1.0+ | 𝐓 1.0+ | ✅ 1.0+ | ✅ v1.0+ | 
| [Logs correlation](https://opentelemetry.io/docs/specs/otel/logs/#log-correlation) | ✅ 1.0+ | ✅ 1.0+ | 𝐓 1.0+ | ✅ 1.0+ | 𝐓 1.0+ | ✅ 1.0+ | ✅ v1.0+ | 
| **[Metrics collection](https://opentelemetry.io/docs/concepts/signals/metrics/)** | ✅ 1.0+ | ✅ 1.0+ | ✅ 1.0+ | ✅ 1.0+ | ✅ 1.0+ | ✅ 1.0+ | 𝐓 v0.7+ | 
| Custom metrics | ✅ 1.0+ | ✅ 1.0+ | ✅ 1.0+ | ✅ 1.0+ | ✅ 1.0+ | ✅ 1.0+ | 𝐓 v0.7+ | 
| Agent health monitoring | ❌  | ❌  | ❌  | ❌  | ❌  | ❌  | ❌  | 
| [Runtime metrics](https://opentelemetry.io/docs/specs/semconv/runtime/) | ✅ 1.0+ | ✅ 1.0+ | 𝐓 1.0+ | ❌  | ❌  | ❌  | ❌  | 
| **Capturing errors / exceptions** | ✅ 1.0+ | ✅ 1.0+ | ✅ 1.0+ | ✅ 1.0+ | ✅ 1.0+ | ✅ 1.0+ | ✅ v1.0+ | 
| Crash reporting | ➖  | ➖  | ➖  | ➖  | ➖  | ❌  | ✅ v1.0+ | 
| **Central configuration** | ❌  | 𝐓 1.5.0+ | 𝐓 1.2.0+ | 𝐓 1.1.0+ | 𝐓 1.4.0+ | 𝐓 1.2.0+ | 𝐓 1.4.0+ | 
| **Profiling integration** | ❌  | 𝐓 1.0+ | ❌  | ❌  | ❌  | ❌  | ❌  | 
| **[TLS for OTLP endpoint](https://opentelemetry.io/docs/specs/otel/protocol/exporter/#endpoint-urls-for-otlphttp)** | ✅ 1.0+ | ✅ 1.0+ | ✅ 1.0+ | ✅ 1.0+ | ✅ 1.0+ | ✅ 1.0+[^1] | ✅ v1.0+[^1] | 
| TLS for OpAMP endpoint | ❌  | ❌  | ✅ 1.7.0+ | ✅ 1.2.0+ | ✅ 1.10.0+ | ✅ 1.2.0+[^1] | ✅ v1.4.0+[^1] | 

**Legend:**

* ✅ Generally available
* 𝐓 In technical preview
* ➖ Not applicable
* ❌ Not available


[^1]: CA-signed certificates only

% end:edot-features

## Support for EDOT SDKs

Elastic provides technical support for EDOT Language SDKs according to Elastic's [Support Policy](https://www.elastic.co/support_policy). EDOT SDKs are meant to be used in combination with the [EDOT Collector](elastic-agent://reference/edot-collector/index.md) or the [{{motlp}}](/reference/motlp.md) to ingest data into Elastic solutions from the EDOT SDKs. Other ingestion paths are not officially supported by Elastic.

Using EDOT SDKs directly with {{product.apm-server}}'s OpenTelemetry intake endpoint is not supported.  
While some data might ingest, Elastic doesn't guarantee:

- Correctness of attributes  
- Alignment with EDOT processing pipelines  
- Enrichment (service metadata, environment, runtime info, and so on)  
- Troubleshooting coverage  

If you require a supported setup, route SDK telemetry through EDOT Collector or use Managed OTel intake.

:::{warning}
Avoid using EDOT SDKs alongside any other {{product.apm}} agent, including Elastic {{product.apm}} agents. Running multiple agents in the same application process might lead to conflicting instrumentation, duplicate telemetry, or other unexpected behavior.
:::

## License

EDOT SDKs are licensed under the [Apache License, Version 2.0](https://www.apache.org/licenses/LICENSE-2.0).
