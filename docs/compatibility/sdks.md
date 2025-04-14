---
title: SDK Distributions
parent: Compatibility & Support
layout: default
nav_order: 4
---

# Compatibility & Support - OTel SDKs

### Legend

| **[Incompatible]** | **[Compatible]** | **[Supported]** |
| ❌ | 🟡 | ✅ |

For the best experience, export data from EDOT SDKs using the [EDOT Collector](https://elastic.github.io/opentelemetry/edot-collector/index).

## Compatibility with EDOT Collector

The following table gives an overview of compatibility and support of EDOT SDKs versions with the EDOT Collector versions:

<table class="compatibility">
    <thead>
        <tr>
            <th rowspan=2><b>EDOT SDK</b></th>
            <th colspan=3><b>EDOT Collector</b></th>
            <th rowspan=2><b>Serverless</b></th>
        </tr>
        <tr>
            <th>< 8.16</th>
            <th>8.16 - 8.19</th>
            <th>9.x</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td style="text-align:left;"><b>EDOT .NET</b></td>
            <td>❌</td>
            <td>🟡</td>
            <td>✅</td>
        </tr>
        <tr>
            <td style="text-align:left;"><b>EDOT Java</b></td>
            <td>❌</td>
            <td>🟡</td>
            <td>✅</td>
        </tr>
        <tr>
            <td style="text-align:left;"><b>EDOT Node.js</b></td>
            <td>❌</td>
            <td>🟡</td>
            <td>✅</td>
        </tr>
        <tr>
            <td style="text-align:left;"><b>EDOT PHP</b></td>
            <td>❌</td>
            <td>🟡</td>
            <td>✅</td>
        </tr>
        <tr>
            <td style="text-align:left;"><b>EDOT Python</b></td>
            <td>❌</td>
            <td>🟡</td>
            <td>✅</td>
        </tr>
        <tr>
            <td style="text-align:left;"><b>EDOT Android</b></td>
            <td>❌</td>
            <td>🟡</td>
            <td>✅</td>
        </tr>
        <tr>
            <td style="text-align:left;"><b>EDOT iOS</b></td>
            <td>❌</td>
            <td>🟡</td>
            <td>✅</td>
        </tr>
    </tbody>
</table>

Refer to the [EDOT Collector compatibility table](./collectors#edot-collector-compatibility-with-elastic-stack) for compatibility with Elastic Stack versions.

{: .note}
> Ingesting data from EDOT SDKs through EDOT Collector into Elastic Stack versions 8.18 or higher is supported (✅).

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
