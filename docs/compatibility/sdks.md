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

For the best (and supported) experience, we recommend exporting data from EDOT SDKs via the [EDOT Collector](https://elastic.github.io/opentelemetry/edot-collector/index).

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

🚧 Coming soon

### EDOT PHP

🚧 Coming soon

### EDOT Python

| EDOT Python | Elastic Stack 8.x | Elastic Stack 9.x | Serverless |
| ----------- | ----------------- | ----------------- | ---------- |
| 1.0.0       | 8.18.0+¹          | 9.0.0+¹           | ✅ ²       |

***1.** Via the EDOT Collector.*

***2.** Via the OTel-native ingest endpoint.*

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
