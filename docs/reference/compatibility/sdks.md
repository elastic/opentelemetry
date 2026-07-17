---
navigation_title: SDK Distributions
description: Compatibility and support information for Elastic OTel SDK versions with {{agent}} versions.
applies_to:
  stack:
  serverless:
    observability:
products:
  - id: cloud-serverless
  - id: observability
  - id: edot-sdk
---

# {{edot}} compatibility and support for OTel SDKs

The following table provides an overview of compatibility and support of Elastic OTel SDKs with {{agent}} versions:

| {{agent}} version        | **< 8.16**         | **8.16 to 8.19**    | **9.x**            |
| :----------------------- | :----------------- | :------------------ | :----------------- |
| **Compatibility**        | [Incompatible]     | [Compatible]        | [Compatible]       |
| **Level of support**     | [Not supported]    | [Not supported]     | [Supported]        |

This applies to all Elastic OTel SDKs:

- Elastic OTel .NET
- Elastic OTel Java
- Elastic OTel Node.js
- Elastic OTel PHP
- Elastic OTel Python
- Elastic OTel Android
- Elastic OTel iOS

Refer to the [{{agent}} compatibility table](collectors.md) for compatibility with {{stack}} versions.

For the best experience, export data from Elastic OTel SDKs using the [{{agent}}](elastic-agent://reference/edot-collector/index.md).

:::{note}
Ingesting data from Elastic OTel SDKs through {{agent}} into {{stack}} versions 8.18 or higher is supported ([Supported]).
:::

## Support matrix for Elastic OTel SDK ingestion

| Ingestion path | Supported | Notes |
|----------------|-----------|-------|
| **{{agent}} (Gateway)** | Yes | Fully tested and recommended. |
| **{{motlp}}** | Yes | Fully supported for {{serverless-full}} and {{ech}}. |
| **{{product.apm-server}} OTel intake** | Not supported | Telemetry might ingest but mapping, enrichment, and troubleshooting are not guaranteed. |

## Supported technologies per Elastic OTel SDK

For compatibility of language-specific technologies check out the following pages for corresponding Elastic OTel SDKs:

- [Supported Technologies - .NET](elastic-otel-dotnet://reference/edot-dotnet/supported-technologies.md)
- [Supported Technologies - Java](elastic-otel-java://reference/edot-java/supported-technologies.md)
- [Supported Technologies - Node.js](elastic-otel-node://reference/edot-node/supported-technologies.md)
- [Supported Technologies - PHP](elastic-otel-php://reference/edot-php/supported-technologies.md)
- [Supported Technologies - Python](elastic-otel-python://reference/edot-python/supported-technologies.md)
- [Supported Technologies - iOS](apm-agent-ios://reference/edot-ios/supported-technologies.md)

## Other SDK distributions

OTel SDK distributions other than the ones listed above are technically compatible ([Compatible]) with Elastic but are not officially supported by Elastic ([Supported]).

[Incompatible]: nomenclature.md
[Compatible]: nomenclature.md
[Not supported]: nomenclature.md
[Supported]: nomenclature.md
