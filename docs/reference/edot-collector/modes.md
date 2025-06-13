---
navigation_title: Deployment modes
description: Deployment modes for the Elastic Distribution of OpenTelemetry (EDOT) Collector, including Agent and Gateway modes and when to use each.
applies_to:
  stack:
  serverless:
    observability:
products:
  - id: cloud-serverless
  - id: observability
  - id: edot-collector
---

# EDOT Collector deployment modes

You can deploy the {{edot}} (EDOT) Collector in different modes to meet various observability requirements. The two primary deployment modes are Agent and Gateway. Depending on whether you're using a self-managed or cloud deployment, each mode fulfills different roles.

This document explains the two primary deployment modes: Agent and Gateway, and when to use each.

These patterns aren't rigid architectural blueprints but flexible approaches that you can adapt to your specific environment and needs.

## EDOT Collector as Agent

In Agent mode, the EDOT Collector runs close to the data source, collecting telemetry data directly from the local environment.

### Characteristics

- Deployed on individual hosts or as DaemonSets in Kubernetes
- Collects data from local sources:
  - Infrastructure metrics (CPU, memory, disk, network)
  - Platform logs (system logs, container logs)
  - Application telemetry via OpenTelemetry SDKs
- Performs initial processing, filtering, and batching
- Forwards data to either:
  - Elastic directly (Elasticsearch or Managed OTLP Endpoint)
  - Another collector running in Gateway mode

### When to use Agent mode

Use the EDOT Collector in Agent mode when:

- You need to collect data directly from hosts or applications
- You want to minimize network traffic by performing initial filtering at the source
- You have a simple deployment with a small number of hosts


## EDOT Collector as Gateway

In Gateway mode, the EDOT Collector acts as a central aggregation point, receiving data from multiple Agent collectors before forwarding it to Elastic.

### Characteristics

- Deployed as a centralized service
- Receives data from other collectors running in Agent mode
- Performs additional processing, enrichment, and aggregation
- Handles the final export to Elastic

### When to use Gateway mode

Use the EDOT Collector in Gateway mode when:

- You have multiple data sources or agents that need centralized processing
- You need to implement organization-wide processing rules
- You want to reduce the number of connections to your Elastic backend
- You need advanced pre-processing before data reaches Elastic
- You're using a self-managed Elasticsearch deployment (required for APM functionality)

### Example configuration

The EDOT Collector in Gateway mode typically includes an OTLP receiver to accept data from Agent collectors:

```yaml
receivers:
  otlp:
    protocols:
      grpc:
        endpoint: 0.0.0.0:4317
      http:
        endpoint: 0.0.0.0:4318
```

## Gateway Requirements for Self-Managed Environments

For self-managed Elasticsearch environments, a Gateway collector configured with the Elasticsearch exporter is necessary for proper data ingestion. This is because:

1. **APM Functionality**: The Gateway includes essential components for APM functionality:
   - The `elastictrace` processor enriches trace data with additional attributes that improve the user experience in Elastic Observability UIs
   - The `elasticapm` connector generates pre-aggregated APM metrics from tracing data

2. **Data Format Translation**: The Gateway handles the translation between OpenTelemetry data formats and Elasticsearch-compatible formats when needed

3. **Efficient Data Routing**: The Gateway uses the routing connector to direct different types of telemetry data to the appropriate pipelines

### Example Gateway configuration for Elasticsearch export

```yaml
processors:
  elastictrace: {}
  
connectors:
  elasticapm: {}
  routing:
    default_pipelines: [metrics/otel]
    error_mode: ignore
    table:
      - context: metric
        statement: route() where IsMatch(instrumentation_scope.name, "github.com/open-telemetry/opentelemetry-collector-contrib/receiver/hostmetricsreceiver/internal/scraper/*")
        pipelines: [metrics/infra/ecs, metrics/otel]

exporters:
  elasticsearch/otel:
    endpoints:
      - ${ELASTIC_ENDPOINT}
    api_key: ${ELASTIC_API_KEY}
    mapping:
      mode: otel
```

## Deployment Patterns by Elastic Deployment Type

### Serverless Observability

- **Recommended Pattern**: Agent mode with direct export to Managed OTLP Endpoint
- **Gateway Requirements**: None - the Managed OTLP Endpoint handles all necessary enrichment
- **Notes**: Simplest deployment model with minimal configuration

### Elastic Cloud (ECH)

- **Current Recommended Pattern**: Agent + Gateway mode
- **Future Option**: Agent mode with direct export to Managed OTLP Endpoint (when available)
- **Gateway Requirements**: Required for APM functionality until Managed OTLP Endpoint is available

### Self-Managed Elasticsearch

- **Required Pattern**: Agent + Gateway mode
- **Gateway Requirements**: Required for APM functionality and proper data formatting
- **Notes**: The Gateway must include the `elastictrace` processor, `elasticapm` connector, and Elasticsearch exporter

## Gateway Pattern Beyond Self-Managed Deployments

The Gateway pattern isn't exclusive to self-managed Elasticsearch deployments. It's a general OpenTelemetry pattern that provides benefits in various scenarios:

- **Kubernetes Deployments**: A Gateway collector centralizes cluster-level telemetry from multiple node-level Agent collectors
- **Multi-Region Deployments**: Regional Gateway collectors aggregate data from multiple Agents before sending to a central destination
- **High-Volume Environments**: Gateway collectors provide buffering and batching to handle high volumes of telemetry data
- **Complex Processing**: When advanced data transformation or filtering is needed before data reaches its destination

## Summary

- **Agent Mode**: Local data collection, close to the source
- **Gateway Mode**: Centralized aggregation, processing, and forwarding
- **Self-Managed Environments**: Require a Gateway with specific Elastic components for APM functionality
- **Serverless/Cloud**: Can use Agent mode directly with Managed OTLP Endpoint (when available)
- **Gateway Pattern**: Useful beyond self-managed deployments for centralization and advanced processing