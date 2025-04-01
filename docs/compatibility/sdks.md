---
title: SDK Distributions
parent: Compatibility & Support
layout: default
nav_order: 3
---

# Compatibility & Support - OTel SDKs
{: .no_toc }

### Legend
{: .no_toc }

| **[Incompatible]** | **[Compatible]** | **[Supported]** |
| ❌ | 🟡 | ✅ |

### Table of content
{: .no_toc }

- TOC
{:toc}

## EDOT SDKs

For the best experience, we recommend exporting data from EDOT SDKs via the [EDOT Collector](https://elastic.github.io/opentelemetry/edot-collector/index).

### Compatibility with EDOT Collector / Elastic Stack

<table class="compatibility">
    <thead>
        <tr>
            <th rowspan=2 colspan=2><b>EDOT SDK</b></th>
            <th colspan=4>EDOT Collector </th>
            <th rowspan=2><b>Serverless</b></th>
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
            <td>1.x</td>
            <td>❌</td>
            <td>🟡</td>
            <td>🟡</td>
            <td>✅</td>
            <td>✅</td>
        </tr>
        <tr>
            <td style="text-align:left;"><b>EDOT Java</b></td>
            <td>1.x</td>
            <td>❌</td>
            <td>🟡</td>
            <td>🟡</td>
            <td>✅</td>
            <td>✅</td>
        </tr>
        <tr>
            <td style="text-align:left;"><b>EDOT Node.js</b></td>
            <td>1.x</td>
            <td>❌</td>
            <td>🟡</td>
            <td>🟡</td>
            <td>✅</td>
            <td>✅</td>
        </tr>
        <tr>
            <td style="text-align:left;"><b>EDOT PHP</b></td>
            <td>1.x</td>
            <td>❌</td>
            <td>🟡</td>
            <td>🟡</td>
            <td>✅</td>
            <td>✅</td>
        </tr>
        <tr>
            <td style="text-align:left;"><b>EDOT Python</b></td>
            <td>1.x</td>
            <td>❌</td>
            <td>🟡</td>
            <td>🟡</td>
            <td>✅</td>
            <td>✅</td>
        </tr>
        <tr>
            <td style="text-align:left;"><b>EDOT Android</b></td>
            <td>1.x</td>
            <td>❌</td>
            <td>🟡</td>
            <td>🟡</td>
            <td>✅</td>
            <td>✅</td>
        </tr>
        <tr>
            <td style="text-align:left;"><b>EDOT iOS</b></td>
            <td>1.x</td>
            <td>❌</td>
            <td>🟡</td>
            <td>🟡</td>
            <td>✅</td>
            <td>✅</td>
        </tr>
    </tbody>
</table>

- Collectors are forward compatible
- Also check the other table, for EDOT Collector compatibility with Stack version compatibility

### EDOT .NET

🚧 Coming soon

### EDOT Java

EDOT Java is a wrapper around the upstream OTel Java Agent and, thus, follows the compatibility of the upstream component.
Elastic **officially supports** (✅) the technologies, JVM versions and operating systems that are tested and documented in the upstream Java Agent:

| Category                 | Compatibility & Support Level  |
|:-------------------------|:------------------------------:|
| [JVMs]                   | ✅                             | 
| [Application Servers]    | ✅                             |
| [Libraries & Frameworks] | ✅                             |

### EDOT Node.js

EDOT Node.js is a wrapper around the upstream OpenTelemetry JavaScript SDK and shares the same Node.js compatibility requirements. See the [EDOT Node.js supported technologies](../edot-sdks/nodejs/supported-technologies) for details.

### EDOT PHP

🚧 Coming soon

### EDOT Python

🚧 Coming soon

### EDOT Android

🚧 Coming soon

### EDOT iOS

🚧 Coming soon

## Other SDK Distributions

🚧 Coming soon

[JVMs]: https://github.com/open-telemetry/opentelemetry-java-instrumentation/blob/main/docs/supported-libraries.md#jvms-and-operating-systems
[Application Servers]: https://github.com/open-telemetry/opentelemetry-java-instrumentation/blob/main/docs/supported-libraries.md#application-servers
[Libraries & Frameworks]: https://github.com/open-telemetry/opentelemetry-java-instrumentation/blob/main/docs/supported-libraries.md#libraries--frameworks
[Incompatible]: ./nomenclature
[Compatible]: ./nomenclature
[Supported]: ./nomenclature
