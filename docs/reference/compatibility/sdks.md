---
navigation_title: SDK Distributions
description: Compatibility and support information for EDOT SDK versions with EDOT Collector versions.
---

# Compatibility & Support - OTel SDKs

### Legend

| **[Incompatible]** | **[Compatible]** | **[Supported]** |
| :----------------- | :--------------- | :-------------- |
| ❌                 | 🟡               | ✅              |

For the best experience, export data from EDOT SDKs using the [EDOT Collector](../edot-collector/index).

## Compatibility with EDOT Collector

The following table gives an overview of compatibility and support of EDOT SDKs versions with the EDOT Collector versions:

| **EDOT SDK**     | **< 8.16** | **8.16 - 8.19** | **9.x** |
| :--------------- | :--------- | :-------------- | :------ |
| **EDOT .NET**    | ❌         | 🟡              | ✅      |
| **EDOT Java**    | ❌         | 🟡              | ✅      |
| **EDOT Node.js** | ❌         | 🟡              | ✅      |
| **EDOT PHP**     | ❌         | 🟡              | ✅      |
| **EDOT Python**  | ❌         | 🟡              | ✅      |
| **EDOT Android** | ❌         | 🟡              | ✅      |
| **EDOT iOS**     | ❌         | 🟡              | ✅      |

Refer to the [EDOT Collector compatibility table](./collectors#edot-collector-compatibility-with-elastic-stack) for compatibility with Elastic Stack versions.

:::{note}
Ingesting data from EDOT SDKs through EDOT Collector into Elastic Stack versions 8.18 or higher is supported (✅).
:::

## Supported Technologies per EDOT SDK

For compatibility of language-specific technologies check out the following pages for corresponding EDOT SDKs:

- [Supported Technologies - .NET](../edot-sdks/dotnet/supported-technologies)
- [Supported Technologies - Java](../edot-sdks/java/supported-technologies)
- [Supported Technologies - Node.js](../edot-sdks/nodejs/supported-technologies)
- [Supported Technologies - PHP](../edot-sdks/php/supported-technologies)
- [Supported Technologies - Python](../edot-sdks/python/supported-technologies)
- [Supported Technologies - Android](https://www.elastic.co/guide/en/apm/agent/android/current/intro.html)
- [Supported Technologies - iOS](https://www.elastic.co/guide/en/apm/agent/swift/current/supported-technologies.html)

## Other SDK Distributions

OTel SDK distributions other than the ones listed above are technically compatible (🟡) with Elastic but are not officially supported by Elastic (✅).

[Incompatible]: ./nomenclature
[Compatible]: ./nomenclature
[Supported]: ./nomenclature
