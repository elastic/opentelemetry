# Kubernetes Onboarding 8.16

This guide will help you get up and running with Kubernetes by walking through the setup and integration of key components, starting with the [OpenTelemetry Operator](https://github.com/open-telemetry/opentelemetry-operator/). The OpenTelemetry Operator is an implementation of a [Kubernetes Operator](https://kubernetes.io/docs/concepts/extend-kubernetes/operator/).

The operator manages:

- [OpenTelemetry Collector](https://github.com/open-telemetry/opentelemetry-collector)
- [auto-instrumentation](https://opentelemetry.io/docs/concepts/instrumentation/automatic/) of the workloads using OpenTelemetry instrumentation libraries

## OpenTelemetry Operator

The [kube-stack Helm Chart](https://github.com/open-telemetry/opentelemetry-helm-charts/tree/main/charts/opentelemetry-kube-stack) will be utilized to manage the installation of the Operator's Custom Resource Definitions (CRDs) alongside the configuration of a suite of collectors, which will instrument various components of the Kubernetes environment to enable comprehensive observability and monitoring.

### Daemonset collectors

The OpenTelemetry components deployed within the DaemonSet collectors are responsible for observing specific signals from each node. To ensure complete data collection, these components must be deployed on every node in the cluster. Failing to do so will result in partial and potentially incomplete data.

- Host Metrics: Collects host metrics (hostmetrics receiver) specific to each node.
- Kubernetes Metrics: Captures metrics related to the Kubernetes infrastructure on each node.
- Logs: Utilizes a filelog receiver to gather logs from all Pods running on the respective node.
- OTLP Traces Receiver: Opens an HTTP and a GRPC port on the node to receive OTLP trace data.

### Deployment collector

The OpenTelemetry components deployed within a Deployment collector focus on gathering data at the cluster level rather than at individual nodes. Unlike DaemonSet collectors, which need to be deployed on every node, a Deployment collector operates as a standalone instance.

- Kubernetes Events: Monitors and collects events occurring across the entire Kubernetes cluster.
- Cluster Metrics: Captures metrics that provide insights into the overall health and performance of the Kubernetes cluster.

### Auto-instrumentation

The Helm Chart is configured to enable zero-code instrumentation using the [Operator's Instrumentation resource](https://github.com/open-telemetry/opentelemetry-operator/?tab=readme-ov-file#opentelemetry-auto-instrumentation-injection) for the following programming languages:

- Go
- Java

## Configuration

Depending on the deployment model (i.e. self-managed, ESS, serverless), different configuration will be needed.

### On-Prem deployment

All signals including logs, metrics, traces/APM go through the collector directly into Elasticsearch using the ES exporter, a collector's processor pipeline will be used to replace the APM server functionality.


1. Create a secret in Kubernetes with the following command.
   ```
   kubectl create -n opentelemetry-operator-system secret generic elastic-secret-otel \
     --from-literal=elastic_endpoint='YOUR_ELASTICSEARCH_ENDPOINT' \
     --from-literal=elastic_api_key='YOUR_ELASTICSEARCH_API_KEY'
   ```
   Don't forget to replace
   - `YOUR_ELASTICSEARCH_ENDPOINT`: your Elasticsearch endpoint (*with* `https://` prefix example: `https://1234567.us-west2.gcp.elastic-cloud.com:443`).
   - `YOUR_ELASTICSEARCH_API_KEY`: your Elasticsearch API Key

2. Execute the following commands to deploy the Helm Chart.

```
$ helm repo add open-telemetry https://open-telemetry.github.io/opentelemetry-helm-charts
$ helm repo update
$ helm install --namespace opentelemetry-operator-system opentelemetry-kube-stack open-telemetry/opentelemetry-kube-stack --values ./onprem_kube_stack_values.yaml
```

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
