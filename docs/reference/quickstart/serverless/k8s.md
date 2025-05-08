---
navigation_title: Kubernetes
description: Learn how to set up the EDOT Collector and EDOT SDKs in a Kubernetes environment with Elastic Cloud Serverless to collect host metrics, logs and application traces.
applies_to:
  stack:
  serverless:
    observability:
products:
  - cloud-serverless
  - observability
---

# Quickstart for Kubernetes on Elastic Cloud Hosted

Learn how to set up the EDOT Collector and EDOT SDKs in a Kubernetes environment with Elastic Cloud Serverless to collect host metrics, logs and application traces.

## Prerequisites

Make sure the following requirements are present:

- The **Kubernetes OpenTelemetry Assets** integration is installed in Kibana.
- The **[System](integrations://system/index.md)** integration is installed in Kibana. Select **Add integration only** to skip the agent installation, as only the integration assets are required.

## Guided setup

:::{include} ../../_snippets/guided-instructions.md
:::

## Manual installation

Follow these steps to deploy the EDOT Collector and EDOT OTel SDKs in Kubernetes.

:::::{stepper}

::::{step} Add the OpenTelemetry repository to Helm

Run the following command to add the charts repository to Helm:

```bash
helm repo add open-telemetry 'https://open-telemetry.github.io/opentelemetry-helm-charts' --force-update
```
::::

::::{step} Set up connection and credentials

Follow these steps to retrieve the managed OTLP endpoint URL for your Serverless project:

1. In Elastic Cloud, open your Observability project.
2. Go to **Add data**, **Application**, **OpenTelemetry**.
3. Select **Managed OTLP Endpoint** in the second step.
4. Copy the OTLP endpoint configuration value.
5. Select Create API Key to generate an API key.

Replace `<ELASTIC_OTLP_ENDPOINT>` and `<ELASTIC_API_KEY>` in the following command to create a namespace and a secret with your credentials.

```bash
kubectl create namespace opentelemetry-operator-system
kubectl create secret generic elastic-secret-otel \
--namespace opentelemetry-operator-system \
--from-literal=elastic_otlp_endpoint='<ELASTIC_OTLP_ENDPOINT>' \
--from-literal=elastic_api_key='<ELASTIC_API_KEY>'
```
::::

::::{step} Install the operator

Install the OpenTelemetry Operator using the `kube-stack` Helm chart with the configured `values.yaml` file.

```bash
helm install opentelemetry-kube-stack open-telemetry/opentelemetry-kube-stack \
--namespace opentelemetry-operator-system \
--values 'https://raw.githubusercontent.com/elastic/elastic-agent/refs/tags/v{{ site.edot_versions.collector }}/deploy/helm/edot-collector/kube-stack/managed_otlp/values.yaml' \
--version '0.3.9'
```

The Operator provides a deployment of the EDOT Collector and configuration environment variables. This allows SDKs and instrumentation to send data to the EDOT Collector without further configuration.
::::

::::{step} Auto-instrument applications

Add a language-specific annotation to your namespace by replacing `<LANGUAGE>` with one of the supported values (`nodejs`, `java`, `python`, `dotnet` or `go`) in the following command. 

```bash
kubectl annotate namespace YOUR_NAMESPACE instrumentation.opentelemetry.io/inject-<LANGUAGE>="opentelemetry-operator-system/elastic-instrumentation"
```

The OpenTelemetry Operator automatically provides the OTLP endpoint configuration and authentication to the SDKs through environment variables. Restart your deployment to ensure the annotations and auto-instrumentations are applied.

For languages where auto-instrumentation is not available, manually instrument your application. See the [Setup section in the corresponding SDK](../../edot-sdks.md).
::::
:::::

## Troubleshooting

The following issues might occur.

### API Key prefix not found

The following error is due to an improperly formatted API key:

```txt
Exporting failed. Dropping data.
{"kind": "exporter", "data_type": }
"Unauthenticated desc = ApiKey prefix not found"
```

Format your API key as `"Authorization": "ApiKey <api-key-value-here>"` or `"Authorization=ApiKey <api-key>"` depending on whether you're using a Collector or SDK.

### Error: too many requests

The managed endpoint has per-project rate limits in place. If you reach this limit, contact our [support team](https://support.elastic.co).
