---
navigation_title: Features
description: Overview of Elastic features available with EDOT.
applies_to:
  stack:
  serverless:
    observability:
products:
  - id: cloud-serverless
  - id: observability
---

# Elastic features available with EDOT

The following table shows Elastic features and their level of support and compatibility with Elastic Distributions of OpenTelemetry (EDOT). Refer to the [SDKs Overview](/reference/edot-sdks/index.md) for SDK-specific features.

| Feature                                                     | Compatibility    | Support level    |
| :-----------------------------------------------------------| :--------------- | :--------------- |
| **APM**                                                     | [Compatible]     | [Supported]      |
| [Service Maps]                                              | [Compatible]     | [Supported]      |
| [Distributed Tracing]                                       | [Compatible]     | [Supported]      |
| [Head-based Sampling (HBS)]                                 | [Compatible]     | [Supported]      |
| *[Tail-based Sampling (TBS)]*                               | [Compatible]     | [Not supported]  |
| [Self-managed, OTel Collector-based TBS]                    | [Compatible]     | [Not supported]  |
| TBS managed / hosted in {{ecloud}}                          | [Incompatible]   | [Not supported]  |
| Runtime metrics                                             | [See language-specific overview](/reference/edot-sdks/index.md) | -                |
| **Infrastructure Monitoring**                               | [Compatible]     | [Supported]      |
| Host view^1^                                                | [Compatible]     | [Supported]      |
| Kubernetes dashboard                                        | [Compatible]     | [Supported]      |
| **Logs Collection**                                         | [Compatible]     | [Supported]      |
| OTel-native, Collector-based logs parsing & processing      | [Compatible]     | [Supported]      |
| OTel-native, Collector-based data routing                   | [Compatible]     | [Supported]      |
| Managed, centralized processing^2^                          | [Incompatible]   | [Not supported]  |
| **Metrics Collection**^3^                                   | [Compatible]     | [Supported]      |
| Automatic metrics mapping                                   | [Compatible]     | [Supported]      |
| Usage of [Time Series Data Streams]                         | [Compatible]     | [Supported]      |
| **Central Management**                                      | [Incompatible]   | [Not supported]  |
| Central management of OTel collectors                       | [Incompatible]   | [Not supported]  |
| Central management of OTel SDKs                             | [Incompatible]   | [Not supported]  |


^1^ Refer to [limitations on host metrics](limitations.md#infrastructure-and-host-metrics)

^2^ Refer to [limitations on Ingest Pipelines](limitations.md#centralized-parsing-and-processing-of-data)

^3^ Refer to [limitations on metrics ingestion](limitations.md#metrics-data-ingestion)

[Incompatible]: nomenclature.md
[Compatible]: nomenclature.md
[Not supported]: nomenclature.md
[Supported]: nomenclature.md

[Service Maps]: docs-content://solutions/observability/apm/service-map.md
[Distributed Tracing]: docs-content://solutions/observability/apm/traces-ui.md
[Head-based Sampling (HBS)]: docs-content://solutions/observability/apm/transaction-sampling.md#apm-head-based-sampling
[Tail-based Sampling (TBS)]: docs-content://solutions/observability/apm/transaction-sampling.md#apm-tail-based-sampling
[Self-managed, OTel Collector-based TBS]: https://opentelemetry.io/blog/2022/tail-sampling/
[Time Series Data Streams]: docs-content://manage-data/data-store/data-streams/time-series-data-stream-tsds.md