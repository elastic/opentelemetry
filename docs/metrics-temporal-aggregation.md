# Metrics temporal aggregation

OpenTelemetry metrics data model provides multiple ways to report metrics temporality:
- cumulative (default)
- delta preferred
- low memory

A complete description and examples are provided in [aggregation temporality documentation](https://opentelemetry.io/docs/specs/otel/metrics/supplementary-guidelines/#aggregation-temporality).

Temporal aggregation effect depends on the OpenTelemetry metric type:

Gauge and up down counters always provide the "last value".

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
