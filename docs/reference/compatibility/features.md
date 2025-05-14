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

The following table shows Elastic features and their level of support and compatibility with Elastic Distributions of OpenTelemetry (EDOT). Refer to the [SDKs Overview](../edot-sdks/index.md) for SDK-specific features.

| Feature                                                                                     | Availability     |
| :------------------------------------------------------------------------------------------ | :--------------- |
| **APM**                                                                                     | [Supported]      |
| [Service Maps]                                                                              | [Supported]      |
| [Distributed Tracing]                                                                       | [Supported]      |
| [Head-based Sampling (HBS)]                                                                 | [Supported]      |
| *[Tail-based Sampling (TBS)]*                                                               | [Compatible]     |
| [Self-managed, OTel collector-based TBS]                                                    | [Compatible]     |
| TBS managed / hosted in Elastic Cloud                                                       | [Incompatible]   |
| Runtime metrics                                                                             | [See language-specific overview](../edot-sdks/index.md) |
| **Infrastructure Monitoring**                                                               | [Supported]      |
| Host view^1^                                                                                | [Supported]      |
| Kubernetes dashboard                                                                        | [Supported]      |
| **Logs Collection**                                                                         | [Supported]      |
| OTel-native, collector-based logs parsing & processing                                      | [Supported]      |
| OTel-native, collector-based data routing                                                   | [Supported]      |
| Managed, centralized processing^2^                                                          | [Incompatible]   |
| **Metrics Collection**^3^                                                                   | [Supported]      |
| Automatic metrics mapping                                                                   | [Supported]      |
| Usage of [Time Series Data Streams]                                                         | [Supported]      |
| **Central Management**                                                                      | [Incompatible]   |
| Central management of OTel collectors                                                       | [Incompatible]   |
| Central management of OTel SDKs                                                             | [Incompatible]   |


^1^ Refer to [limitations on host metrics](limitations.md#infrastructure-and-host-metrics)

^2^ Refer to [limitations on Ingest Pipelines](limitations.md#centralized-parsing-and-processing-of-data)

^3^ Refer to [limitations on metrics ingestion](limitations.md#metrics-data-ingestion)

[Incompatible]: nomenclature.md
[Compatible]: nomenclature.md
[Supported]: nomenclature.md

[Service Maps]: docs-content://solutions/observability/apm/service-map.md
[Distributed Tracing]: docs-content://solutions/observability/apm/traces-ui.md
[Head-based Sampling (HBS)]: docs-content://solutions/observability/apm/transaction-sampling.md#apm-head-based-sampling
[Tail-based Sampling (TBS)]: docs-content://solutions/observability/apm/transaction-sampling.md#apm-tail-based-sampling
[Self-managed, OTel collector-based TBS]: https://opentelemetry.io/blog/2022/tail-sampling/
[Time Series Data Streams]: docs-content://manage-data/data-store/data-streams/time-series-data-stream-tsds.md