---
navigation_title: Reference
description: EDOT reference documentation.
---

# Reference

The following sub-pages contain reference documentation for EDOT.

## 🔭 What is OpenTelemetry?
[OpenTelemetry](https://opentelemetry.io/docs/) is a vendor-neutral observability framework for collecting, processing, and exporting telemetry data. If you are new to OpenTelemetry we recommend reading OpenTelemetry [concepts](https://opentelemetry.io/docs/concepts/) and [components](https://opentelemetry.io/docs/concepts/components/).

## 🇪 What is EDOT?

**Elastic Distributions of OpenTelemetry (EDOT)** is an open-source ecosystem of tailored [OpenTelemetry distributions](https://opentelemetry.io/docs/concepts/distributions/), comprising an [OpenTelemetry Collector](https://opentelemetry.io/docs/collector/) and various OpenTelemetry [Language SDKs](https://opentelemetry.io/docs/languages/).
![EDOT-Distributions](./images/EDOT-SDKs-Collector.png)
Each EDOT distribution is assembled with carefully curated OpenTelemetry components, then rigorously tested to ensure production readiness. This provides a reliable and optimized OpenTelemetry experience, enabling seamless adoption with confidence and expert support.

## 🗂️ Available EDOT Distributions

| EDOT Distribution | Status |
|:-------------------|:---------------|
| [EDOT Collector](./edot-collector/index) | GA |
| [EDOT .NET](./edot-sdks/dotnet/index) | GA |
| [EDOT Java](./edot-sdks/java/index) | GA |
| [EDOT Node.js](./edot-sdks/nodejs/index) | GA |
| [EDOT PHP](./edot-sdks/php/index) | GA |
| [EDOT Python](./edot-sdks/python/index) | GA |
| [EDOT Android](https://www.elastic.co/guide/en/apm/agent/android/current/intro.html) | GA |
| [EDOT iOS](https://www.elastic.co/guide/en/apm/agent/swift/current/intro.html) | GA |

<sup>(*)</sup> GA coming soon

## 🟢 Production Readiness & Support

Each EDOT distribution undergoes production-grade testing before being declared Generally Available (GA). Elastic provides full support for GA releases in accordance with our [support matrix](https://www.elastic.co/support/matrix) and SLAs.

Technical Preview distributions receive best-effort support and are not covered under standard SLAs.

## 🚀 Get Started

Pick the right [Quickstart Guide](./quickstart/index) for your environment

**or** choose your observability use case:

- [Monitoring on Kubernetes](./use-cases/kubernetes/index)
- [LLM Observability](./use-cases/llm/index)

## 📥 Report an issue or provide feedback
To report an issue or provide feedback on EDOT, please [submit a github issue](https://github.com/elastic/opentelemetry/issues/new/choose).

## Component Versions

These documentation pages are optimized for the following versions of the corresponding EDOT components and Elastic Stack.

| Component | Version |
|:---|:---:|
|Elastic Stack | <STACK_VERSION> |
|EDOT Collector| <COLLECTOR_VERSION> |
|EDOT .NET| <DOTNET_VERSION> |
|EDOT Java| <JAVA_VERSION> |
|EDOT Node.js| <NODEJS_VERSION> |
|EDOT PHP| <PHP_VERSION> |
|EDOT Python| <PYTHON_VERSION> |
|EDOT Android| <ANDROID_VERSION> |
|EDOT iOS| <IOS_VERSION> |

For other versions [visit the documentation sources](https://github.com/elastic/opentelemetry/tags) in the GitHub repository.