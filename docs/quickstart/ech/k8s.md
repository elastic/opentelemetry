---
title: Kubernetes
layout: default
nav_order: 1
parent: Elastic Cloud Hosted
---

# Quickstart - Kubernetes - Hosted

☸️ Kubernetes
{: .label .label-purple }

🗄️ Elastic Cloud Hosted
{: .label .label-blue }

The quick start for Kubernetes with Elastic Cloud Hosted covers the collection of OpenTelemetry data for infrastructure monitoring,
logs collection and application monitoring.

1. **Add the OpenTelemetry repository to Helm**

    ```bash
    helm repo add open-telemetry 'https://open-telemetry.github.io/opentelemetry-helm-charts' --force-update
    ```

2. **Setup Credentials**

    Retrieve the `Elasticsearch Endpoint` and the `Elastic API Key` for your Elastic Cloud deployment by [following these instructions](./#retrieving-connection-details-for-your-elastic-cloud-deployment).

    Replace both, `<ELASTICSEARCH_ENDPOINT>` and `<ELASTIC_API_KEY>` in the below command to create a namespace and a secret with your credentials.

    ```bash
    kubectl create namespace opentelemetry-operator-system
    kubectl create secret generic elastic-secret-otel \
    --namespace opentelemetry-operator-system \
    --from-literal=elastic_endpoint='<ELASTICSEARCH_ENDPOINT>' \
    --from-literal=elastic_api_key='<ELASTIC_API_KEY>'
    ```

3. **Install Operator**

    Install the OpenTelemetry Operator using the kube-stack Helm chart with the pre-configured `values.yaml` file.

    ```bash
    helm install opentelemetry-kube-stack open-telemetry/opentelemetry-kube-stack \
    --namespace opentelemetry-operator-system \
    --values 'https://raw.githubusercontent.com/elastic/elastic-agent/refs/tags/v{{ site.edot_versions.collector }}/deploy/helm/edot-collector/kube-stack/values.yaml' \
    --version '0.3.9'
    ```

4. **Auto-instrument Applications**

    Add a language-specific annotation to your namespace by replacing `<LANGUAGE>` with one of the supported values (`nodejs`, `java`, `python`, `dotnet` or `go`) in the below command. 

    ```bash
    kubectl annotate namespace YOUR_NAMESPACE instrumentation.opentelemetry.io/inject-<LANGUAGE>="opentelemetry-operator-system/elastic-instrumentation"
    ```

    Restart your deployment to ensure the annotations and auto-instrumentations are applied.

    For languages where auto-instrumentation is not available, you will need to manually instrument your application. See the [Setup section in the corresponding SDK](../../edot-sdks).
