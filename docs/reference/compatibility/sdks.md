---
navigation_title: SDK Distributions
description: Compatibility and support information for EDOT SDK versions with EDOT Collector versions.
applies_to:
  stack:
  serverless:
    observability:
products:
  - cloud-serverless
  - observability
---

# Compatibility and support for OTel SDKs

The following table provides an overview of compatibility and support of EDOT SDKs versions with the EDOT Collector versions:

|                    | **Collector < 8.16**   | **Collector 8.16 to 8.19** | **Collector 9.x**   |
| :----------------- | :--------------- | :---------------- | :-------------- |
| **EDOT .NET**      | [Incompatible]   | [Compatible]      | [Supported]     |
| **EDOT Java**      | [Incompatible]   | [Compatible]      | [Supported]     |
| **EDOT Node.js**   | [Incompatible]   | [Compatible]      | [Supported]     |
| **EDOT PHP**       | [Incompatible]   | [Compatible]      | [Supported]     |
| **EDOT Python**    | [Incompatible]   | [Compatible]      | [Supported]     |
| **EDOT Android**   | [Incompatible]   | [Compatible]      | [Supported]     |
| **EDOT iOS**       | [Incompatible]   | [Compatible]      | [Supported]     |

Refer to the [EDOT Collector compatibility table](collectors.md) for compatibility with Elastic Stack versions.

For the best experience, export data from EDOT SDKs using the [EDOT Collector](../edot-collector/index.md).

:::{note}
Ingesting data from EDOT SDKs through EDOT Collector into Elastic Stack versions 8.18 or higher is supported ([Supported]).
:::

## Supported technologies per EDOT SDK

For compatibility of language-specific technologies check out the following pages for corresponding EDOT SDKs:

- [Supported Technologies - .NET](../edot-sdks/dotnet/supported-technologies.md)
- [Supported Technologies - Java](../edot-sdks/java/supported-technologies.md)
- [Supported Technologies - Node.js](../edot-sdks/nodejs/supported-technologies.md)
- [Supported Technologies - PHP](../edot-sdks/php/supported-technologies.md)
- [Supported Technologies - Python](../edot-sdks/python/supported-technologies.md)
- [Supported Technologies - Android](apm-agent-android://reference/index.md)
- [Supported Technologies - iOS](apm-agent-ios://reference/index.md)

## Other SDK distributions

OTel SDK distributions other than the ones listed above are technically compatible ([Compatible]) with Elastic but are not officially supported by Elastic ([Supported]).

[Incompatible]: nomenclature.md
[Compatible]: nomenclature.md
[Supported]: nomenclature.md
