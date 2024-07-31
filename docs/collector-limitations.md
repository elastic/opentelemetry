# Elastic OpenTelemetry Collector limitations

The Elastic Distribution for the OpenTelemetry Collector has the following limitations:

- `host.network.*` metrics aren't present from OpenTelemetry side.
- `process.state` isn't present in the OpenTelemetry host metric. It's set to a dummy value of **Unknown** in the **State** column of the host processes table.
- The Elasticsearch exporter handles the metadata fields, but **Host OS version** and**Operating system** may show as "N/A" and **Host IP** may show different values.
- The CPU scraper needs to be enabled to collect the `systm.load.cores` metric, which affects the **Normalized Load** column in the **Hosts** table and the **Normalized Load** visualization on the host detailed view.