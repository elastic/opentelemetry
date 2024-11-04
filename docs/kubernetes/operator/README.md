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
- [Limitations](#limitations)

## Prerequisites

- Elastic Stack (self-managed or [Elastic Cloud](https://www.elastic.co/cloud)) version 8.16.0 or higher, or an [Elasticsearch serverless](https://www.elastic.co/docs/current/serverless/elasticsearch/get-started) project.

- A Kubernetes version supported by the OpenTelemetry Operator (refer to the operator's [compatibility matrix](https://github.com/open-telemetry/opentelemetry-operator/blob/main/docs/compatibility.md#compatibility-matrix) for more details).

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

- [OpenTelemetry Collectors](https://github.com/open-telemetry/opentelemetry-collector): Agents responsible for receiving, processing and exporting telemetry data such as logs, metrics, and traces.
- [Instrumentation](https://opentelemetry.io/docs/kubernetes/operator/automatic): Used for the atomatic instrumentation of workloads by leveraging OpenTelemetry instrumentation libraries.

All signals including logs, metrics, traces are processed by the collectors and sent directly to Elasticsearch via the ES exporter. A collector's processor pipeline replaces the traditional APM server functionality for handling application traces.

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

## Deploying components using Kibana Onboarding UX

The preferred method for deploying all components is through the Kibana Onboarding UX. Follow these steps:

1. Navigate in Kibana to **Observability** --> **Add data**
2. Select **Kubernetes**, then choose **Kubernetes monitoring with EDOT Collector**.
3. Follow the on-screen instructions to install the OpenTelemetry Operator using the Helm Chart and the provided `values.yaml`.

Notes:
- If the `elastic_endpoint` showed by the UI is not valid for your environment, replace it with the correct Elasticsearch endpoint.
- The displayed `elastic_api_key` corresponds to an API key that is automatically generated when the onboarding process is initiated.

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

For troubleshooing details and verification steps, refer to [Troubleshooting auto-instrumentation](/docs/kubernetes/operator/troubleshoot-auto-instrumentation.md).

## Limitations

### Cert manager

In Kubernetes, in order for the API server to communicate with the webhook component (created by the Operator), the webhook requires a TLS certificate that the API server is configured to trust. The previous provided configurations sets the Helm Chart to auto generate the required TLS certificates with an expiration policy of 365 days. These certificates **won't be renewed** if the Helm Chart's release is not manually updated. For production environments, it is highly recommended to use a certificate manger like [cert-manager](https://cert-manager.io/docs/installation/).

If `cert-manager` CRDs are already present in your Kubernetes environment, you can configure the Operator to use them with the following modifications in the values file:


```diff
opentelemetry-operator:
  manager:
    extraArgs:
      - --enable-go-instrumentation
  admissionWebhooks:
    certManager:
-      enabled: false
+      enabled: true

-autoGenerateCert:
-  enabled: true
-  recreate: true
```
