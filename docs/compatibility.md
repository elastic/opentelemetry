---
title: Compatibility & Support
layout: default
nav_order: 4
---

# Compatibility & Support
{: .no_toc }

OpenTelemetry (OTel) is a modular, extensible framework designed to integrate with a wide range of technologies. Its architecture enables interoperability across many components, extensions, and tools—giving users flexibility to shape their observability pipelines.

Elastic Distributions for OpenTelemetry (EDOT) are built from upstream OTel components and are **technically compatible** with a broad set of community components. Users can also send data to Elastic using other upstream OTel components or distributions like the contrib Collector and OTel SDKs, which are *technically compatible* with Elastic’s ingestion APIs.

**"Supported through Elastic”** refers to components and configurations that Elastic has explicitly tested, validated, and committed to maintaining under our [Support Policies](https://www.elastic.co/support). This includes regular updates, issue triaging, and guidance from Elastic’s support and engineering teams. Components outside of this supported set may still work, but Elastic does not provide guaranteed support or troubleshooting assistance for them.

In the following sections we differentiate the following compatibility and support states:

| State | Description | Symbol |
|:---|:---|:---:|
| **Incompatible** | Component, use case or ingestion path is technically not compatible, thus, functionality is likely to be significantly impacted.  | ✖️ |
| **Compatible** | Component, use case or ingestion path is *technically compatible*. The functionality is not expected to be impaired, though, minor deviations may occur. Component, use case or ingestion path is *not officially support by Elastic*, hence, Elastic does not provide guaranteed support or troubleshooting assistance | ✔️ |
| **Supported** | Component, use case or ingestion path is *technically compatible* and Elastic provides *official support*. The functionality is explicitly tested. Limitations will be documented. | ✅ |

### Table of Content
{: .no_toc }

- TOC
{:toc}

## EDOT Collector 

### EDOT Collector Compatibility - Elastic Stack

To help you start using EDOT as early as possible, we’re enabling backwards compatibility for EDOT Collector versions 9.0+ with Elastic Stack versions 8.18+.
The following table gives an overview of compatibility and support of EDOT Collector versions with Elastic Stack versions.

<table class="compatibility">
    <thead>
        <tr>
            <th rowspan=2><b>EDOT Collector Version</b></th>
            <th colspan=5>Elastic Stack</th>
        </tr>
        <tr>
            <th>< 8.16</th>
            <th>8.16 - 8.17</th>
            <th>8.18</th>
            <th>8.19</th>
            <th>9.0</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td><b>8.x</b></td>
            <td>✖️</td>
            <td>✔️</td>
            <td>✔️</td>
            <td>✔️</td>
            <td>✔️</td>
        </tr>
        <tr>
            <td><b>9.0</b></td>
            <td>✖️</td>
            <td>✔️</td>
            <td>✅</td>
            <td>✅</td>
            <td>✅</td>
        </tr>
    </tbody>
</table>

### EDOT Collector Compatibility - Components
The EDOT Collector includes two types of components with different compatibility and support scope:

**Core Components**
These are used by default in Elastic’s onboarding flows and are essential for common use cases. They are **fully supported** (✅) under your Service Level Agreement (SLA).

**Extended Components**
A curated set of optional components that enhance functionality and are **technically compatible** (✔️). These are not part of Elastic’s core product journeys and are not covered by SLAs. You’re free to use them, but Elastic provides limited support.

