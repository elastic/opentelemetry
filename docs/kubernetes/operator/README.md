# Get started with OpenTelemetry for Kubernetes Observability

This guide describes how to:

- Install the [OpenTelemetry Operator](https://github.com/open-telemetry/opentelemetry-operator/) using the [kube-stack Helm Chart](https://github.com/open-telemetry/opentelemetry-helm-charts/tree/main/charts/opentelemetry-kube-stack).
- Use the EDOT Collector to send Kubernetes logs, metrics, and application traces to an Elasticsearch cluster.
- Use the operator for applications [auto-instrumentation](https://opentelemetry.io/docs/kubernetes/operator/automatic/) in all supported languages.

## Table of Contents

- [Prerequisites](#prerequisites)
- [Compatibility Matrix](#compatibility-matrix)
- [Components description](#components-description)
- [Deploying components using Kibana Onboarding UX](#deploying-components-using-kibana-onboarding-ux)
- [Manual deployment of all components](#manual-deployment-of-all-components)
- [Installation verification](#installation-verification)
- [Instrumenting applications](#instrumenting-applications)
- [Upgrades](#operator-upgrade)
- [Customizing configuration](#custom-configuration)
- [Cert-manager integrated installation](#cert-manager)

## Prerequisites

- Elastic Stack (self-managed or [Elastic Cloud](https://www.elastic.co/cloud)) version 8.16.0 or higher, or an [Elasticsearch serverless](https://www.elastic.co/docs/current/serverless/elasticsearch/get-started) project.

- A Kubernetes version supported by the OpenTelemetry Operator (refer to the operator's [compatibility matrix](https://github.com/open-telemetry/opentelemetry-operator/blob/main/docs/compatibility.md#compatibility-matrix) for more details).

- If you opt for automatic certificate generation and renewal on the OpenTelemetry Operator, you need to install [cert-manager](https://cert-manager.io/docs/installation/) in the Kubernetes cluster. By default, the operator installation uses a self-signed certificate and **doesn't require** cert-manager.

## Compatibility Matrix

The minimum supported version of the Elastic Stack for OpenTelemetry-based monitoring on Kubernetes is `8.16.0`. Different Elastic Stack releases support specific versions of the [kube-stack Helm Chart](https://github.com/open-telemetry/opentelemetry-helm-charts/tree/main/charts/opentelemetry-kube-stack).

The following is the current list of supported versions:

| Stack Version | Helm Chart Version |    Values file     |
|---------------|--------------------|--------------------|
| Serverless    | 0.3.0              | values.yaml  |
| 8.16.0        | 0.3.0              | values.yaml  |

When [installing the release](#manual-deployment-of-all-components), ensure you use the right `--version` and `-f <values-file>` parameters. Values files are available in the [resources directory](/resources/kubernetes/operator/helm).

## Components description

### OpenTelemetry Operator

The OpenTelemetry Operator is a [Kubernetes Operator](https://kubernetes.io/docs/concepts/extend-kubernetes/operator/) implementation designed to manage OpenTelemetry resources in a Kubernetes environment. It defines and oversees the following Custom Resource Definitions (CRDs):

- [OpenTelemetry Collectors](https://github.com/open-telemetry/opentelemetry-collector): Agents responsible for receiving, processing, and exporting telemetry data such as logs, metrics, and traces.
- [Instrumentation](https://opentelemetry.io/docs/kubernetes/operator/automatic): Leverages OpenTelemetry instrumentation libraries to automatically instrument workloads.

All signals including logs, metrics, and traces are processed by the collectors and sent directly to Elasticsearch using the ES exporter. A collector's processor pipeline replaces the traditional APM server functionality for handling application traces.

### Kube-stack Helm Chart

The [kube-stack Helm Chart](https://github.com/open-telemetry/opentelemetry-helm-charts/tree/main/charts/opentelemetry-kube-stack) is used to manage the installation of the operator (including its CRDs) and to configure a suite of collectors, which instrument various Kubernetes components to enable comprehensive observability and monitoring.

The chart is installed with a provided default `values.yaml` file that can be customized when needed.

### DaemonSet collectors

The OpenTelemetry components deployed within the DaemonSet collectors are responsible for observing specific signals from each node. To ensure complete data collection, these components must be deployed on every node in the cluster. Failing to do so will result in partial and potentially incomplete data.

The DaemonSet collectors handle the following data:

- Host Metrics: Collects host metrics (hostmetrics receiver) specific to each node.
- Kubernetes Metrics: Captures metrics related to the Kubernetes infrastructure on each node.
- Logs: Utilizes a filelog receiver to gather logs from all Pods running on the respective node.
- OTLP Traces Receiver: Opens an HTTP and a GRPC port on the node to receive OTLP trace data.

### Deployment collector

The OpenTelemetry components deployed within a Deployment collector focus on gathering data at the cluster level rather than at individual nodes. Unlike DaemonSet collectors, which need to be deployed on every node, a Deployment collector operates as a standalone instance.

The Deployment collector handles the following data:

- Kubernetes Events: Monitors and collects events occurring across the entire Kubernetes cluster.
- Cluster Metrics: Captures metrics that provide insights into the overall health and performance of the Kubernetes cluster.

### Auto-instrumentation

The Helm Chart is configured to enable zero-code instrumentation using the [Operator's Instrumentation resource](https://github.com/open-telemetry/opentelemetry-operator/?tab=readme-ov-file#opentelemetry-auto-instrumentation-injection) for the following programming languages:

- Go
- Java
- Node.js
- Python
- .NET

## Deploy components using the guided onboarding

The guided onboarding simplifies deploying your Kubernetes components by setting up an [API Key](https://www.elastic.co/guide/en/kibana/current/api-keys.html) and the needed [Integrations](https://www.elastic.co/docs/current/en/integrations) in the background. Follow these steps to use the guided onboarding:

1. In Kibana, navigate to **Observability** → **Add data**.
2. Select **Kubernetes**, then choose **Kubernetes monitoring with EDOT Collector**.
3. Follow the on-screen instructions to install the OpenTelemetry Operator using the Helm Chart and the provided `values.yaml`.

Notes on installing the OpenTelemetry Operator:
- Make sure the `elastic_endpoint` shown in the installation command is valid for your environment. If not, replace it with the correct Elasticsearch endpoint.
- The `elastic_api_key` shown in the installation command corresponds to an API key created by Kibana when the onboarding process is initiated.

> [!NOTE]
> The default installation deploys an OpenTelemetry Operator with a self-signed TLS certificate generated by He
> To automatically generate and renew certificates, refer to [cert-manager integrated installation](#cert-manager) for instructions on customizing the `values.yaml` file before running the `helm install` command.

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
- When using the [Kibana onboarding UX](#deploying-components-using-kibana-onboarding-ux), the previous actions are automatically handled by Kibana.

### Operator Installation

1. Create the `opentelemetry-operator-system` Kubernetes namespace:
```
$ kubectl create namespace opentelemetry-operator-system
```

2. Create a secret in Kubernetes with the following command.
   ```
   kubectl create -n opentelemetry-operator-system secret generic elastic-secret-otel \
     --from-literal=elastic_endpoint='YOUR_ELASTICSEARCH_ENDPOINT' \
     --from-literal=elastic_api_key='YOUR_ELASTICSEARCH_API_KEY'
   ```
   Don't forget to replace
   - `YOUR_ELASTICSEARCH_ENDPOINT`: your Elasticsearch endpoint (*with* `https://` prefix example: `https://1234567.us-west2.gcp.elastic-cloud.com:443`).
   - `YOUR_ELASTICSEARCH_API_KEY`: your Elasticsearch API Key

3. Execute the following commands to deploy the Helm Chart.

```
$ helm repo add open-telemetry https://open-telemetry.github.io/opentelemetry-helm-charts
$ helm repo update
$ helm upgrade --install --namespace opentelemetry-operator-system opentelemetry-kube-stack open-telemetry/opentelemetry-kube-stack --values ./resources/kubernetes/operator/helm/values.yaml --version 0.3.0
```

## Installation verification:

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
   - In **Kibana Discovery**, confirm the availability of data under the `__logs-*__` data view.

5. **Metrics Data Availability in Kibana**
   - In **Kibana Discovery**, ensure data is available under the `__metrics-*__` data view.

## Instrumenting Applications

To enable auto-instrumentation, add the corresponding annotation to the pods of existing deployments (`spec.template.metadata.annotations`), or to the desired namespace (to auto-instrument all pods in the namespace):

```yaml
metadata:
  annotations:
    instrumentation.opentelemetry.io/inject-<LANGUAGE>: "opentelemetry-operator-system/elastic-instrumentation"
```

where ``<LANGUAGE>`` is one of: `go` , `java`, `nodejs`, `python`, `dotnet`

For detailed instructions and examples on how to instrument applications in Kubernetes using the OpenTelemetry Operator, refer to [Instrumenting applications](/docs/kubernetes/operator/instrumenting-applications.md).

For troubleshooting details and verification steps, refer to [Troubleshooting auto-instrumentation](/docs/kubernetes/operator/troubleshoot-auto-instrumentation.md).

<a name="operator-upgrade"></a>

## Upgrades

> [!NOTE]
> Before upgrading or updating the release configuration refer to [compatibility matrix](#compatibility-matrix) for the list of supported versions and [customizing configuration](#custom-configuration) for a list of supported configurable parameters.

To upgrade an installed release, run:

```bash
helm repo update open-telemetry # update information of available charts locally
helm search repo open-telemetry/opentelemetry-kube-stack --versions # list available versions of the chart

helm upgrade --namespace opentelemetry-operator-system opentelemetry-kube-stack open-telemetry/opentelemetry-kube-stack \
 --values <updated_values_file> --version <updated_version>
```

If [cert-manager integration](#cert-manager) is disabled, helm will generate a new self-signed TLS certificate with every update, even if there are no actual changes to apply.

<a name="custom-configuration"></a>

## Customizing configuration

To customize the installation parameters, change the configuration values provided in `values.yaml` file, or override them using `--set parameter=value` during the installation.

To update an installed release, run a `helm upgrade` with the updated `values.yaml` file. Depending on the changes, some Pods may need to be restarted for the updates to take effect. Refer to [upgrades](#operator-upgrade) for a command example.

### Configurable parameters

The following table lists common parameters that might be relevant for your use case:

| `values.yaml` parameter          |     Description      |
|----------------------------------|----------------------|
| `clusterName`                    | Sets the `k8s.cluster.name` field in all collected data. The cluster name is automatically detected for `EKS/GKE/AKS` clusters, but it might be useful for other environments. When monitoring multiple Kubernetes clusters, ensure that the cluster name is properly set in all your environments.<br><br>Refer to the [resourcedetection processor](https://github.com/open-telemetry/opentelemetry-collector-contrib/blob/main/processor/resourcedetectionprocessor/README.md#cluster-name) for more details about cluster name detection. |
| `collectors.cluster.resources`   | Configures CPU and memory requests and limits applied to the `Deployment` EDOT Collector responsible for cluster-level metrics.<br>This setting follows the standard [Kubernetes resources syntax](https://kubernetes.io/docs/concepts/configuration/manage-resources-containers/#requests-and-limits) for specifying requests and limits. |
| `collectors.daemon.resources`    | Configures CPU and memory requests and limits applied to the `DaemonSet` EDOT Collector responsible for node-level metrics and application traces.<br>This setting follows the standard [Kubernetes resources syntax](https://kubernetes.io/docs/concepts/configuration/manage-resources-containers/#requests-and-limits) for specifying requests and limits. |
| `certManager.enabled`    | Defaults to `false`.<br>Refer to [cert-manager integrated installation](#cert-manager) for more details. |
| `instrumentation.<language>.image`    | Container image used for `zero-code` provisioning. Refer to [instrumenting applications](./intrumenting-applications.md) for more details. |
| `instrumentation.exporter.endpoint`    | Exporter endpoint for the EDOT SDK agent. Refer to [instrumenting applications](./intrumenting-applications.md) for more details. |
| `exporters.debug.verbosity` | Verbosity level for debug logs of the [Elasticsearch exporter](https://github.com/open-telemetry/opentelemetry-collector-contrib/blob/main/exporter/elasticsearchexporter/README.md) of the collectors.<br>Defaults to `basic`. Can be any of `basic`, `detailed`.<br>Applicable to `collectors.daemon.config.exporters.debug.verbosity` and `collectors.cluster.config.exporters.debug.verbosity` |

> [!NOTE]
> The `namespace` of the installation cannot be changed and must be set to `opentelemetry-operator-system` during the helm chart installation.

For more details of all existing parameters, the provided `values.yaml` includes comments and is largely self-explanatory.

<!-- Do not change this anchor name as it's used by Kibana OTel+k8s Onboarding UX -->
<a name="cert-manager"></a>

## Cert-manager integrated installation

In Kubernetes, for the API server to communicate with the webhook component (created by the operator), the webhook requires a TLS certificate that the API server is configured to trust. The default provided configuration sets the Helm Chart to auto generate the required certificate as a self-signed certificate with an expiration policy of 365 days. These certificates **won't be renewed** if the Helm Chart's release is not manually updated. For production environments, we highly recommend using a certificate manager like [cert-manager](https://cert-manager.io/docs/installation/).

Integrating the operator with [cert-manager](https://cert-manager.io/) enables automatic generation and renewal of the TLS certificate. This section assumes that cert-manager and its CRDs are already installed in your Kubernetes environment. If that's not the case, refer to the [cert-manager installation guide](https://cert-manager.io/docs/installation/) before continuing.

Follow any of the following options to install the OpenTelemetry Operator Helm Chart integrated with `cert-manager`:

* Add `--set opentelemetry-operator.admissionWebhooks.certManager.enabled=true --set opentelemetry-operator.admissionWebhooks.autoGenerateCert=null` to the installation command. For example:

```bash
helm upgrade --install --namespace opentelemetry-operator-system opentelemetry-kube-stack open-telemetry/opentelemetry-kube-stack \
--values ./resources/kubernetes/operator/helm/values.yaml --version 0.3.3 \
--set opentelemetry-operator.admissionWebhooks.certManager.enabled=true --set opentelemetry-operator.admissionWebhooks.autoGenerateCert=null
```

* Keep an updated copy of the `values.yaml` file by following these steps:

  1. **Update** the `values.yaml` file with the following changes:

      - **Enable cert-manager integration for admission webhooks.**

        ```yaml
        opentelemetry-operator:
          admissionWebhooks:
            certManager:
              enabled: true  # Change from `false` to `true`
        ```

      - **Remove the generation of a self-signed certificate.**

        ```yaml
        # Remove the following lines:
            autoGenerateCert:
              enabled: true
              recreate: true
        ```

  2. Run the installation (or upgrade) command pointing to the updated file. For example, assuming that the updated file has been saved as `values_cert-manager.yaml`:

    ```bash
    helm upgrade --install --namespace opentelemetry-operator-system opentelemetry-kube-stack open-telemetry/opentelemetry-kube-stack \
    --values ./resources/kubernetes/operator/helm/values_cert-manager.yaml --version 0.3.0
    ```
