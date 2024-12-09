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

## Elasticsearch storage limitations 

Currently, OpenTelemetry `counter` metrics are stored as a TSDS `counter` in Elasticsearch, which means they are stored
as a monotonically increasing value. The absolute value of those metrics is often useless, and we are almost always
interested in the rate rather than the absolute value.

Elasticsearch only supports delta histograms, and cumulative histograms are discarded.

As a consequence, metrics sent to Elasticsearch currently need to use the "delta preferred" to properly store histograms.
See [metrics temporal aggregation](metrics-temporal-aggregation.md) for more details.

## Kibana/Lens limitations

TODO