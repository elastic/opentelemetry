---
title: Configuration
layout: default
nav_order: 3
---

## Upstream collector configuration examples

Use the Elastic [example configurations](https://github.com/elastic/elastic-agent/tree/main/internal/pkg/otel/samples) as a reference when configuring your upstream collector.

## Collector Configuration

The EDOT Collector uses a YAML-based configuration file. Below is a sample configuration:

```
  hostmetrics/system:
    collection_interval: 30s
    scrapers:
      cpu:
      memory:
      disk:

  # Receiver for platform logs
  filelog/platformlogs:
    include: [ /var/log/*.log ]
    start_at: end

processors:
  resourcedetection:
    detectors: ["system"]
  attributes/dataset:
    actions:
      - key: event.dataset
        from_attribute: data_stream.dataset
        action: upsert

exporters:
  elasticsearch:
    endpoints: ["${env:ELASTIC_ENDPOINT}"]
    api_key: ${env:ELASTIC_API_KEY}
    mapping:
      mode: ecs

service:
  extensions: [file_storage]
  pipelines:
    metrics:
      receivers: [hostmetrics/system]
      processors: [resourcedetection, attributes/dataset]
      exporters: [elasticsearch]
    logs:
      receivers: [filelog/platformlogs]
      processors: [resourcedetection]
      exporters: [elasticsearch]

```

**Note**: Replace `"https://your-elastic-instance:9200"` with your Elastic instance URL and `"YOUR_API_KEY"` with your API key.

For comprehensive configuration options, consult the [OpenTelemetry Collector documentation](https://github.com/open-telemetry/opentelemetry-collector).



