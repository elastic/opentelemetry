---
title: Overview
layout: default
nav_order: 1
---

# EDOT Language SDKs

The Elastic Distributions of OpenTelemetry (EDOT) Language SDKs (aka. application agents) are thin wrappers around corresponding upstream [OpenTelemetry SDKs](https://opentelemetry.io/docs/languages/), preconfigured for best experience with Elastic Observability.
EDOT Language SDKs are fully compatible with and can be used as a drop in replacement for upstream OTel SDKs. 
In addition, EDOT SDKs provide some popular, enterprise add-on features Elastic APM users might know from classic Elastic APM agents.

![](../images/edot-sdks.png)

Currently, the following EDOT SDKs are availble:

| EDOT SDK | Release Status |
|:-------------------|:---------------|
| [EDOT .NET](./dotnet/index) | Technical Preview |
| [EDOT Java](./java/index) | GA |
| [EDOT Node.js](./nodejs/index) | Technical Preview |
| [EDOT PHP](./php/index) | Technical Preview |
| [EDOT Python](./python/index) | Technical Preview |
| [EDOT Android](./android/index) | Technical Preview |
| [EDOT iOS](./ios/index) | GA |

For languages for which Elastic does not offer its own distribution, we recommend using the upstream OTel SDKs:

| Language | Release Status |
|:-------------------|:---------------|
| JS / Browser | [Vanilla OTel RUM SDK/API](https://opentelemetry.io/docs/languages/js/) |
| Rust       | [Vanilla OTel Rust SDK/API](https://opentelemetry.io/docs/languages/rust/) |
| Ruby       | [Vanilla OTel Ruby SDK/API](https://opentelemetry.io/docs/languages/ruby/) |
| Go         | [Vanilla OTel Go SDK/API](https://opentelemetry.io/docs/languages/go/) |
| C++        | [Vanilla OTel C++ SDK/API](https://opentelemetry.io/docs/languages/cpp/)  |

## Elastic Support for EDOT SDKs

Elastic provides technical support for EDOT Language SDKs according to Elastic's [Support Policy](https://www.elastic.co/support_policy). EDOT SDKs are meant to be used in combination with the [EDOT Collector](../edot-collector/index) or Elastic's managed OTLP endpoint (on Elastic Cloud Serverless) to ingest data into Elastic solutions from the EDOT SDKs. Other ingestion paths are not officially supported by Elastic.

### 📄 License
EDOT SDKs are licensed under the [Apache License, Version 2.0](https://www.apache.org/licenses/LICENSE-2.0). 