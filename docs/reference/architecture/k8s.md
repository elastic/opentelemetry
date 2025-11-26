---
navigation_title: Kubernetes environments
description: Recommended EDOT architecture for Kubernetes environments.
applies_to:
  stack:
  serverless:
    observability:
products:
  - id: cloud-serverless
  - id: observability
  - id: edot-collector
---

# Kubernetes Environments

The recommended OTel architecture for Kubernetes clusters includes a set of OpenTelemetry collectors in different forms. The following diagram shows the different forms:

![K8s-Cluster](../images/arch-k8s-cluster.png)

## Daemon form

The Collector in Daemon form is deployed on each Kubernetes node as an [edge collector](index.md#understanding-edge-deployment) to collect node-local logs and host metrics.

The daemon collector also receives telemetry from applications instrumented with OTel SDKs and running on corresponding nodes.

That Collector enriches the application telemetry with resource information such as host and Kubernetes metadata.

All data is then sent through OTLP to the OTel or EDOT Collector in gateway mode.

## Cluster form

The Collector in Cluster form collects Kubernetes cluster-level metrics and sends them to the OTel or EDOT Gateway Collector using OTLP.

## Gateway form

The OTel or EDOT Collector in gateway form gathers the OTel data from all other collectors and ingests it into the Elastic backend.

For self-managed, ECE, and ECK deployment models the gateway Collector does some additional preprocessing of data.

## Deployment scenarios

Refer to the recommended architectures per Elastic deployment scenarios.

::::{note}
Elastic's Observability solution is technically compatible with setups that are fully based on contrib OTel components, as long as the ingestion path follows the recommendations outlined in following sections for the different Elastic deployment options.
::::

### {{serverless-full}}

{{serverless-full}} provides a [Managed OTLP Endpoint](/reference/motlp.md) for ingestion of OpenTelemetry data.

![K8s-Serverless](../images/arch-k8s-serverless.png)

For a Kubernetes setup, that means the gateway Collector passes through the OTel data in native format using the OTLP protocol to the Managed OTLP Endpoint. There is no need for the gateway Collector to do any Elastic-specific pre-processing.

### {{ech}}

Starting from version 9.2, {{ech}} provides a [Managed OTLP Endpoint](/reference/motlp.md) for ingestion of OpenTelemetry data.

For a Kubernetes setup, that means the gateway Collector can pass through the OTel data in native format using the OTLP protocol to the Managed OTLP Endpoint. There is no need for the gateway Collector to do any Elastic-specific preprocessing.

Alternatively, you can run a self-hosted EDOT Collector in gateway mode. The gateway Collector needs to do some preprocessing, aggregation of metrics and, finally, it uses the {{es}} exporter to ingest data into ECH. While the Daemon and Cluster collectors, as well as the OTel SDKs, can stay fully vendor agnostic or upstream, the gateway Collector needs to be either an EDOT Collector or a [custom, EDOT-like Collector](elastic-agent://reference/edot-collector/custom-collector.md) containing the [required components and pre-processing pipelines](elastic-agent://reference/edot-collector/config/default-config-k8s.md#direct-ingestion-into-elasticsearch).

![K8s-ECH](../images/arch-k8s-ech.png)

### Self-managed

With a self-managed scenario the gateway Collector ingests data directly into the self-managed {{es}} instance.

![K8s-self-managed](../images/arch-k8s-self-managed.png)

The gateway Collector does some preprocessing and aggregation of OTel data before ingesting it into {{es}}.

While the Daemon and Cluster collectors, as well as the OTel SDKs, can stay fully vendor agnostic or upstream, the gateway Collector needs to be either an EDOT Collector or a [custom, EDOT-like Collector](elastic-agent://reference/edot-collector/custom-collector.md) containing the [required components and pre-processing pipelines](elastic-agent://reference/edot-collector/config/default-config-k8s.md#direct-ingestion-into-elasticsearch).

::::{note}
Compared to [Elastic's classic ingestion paths](docs-content://solutions/observability/apm/use-opentelemetry-with-apm.md) for OTel data, with the EDOT gateway Collector there is no need for {{product.apm-server}} anymore.

Refer to [EDOT data streams compared to classic {{product.apm}}](../compatibility/data-streams.md) for a detailed comparison of data streams, mappings, and storage models.
::::
