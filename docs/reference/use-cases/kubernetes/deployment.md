---
title: Deployment
layout: default
nav_order: 3
parent: Monitoring on Kubernetes
grand_parent: Use Cases
---

# Deployment

You can use the [guided onboarding](#deploy-components-using-the-guided-onboarding) or [deploy all components manually](#manual-deployment-of-all-components)

## Deploy components using the guided onboarding

The guided onboarding simplifies deploying your Kubernetes components by setting up an [API Key](https://www.elastic.co/guide/en/kibana/current/api-keys.html) and the needed [Integrations](https://www.elastic.co/docs/current/en/integrations) in the background. Follow these steps to use the guided onboarding:

1. In Kibana, navigate to **Observability** → **Add data**.
2. Select **Kubernetes**, then choose **Kubernetes monitoring with EDOT Collector**.
3. Follow the on-screen instructions to install the OpenTelemetry Operator using the Helm chart and the provided `values.yaml`.

Notes on installing the OpenTelemetry Operator:
- Make sure the `elastic_endpoint` shown in the installation command is valid for your environment. If not, replace it with the correct Elasticsearch endpoint.
- The `elastic_api_key` shown in the installation command corresponds to an API key created by Kibana when the onboarding process is initiated.

{: .note }
> The default installation deploys an OpenTelemetry Operator with a self-signed TLS certificate.
> To automatically generate and renew certificates, refer to [cert-manager integrated installation](./customization#cert-manager-integrated-installation) for instructions on customizing the `values.yaml` file before running the `helm install` command.

## Manual deployment of all components

### Elastic Stack preparations

Before installing the operator follow these actions:

1. Create an [API Key](https://www.elastic.co/guide/en/kibana/current/api-keys.html), and make note of its value.
(TBD: details of API key permissions).

2. Install the following integrations in Kibana:
    - `System`
    - `Kubernetes`
    - `Kubernetes OpenTelemetry Assets`

Notes:
- When using the [Kibana onboarding UX](#deploy-components-using-the-guided-onboarding), the previous actions are automatically handled by Kibana.

### Operator Installation

1. Create the `opentelemetry-operator-system` Kubernetes namespace:

    ```bash
    $ kubectl create namespace opentelemetry-operator-system
    ```

2. Create a secret in the created namespace with the following command:

   ```bash
   kubectl create -n opentelemetry-operator-system secret generic elastic-secret-otel \
     --from-literal=elastic_endpoint='YOUR_ELASTICSEARCH_ENDPOINT' \
     --from-literal=elastic_api_key='YOUR_ELASTICSEARCH_API_KEY'
   ```

   Don't forget to replace
   - `YOUR_ELASTICSEARCH_ENDPOINT`: Elasticsearch endpoint (**with `https://` prefix**). For example: `https://1234567.us-west2.gcp.elastic-cloud.com:443`.
   - `YOUR_ELASTICSEARCH_API_KEY`: Elasticsearch API Key created in the previous step.

3. If you need to [customize the configuration](./customization#customizing-configuration), make a copy of the `values.yaml` file and adapt it to your needs. Refer to the [compatibility matrix](./prerequisites-compatibility#compatibility-matrix) for a complete list of available manifests in the `release branches`. 

4. Run the following commands to deploy the `opentelemetry-kube-stack` Helm chart, using the appropriate values file:

    ```bash
    helm repo add open-telemetry https://open-telemetry.github.io/opentelemetry-helm-charts
    helm repo update
    helm upgrade --install --namespace opentelemetry-operator-system opentelemetry-kube-stack open-telemetry/opentelemetry-kube-stack \
          --values 'https://raw.githubusercontent.com/elastic/elastic-agent/refs/tags/v{{ site.edot_versions.collector }}/deploy/helm/edot-collector/kube-stack/values.yaml' \
          --version 0.3.3
    ```

## Installation verification

Regardless of the installation method followed, perform the following checks to verify that everything is running properly:

1. **Check Pods Status**
   - Ensure the following components are running without errors:
     - **Operator Pod**
     - **DaemonSet Collector Pod**
     - **Deployment Collector Pod**

2. **Validate Instrumentation Object**
   - Confirm that the **Instrumentation object** is deployed and configured with a valid **endpoint**.

3. **Kibana Dashboard Check**
   - Verify that the **[OTEL][Metrics Kubernetes] Cluster Overview** dashboard in **Kibana** is displaying data correctly.

4. **Log Data Availability in Kibana**
   - In **Kibana Discover**, confirm the availability of data under the `__logs-*__` data view.

5. **Metrics Data Availability in Kibana**
   - In **Kibana Discover**, ensure data is available under the `__metrics-*__` data view.
