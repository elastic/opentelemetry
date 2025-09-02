---
navigation_title: Use the upstream Collector
description: Learn how to send data to Elastic Observability using the upstream OpenTelemetry Collector instead of EDOT.
applies_to:
  stack:
  serverless:
    observability:
  product:
    edot_collector: ga
products:
  - id: cloud-serverless
  - id: observability
  - id: edot-collector
---

# Send data to {{serverless-full}} using the upstream Collector

While the [{{edot}} (EDOT) Collector](/reference/index.md) provides a streamlined experience with pre-selected components, you can also use the contrib OpenTelemetry Collector or a custom distribution to send data to Elastic Observability. This approach requires more configuration but gives you equal control over your OpenTelemetry setup.

## Overview

The contrib OpenTelemetry Collector is the community-maintained version that provides the foundation for all OpenTelemetry distributions. To configure it to work with Elastic Observability, you need to:

- Manually select and configure components.
- Set up proper data processing pipelines.
- Handle authentication and connection details.
- Ensure required components have been properly configured in accordance to your use case.

## Deployment scenarios

The configuration requirements vary depending on your use case and the Elastic deployment model you want to send data to. The following sections outline what you need for each scenario.

### Elastic Cloud Serverless

{{serverless-full}} provides a [Managed OTLP Endpoint](/reference/motlp.md) that accepts OpenTelemetry data in its native format. This makes it the simplest scenario for using upstream components because scaling and signal processing (eg. producing metrics from events) is handled by Elastic.

The following configuration example shows how to send data to the Managed OTLP Endpoint:

```yaml
exporters:
  otlp:
    endpoint: "https://your-deployment.elastic-cloud.com:443"
    headers:
      authorization: "Bearer YOUR_API_KEY"

service:
  pipelines:
    traces:
      exporters: [otlp]
    metrics:
      exporters: [otlp]
    logs:
      exporters: [otlp]
```

### Elastic Cloud Hosted (ECH)

Managed OTLP is yet to come to {{ech}}, meanwhile you need to setup an instance of EDOT that works as a gateway, handling processing required for some use cases (eg. deriving metrics from events in APM) and writes data directly to Elasticsearch using the Elasticsearch exporter. You can point your contrib collector OTLP exporter to the EDOT gateway

```yaml
receivers:
  - gomod: go.opentelemetry.io/collector/receiver/otlpreceiver

processors:
  - gomod: github.com/open-telemetry/opentelemetry-collector-contrib/processor/resourcedetectionprocessor
  - gomod: github.com/open-telemetry/opentelemetry-collector-contrib/processor/attributesprocessor
  - gomod: go.opentelemetry.io/collector/processor/batchprocessor

exporters:
  - gomod: github.com/open-telemetry/opentelemetry-collector-contrib/exporter/elasticsearchexporter
```

The following configuration example shows how to send data to Elasticsearch:

```yaml
receivers:
  otlp:
    protocols:
      grpc:
        endpoint: 0.0.0.0:4317
      http:
        endpoint: 0.0.0.0:4318

processors:
  resourcedetection:
    detectors: [env, system, gcp, ecs, ec2, azure, aks, eks, gke]
    timeout: 5s
    override: true
  
  attributes:
    actions:
      - key: service.name
        value: "your-service-name"
        action: insert
  
  batch:
    timeout: 1s
    send_batch_size: 1024

exporters:
  elasticsearch:
    endpoints: ["https://your-ech-instance.elastic-cloud.com:9243"]
    user: "elastic"
    password: "YOUR_PASSWORD"
    tls:
      insecure: false
    num_workers: 4
    timeout: 90s

service:
  pipelines:
    traces:
      receivers: [otlp]
      processors: [resourcedetection, attributes, batch]
      exporters: [elasticsearch]
    metrics:
      receivers: [otlp]
      processors: [resourcedetection, attributes, batch]
      exporters: [elasticsearch]
    logs:
      receivers: [otlp]
      processors: [resourcedetection, attributes, batch]
      exporters: [elasticsearch]
```

### Self-managed Elastic Stack

Self-managed deployments have similar requirements to ECH but with your own Elasticsearch instance. The configuration is similar to ECH. In addition you need to:

- Point to your self-managed Elasticsearch instance.
- Configure appropriate security settings.
- Ensure your Elasticsearch version is compatible.
- Set up proper index templates and mappings.

## Building a custom upstream Collector

To use the upstream OpenTelemetry Collector with Elastic Observability, you need to build a custom distribution that includes the required components.

## Configuration best practices

When using the upstream OpenTelemetry Collector with Elastic Observability, follow these best practices.

### Resource detection

Always include the `resourcedetectionprocessor` to automatically add host, cloud, and Kubernetes metadata:

```yaml
processors:
  resourcedetection:
    detectors: [env, system, gcp, ecs, ec2, azure, aks, eks, gke]
    timeout: 5s
    override: true
```

### Attribute processing

Use the `attributesprocessor` to ensure consistent attribute naming and add required metadata:

```yaml
processors:
  attributes:
    actions:
      - key: service.name
        value: "your-service-name"
        action: insert
      - key: service.version
        value: "1.0.0"
        action: insert
```

### Batching

Configure the `batchprocessor` for optimal performance:

```yaml
processors:
  batch:
    timeout: 1s
    send_batch_size: 1024
    send_batch_max_size: 2048
```

### Security

For production deployments, always use secure connections:

```yaml
exporters:
  elasticsearch:
    tls:
      insecure: false
      ca_file: "/path/to/ca.crt"
    user: "elastic"
    password: "YOUR_PASSWORD"
```

## Limitations and considerations

Using the upstream OpenTelemetry Collector instead of EDOT comes with some trade-offs. Refer to [EDOT compared to upstream OpenTelemetry](/reference/compatibility/edot-vs-upstream.md) for more information.

## Next steps

- [Build a custom EDOT-like collector](/reference/edot-collector/custom-collector.md) for more control.
- [Configure the EDOT Collector](/reference/edot-collector/config/index.md) for optimal Elastic integration.
- [Learn about EDOT components](/reference/edot-collector/components.md) to understand what's included.
- [Explore deployment architectures](/reference/architecture/index.md) for different environments.
