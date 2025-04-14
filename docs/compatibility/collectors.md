---
title: Collector Distributions
parent: Compatibility & Support
layout: default
nav_order: 3
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

### EDOT Collector compatibility with Elastic stack

The following table gives an overview of compatibility and support of EDOT Collector versions with Elastic Stack versions.

<table class="compatibility">
    <thead>
        <tr>
            <th rowspan=2><b>EDOT Collector version</b></th>
            <th colspan=5>Elastic stack version</th>
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
            <td><b>9.0</b></td>
            <td>❌</td>
            <td>🟡</td>
            <td>✅</td>
            <td>✅</td>
            <td>✅</td>
        </tr>
    </tbody>
</table>

### Components

For information on the compatibility of each Collector component, refer to the [full list of Core and Extended components](../edot-collector/components).

### Operating systems

The following table gives an overview of compatibility and support of EDOT Collector versions with different operating systems.

| **EDOT Collector version** | Linux/arm64  | Linux/amd64    | Windows    | macOS     |
|:--------------------------:|:------------:|:--------------:|:----------:|:---------:|
| **9.x**                    | ✅           | ✅              | 🟡          | 🟡         |

## Other Collector distributions

Non-EDOT distributions of the OTel Collector, such as custom Collector builds, upstream Collector distributions, and so on aren't officially supported through Elastic but are technically compatible (🟡) if they contain the [required OTel Collector components](../edot-collector/custom-collector) and are configured like the EDOT Collector.

You can retrieve required components and configuration options from the [sample configuration files](https://github.com/elastic/elastic-agent/tree/v{{ site.edot_versions.collector }}/internal/pkg/otel/samples/linux) for the EDOT Collector.

[Incompatible]: ./nomenclature
[Compatible]: ./nomenclature
[Supported]: ./nomenclature
[Extended]: ./nomenclature#extended-components
[Core]: ./nomenclature#core-components
[OTel Core Repo]: https://github.com/open-telemetry/opentelemetry-collector 
[OTel Contrib Repo]: https://github.com/open-telemetry/opentelemetry-collector-contrib
[Elastic Repo]: https://github.com/elastic/opentelemetry-collector-components