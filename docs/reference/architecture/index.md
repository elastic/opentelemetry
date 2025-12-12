---
navigation_title: Reference Architecture
description: Recommended architectures for EDOT with different Elastic deployment options.
applies_to:
  stack:
  serverless:
    observability:
products:
  - id: cloud-serverless
  - id: observability
  - id: edot-collector
---

# EDOT reference architecture

The following sections outline the recommended architectures for Elastic Distributions of OpenTelemetry (EDOT) with different Elastic deployment options.

- [Hosts and VMs](hosts_vms.md)
- [Kubernetes](k8s.md)

## Understanding edge deployment

In the context of OpenTelemetry architecture, 'edge' refers to the environment where applications are running: individual hosts, virtual machines, or as daemon sets on Kubernetes nodes. Collectors deployed in these environments perform two primary functions:

1. They gather logs, infrastructure metrics, application traces, profiles, and other telemetry from the local environment.
2. They enrich application telemetry from OpenTelemetry SDKs running on the same host or node with resource metadata, such as host information and Kubernetes attributes.

### Vendor-neutral collector deployments on edge environments

You can use any OpenTelemetry Collector distribution at the edge, including:

- The contrib OpenTelemetry Collector.
- Custom-built Collector distributions.
- The {{edot}} Collector.
- Any shipper capable of sending valid OTLP data.

The only requirement is that collectors deployed on edge environments send data using valid OpenTelemetry Protocol (OTLP) to {{ecloud}} (using managed OTLP endpoint) or to the OTLP receiver of a gateway EDOT collector for self-managed deployments.

While any OTLP-compatible collector works at the edge, using EDOT provides a more streamlined experience with:

- Preconfigured components optimized for {{product.observability}}.
- Curated receivers and processors for common use cases.
- Simplified setup and configuration.

## Understanding the {{product.observability}} backend [understanding-the-elastic-observability-backend]

The {{product.observability}} backend is the ingestion and storage layer where your telemetry data is processed, indexed, and made available for analysis. This includes:

- **{{es}}**: Stores and indexes your telemetry data.
- **{{kib}}**: Provides visualization and analysis interfaces.
- **Managed OTLP Endpoint** (for {{serverless-full}} and {{ech}}): A managed ingestion service that receives OTLP data.
- **Gateway Collector** (for self-managed, ECE, and ECK): An EDOT Collector running in gateway mode that serves as the ingestion layer.

:::{note}
When a Collector in gateway mode is deployed, it is considered part of the {{product.observability}} backend, not part of the edge deployment. The Collector in gateway mode sits between your edge collectors and {{es}}, acting as a centralized ingestion and preprocessing layer.
:::

### When gateway mode is required

The need for an EDOT Collector in gateway mode as part of your Elastic backend depends on your deployment type:

**{{serverless-full}} and {{ech}}**: Edge collectors can send OTLP data directly to the [Managed OTLP Endpoint](/reference/motlp.md) without requiring a self-managed Gateway Collector. The Managed OTLP Endpoint provides a fully managed ingestion layer as part of the Elastic backend. You can optionally deploy an EDOT Collector in gateway mode as part of your edge environment if you need additional processing before data reaches the Managed OTLP Endpoint.

**Self-managed, ECE, and ECK deployments**: An EDOT Collector in gateway mode is **required as part of your {{product.observability}} backend**. This Gateway Collector exposes the OTLP endpoint that edge collectors send data to, and handles essential preprocessing, including:

- Metrics aggregation for traces and logs, which improves {{product.apm}} UI performance with lower latency.
- Format conversion for optimal storage in {{es}}.

For detailed information about Agent and Gateway modes and their specific requirements, refer to the [deployment mode documentation](elastic-agent://reference/edot-collector/modes.md).

## Oxford comma test

The system supports indexing, searching and analytics.

## Plural abbreviations test

Multiple API's are available. The CPU's performance depends on the GPU's capabilities.

