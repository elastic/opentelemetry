---
navigation_title: Kubernetes
applies_to:
  stack:
  serverless:
---

# Quickstart

The quick start for Kubernetes with Elastic Cloud Serverless covers the collection of OpenTelemetry data for infrastructure monitoring,
logs collection and application monitoring.

1. **Add the OpenTelemetry repository to Helm**

    ```bash
    helm repo add open-telemetry 'https://open-telemetry.github.io/opentelemetry-helm-charts' --force-update
    ```

2. **Setup Connection & Credentials**

    Retrieve the `Elastic OTLP Endpoint` and the `Elastic API Key` for your Serverless Project by [following these instructions](./#retrieve-connection-details-for-your-project).

    Replace both, `<ELASTIC_OTLP_ENDPOINT>` and `<ELASTIC_API_KEY>` in the below command to create a namespace and a secret with your credentials.

    ```bash
    kubectl create namespace opentelemetry-operator-system
    kubectl create secret generic elastic-secret-otel \
    --namespace opentelemetry-operator-system \
    --from-literal=elastic_otlp_endpoint='<ELASTIC_OTLP_ENDPOINT>' \
    --from-literal=elastic_api_key='<ELASTIC_API_KEY>'
    ```

3. **Install Operator**

    Install the OpenTelemetry Operator using the kube-stack Helm chart with the pre-configured `values.yaml` file.

    ```bash
    helm install opentelemetry-kube-stack open-telemetry/opentelemetry-kube-stack \
    --namespace opentelemetry-operator-system \
    --values 'https://raw.githubusercontent.com/elastic/elastic-agent/refs/tags/v{{ site.edot_versions.collector }}/deploy/helm/edot-collector/kube-stack/managed_otlp/values.yaml' \
    --version '0.3.9'
    ```

    The Operator will provide a deployment of the EDOT Collector and provide the configuration environment variables, thus enabling SDKs and instrumentation to send data to the EDOT Collector without further configuration.

4. **Auto-instrument Applications**

    Add a language-specific annotation to your namespace by replacing `<LANGUAGE>` with one of the supported values (`nodejs`, `java`, `python`, `dotnet` or `go`) in the below command. 

    ```bash
    kubectl annotate namespace YOUR_NAMESPACE instrumentation.opentelemetry.io/inject-<LANGUAGE>="opentelemetry-operator-system/elastic-instrumentation"
    ```

    The OpenTelemetry Operator will automatically provide the OTLP endpoint configuration and authentication to the SDKs through environment variables.

    Restart your deployment to ensure the annotations and auto-instrumentations are applied.

    For languages where auto-instrumentation is not available, you will need to manually instrument your application. See the [Setup section in the corresponding SDK](../../edot-sdks).

## Troubleshoot

### Api Key prefix not found

The following error is due to an improperly formatted API key:

```txt
Exporting failed. Dropping data.
{"kind": "exporter", "data_type": }
"Unauthenticated desc = ApiKey prefix not found"
```

Format your API key as `"Authorization": "ApiKey <api-key-value-here>"` or `"Authorization=ApiKey <api-key>"` depending on whether you're using a Collector or SDK.

### Error: too many requests

The managed endpoint has per-project rate limits in place. If you reach this limit, contact our [support team](https://support.elastic.co).
