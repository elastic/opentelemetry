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
  - id: edot-sdk
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

For the best experience, export data from EDOT SDKs using the [EDOT Collector](elastic-agent://reference/edot-collector/index.md).

:::{note}
Ingesting data from EDOT SDKs through EDOT Collector into Elastic Stack versions 8.18 or higher is supported ([Supported]).
:::

## Supported technologies per EDOT SDK

For compatibility of language-specific technologies check out the following pages for corresponding EDOT SDKs:

- [Supported Technologies - .NET](elastic-otel-dotnet://reference/supported-technologies.md)
- [Supported Technologies - Java](elastic-otel-java://reference/supported-technologies.md)
- [Supported Technologies - Node.js](elastic-otel-node://reference/supported-technologies.md)
- [Supported Technologies - PHP](elastic-otel-php://reference/supported-technologies.md)
- [Supported Technologies - Python](elastic-otel-python://reference/supported-technologies.md)
- [Supported Technologies - Android](apm-agent-android://reference/automatic-instrumentation.md#supported-instrumentations)
- [Supported Technologies - iOS](apm-agent-ios://reference/supported-technologies.md)

## Other SDK distributions

OTel SDK distributions other than the ones listed above are technically compatible ([Compatible]) with Elastic but are not officially supported by Elastic ([Supported]).

[Incompatible]: nomenclature.md
[Compatible]: nomenclature.md
[Not supported]: nomenclature.md
[Supported]: nomenclature.md
