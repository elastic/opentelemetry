---
title: Collector Distributions
parent: Compatibility & Support
layout: default
nav_order: 2
---
# Compatibility & Support - OTel Collectors
{: .no_toc }

### Legend
{: .no_toc }

| **[Incompatible]** | **[Compatible]** | **[Supported]** |
| ❌ | 🟡 | ✅ |

### Table of content
{: .no_toc }

- TOC
{:toc}

## EDOT Collector 

### EDOT Collector Compatibility - Elastic Stack

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
            <td>❌</td>
            <td>🟡</td>
            <td>🟡</td>
            <td>🟡</td>
            <td>🟡</td>
        </tr>
        <tr>
            <td><b>9.0</b></td>
            <td>❌</td>
            <td>🟡</td>
            <td>✅</td>
            <td>✅</td>
            <td>✅</td>
        </tr>
    </tbody>
</table>

### EDOT Collector Compatibility - Components

The components included in the EDOT Collector are categorized into **[Core]** and **[Extended]** components:

| **Component**                | **GitHub Repo**        | **EDOTCol 8.x** | **EDOTCol 9.x**         |
|:-----------------------------|:------------------------|-----------------|--------------------------|
|**Receivers**                 |                        |                 |                          |
| filelogreceiver              | [OTel Contrib Repo]    | 🟡 [Extended]        | ✅ [Core] (since 9.0)      |
| hostmetricsreceiver          | [OTel Contrib Repo]    | 🟡 [Extended]        | ✅ [Core] (since 9.0)      |
| k8sclusterreceiver           | [OTel Contrib Repo]    | 🟡 [Extended]        | ✅ [Core] (since 9.0)      |
| k8sobjectsreceiver           | [OTel Contrib Repo]    | 🟡 [Extended]        | ✅ [Core] (since 9.0)      |
| kubeletstatsreceiver         | [OTel Contrib Repo]    | 🟡 [Extended]        | ✅ [Core] (since 9.0)      |
| otlpreceiver                 | [OTel Core Repo]       | 🟡 [Extended]        | ✅ [Core] (since 9.0)      |
| **Exporters**                |                        |                 |                          |
| elasticsearchexporter        | [OTel Contrib Repo]    | 🟡 [Extended]        | ✅ [Core] (since 9.0)      |
| otlpexporter                 | [OTel Core Repo]       | 🟡 [Extended]        | ✅ [Core] (since 9.0)      |
| **Processors**               |                        |                 |                          |
| attributesprocessor          | [OTel Contrib Repo]    | 🟡 [Extended]        | ✅ [Core] (since 9.0)      |
| batchprocessor               | [OTel Core Repo]       | 🟡 [Extended]        | ✅ [Core] (since 9.0)      |
| elasticinframetricsprocessor | [Elastic Repo]         | 🟡 [Extended]        | ✅ [Core] (since 9.0)      |
| elastictraceprocessor        | [Elastic Repo]         | 🟡 [Extended]        | ✅ [Core] (since 9.0)      |
| k8sattributesprocessor       | [OTel Contrib Repo]    | 🟡 [Extended]        | ✅ [Core] (since 9.0)      |
| resourceprocessor            | [OTel Contrib Repo]    | 🟡 [Extended]        | ✅ [Core] (since 9.0)      |
| resourcedetectionprocessor   | [OTel Contrib Repo]    | 🟡 [Extended]        | ✅ [Core] (since 9.0)      |
| **Connectors**               |                        |                 |                          |
| elasticapmconnector          | [Elastic Repo]         | 🟡 [Extended]        | ✅ [Core] (since 9.0)      |
| routingconnector             | [OTel Contrib Repo]    | 🟡 [Extended]        | ✅ [Core] (since 9.0)      |

See the **[full list of Core & Extended EDOT Collector components here](../edot-collector/components)**.

### EDOT Collector Compatibility - Operating Systems

The following table gives an overview of compatibility and support of EDOT Collector versions with different operating systems.

| **EDOT Collector Version** | Linux/arm64  | Linux/amd64    | Windows    | macOS     |
|:--------------------------:|:------------:|:--------------:|:----------:|:---------:|
| **8.x**                    | 🟡            | 🟡              | 🟡          | 🟡         |
| **9.x**                    | ✅           | ✅              | 🟡          | 🟡         |

## Other Collector Distributions

Other, non-EDOT distributions of the OTel Collector (such as custom Collector builds, upstream Collector distributions, etc.) are **technically compatible** (🟡) (but *not officially supported* through Elastic) if they contain the required OTel Collector components and are configured analogously to the EDOT Collector.

Required components and configuration options per use case can be retrieved from the [sample configuration files](https://github.com/elastic/elastic-agent/tree/v{{ site.edot_versions.collector }}/internal/pkg/otel/samples/linux) for the EDOT Collector.

[Incompatible]: ./nomenclature
[Compatible]: ./nomenclature
[Supported]: ./nomenclature
[Extended]: ./nomenclature#extended-components
[Core]: ./nomenclature#core-components
[OTel Core Repo]: https://github.com/open-telemetry/opentelemetry-collector 
[OTel Contrib Repo]: https://github.com/open-telemetry/opentelemetry-collector-contrib
[Elastic Repo]: https://github.com/elastic/opentelemetry-collector-components