---
title: Kubernetes
layout: default
nav_order: 1
parent: Self-managed
---

# Quick Start - Kubernetes - Self-managed

The quick start for Kubernetes covers collection of OpenTelemetry data for infrastructure monitoring, logs collection and application  monitoring. These instructions will install an OpenTelemetry Operator preconfigured to automate orchestration of EDOT as below:
 
* **EDOT Collector Cluster:** Collect cluster metrics
* **EDOT Collector Daemon:** Collect node metrics and logs
* **EDOT Collector Gateway:** perform APM pre-processing (when applicable). Route all telemetry to Elastic,  
* **EDOT SDKs**: Annotated applications will be auto-instrumented with EDOT SDKs
  
![K8s-architecture](../../images/EDOT-K8s-architecture.png)

## Kubernetes Infrastructure Metrics and Log Collection

Add the OpenTelemetry repository to Helm:

```bash
helm repo add open-telemetry 'https://open-telemetry.github.io/opentelemetry-helm-charts' --force-update
```

Retrieve your [Elasticsearch endpoint](https://www.elastic.co/guide/en/kibana/current/search-space-connection-details.html) and [API key](https://www.elastic.co/guide/en/kibana/current/api-keys.html) and replace both in the below command to create a namespace and a secret with your credentials.

```bash
kubectl create namespace opentelemetry-operator-system
kubectl create secret generic elastic-secret-otel \
  --namespace opentelemetry-operator-system \
  --from-literal=elastic_endpoint='<ELASTICSEARCH_ENDPOINT>' \
  --from-literal=elastic_api_key='<BASE64_APIKEY>'
```

Install the OpenTelemetry Operator using the kube-stack Helm chart with our pre-configured `values.yaml` file that will indicate to the operator how to orchestrate and configure EDOT.

```bash
helm install opentelemetry-kube-stack open-telemetry/opentelemetry-kube-stack \
  --namespace opentelemetry-operator-system \
  --values 'https://raw.githubusercontent.com/elastic/elastic-agent/refs/tags/v8.17.2/deploy/helm/edot-collector/kube-stack/values.yaml' \
  --version '0.3.9'
```

### Install cert-manager (recommended)

For automatic certificate renewal, we recommend installing [cert-manager](https://cert-manager.io/docs/installation/), and customize the `values.yaml` file before the installation as described in [this section](https://github.com/elastic/opentelemetry/tree/8.16/docs/kubernetes/operator#cert-manager).

### Change Log Collection Configuration (optional)

New log messages are collected from the setup onward.
The default log path is `/var/log/*`. You can change this or include other paths in the EDOT collector configuration, for advanced settings visit [filelog receiver documentation.](https://github.com/open-telemetry/opentelemetry-collector-contrib/tree/main/receiver/filelogreceiver)

To edit settings change the below section in the Helm `values.yml` file: 

```yaml
        filelog:
          retry_on_failure:
            enabled: true
          start_at: end
          exclude:
            # exlude collector logs
            - /var/log/pods/*opentelemetry-kube-stack*/*/*.log
          include:
            - /var/log/pods/*/*/*.log
          include_file_name: false
          include_file_path: true
          operators:
            - id: container-parser # Extract container's metadata
              type: container
```

## Kubernetes Application Monitoring

The following languages are currently supported for auto-instrumentation: Node.js, Java, Python, .NET and Go. 

Choose the annotation method that best suits your needs and apply the instructions for the corresponding language:

### Annotate a specific Deployment

Add a language-specific annotation to your Kubernetes Deployment manifest and restart your deployment. Replace `<LANGUAGE>` with one of the supported values: `nodejs`, `java`, `python`, `dotnet` or `go`  

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: myapp
spec:
  # ...
  template:
    metadata:
      annotations:
        instrumentation.opentelemetry.io/inject-<LANGUAGE>: "opentelemetry-operator-system/elastic-instrumentation"
      # ...
    spec:
      containers:
      - image: myapplication-image
        name: app
      # ...
```

### Annotate all resources in a namespace

Add a language-specific annotation to your namespace by replacing `<LANGUAGE>` with one of the supported values: `nodejs`, `java`, `python`, `dotnet` or `go` in the below command. 

```bash
kubectl annotate namespace my-namespace instrumentation.opentelemetry.io/inject-<LANGUAGE>="opentelemetry-operator-system/elastic-instrumentation"
```

For both methods, Restart deployment and ensure the annotations are applied and the auto-instrumentation library is injected.

For languages where auto-instrumentation is not available, visit [this page](https://ela.st/8-16-otel-apm-instrumentation)