---
navigation_title: Limitations
description: Limitations of Elastic Distributions of OpenTelemetry (EDOT) compared to classic Elastic data collection mechanisms.
applies_to:
  stack:
  serverless:
    observability:
  products:
    - cloud-serverless
    - observability
---

# Limitations of Elastic Distributions of OpenTelemetry

The Elastic Distributions of OpenTelemetry (EDOT) come with a new way of ingesting data in OTel-native way and format. Elastic is continuously working on providing a great experience with OTel-native data within Elastic solutions, contributing popular Elastic features to the upstream OpenTelemetry projects and aligning concepts with OpenTelemetry.

While EDOT and OTel-native data collection already covers most of the core Observability use cases, the following limitations apply compared to data collection with classic Elastic data collection mechanisms.

## Centralized parsing and processing of data

With OTel-native ingestion of data, for example through the EDOT Collector or the Managed OTLP endpoint, [Elasticsearch Ingest Pipelines](docs-content://manage-data/ingest/transform-enrich/ingest-pipelines.md) are not supported.

The OTel-native data format in Elasticsearch contains dotted fields. Ingest Pipeline processors can't access fields that have a dot in their name without having previously transformed the dotted field into an object using the [`Dot expander processor`](elasticsearch://reference/enrich-processor/dot-expand-processor.md).

To process your OTel data, for example to parse logs data, route data to datastreams, and so on, use [Collector processors](https://opentelemetry.io/docs/collector/configuration/#processors), [`filelogreceiver` operators](https://github.com/open-telemetry/opentelemetry-collector-contrib/blob/main/pkg/stanza/docs/operators/README.md#what-operators-are-available) and other OTel-native processing capabilities.

Refer to [these examples](../edot-collector/config/configure-logs-collection.md) on how to process log data with the (EDOT) OTel Collector.

## Infrastructure and host metrics

Due to limitations and gaps in data collection with the upstream OTel `hostmetrics`, there are corresponding limitations with the curated infrastructure and host metrics UIs in Elastic.

| Limitation                                      | Explanation                                                                                                                                                                                                                     |
|------------------------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Host network panels do not display data in some Elastic Observability UIs. | Due to an upstream limitation, `host.network.*` metrics are not available from OpenTelemetry.                                                                                                                                   |
| Process state is unavailable in OpenTelemetry host metrics. | The `process.state` metric is not present and is assigned a dummy value of "Unknown" in the State column of the host processes table.                                                                                           |
| Host OS version and operating system may show as "N/A". | Although the Elasticsearch exporter processes resource attributes, it may not populate these values.                                                                                                                            |
| Normalized Load data is missing unless the CPU scraper is enabled. | The `system.load.cores` metric is required for the Normalized Load column in the Hosts table and the Normalized Load visualization in the host detailed view.                                                                    |
| MacOS collectors do not support CPU and disk metrics. | The `hostmetrics receiver` does not collect these metrics on macOS, leaving related fields empty.                    |
| Permission issues may cause error logs for process metrics | The `hostmetrics receiver` logs errors if it cannot access certain process information due to insufficient permissions. |

When collecting host metrics through a distribution of the OTel Collector other than EDOT, make sure to enable required metrics that are otherwise disabled by default. Use the EDOT Collector [sample config](https://github.com/elastic/elastic-agent/blob/main/internal/pkg/otel/samples/linux/logs_metrics_traces.yml) for the `hostmetrics` receiver as reference.

## Metrics data ingestion

### Histograms in delta temporality only

Ingestion of OpenTelemetry metrics with the type [`Histogram`](https://opentelemetry.io/docs/specs/otel/metrics/data-model/#histogram) are only supported with [`delta temporality`](https://opentelemetry.io/docs/specs/otel/metrics/data-model/#temporality). Histograms with `cumulative` temporality are dropped before being ingested into Elasticsearch.

Make sure to export histogram metrics with delta temporality or use the [`cumulativetodelta processor`](https://github.com/open-telemetry/opentelemetry-collector-contrib/tree/main/processor/cumulativetodeltaprocessor) as a workaround to convert the temporality for histogram metrics.

### Timestamps precision

As of now, nanoseconds timestamps from the OTel signals are stored with microsecond precision in Elasticsearch.

## Limitations on managed Kubernetes environments

Due to limitations with permissions on managed Kubernetes environments, such as GKE Autopilot or AWS Fargate, the default configurations and onboarding flows for EDOT don't fully work in those environments. This might result in decreased collection of data and certain observability views not showing that data.

## Limitations with APM

### Allowed characters in service names

The `service.name` must conform to this regular expression: `^[a-zA-Z0-9 _-]+$`. 

Your service name must only contain characters from the ASCII alphabet, numbers, dashes, underscores and spaces.

### Runtime metrics

Currently, there are limitations with visualizing language-specific runtime metrics in corresponding **Service > Metrics** tab.

Runtime metrics can be ingested and used to create custom dashboards. As a temporary workaround users can create dashboards from the runtime metrics and attach them as custom dashboards to corresponding services.

## Additional information

For backwards compatibility reasons, Kubernetes metrics and host metrics are ingested twice, once in OTel format and once in Elastic Common Schema (ECS) format.
