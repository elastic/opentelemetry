---
title: Overview
layout: default
nav_order: 1
---

# EDOT Collector

The **Elastic Distribution of OpenTelemetry (EDOT) Collector** is an open-source distribution of the [OpenTelemetry Collector](https://github.com/open-telemetry/opentelemetry-collector).

Built on OpenTelemetry’s modular [architecture](https://opentelemetry.io/docs/collector/), the EDOT Collector offers a curated and fully supported selection of Receivers, Processors, Exporters, and Extensions. Designed for production-grade reliability. 

## 🚀 Get started
The quickest way to get started with EDOT is to follow our [quickstart guide](../quickstart/index).

## 🎛️ Collector configuration
The EDOT collector can be configured using the standard OTel collector configuration file or values.yml if you have deployed using Helm.

For full details on each option visit [this page](./config/index)

## 🧩 EDOT Collector components

The Elastic Distribution of OpenTelemetry (EDOT) Collector is built on OpenTelemetry’s modular architecture, integrating a carefully curated selection of Receivers, Processors, Exporters, and Extensions to ensure stability, scalability, and seamless observability. 

Visit [this page](./components) for the full list of OTel Collector components embedded in the EDOT Collector.

To request a component to be added to EDOT Collector, please submit a [GitHub issue here](https://github.com/elastic/opentelemetry/issues/new/choose).

## Collector Limitations
The EDOT collector has some limitations which are mostly inherited from the upstream components, see the [full list](./edot-collector-limitations) here before troubleshooting.

### 📄 License
View details of license for [EDOT Collector](https://github.com/elastic/elastic-agent/blob/main/LICENSE.txt). 