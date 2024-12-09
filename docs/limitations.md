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

The [Elasticsearch exporter](https://github.com/open-telemetry/opentelemetry-collector-contrib/blob/main/exporter/elasticsearchexporter) only support histograms with delta temporality,
as a consequence SDKs must be configured to report or convert them as delta.
Changing temporal aggregation also impacts [visualizations](#visualizations).

OpenTelemetry SDKs provide multiple ways to report metrics temporality:
- cumulative (default)
- delta preferred
- low memory

A complete description and examples are provided in [aggregation temporality documentation](https://opentelemetry.io/docs/specs/otel/metrics/supplementary-guidelines/#aggregation-temporality).

With `low memory`, `counter` metrics are reported either as `delta` or `cumulative` when they are captured synchronously
or asynchronously. Because querying `counter` metrics currently depends on temporal aggregation (see [Visualizations](#visualizations))
this means visualizations depend on metric synchronous/asynchronous value capture.

Temporal aggregation effect depends on the OpenTelemetry metric type:

Gauge and up down counters always provide the "last value", which means that the producers of those metrics only reads
the last value, they don't keep track of the previous nor compute a delta.

| metric type / temporal aggregation | cumulative | delta preferred |
|------------------------------------|------------|-----------------|
| gauge                              | last value | last value      |
| up down counter                    | last value | last value      |
| counter                            | cumulative | delta           |
| histogram                          | cumulative | delta           |


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

# Visualizations

With `counter` metrics, the absolute value is not relevant but the _rate_ of the value is, for example with a `counter`
for the "number of HTTP requests", a visualization would likely be "number of HTTP requests per minute", this is usually
implemented in Kibana/Lens with a `Counter rate` function applied on the time series.

As a consequence, visualizations of `counter` metrics are currently tied to the metric temporal aggregation used, which
means changing a metric temporal aggregation will require to modify visualizations or creating dedicated visualizations
per temporal aggregation.