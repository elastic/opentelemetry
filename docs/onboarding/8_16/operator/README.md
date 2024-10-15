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
- [Customizing installation](#customizing-installation)
- [Limitations](#limitations)

## Prerequisites

- Elastic Stack in version 8.16.0 or higher (self-managed, ESS, or Serverless).
- Kubernetes x.y (TBD)

## Compatibility Matrix

The minimum supported version of the Elastic Stack for the OpenTelemetry based monitoring on Kubernetes is `8.16.0`. Different stack releases will support certain versions of the kube-stack Helm Chart](https://github.com/open-telemetry/opentelemetry-helm-charts/tree/main/charts/opentelemetry-kube-stack).

This is the current list of supported versions:

| Stack Version | Helm Chart Version |    Values file     |
|---------------|--------------------|--------------------|
| 8.16.0        | 0.2.2              | values-0.2.2.yaml  |

When installing the release, use the right `--version` and `-f values-x.y.z.yaml` parameters.

## Components description

### OpenTelemetry Operator

The OpenTelemetry Operator is an implementation of a [Kubernetes Operator](https://kubernetes.io/docs/concepts/extend-kubernetes/operator/). It defines and manages the following Custom Resource Definitions (CRDs)

- [OpenTelemetry Collector](https://github.com/open-telemetry/opentelemetry-collector).
- [auto-instrumentation](https://opentelemetry.io/docs/concepts/instrumentation/automatic/) of the workloads using OpenTelemetry instrumentation libraries.

All signals including logs, metrics, traces/APM go through the collectors directly into Elasticsearch using the ES exporter. A collector's processor pipeline will be used to replace the APM server functionality for application traces.

### Kube-stack Helm Chart

The [kube-stack Helm Chart](https://github.com/open-telemetry/opentelemetry-helm-charts/tree/main/charts/opentelemetry-kube-stack) will be utilized to manage the installation of the operator (including its CRDs) and configure a suite of collectors, which will instrument various Kubernetes components to enable comprehensive observability and monitoring.

The chart is installed with a provided default `values.yaml` file that can be customized when needed.

### Daemonset collectors

The OpenTelemetry components deployed within the DaemonSet collectors are responsible for observing specific signals from each node. To ensure complete data collection, these components must be deployed on every node in the cluster. Failing to do so will result in partial and potentially incomplete data.

The Daemonset collectors handle the following data:

- Host Metrics: Collects host metrics (hostmetrics receiver) specific to each node.
- Kubernetes Metrics: Captures metrics related to the Kubernetes infrastructure on each node.
- Logs: Utilizes a filelog receiver to gather logs from all Pods running on the respective node.
- OTLP Traces Receiver: Opens an HTTP and a GRPC port on the node to receive OTLP trace data.

### Deployment collector

The OpenTelemetry components deployed within a Deployment collector focus on gathering data at the cluster level rather than at individual nodes. Unlike DaemonSet collectors, which need to be deployed on every node, a Deployment collector operates as a standalone instance.

The deployment collector handles the following data:

- Kubernetes Events: Monitors and collects events occurring across the entire Kubernetes cluster.
- Cluster Metrics: Captures metrics that provide insights into the overall health and performance of the Kubernetes cluster.

### Auto-instrumentation

The Helm Chart is configured to enable zero-code instrumentation using the [Operator's Instrumentation resource](https://github.com/open-telemetry/opentelemetry-operator/?tab=readme-ov-file#opentelemetry-auto-instrumentation-injection) for the following programming languages:

- Go
- Java
- Node.js
- Python
- .NET

To enable auto-instrumentation, add the corresponding annotation to the pods of existing deployments (`spec.template.metadata.annotations`), or to the desired namespace (to auto-instrument all pods in the namespace):

```yaml
metadata:
  annotations:
    instrumentation.opentelemetry.io/inject-<LANGUAGE>: "opentelemetry-operator-system/elastic-instrumentation"
```

where <LANGUAGE> is one of: `go` , `java`, `nodejs`, `python`, `dotnet`

## Deploying components using Kibana Onboarding UX

The recommended way to deploy all the components is to follow the Kibana Onboarding UX. To do that:

1. Go to Kibana --> **Observability** --> **Add data**
2. Select **Kubernetes**, then **Kubernetes monitoring with EDOT Collector**.
3. Follow the instructions within the page to install the OpenTelemetry Operator with the Helm Chart and the provided values.yaml.

Notes:
- If the `elastic_endpoint` showed by the UI is not valid for your environment, replace it with the right Elasticsearch endpoint.
- The displayed `elastic_api_key` belongs to an API key created automatically when the onboarding flow is opened.

## Manual deployment of all components

### Elastic Stack preparations

Before installing the operator follow these actions:

1. Create an [API Key](https://www.elastic.co/guide/en/kibana/current/api-keys.html), and make note of its value (TBD: details of API key permissions).

2. Install the following integrations in Kibana:
  - `System`
  - `Kubernetes`
  - `Kubernetes OpenTelemetry Assets`

Notes:
- When `Kibana onboarding UX` is used, the previous actions are automatically performed by Kibana.

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
$ helm upgrade --install --namespace opentelemetry-operator-system opentelemetry-kube-stack open-telemetry/opentelemetry-kube-stack --values ./resources/kubernetes/operator/helm/values.yaml --version 0.2.2
```

## Installation verification

Perform the following steps to verify that all components are healthy:
(TBD)

## Customizing installation

(TBD - share use cases that might require customization)
If provided `values.yaml` is not valid you can update it and point it on `helm install` command.

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
