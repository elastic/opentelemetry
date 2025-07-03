---
navigation_title: SDK Distributions
description: Compatibility and support information for EDOT SDK versions with EDOT Collector versions.
applies_to:
  stack:
  serverless:
    observability:
products:
  - id: cloud-serverless
  - id: observability
---

# Compatibility and support for OTel SDKs

The following table provides an overview of compatibility and support of EDOT SDKs with EDOT Collector versions:

| EDOT Collector version        | **< 8.16**         | **8.16 to 8.19**    | **9.x**            |
| :----------------------- | :----------------- | :------------------ | :----------------- |
| **Compatibility**        | [Incompatible]     | [Compatible]        | [Compatible]       |
| **Level of support**     | [Not supported]    | [Not supported]     | [Supported]        |

This applies to all EDOT SDKs:

- EDOT .NET
- EDOT Java
- EDOT Node.js
- EDOT PHP
- EDOT Python
- EDOT Android
- EDOT iOS

Refer to the [EDOT Collector compatibility table](collectors.md) for compatibility with Elastic Stack versions.

For the best experience, export data from EDOT SDKs using the [EDOT Collector](/reference/edot-collector/index.md).

:::{note}
Ingesting data from EDOT SDKs through EDOT Collector into Elastic Stack versions 8.18 or higher is supported ([Supported]).
:::

## Supported technologies per EDOT SDK

For compatibility of language-specific technologies check out the following pages for corresponding EDOT SDKs:

- [Supported Technologies - .NET](/reference/edot-sdks/dotnet/supported-technologies.md)
- [Supported Technologies - Java](/reference/edot-sdks/java/supported-technologies.md)
- [Supported Technologies - Node.js](/reference/edot-sdks/nodejs/supported-technologies.md)
- [Supported Technologies - PHP](/reference/edot-sdks/php/supported-technologies.md)
- [Supported Technologies - Python](/reference/edot-sdks/python/supported-technologies.md)
- [Supported Technologies - Android](apm-agent-android://reference/index.md)
- [Supported Technologies - iOS](apm-agent-ios://reference/index.md)

## Other SDK distributions

OTel SDK distributions other than the ones listed above are technically compatible ([Compatible]) with Elastic but are not officially supported by Elastic ([Supported]).

[Incompatible]: nomenclature.md
[Compatible]: nomenclature.md
[Not supported]: nomenclature.md
[Supported]: nomenclature.md
