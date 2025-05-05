---
navigation_title: Overview
description: Introduction to the Elastic Distribution of OpenTelemetry (EDOT) Collector, a curated and supported distribution of the OpenTelemetry Collector.
applies_to:
  stack:
  serverless:
---

# EDOT Collector

The **Elastic Distribution of OpenTelemetry (EDOT) Collector** is an open-source distribution of the [OpenTelemetry Collector](https://github.com/open-telemetry/opentelemetry-collector).

Built on OpenTelemetry’s modular [architecture](https://opentelemetry.io/docs/collector/), the EDOT Collector offers a curated and fully supported selection of Receivers, Processors, Exporters, and Extensions. Designed for production-grade reliability.

## 🚀 Get started
The quickest way to get started with EDOT is to follow our [quickstart guide](../quickstart/index.md).

## 🎛️ Collector configuration
The EDOT collector can be configured using the standard OTel collector configuration file or values.yml if you have deployed using Helm.

For full details on each option visit [this page](./config/index.md)

## 🧩 EDOT Collector components

The Elastic Distribution of OpenTelemetry (EDOT) Collector is built on OpenTelemetry’s modular architecture, integrating a carefully curated selection of Receivers, Processors, Exporters, and Extensions to ensure stability, scalability, and seamless observability.

Visit [this page](./components) for the full list of OTel Collector components embedded in the EDOT Collector.

To request a component to be added to EDOT Collector, please submit a [GitHub issue here](https://github.com/elastic/opentelemetry/issues/new/choose).

## Collector Limitations
The EDOT collector has some limitations which are mostly inherited from the upstream components, see the [full list](../compatibility/limitations) here before troubleshooting.

### 📄 License
View details of license for [EDOT Collector](https://github.com/elastic/elastic-agent/blob/main/LICENSE.txt).