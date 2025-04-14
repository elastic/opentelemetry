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

## Compatibility with EDOT Collector and Elastic stack

<table class="compatibility">
    <thead>
        <tr>
            <th rowspan=2 colspan=2><b>EDOT SDK</b></th>
            <th colspan=4>EDOT Collector </th>
        </tr>
        <tr>
            <th>< 8.16</th>
            <th>< 8.18</th>
            <th>8.18+</th>
            <th>9.0+</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td style="text-align:left;"><b>EDOT .NET</b></td>
            <td>❌</td>
            <td>🟡</td>
            <td>🟡</td>
            <td>✅</td>
        </tr>
        <tr>
            <td style="text-align:left;"><b>EDOT Java</b></td>
            <td>❌</td>
            <td>🟡</td>
            <td>🟡</td>
            <td>✅</td>
        </tr>
        <tr>
            <td style="text-align:left;"><b>EDOT Node.js</b></td>
            <td>❌</td>
            <td>🟡</td>
            <td>🟡</td>
            <td>✅</td>
        </tr>
        <tr>
            <td style="text-align:left;"><b>EDOT PHP</b></td>
            <td>❌</td>
            <td>🟡</td>
            <td>🟡</td>
            <td>✅</td>
        </tr>
        <tr>
            <td style="text-align:left;"><b>EDOT Python</b></td>
            <td>❌</td>
            <td>🟡</td>
            <td>🟡</td>
            <td>✅</td>
        </tr>
        <tr>
            <td style="text-align:left;"><b>EDOT Android</b></td>
            <td>❌</td>
            <td>🟡</td>
            <td>🟡</td>
            <td>✅</td>
        </tr>
        <tr>
            <td style="text-align:left;"><b>EDOT iOS</b></td>
            <td>❌</td>
            <td>🟡</td>
            <td>🟡</td>
            <td>✅</td>
        </tr>
    </tbody>
</table>

Refer to the [EDOT Collector compatibility table](./collectors#edot-collector-compatibility---elastic-stack) for compatibility with Elastic Stack versions.

For compatibility of language-specific technologies also check out the "Supported Technologies" pages of the [EDOT SDKs documentation](../edot-sdks/index).

### EDOT Java

EDOT Java is a wrapper around the upstream OTel Java Agent and, thus, follows the compatibility of the upstream component.
Elastic **officially supports** (✅) the technologies, JVM versions and operating systems that are tested and documented in the upstream Java Agent:

| Category                                                                                                                                                   | Compatibility & Support Level |
|:-----------------------------------------------------------------------------------------------------------------------------------------------------------|:-----------------------------:|
| [JVMs](https://github.com/open-telemetry/opentelemetry-java-instrumentation/blob/main/docs/supported-libraries.md#jvms-and-operating-systems)              |               ✅               |
| [Application Servers](https://github.com/open-telemetry/opentelemetry-java-instrumentation/blob/main/docs/supported-libraries.md#application-servers )     |               ✅               |
| [Libraries & Frameworks](https://github.com/open-telemetry/opentelemetry-java-instrumentation/blob/main/docs/supported-libraries.md#libraries--frameworks) |               ✅               |

### EDOT Node.js

EDOT Node.js is a wrapper around the upstream OpenTelemetry JavaScript SDK and shares the same Node.js compatibility requirements. See the [EDOT Node.js supported technologies](../edot-sdks/nodejs/supported-technologies) for details.

| Category                                                                          | Compatibility & Support Level |
|:----------------------------------------------------------------------------------|:-----------------------------:|
| [Node.js](../edot-sdks/nodejs/supported-technologies.html#nodejs-versions)        |               ✅               |
| [TypeScript](../edot-sdks/nodejs/supported-technologies.html#typescript-versions) |               ✅               |

### EDOT PHP

| Category                                                                                      | Compatibility & Support Level |
|:----------------------------------------------------------------------------------------------|:-----------------------------:|
| [PHP](../edot-sdks/php/supported-technologies.html#php-versions)                              |               ✅               |
| [PHP SAPI's](../edot-sdks/php/supported-technologies.html#supported-php-sapis)                |               ✅               |
| [Operating Systems](../edot-sdks/php/supported-technologies.html#supported-operating-systems) |               ✅               |
| [Frameworks](../edot-sdks/php/supported-technologies.html#instrumented-frameworks)            |               ✅               |
| [Libraries](../edot-sdks/php/supported-technologies.html#instrumented-libraries)              |               ✅               |

### EDOT Python

| Category                                                                             | Compatibility & Support Level |
|:-------------------------------------------------------------------------------------|:-----------------------------:|
| [Python](../edot-sdks/python/supported-technologies.html#python-versions)            |               ✅               |
| [Instrumentations](../edot-sdks/python/supported-technologies.html#instrumentations) |               ✅               |


### EDOT Android

| Category                                                                                                                                       | Compatibility & Support Level |
|:-----------------------------------------------------------------------------------------------------------------------------------------------|:-----------------------------:|
| [Frameworks](https://www.elastic.co/guide/en/apm/agent/android/current)          |               ✅               |

### EDOT iOS

| Category                                                                                          | Compatibility & Support Level |
|:--------------------------------------------------------------------------------------------------|:-----------------------------:|
| [Frameworks](https://www.elastic.co/guide/en/apm/agent/swift/current/supported-technologies.html) |               ✅               |


## Other SDK Distributions

OTel SDK distributions other than the ones listed above are usually *technically compatible* (🟡) with Elastic but are *not officially supported by Elastic* (✅).

[Incompatible]: ./nomenclature
[Compatible]: ./nomenclature
[Supported]: ./nomenclature
