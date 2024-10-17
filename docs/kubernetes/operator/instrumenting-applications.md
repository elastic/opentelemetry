# Instrumenting applications with EDOT on Kubernetes

This section provides guidance and examples for applications instrumentation in a Kubernetes environment for all the supported languages.

Elastic offers several Distributions that extend [OpenTelemetry language SDKs](https://opentelemetry.io/docs/languages/):

* [EDOT Java](https://github.com/elastic/elastic-otel-java)
* [EDOT .NET](https://github.com/elastic/elastic-otel-dotnet)
* [EDOT Node.js](https://github.com/elastic/elastic-otel-node)
* [EDOT Python](https://github.com/elastic/elastic-otel-python)
* [EDOT PHP](https://github.com/elastic/elastic-otel-php/)

In Kubernetes environments with the OpenTelemetry Operator, [**automatic (or zero-code) instrumentation**](https://opentelemetry.io/docs/kubernetes/operator/automatic/) simplifies the process by automatically injecting and configuring instrumentation libraries into the targeted Pods.

On the other hand, **manual instrumentation** in Kubernetes with OpenTelemetry involves adding specific OpenTelemetry SDKs and APIs directly into your application’s code. This approach provides more granular control over what and how data is captured, allowing you to customize trace spans, metrics, and logging based on your application’s logic.

## Table of contents

- [Prerequisites](#prerequisites)
- [Auto-instrumentation](#auto-instrumentation)
- [Manual instrumentation](#manual-instrumentation)


## Prerequisites

- Install the OpenTelemetry operator and EDOT collectors following the [./README.md](getting started guide).

## Auto-instrumentation

Zero-code instrumenation is handled by the operator with the help of `Instrumenation` objects.

During the installation of the Operator, an `Instrumentation` object with name `elastic-instrumentation` in namespace `opentelemetry-operator-system` should have been created. This object stores important parameters:

- The **exporter endpoint**: It represents the destination for the traces, in this case the HTTP receiver configured in the EDOT DaemonSet Collector. That endpoint has to be reachable by the Pods being instrumented.

```yaml
  exporter:
    endpoint: http://opentelemetry-kube-stack-daemon-collector.opentelemetry-operator-system.svc.cluster.local:4318
```

(TBD: Note about only supporting HTTP exporters currently?)

- The **images** for the different languages: Used by the Operator to inject the right libraries into the Pods.

```yaml
  dotnet:
    image: docker.elastic.co/observability/elastic-otel-dotnet:edge
  java:
    image: docker.elastic.co/observability/elastic-otel-javaagent:1.0.0
  nodejs:
    image: docker.elastic.co/observability/elastic-otel-node:edge
  python:
    image: docker.elastic.co/observability/elastic-otel-python:edge
```

### Configuring auto-instrumentation




## Namespace based annotations

```
#Annotate app namespace

kubectl annotate namespace <app-namespace> instrumentation.opentelemetry.io/inject-java="opentelemetry-operator-system/elastic-instrumentation"

#Restart the java-app to get the new annotation
kubectl rollout restart deployment <my-app> -n <app-namespace>
```


## Manual instrumentation

