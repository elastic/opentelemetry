# Elastic Distribution of OpenTelemetry limitations

## Collector limitations

The Elastic Distribution of the OpenTelemetry Collector has the following limitations:

- Because of an upstream limitation, `host.network.*` metrics aren't present from the OpenTelemetry side.
- `process.state` isn't present in the OpenTelemetry host metric. It's set to a dummy value of **Unknown** in the **State** column of the host processes table.
- The Elasticsearch exporter handles the resource attributes, but **Host OS version** and **Operating system** may show as "N/A".
- The CPU scraper needs to be enabled to collect the `systm.load.cores` metric, which affects the **Normalized Load** column in the **Hosts** table and the **Normalized Load** visualization on the host detailed view.
- The [`hostmetrics receiver`](https://github.com/open-telemetry/opentelemetry-collector-contrib/tree/main/receiver/hostmetricsreceiver) doesn't support CPU and disk metrics on MacOS. These values will stay empty for collectors running on MacOS.
- The console shows error Log messages when the [`hostmetrics receiver`](https://github.com/open-telemetry/opentelemetry-collector-contrib/tree/main/receiver/hostmetricsreceiver) can't access some of the process information due to permission issues.
- The console shows mapping errors initially until mapping occurs.

## Metrics temporal aggregation

OpenTelemetry metrics data model provides multiple ways to report metrics temporality:
- cumulative (default)
- delta preferred
- low memory

A complete description and examples are provided in [aggregation temporality documentation](https://opentelemetry.io/docs/specs/otel/metrics/supplementary-guidelines/#aggregation-temporality).

Temporal aggregation effect depends on the OpenTelemetry metric type:

Gauge and up down counters always provide the "last value", which means that the producers of those metrics only reads
the last value, they don't keep track of the previous nor compute a delta.

| metric type / temporal aggregation | cumulative | delta preferred | low memory                                   |
|------------------------------------|------------|-----------------|----------------------------------------------|
| gauge                              | last value | last value      | last value                                   |
| up down counter                    | last value | last value      | last value                                   |
| counter                            | cumulative | delta           | synchronous: delta, asynchronous: cumulative |
| histogram                          | cumulative | delta           | delta                                        |

When metrics are stored in Elasticsearch with the `otel` mode,
OpenTelemetry metrics will be written to Time Series Data Stream (TSDS) which currently only support delta histograms.

As a consequence, metrics sent to Elasticsearch currently need to use the "delta preferred" to properly store histograms,
otherwise they will be discarded by the collector.

Setting `OTEL_EXPORTER_OTLP_METRICS_TEMPORALITY_PREFERENCE=delta` should allow to configure SDKs to change the default value.
(see [reference](https://github.com/open-telemetry/opentelemetry-specification/blob/main/spec-compliance-matrix.md#environment-variables) on supported SDKs).

In the case were the producer of `counter` or `histogram` metrics can't be configured with `delta preferred` behavior to report them with `delta`
temporal aggregation, using the collector [`cumulativetodelta`](https://github.com/open-telemetry/opentelemetry-collector-contrib/blob/main/processor/cumulativetodeltaprocessor)
processor can be used to convert from `cumulative` to `delta`.

Using [`cumulativetodelta`](https://github.com/open-telemetry/opentelemetry-collector-contrib/blob/main/processor/cumulativetodeltaprocessor)
does however involves some challenges as it makes the processor stateful:

- metrics from a given producer must be sent to the same collector instance
- increases memory usage to keep track of per-metric state
- metrics needs to be configured at the collector level to opt-in/out of this processing

As a consequence, using the `cumulativetodelta` processor is recommended close to the edge (where metrics are produced),
and less recommended late in the data pipeline due to scalability challenges.
