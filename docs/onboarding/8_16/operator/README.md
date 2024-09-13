# OpenTelemetry Operator

## Elasticsearch secrets

```
$ kubectl create namespace opentelemetry-operator-system
$ kubectl create -n opentelemetry-operator-system secret generic elastic-secret-otel \
     --from-literal=elastic_endpoint='https://test-otel-blablabla.es.us-central1.gcp.cloud.es.io/' \
     --from-literal=elastic_api_key='asdfghjkl=='
```

## Deployment

```
$ helm repo add open-telemetry https://open-telemetry.github.io/opentelemetry-helm-charts
$ helm repo update
$ helm install --namespace opentelemetry-operator-system opentelemetry-kube-stack open-telemetry/opentelemetry-kube-stack --values ./onprem_kube_stack_values.yaml
```
