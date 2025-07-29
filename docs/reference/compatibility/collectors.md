---
navigation_title: Collector distributions
description: Compatibility and support information for EDOT Collector versions with Elastic Stack versions and operating systems.
applies_to:
  stack:
  serverless:
    observability:
products:
  - id: cloud-serverless
  - id: observability
  - id: edot-collector
---

# Compatibility and support for OTel Collectors

The following table provides an overview of compatibility and support of {{edot}} Collector versions with {{stack}} (ELK) versions.

#### EDOT Collector 9.x

| ELK stack version           | **ELK < 8.16** | **ELK 8.16 - 8.17** | **ELK 8.18 - 8.19** | **ELK 9.0** |
| :-------------------------- | :------------- | :------------------ | :------------------ | :---------- |
| **Compatibility**           | [Incompatible] | [Compatible]        | [Compatible]        | [Compatible]|
| **Level of support**        | [Not supported] | [Not supported]    | [Supported]         | [Supported] |

:::{note}
If you're on {{stack}} 8.18 or 8.19 and require Elastic support, use EDOT Collector version 9.x, as this combination is officially [Supported].
:::

## Operating Systems

The following table provides an overview of compatibility and support of EDOT Collector versions with different operating systems.

#### EDOT Collector 9.x

These operating systems and distributions are [compatible] with EDOT Collector 9.x:

| OS Type | Architecture | Distribution or version                                  | Level of support     |
| :------ | :----------- | :------------------------------------------------------- | :------------------- |
| Linux   | amd64        | Ubuntu 24.04, 22.04, 20.04                               | [Supported]          |
| Linux   | arm64        | Ubuntu 24.04, 22.04, 20.04                               | [Supported]          |
| Linux   | amd64        | RHEL 8                                                   | [Supported]          |
| macOS   | amd64        | macOS 10.x and higher                                    | [Not supported]      |
| macOS   | arm64        | macOS 10.x and higher                                    | [Not supported]      |
| Windows | amd64        | Server 2022, 2022 Core, 2019, 2019 Core, 2016, 2016 Core | [Not supported]      |

The following Kubernetes distributions are [compatible] with EDOT Collector 9.x:

| Kubernetes  | Architecture     | Version                                                  |
| :---------- | :--------------- | :------------------------------------------------------- |
| Kubernetes  | amd64, arm64     | 1.33.0, 1.32.0, 1.31.0, 1.30.2, 1.29.4, 1.28.9, 1.27.16  |

::::{note}
The EDOT Collector is compatible with GKE, EKS and AKS. Refer to [Limitations on managed Kubernetes environments](/reference/compatibility/limitations.md#limitations-on-managed-kubernetes-environments) for more information.
::::

## EDOT Collector components

For information on the compatibility of each Collector component, refer to the [full list of Core and Extended components](/reference/edot-collector/components.md).

## Other Collector distributions

Non-EDOT distributions of the OTel Collector, such as custom Collector builds, upstream Collector distributions, and so on aren't officially supported through Elastic but are technically compatible ([Compatible]) if they contain the [required OTel Collector components](/reference/edot-collector/custom-collector.md) and are configured like the EDOT Collector.

You can retrieve required components and configuration options from the [example configuration files](https://github.com/elastic/elastic-agent/tree/v<COLLECTOR_VERSION>/internal/pkg/otel/samples/linux) for the EDOT Collector.

For a comparison between EDOT and the upstream OTel, refer to [EDOT compared to upstream OTel](edot-vs-upstream.md).

[Incompatible]: nomenclature.md
[Compatible]: nomenclature.md
[Not supported]: nomenclature.md
[Supported]: nomenclature.md
[Extended]: nomenclature.md#extended-components
[Core]: nomenclature.md#core-components
