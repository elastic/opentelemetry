---
navigation_title: Kubernetes environments
description: Recommended EDOT architecture for Kubernetes environments.
applies_to:
  stack:
  serverless:
    observability:
products:
  - cloud-serverless
  - observability
---

# Kubernetes Environments

The recommended OTel architecture for Kubernetes clusters includes a set of OpenTelemetry collectors in different modes. The following diagram shows the different modes:

![K8s-Cluster](./../images/arch-k8s-cluster.png)

## Daemon mode

The Collector in Daemon mode is deployed on each Kubernetes node to collect nodes-local logs and host metrics.

The daemon collector also receives telemetry from applications instrumented with OTel SDKs and running on corresponding nodes.

That collector enriches the application telemetry with resource information such as host and Kubernetes metadata.

All data is then being sent through OTLP to the OTel or EDOT Gateway Collector.

## Cluster mode

The Collector in Cluster mode collects Kubernetes cluster-level metrics and sends them to the OTel or EDOT Gateway Collector using OTLP.

## Gateway mode

The OTel or EDOT Collector in Gateway mode gathers the OTel data from all other collectors and ingests it into the Elastic backend.

For self-managed and Elastic Cloud Hosted deployment models the Gateway collector does some additional pre-processing of data.

## Deployment scenarios

See the recommended architectures per Elastic deployment scenarios:

::::{note}
Elastic's Observability solution is technically compatible with setups that are fully based on upstream OTel components, as long as the ingestion path follows the recommendations outlined in following sub-sections for the different Elastic deployment options.
::::

### Elastic Cloud Serverless

Elastic Cloud Serverless provides a managed OTLP endpoint for ingestion of OpenTelemetry data.

![K8s-Serverless](./../images/arch-k8s-serverless.png)

For a Kubernetes setup, that means the Gateway Collector passes through the OTel data in native format using the OTLP protocol to the managed OTLP endpoint. There is no need for the Gateway Collector to do any Elastic-specific pre-processing.

### Elastic Cloud Hosted

With Elastic Cloud Hosted (ECH), OTel data is being directly ingested into the Elastic-hosted Elasticsearch instance.

![K8s-ECH](./../images/arch-k8s-ech.png)

The Gateway Collector needs to do some preprocessing, aggregation of metrics and, finally, it uses the Elasticsearch exporter to ingest data into ECH. 

While the Daemon and Cluster collectors, as well as the OTel SDKs, can stay fully vendor agnostic or upstream, the Gateway Collector needs to be either an EDOT Collector or a [custom, EDOT-like collector](../edot-collector/custom-collector) containing the [required components and pre-processing pipelines](../edot-collector/config/default-config-k8s#direct-ingestion-into-elasticsearch).

If required, users can build their custom, EDOT-like collector [following these instructions](../edot-collector/custom-collector#build-a-custom-edot-like-collector).

::::{note}
The EDOT Gateway Collector does not send data through Elastic's Integration / APM Server on ECH to ingest data into Elasticsearch.
::::

::::{important}
If self-managing an EDOT Gateway is not a valid option for you, refer to [Elastic's classic ingestion path for OTel data on ECH](https://www.elastic.co/guide/en/observability/current/apm-open-telemetry.html).
::::

### Self-managed

With a self-managed scenario the Gateway Collector ingests data directly into the self-managed Elasticsearch instance.

![K8s-self-managed](./../images/arch-k8s-self-managed.png)

The Gateway Collector does some preprocessing and aggregation of OTel data before ingesting it into Elasticsearch. 

While the Daemon and Cluster collectors, as well as the OTel SDKs, can stay fully vendor agnostic or upstream, the Gateway Collector needs to be either an EDOT Collector or a [custom, EDOT-like collector](../edot-collector/custom-collector) containing the [required components and pre-processing pipelines](../edot-collector/config/default-config-k8s#direct-ingestion-into-elasticsearch).

::::{note}
Compared to [Elastic's classic ingestion paths](https://www.elastic.co/guide/en/observability/current/apm-open-telemetry.html) for OTel data, with the EDOT Gateway Collector there is no need for an APM Server anymore.
::::
