# Elastic Distribution of OpenTelemetry Collector limitations

The Elastic Distribution of the OpenTelemetry Collector has the following limitations:

- Because of an upstream limitation, `host.network.*` metrics aren't present from the OpenTelemetry side.
- `process.state` isn't present in the OpenTelemetry host metric. It's set to a dummy value of **Unknown** in the **State** column of the host processes table.
- The Elasticsearch exporter handles the resource attributes, but **Host OS version** and **Operating system** may show as "N/A".
- The CPU scraper needs to be enabled to collect the `systm.load.cores` metric, which affects the **Normalized Load** column in the **Hosts** table and the **Normalized Load** visualization on the host detailed view.
- The [`hostmetrics receiver`](https://github.com/open-telemetry/opentelemetry-collector-contrib/tree/main/receiver/hostmetricsreceiver) doesn't support CPU and disk metrics on MacOS. These values will stay empty for collectors running on MacOS.
- The console shows error Log messages when the [`hostmetrics receiver`](https://github.com/open-telemetry/opentelemetry-collector-contrib/tree/main/receiver/hostmetricsreceiver) can't access some of the process information due to permission issues.
- The console shows mapping errors initially until mapping occurs.