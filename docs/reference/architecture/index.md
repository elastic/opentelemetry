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

In the context of OpenTelemetry architecture, *edge* refers to collectors deployed close to your data sources—running on individual hosts, virtual machines, or as daemon sets on Kubernetes nodes. These edge collectors perform two primary functions:

1. They gather logs, infrastructure metrics, application traces, profiles, and other telemetry from the local environment.
2. They enrich application telemetry from OpenTelemetry SDKs running on the same host or node with resource metadata, such as host information and Kubernetes attributes.

### Collector flexibility at the edge

You can use any OpenTelemetry Collector distribution at the edge, including:

- The contrib OpenTelemetry Collector.
- Custom-built Collector distributions.
- The {{edot}} Collector.

The only requirement is that edge collectors send data using the **OpenTelemetry Protocol (OTLP)** to either a gateway Collector or directly to {{product.observability}}.

While any OTLP-compatible collector works at the edge, **using EDOT provides a more streamlined experience** with:

- Preconfigured components optimized for {{product.observability}}.
- Curated receivers and processors for common use cases.
- Simplified setup and configuration.

### When gateway mode is required

The need for an EDOT Collector in gateway mode depends on your Elastic deployment type:

**{{serverless-full}} and {{ech}}**: Edge collectors can send OTLP data directly to the [Managed OTLP Endpoint](/reference/motlp.md) without requiring a Gateway Collector. The Managed OTLP Endpoint handles all necessary preprocessing and data transformation.

**Self-managed, ECE, and ECK deployments**: An EDOT Collector in Gateway mode is **required** between your edge collectors and {{es}}. The gateway Collector performs essential preprocessing, including:

- Data enrichment and transformation.
- Metrics aggregation.
- Format conversion for optimal storage in {{es}}.

:::{note}
Refer to the [deployment mode documentation](elastic-agent://reference/edot-collector/modes.md) for detailed information about Agent and Gateway modes and their specific requirements.
:::

