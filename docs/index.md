---
title: Introduction
layout: default
nav_order: 1
---

# Elastic Distributions of OpenTelemetry (EDOT)

## 🔭 What is OpenTelemetry?
[OpenTelemetry](https://opentelemetry.io/docs/) is a vendor-neutral observability framework for collecting, processing, and exporting telemetry data. If you are new to OpenTelemetry we recommended reading OpenTelemetry [concepts](https://opentelemetry.io/docs/concepts/) and [components](https://opentelemetry.io/docs/concepts/components/).

## 🇪 What is EDOT?

**Elastic Distributions of OpenTelemetry (EDOT)** is an open-source ecosystem of tailored [OpenTelemetry distributions](https://opentelemetry.io/docs/concepts/distributions/), comprising an [OpenTelemetry Collector](https://opentelemetry.io/docs/collector/) and various OpenTelemetry [Language SDKs](https://opentelemetry.io/docs/languages/).
![EDOT-Distributions](./images/EDOT-SDKs-Collector.png)
Each EDOT distribution is asssembled with carefully curated OpenTelemetry components, then rigorously tested to ensure production readiness. This provides a reliable and optimized OpenTelemetry experience, enabling seamless adoption with confidence and expert support.

## 🗂️ Available EDOT Distributions

| EDOT Distribution | Status |
|:-------------------|:---------------|
| [EDOT Collector](./edot-collector/index) | Technical Preview |
| [EDOT .NET](./edot-sdks/dotnet/index) | Technical Preview |
| [EDOT Java](./edot-sdks/java/index) | GA |
| [EDOT Node.js](./edot-sdks/nodejs/index) | Technical Preview |
| [EDOT PHP](./edot-sdks/php/index) | Technical Preview |
| [EDOT Python](./edot-sdks/python/index) | Technical Preview |
| [EDOT Android](./edot-sdks/android/index) | Technical Preview |
| [EDOT iOS](./edot-sdks/ios/index) | GA |

## 🟢 Production Readiness & Support
Each EDOT distribution undergoes production-grade testing before being declared Generally Available (GA). Elastic provides full support for GA releases in accordance with our [support matrix](https://www.elastic.co/support/matrix) and SLAs.

Technical Preview distributions receive best-effort support and are not covered under standard SLAs.

## 🚀 Get Started

Pick the right [Quickstart Guide](./quickstart/index) for your environment 

**or** choose your observability use case:

- [Monitoring on Kubernetes](./use-cases/kubernetes/index)
- [Collecting Logs](./use-cases/logs/index)
- [Monitoring Hosts](./use-cases/host-metrics/index)
- [Instrumenting Applications](./use-cases/application/index)

## 📥 Report an issue or provide feedback
To report an issue or provide feedback on EDOT, please [submit a github issue](https://github.com/elastic/opentelemetry/issues/new/choose).