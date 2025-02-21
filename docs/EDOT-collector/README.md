# EDOT Collector

The **Elastic Distribution of OpenTelemetry (EDOT) Collector** is an open-source distribution of the [OpenTelemetry Collector](https://github.com/open-telemetry/opentelemetry-collector).

Built on OpenTelemetry’s modular [architecture](https://opentelemetry.io/docs/collector/), the EDOT Collector offers a curated and fully supported selection of Receivers, Processors, Exporters, and Extensions. Designed for production-grade reliability. 

For comprehensive details on EDOT Collector components, visit [EDOT Collector Components](docs/EDOT-collector/collector-components.md).

## Installation

* [Kubernetes Full Observability](#kubernetes-full-observability)
* [Linux](#linux)



### Kubernetes Full Observability (Recommended)
These instructions will install the OpenTelemetry Operator preconfigured to:

* Orchestrate various instances of EDOT with the below purpose:
  * EDOT Collector Cluster: Collect cluster metrics
  * EDOT Collector Daemon: Collect node metrics and logs
  * EDOT Collector Gateway: Route all telemetry, perform APM pre-processing (eg. derive span metrics)
* Auto-instrument applications that are annotated as described in the instructions

##### 1. Install the OpenTelemetry Operator
Add the OpenTelemetry repository to Helm:
```
helm repo add open-telemetry 'https://open-telemetry.github.io/opentelemetry-helm-charts' --force-update
```
Retrieve your [Elasticsearch endpoint](https://www.elastic.co/guide/en/kibana/current/search-space-connection-details.html) and [API key](https://www.elastic.co/guide/en/kibana/current/api-keys.html) and replace both in the below command to create a namespace and a secret with your credentials.
```
kubectl create namespace opentelemetry-operator-system
kubectl create secret generic elastic-secret-otel \
  --namespace opentelemetry-operator-system \
  --from-literal=elastic_endpoint='<ELASTICSEARCH_ENDPOINT>' \
  --from-literal=elastic_api_key='<BASE64_APIKEY>'
```
Install the OpenTelemetry Operator using the kube-stack Helm chart with a pre-configured `values.yaml` file that will orchestrate EDOT Collector. 
```
helm install opentelemetry-kube-stack open-telemetry/opentelemetry-kube-stack \
  --namespace opentelemetry-operator-system \
  --values 'https://raw.githubusercontent.com/elastic/elastic-agent/51942e903eb69bb295920763b10a1c8bec68d1e8/deploy/helm/edot-collector/kube-stack/values.yaml' \
  --version '0.3.9'
```
**Install cert-manager (optional)**
For automatic certificate renewal, we recommend installing [cert-manager](https://cert-manager.io/docs/installation/), and customize the values.yaml file before the installation as described in our [documentation](https://github.com/elastic/opentelemetry/tree/8.16/docs/kubernetes/operator#cert-manager).

##### 2. Instrument your applications (optional)
The following languages are currently supported for auto-instrumentation: **Node.js, Java, Python, .NET and Go.**. Select a programming and one of the below annotations methods

**Annotate a specific Deployment**
Add a language-specific annotation to your Kubernetes Deployment manifest and restart your deployment. Replace 'LANGUAGE' with one of the supported values: `nodejs`, `java`, `python`, `dotnet` or `go`  
```
apiVersion: apps/v1
kind: Deployment
metadata:
  name: myapp
spec:
  ...
  template:
    metadata:
      annotations:
        instrumentation.opentelemetry.io/inject-'LANGUAGE': "opentelemetry-operator-system/elastic-instrumentation"
      ...
    spec:
      containers:
      - image: myapplication-image
        name: app
      ...
```
**Annotate all resources in a namespace**
Add a language-specific annotation to your namespace by replacing 'LANGUAGE' with one of the supported values: `nodejs`, `java`, `python`, `dotnet` or `go` in the below command. 
```
kubectl annotate namespace my-namespace instrumentation.opentelemetry.io/inject-nodejs="opentelemetry-operator-system/elastic-instrumentation"
```
Restart relevant language deployments already running in the namespace.

For other languages where auto-instrumentation is not available, refer to the documentation

### Linux
Run the below commands to download the EDOT Collector package relevant to your system's architecture. 
```
arch=$(if ([[ $(arch) == "arm" || $(arch) == "aarch64" ]]); then echo "arm64"; else echo $(arch); fi)
 
curl --output elastic-distro-8.18.0-SNAPSHOT-linux-$arch.tar.gz --url https://snapshots.elastic.co/8.18.0-72dd839e/downloads/beats/elastic-agent/elastic-agent-8.18.0-SNAPSHOT-linux-$arch.tar.gz --proto '=https' --tlsv1.2 -fOL && mkdir -p elastic-distro-8.18.0-SNAPSHOT-linux-$arch && tar -xvf elastic-distro-8.18.0-SNAPSHOT-linux-$arch.tar.gz -C "elastic-distro-8.18.0-SNAPSHOT-linux-$arch" --strip-components=1 && cd elastic-distro-8.18.0-SNAPSHOT-linux-$arch

rm ./otel.yml && curl https://raw.githubusercontent.com/elastic/elastic-agent/a4d698f501d625f8d6ebb21badbcecdce6bd32a0/internal/pkg/otel/samples/linux/platformlogs_hostmetrics.yml -o otel.yml && mkdir -p ./data/otelcol && sed -i 's#\${env:STORAGE_DIR}#'"$PWD"/data/otelcol'#g' ./otel.yml
```
Run EDOT collector by replacing your endpoint and apiKey:
## Configuration

The EDOT Collector uses a YAML-based configuration file. Below is a sample configuration:

```receivers:
  # Receiver for system metrics
  hostmetrics/system:
    collection_interval: 30s
    scrapers:
      cpu:
      memory:
      disk:

  # Receiver for platform logs
  filelog/platformlogs:
    include: [ /var/log/*.log ]
    start_at: end

processors:
  resourcedetection:
    detectors: ["system"]
  attributes/dataset:
    actions:
      - key: event.dataset
        from_attribute: data_stream.dataset
        action: upsert

exporters:
  elasticsearch:
    endpoints: ["${env:ELASTIC_ENDPOINT}"]
    api_key: ${env:ELASTIC_API_KEY}
    mapping:
      mode: ecs

service:
  extensions: [file_storage]
  pipelines:
    metrics:
      receivers: [hostmetrics/system]
      processors: [resourcedetection, attributes/dataset]
      exporters: [elasticsearch]
    logs:
      receivers: [filelog/platformlogs]
      processors: [resourcedetection]
      exporters: [elasticsearch]

```

**Note**: Replace `"https://your-elastic-instance:9200"` with your Elastic instance URL and `"YOUR_API_KEY"` with your API key.

For comprehensive configuration options, consult the [OpenTelemetry Collector documentation](https://github.com/open-telemetry/opentelemetry-collector).

## Advanced Features

The EDOT Collector supports:

- **Auto-Instrumentation**: Seamless integration with OpenTelemetry SDKs.
- **Built-in Processors**: Includes functionalities like batching and attribute processing.
- **Multi-Backend Support**: Extendable to other backends such as Jaeger, Prometheus, or Kafka.

## Troubleshooting

If you encounter issues:

- **Check Logs**: Review the Collector's logs for error messages.
- **Validate Configuration**: Use the `--dry-run` option to test configurations.
- **Community Support**: Engage with the OpenTelemetry community via [GitHub Discussions](https://github.com/open-telemetry/opentelemetry-collector/discussions).

---

*For more detailed information, refer to the [OpenTelemetry Collector GitHub repository](https://github.com/open-telemetry/opentelemetry-collector).*
