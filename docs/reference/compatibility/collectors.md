---
navigation_title: Collector Distributions
description: Compatibility and support information for EDOT Collector versions with Elastic Stack versions and operating systems.
---
# Compatibility & Support - OTel Collectors

### Legend

| **[Incompatible]** | **[Compatible]** | **[Supported]** |
| :----------------- | :--------------- | :-------------- |
| ❌                 | 🟡               | ✅              |

## EDOT Collector

### EDOT Collector compatibility with Elastic stack

The following table gives an overview of compatibility and support of EDOT Collector versions with Elastic Stack versions.

| **EDOT Collector version** | **< 8.16** | **8.16 - 8.17** | **8.18** | **8.19** | **9.0** |
| :------------------------- | :--------- | :-------------- | :------- | :------- | :------ |
| **9.0**                    | ❌         | 🟡              | ✅       | ✅       | ✅      |

:::{note}
EDOT Collector supports Elastic Stack versions 8.18 and higher. Use the generally available 9.x versions and higher of the EDOT Collector to ingest data into Elastic Stack versions 8.18 or higher under Elastic's official support (✅).
:::

### EDOT Collector Compatibility - Components

For information on the compatibility of each Collector component, refer to the [full list of Core and Extended components](../edot-collector/components).

### EDOT Collector Compatibility - Operating Systems

The following table gives an overview of compatibility and support of EDOT Collector versions with different operating systems.

| **EDOT Collector version** | **Linux/arm64** | **Linux/amd64** | **Windows** | **macOS** |
| :------------------------- | :-------------- | :-------------- | :---------- | :-------- |
| **9.x**                    | ✅              | ✅              | 🟡          | 🟡        |

## Other Collector distributions

Non-EDOT distributions of the OTel Collector, such as custom Collector builds, upstream Collector distributions, and so on aren't officially supported through Elastic but are technically compatible (🟡) if they contain the [required OTel Collector components](../edot-collector/custom-collector) and are configured like the EDOT Collector.

You can retrieve required components and configuration options from the [sample configuration files](https://github.com/elastic/elastic-agent/tree/v<COLLECTOR_VERSION>/internal/pkg/otel/samples/linux) for the EDOT Collector.

[Incompatible]: ./nomenclature
[Compatible]: ./nomenclature
[Supported]: ./nomenclature
[Extended]: ./nomenclature#extended-components
[Core]: ./nomenclature#core-components
[OTel Core Repo]: https://github.com/open-telemetry/opentelemetry-collector
[OTel Contrib Repo]: https://github.com/open-telemetry/opentelemetry-collector-contrib
[Elastic Repo]: https://github.com/elastic/opentelemetry-collector-components