| **Component**                | **GitHub Repo**        | **EDOTCol 8.x** | **EDOTCol 9.x**         |
|:-----------------------------|:------------------------|-----------------|--------------------------|
|**Receivers**                 |                        |                 |                          |
| filelogreceiver              | [OTel Contrib Repo]    | ✔️ Extended        | ✅ Core (since 9.0)      |
| hostmetricsreceiver          | [OTel Contrib Repo]    | ✔️ Extended        | ✅ Core (since 9.0)      |
| k8sclusterreceiver           | [OTel Contrib Repo]    | ✔️ Extended        | ✅ Core (since 9.0)      |
| k8sobjectsreceiver           | [OTel Contrib Repo]    | ✔️ Extended        | ✅ Core (since 9.0)      |
| kubeletstatsreceiver         | [OTel Contrib Repo]    | ✔️ Extended        | ✅ Core (since 9.0)      |
| otlpreceiver                 | [OTel Core Repo]       | ✔️ Extended        | ✅ Core (since 9.0)      |
| **Exporters**                |                        |                 |                          |
| elasticsearchexporter        | [OTel Contrib Repo]    | ✔️ Extended        | ✅ Core (since 9.0)      |
| otlpexporter                 | [OTel Core Repo]       | ✔️ Extended        | ✅ Core (since 9.0)      |
| **Processors**               |                        |                 |                          |
| attributesprocessor          | [OTel Contrib Repo]    | ✔️ Extended        | ✅ Core (since 9.0)      |
| batchprocessor               | [OTel Core Repo]       | ✔️ Extended        | ✅ Core (since 9.0)      |
| elasticinframetricsprocessor | [Elastic Repo]         | ✔️ Extended        | ✅ Core (since 9.0)      |
| elastictraceprocessor        | [Elastic Repo]         | ✔️ Extended        | ✅ Core (since 9.0)      |
| k8sattributesprocessor       | [OTel Contrib Repo]    | ✔️ Extended        | ✅ Core (since 9.0)      |
| resourceprocessor            | [OTel Contrib Repo]    | ✔️ Extended        | ✅ Core (since 9.0)      |
| resourcedetectionprocessor   | [OTel Contrib Repo]    | ✔️ Extended        | ✅ Core (since 9.0)      |
| **Connectors**               |                        |                 |                          |
| elasticapmconnector          | [Elastic Repo]         | ✔️ Extended        | ✅ Core (since 9.0)      |
| routingconnector             | [OTel Contrib Repo]    | ✔️ Extended        | ✅ Core (since 9.0)      |

See the **full list of Core & Extended EDOT Collector components [here](./edot-collector/components)**.

{: .note-title}
> Recommendation
>
> For the best support experience, we recommend relying on *Core Components*, and using *Extended Components* only when required.

{: .warning}
> Since the EDOT Collector is built on upstream OpenTelemetry, breaking upstream changes (e.g., to semantic conventions or configuration options) may impact both, *Extended Components* and *Core Components*. Elastic highlights and manages these through docs and support channels.

### EDOT Collector Compatibility - Operating Systems

The following table gives an overview of compatibility and support of EDOT Collector versions with different operating systems.

| **EDOT Collector Version** | Linux/arm64  | Linux/amd64    | Windows    | macOS     |
|:--------------------------:|:------------:|:--------------:|:----------:|:---------:|
| **8.x**                    | ✔️            | ✔️              | ✔️          | ✔️         |
| **9.x**                    | ✅           | ✅              | ✔️          | ✔️         |

### Other Collector Distributions

Other, non-EDOT distributions of the OTel Collector (such as custom Collector builds, upstream Collector distributions, etc.) are **technically compatible** (✔️) (but *not officially supported* through Elastic) if they contain the required OTel Collector components and are configured analogously to the EDOT Collector.

Required components and configuration options per use case can be retrieved from the [sample configuration files](https://github.com/elastic/elastic-agent/tree/v{{ site.edot_versions.collector }}/internal/pkg/otel/samples/linux) for the EDOT Collector.

## EDOT SDKs

### EDOT .NET

🚧 Coming soon

### EDOT Java

EDOT Java is a wrapper around the upstream OTel Java Agent and, thus, follows the compatibility of the upstream component.
Elastic **officially supports** (✅) the technologies, JVM versions and operating systems that are tested and documented in the upstream Java Agent:

| Category                 | Compatibility & Support Level  |
|:-------------------------|:------------------------------:|
| [JVMs]                   | ✅                             | 
| [Application Servers]    | ✅                             |
| [Libraries & Frameworks] | ✅                             |

### EDOT Node.js

🚧 Coming soon

### EDOT PHP

🚧 Coming soon

### EDOT Python

🚧 Coming soon

### EDOT Android

🚧 Coming soon

### EDOT iOS

🚧 Coming soon

[OTel Core Repo]: https://github.com/open-telemetry/opentelemetry-collector 
[OTel Contrib Repo]: https://github.com/open-telemetry/opentelemetry-collector-contrib
[Elastic Repo]: https://github.com/elastic/opentelemetry-collector-components
[JVMs]: https://github.com/open-telemetry/opentelemetry-java-instrumentation/blob/main/docs/supported-libraries.md#jvms-and-operating-systems
[Application Servers]: https://github.com/open-telemetry/opentelemetry-java-instrumentation/blob/main/docs/supported-libraries.md#application-servers
[Libraries & Frameworks]: https://github.com/open-telemetry/opentelemetry-java-instrumentation/blob/main/docs/supported-libraries.md#libraries--frameworks