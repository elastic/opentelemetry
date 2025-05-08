---
title: Features 
layout: default
parent: Compatibility & Support
nav_order: 2
---

# Elastic Features available with EDOT

### Legend
{: .no_toc }

| **[Incompatible]** | **[Compatible]** | **[Supported]** |
| ❌ | 🟡 | ✅ |

### Features

| Feature | Availability |
|:---|:---:|
| **APM** | ✅ |
| &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; [Service Maps] | ✅ |
| &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; [Distributed Tracing] | ✅ |
| &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; [Head-based Sampling (HBS)] | ✅ |
| &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; *[Tail-based Sampling (TBS)]* | 🟡 |
| &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; [Self-managed, OTel collector-based TBS] | 🟡 |
| &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; TBS managed / hosted in Elastic Cloud | ❌ |
| &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Runtime metrics<sup>(1)</sup> | ⚪ |
| **Infrastructure Monitoring** | ✅ |
| &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Host view<sup>(2)</sup> | ✅ |
| &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Kubernetes dashboard | ✅ |
| **Logs Collection** | ✅ |
| &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; OTel-native, collector-based logs parsing & processing | ✅ |
| &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; OTel-native, collector-based data routing | ✅ |
| &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Managed, centralized processing<sup>(3)</sup> | ❌ |
| **Metrics Collection**<sup>(4)</sup> | ✅ |
| &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Automatic metrics mapping | ✅ |
| &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Usage of [Time Series Data Streams](https://www.elastic.co/guide/en/elasticsearch/reference/current/tsds.html) | ✅ |
| **Central Management** | ❌ |
| &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Central management of OTel collectors | ❌ |
| &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Central management of OTel SDKs | ❌ |


<sup>(1)</sup> see [language-specific features overview](../edot-sdks/index#features)

<sup>(2)</sup> see [limitations on host metrics](./limitations#infrastructure--host-metrics)

<sup>(3)</sup> see [limitations on Ingest Pipelines](./limitations#centralized-parsing-and-processing-of-data)

<sup>(4)</sup> see [limitations on metrics ingestion](./limitations#ingestion-of-metrics-data)

Check out the [SDKs Overview](../edot-sdks/index#features) page for SDK-specific features.

[Incompatible]: ./nomenclature
[Compatible]: ./nomenclature
[Supported]: ./nomenclature

[Service Maps]: https://www.elastic.co/guide/en/observability/current/apm-service-maps.html
[Distributed Tracing]: https://www.elastic.co/guide/en/observability/current/apm-traces.html
[Head-based Sampling (HBS)]: https://www.elastic.co/guide/en/observability/current/apm-sampling.html#apm-head-based-sampling
[Tail-based Sampling (TBS)]: https://www.elastic.co/guide/en/observability/current/apm-sampling.html#apm-tail-based-sampling
[Self-managed, OTel collector-based TBS]: https://opentelemetry.io/blog/2022/tail-sampling/