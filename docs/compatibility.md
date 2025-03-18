---
title: Compatibility
layout: default
nav_order: 4
---

# Compatibility

## EDOT Collector 

### EDOT Collector compatibility with Elastic stack
To help you start using EDOT as early as possible, we’re enabling backwards compatibility for EDOT Collector versions 9.0+ with Elastic Stack versions 8.18+.

| **EDOT Collector Version** | Elastic Stack 8.17                        | Elastic Stack 8.18                        | Elastic Stack 8.19                        | Elastic Stack 9.0                         | Elastic Stack 9.1                         |
|:--------------------------:|:-----------------------------------------:|:-----------------------------------------:|:-----------------------------------------:|:-----------------------------------------:|:-----------------------------------------:|
| **8.x**                    | <span style="color:gray">✖</span>         | <span style="color:gray">✖</span>         | <span style="color:gray">✖</span>         | <span style="color:gray">✖</span>         | <span style="color:gray">✖</span>         |
| **9.0**                    | <span style="color:gray">✖</span>         | ✅                                         | ✅                                         | ✅                                         | ✅                                         |
| **9.1**                    | <span style="color:gray">✖</span>         | ✅                                         | ✅                                         | ✅                                         | ✅                                         |

### EDOT Collector supported components
The EDOT Collector includes two types of components with different support scope:

**Core Components**
These are used by default in Elastic’s onboarding flows and are essential for common use cases. They are fully supported under your Service Level Agreement (SLA).

**Extended Components**
A curated set of optional components that enhance functionality. These are not part of Elastic’s core product journeys and are not covered by SLAs. You’re free to use them, but Elastic provides limited support.

> ⚠️ Recommendation: For the best support experience, we recommend relying on Core components, and using Extended components only when required.

> 🔄 Upstream Changes: Since the EDOT Collector is built on upstream OpenTelemetry, changes (e.g., to semantic conventions or config options) may impact components. Elastic highlights and manages these through docs and support channels.

<!-- start:edot-collector-components-table -->

| **Component**                | **GitHub Repo**                                                                                      | **EDOTCol 8.x** | **EDOTCol 9.x**         |
|-----------------------------|-------------------------------------------------------------------------------------------------------|-----------------|--------------------------|
| **Receivers**               |                                                                                                       |                 |                          |
| filelogreceiver             | [Contrib](https://github.com/open-telemetry/opentelemetry-collector-contrib)                         | Extended        | ✅ Core (since 9.0)      |
| hostmetricsreceiver         | [Contrib](https://github.com/open-telemetry/opentelemetry-collector-contrib)                         | Extended        | ✅ Core (since 9.0)      |
| k8sclusterreceiver          | [Contrib](https://github.com/open-telemetry/opentelemetry-collector-contrib)                         | Extended        | ✅ Core (since 9.0)      |
| k8sobjectsreceiver          | [Contrib](https://github.com/open-telemetry/opentelemetry-collector-contrib)                         | Extended        | ✅ Core (since 9.0)      |
| kubeletstatsreceiver        | [Contrib](https://github.com/open-telemetry/opentelemetry-collector-contrib)                         | Extended        | ✅ Core (since 9.0)      |
| otlpreceiver                | [Core](https://github.com/open-telemetry/opentelemetry-collector)                                    | Extended        | ✅ Core (since 9.0)      |
| **Exporters**               |                                                                                                       |                 |                          |
| elasticsearchexporter       | [Contrib](https://github.com/open-telemetry/opentelemetry-collector-contrib)                         | Extended        | ✅ Core (since 9.0)      |
| otlpexporter                | [Core](https://github.com/open-telemetry/opentelemetry-collector)                                    | Extended        | ✅ Core (since 9.0)      |
| **Processors**              |                                                                                                       |                 |                          |
| attributesprocessor         | [Contrib](https://github.com/open-telemetry/opentelemetry-collector-contrib)                         | Extended        | ✅ Core (since 9.0)      |
| batchprocessor              | [Core](https://github.com/open-telemetry/opentelemetry-collector)                                    | Extended        | ✅ Core (since 9.0)      |
| elasticinframetricsprocessor | [Elastic](https://github.com/elastic/opentelemetry-collector-components)                            | Extended        | ✅ Core (since 9.0)      |
| elastictraceprocessor       | [Elastic](https://github.com/elastic/opentelemetry-collector-components)                             | Extended        | ✅ Core (since 9.0)      |
| k8sattributesprocessor      | [Contrib](https://github.com/open-telemetry/opentelemetry-collector-contrib)                         | Extended        | ✅ Core (since 9.0)      |
| resourceprocessor           | [Contrib](https://github.com/open-telemetry/opentelemetry-collector-contrib)                         | Extended        | ✅ Core (since 9.0)      |
| resourcedetectionprocessor  | [Contrib](https://github.com/open-telemetry/opentelemetry-collector-contrib)                         | Extended        | ✅ Core (since 9.0)      |
| **Connectors**              |                                                                                                       |                 |                          |
| elasticapmconnector         | [Elastic](https://github.com/elastic/opentelemetry-collector-components)                             | Extended        | ✅ Core (since 9.0)      |
| routingconnector            | [Contrib](https://github.com/open-telemetry/opentelemetry-collector-contrib)                         | Extended        | ✅ Core (since 9.0)      |

<!-- end:edot-collector-components-table -->



See the full list of core & extended EDOT components [here](https://elastic.github.io/opentelemetry/edot-collector/components.html)


### EDOT Collector supported OS

| **EDOT Collector Version** | Linux/arm64                           | Linux/amd64                           | Windows                                | macOS                                  |
|:--------------------------:|:-------------------------------------:|:-------------------------------------:|:--------------------------------------:|:--------------------------------------:|
| **8.x**                    | <span style="color:gray">✖</span>     | <span style="color:gray">✖</span>     | <span style="color:gray">✖</span>     | <span style="color:gray">✖</span>     |
| **9.x**                    | ✅                                     | ✅                                     | <span style="color:gray">✖</span>     | <span style="color:gray">✖</span>     |
