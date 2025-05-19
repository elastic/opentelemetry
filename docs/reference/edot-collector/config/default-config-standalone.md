---
navigation_title: Default config (Standalone)
description: Default configuration of the EDOT Collector in standalone mode.
applies_to:
  stack:
  serverless:
    observability:
products:
  - id: cloud-serverless
  - id: observability
  - id: edot-collector
---

# Default configuration of the EDOT Collector (Standalone)

The default configuration of the Elastic Distribution of OpenTelemetry (EDOT) Collector includes pipelines for the collection of logs, host metrics, and data from OpenTelemetry SDKs.

The following sampling files are available:

| Use Cases | Direct ingestion into Elasticsearch | Managed OTLP Endpoint |
|---|---|---|
| Platform logs | [Logs - ES] | [Logs - OTLP] |
| Platform logs and host metrics | [Logs &#124; Metrics - ES] | [Logs &#124; Metrics - OTLP] |
| Platform logs, host metrics, <br> and application telemetry | [Logs &#124; Metrics &#124; App - ES]<br>(*default*) | [Logs &#124; Metrics &#124; App - OTLP]<br>(*default*) |

Use the previous example configurations as a reference when configuring your upstream collector or customizing your EDOT Collector configuration.

The following sections describe the default pipelines by use cases.

## Direct ingestion into Elasticsearch

For self-managed and Elastic Cloud Hosted stack deployment use cases, ingest OpenTelemetry data from the EDOT Collector directly into Elasticsearch using the [`elasticsearch`] exporter.

Learn more about the configuration options for the `elasticsearch` exporter in the [corresponding documentation](https://github.com/open-telemetry/opentelemetry-collector-contrib/blob/main/exporter/elasticsearchexporter/README.md#configuration-options).

The `elasticsearch` exporter comes with two relevant data ingestion modes:

- `ecs`: Writes data in backwards compatible Elastic Common Schema (ECS) format. Original attribute names and semantics might be lost during translation.
- `otel`: OTel attribute names and semantics are preserved.

The goal of EDOT is to preserve OTel data formats and semantics as much as possible, so `otel` is the default mode for the EDOT Collector. Some use cases might require data to be exported in ECS format for backwards compatibility.

### Logs collection pipeline

For logs collection, the default configuration uses the [`filelog`] receiver to read log entries from files.  In addition, the [`resourcedetection`] processor enriches the log entries with metadata about the corresponding host and operating system.

Data is exported directly to Elasticsearch using the [`elasticsearch`] exporter in `OTel-native` mode.

### Application and traces collection pipeline

The application pipeline in the EDOT Collector receives data from OTel SDKs through the [`OTLP`] receiver. While logs and metrics are exported verbatim into Elasticsearch, traces require two additional components.

The [`elastictrace`] processor enriches trace data with additional attributes that improve the user experience in the Elastic Observability UIs. In addition, the [`elasticapm`] connector generates pre-aggregated APM metrics from tracing data.

Application-related OTel data is ingested into Elasticsearch in OTel-native format using the [`elasticsearch`] exporter.

:::{note}
Both components, `elastictrace` and `elasticapm` are required for Elastic APM UIs to work properly. As they aren't included in the OpenTelemetry [Collector Contrib repository](https://github.com/open-telemetry/opentelemetry-collector-contrib), you can:

* Use the EDOT Collector with the available configuration to ingest data into Elasticsearch.
* [Build a custom, EDOT-like Collector](../custom-collector.md) for ingesting data into Elasticsearch.
* Use Elastic's [managed OTLP endpoint](../../quickstart/serverless/index.md) that does the enrichment for you.
:::

### Host metrics collection pipeline

The host metrics pipeline uses the [`hostmetrics`] receiver to collect `disk`, `filesystem`, `cpu`, `memory`, `process` and `network` metrics for the corresponding host.

For backwards compatibility, host metrics are translated into ECS-compatible system metrics using the [`elasticinframetrics`] processor. Finally, metrics are ingested in `ecs` format through the [`elasticsearch`] exporter.

The [`resourcedetection`] processor enriches the metrics with meta information about the corresponding host and operating system. The [`attributes`] and [`resource`] processor are used to set some fields for proper routing of the ECS-based system metrics data into corresponding Elasticsearch data streams.

## Using the Managed OTLP Endpoint

When ingesting OTel data through Elastics Managed OTLP endpoint, all the enrichment that is required for an optimal experience in the Elastic solutions happens at the managed OTLP endpoint level and is transparent to users. 

The Collector configuration for all the use cases involving the Managed OTLP endpoint is only concerned with local data collection and context enrichment.

Platform logs are scraped with the [`filelog`] receiver, host metrics are collected through the [`hostmetrics`] receiver and both signals are enriched with meta information through the [`resourcedetection`] processor.

Data from OTel SDKs is piped through the [`OTLP`] receiver directly to the OTLP exporter that sends data for all the signals to the managed OTLP endpoint.

With the managed OTLP Endpoint there is no need for configuring any Elastic-specific components, such as [`elasticinframetrics`], [`elastictrace`] processors, [`elasticapm`] connector or the [`elasticsearch`] exporter. Edge setup and configuration can be 100% vendor agnostic.

[`attributes`]: https://github.com/open-telemetry/opentelemetry-collector-contrib/tree/main/processor/attributesprocessor
[`filelog`]: https://github.com/open-telemetry/opentelemetry-collector-contrib/tree/main/receiver/filelogreceiver
[`hostmetrics`]: https://github.com/open-telemetry/opentelemetry-collector-contrib/tree/main/receiver/hostmetricsreceiver
[`elasticsearch`]: https://github.com/open-telemetry/opentelemetry-collector-contrib/tree/main/exporter/elasticsearchexporter
[`elasticinframetrics`]: https://github.com/elastic/opentelemetry-collector-components/tree/main/processor/elasticinframetricsprocessor
[`elastictrace`]: https://github.com/elastic/opentelemetry-collector-components/tree/main/processor/elastictraceprocessor
[`elasticapm`]: https://github.com/elastic/opentelemetry-collector-components/tree/main/connector/elasticapmconnector
[`resource`]: https://github.com/open-telemetry/opentelemetry-collector-contrib/tree/main/processor/resourceprocessor
[`resourcedetection`]: https://github.com/open-telemetry/opentelemetry-collector-contrib/tree/main/processor/resourcedetectionprocessor
[`OTLP`]: https://github.com/open-telemetry/opentelemetry-collector/tree/main/receiver/otlpreceiver
[Logs - ES]: https://raw.githubusercontent.com/elastic/elastic-agent/refs/heads/main/internal/pkg/otel/samples/linux/platformlogs.yml
[Logs - OTLP]: https://raw.githubusercontent.com/elastic/elastic-agent/refs/heads/main/internal/pkg/otel/samples/linux/managed_otlp/platformlogs.yml
[Logs &#124; Metrics - ES]: https://raw.githubusercontent.com/elastic/elastic-agent/refs/heads/main/internal/pkg/otel/samples/linux/platformlogs_hostmetrics.yml
[Logs &#124; Metrics - OTLP]: https://raw.githubusercontent.com/elastic/elastic-agent/refs/heads/main/internal/pkg/otel/samples/linux/managed_otlp/platformlogs_hostmetrics.yml
[Logs &#124; Metrics &#124; App - ES]: https://raw.githubusercontent.com/elastic/elastic-agent/refs/heads/main/internal/pkg/otel/samples/linux/logs_metrics_traces.yml
[Logs &#124; Metrics &#124; App - OTLP]: https://raw.githubusercontent.com/elastic/elastic-agent/refs/heads/main/internal/pkg/otel/samples/linux/managed_otlp/logs_metrics_traces.yml
