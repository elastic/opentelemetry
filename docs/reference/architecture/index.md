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

### Vendor neutral collector deployments on edge environments

You can use any OpenTelemetry Collector distribution at the edge, including:

- The contrib OpenTelemetry Collector.
- Custom-built Collector distributions.
- The {{edot}} Collector.
- Any shipper capable of sending valid OTLP data.


The only requirement is that collectors deployed on edge environments send data using valid OpenTelemetry Protocol (OTLP) to Elastic Cloud (via managed OTLP endpoint) or to the OTLP receiver of a gateway EDOT collector for self-managed deployments.

While any OTLP-compatible collector works at the edge, using EDOT provides a more streamlined experience with:

- Preconfigured components optimized for {{product.observability}}.
- Curated receivers and processors for common use cases.
- Simplified setup and configuration.

### When gateway mode is required

The need for an EDOT Collector in gateway mode depends on your Elastic deployment type:

**{{serverless-full}} and {{ech}}**: Edge collectors can send OTLP data directly to the [Managed OTLP Endpoint](/reference/motlp.md) without requiring a Gateway Collector. The Managed OTLP Endpoint provides a managed durable and resilient ingestion layer.

**Self-managed, ECE, and ECK deployments**: An EDOT Collector in Gateway mode is required as part of the stack, this collector will expose the OTLP endpoint that collectors deployed at the edge can send data to. The gateway Collector handles essential preprocessing, including:

- Data enrichment and transformation.
- Metrics aggregation for traces and logs which improves APM UI performance with lower latency.
- Format conversion for optimal storage in {{es}}.

:::{note}
Refer to the [deployment mode documentation](elastic-agent://reference/edot-collector/modes.md) for detailed information about Agent and Gateway modes and their specific requirements.
:::

