---
navigation_title: Prerequisites and compatibility
description: Prerequisites and compatibility information for monitoring Kubernetes with EDOT.
applies_to:
  stack:
  serverless:
    observability:
products:
  - cloud-serverless
  - observability
---

# Prerequisites

Before setting up observability for Kubernetes, make sure you have the following:

- Elastic Stack (self-managed or [Elastic Cloud](https://www.elastic.co/cloud)) version 8.16.0 or higher, or an [Elasticsearch serverless](https://www.elastic.co/docs/current/serverless/elasticsearch/get-started) project.

- A Kubernetes version supported by the OpenTelemetry Operator. Refer to the operator's [compatibility matrix](https://github.com/open-telemetry/opentelemetry-operator/blob/main/docs/compatibility.md#compatibility-matrix) for more details.

- If you opt for automatic certificate generation and renewal on the OpenTelemetry Operator, install [cert-manager](https://cert-manager.io/docs/installation/) in the Kubernetes cluster. By default, the operator uses a self-signed certificate and doesn't require cert-manager.

## Compatibility matrix

The minimum supported version of the Elastic Stack for OpenTelemetry-based monitoring on Kubernetes is `8.16.0`. Different Elastic Stack releases support specific versions of the [kube-stack Helm chart](https://github.com/open-telemetry/opentelemetry-helm-charts/tree/main/charts/opentelemetry-kube-stack).

The following is the current list of supported versions:

| Stack Version | Helm chart Version |    Values file     |
|---------------|--------------------|--------------------|
| Serverless    | 0.3.3              | [values.yaml](https://github.com/elastic/elastic-agent/blob/main/deploy/helm/edot-collector/kube-stack/managed_otlp/values.yaml)  |
| 8.16.0        | 0.3.3              | [values.yaml](https://raw.githubusercontent.com/elastic/opentelemetry/refs/heads/8.16/resources/kubernetes/operator/helm/values.yaml)  |
| 8.17.0        | 0.3.3              | [values.yaml](https://raw.githubusercontent.com/elastic/elastic-agent/refs/heads/8.17/deploy/helm/edot-collector/kube-stack/values.yaml) |
| 9.0.0         | 0.3.3              | [values.yaml](https://github.com/elastic/elastic-agent/blob/main/deploy/helm/edot-collector/kube-stack/managed_otlp/values.yaml) |

When [installing the release](./deployment#manual-deployment-of-all-components), make sure you use the right `--version` and `-f <values-file>` parameters.