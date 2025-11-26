---
navigation_title: Hosts / VMs environments
description: Recommended EDOT architecture for host or virtual machine environments.
applies_to:
  stack:
  serverless:
    observability:
products:
  - id: cloud-serverless
  - id: observability
  - id: edot-collector
---

# Hosts and VMs environments

On host or virtual machine environments, deploy local, per-host OpenTelemetry Collector instances at the [edge](index.md#understanding-edge-deployment).

![VM-Edge](../images/arch-vm-edge.png)

These edge collectors have two main purposes:

1.  The collection of local logs and infrastructure metrics. Refer to [this sample config file](https://github.com/elastic/elastic-agent/blob/main/internal/pkg/otel/samples/linux/managed_otlp/platformlogs_hostmetrics.yml) for recommended Collector receiver configurations for hostmetrics and logs.
2.  Enriching application telemetry from OTel SDKs that run within the instrumented applications on corresponding hosts with resource information.

## Deployment scenarios

Refer to the recommended architectures per Elastic deployment scenarios.

:::{note}
Elastic's Observability solution is technically compatible with edge setups that are fully based on contrib OTel components as long as the ingestion path follows the recommendations outlined in the following sections.
:::

### {{serverless-full}}

{{serverless-full}} provides a [Managed OTLP Endpoint](/reference/motlp.md) for ingestion of OpenTelemetry data.

![VM-Serverless](../images/arch-vm-serverless.png)

Users can send their OTel data from the edge setup in OTel-native format through OTLP without any additional requirements for self-managed preprocessing of data.

### {{ech}}

Starting from version 9.2, {{ech}} provides a [Managed OTLP Endpoint](/reference/motlp.md) for ingestion of OpenTelemetry data. Users can send their OTel data from the edge setup in OTel-native format through OTLP without any additional requirements for self-managed preprocessing of data.

Alternatively, you can run a self-hosted EDOT Collector in gateway mode to ingest OTel data from the edge setup. The EDOT Collector in gateway mode enriches and pre-aggregates the data before ingesting it directly into {{es}}. If required, you can build your custom, EDOT-like Collector [following these instructions](elastic-agent://reference/edot-collector/custom-collector.md).

![VM-ECH](../images/arch-vm-ech.png)

### Self-managed

In a self-managed deployment scenario, you need to host an EDOT Collector in gateway mode that preprocesses and ingests OTel data from the edge setup into the self-managed {{stack}}.

![VM-self-managed](../images/arch-vm-self-managed.png)

:::{note}
Compared to [Elastic's classic ingestion paths](docs-content://solutions/observability/apm/use-opentelemetry-with-apm.md) for OTel data, with the EDOT Collector in gateway mode there is no need for {{product.apm-server}} anymore. 

Refer to [EDOT data streams compared to classic {{product.apm}}](../compatibility/data-streams.md) for a detailed comparison of data streams, mappings, and storage models.
:::