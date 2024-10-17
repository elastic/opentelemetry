# Instrumenting applications with EDOT on Kubernetes

This section provides guidance and examples for applications instrumentation in a Kubernetes environment for all the supported languages.

Elastic Distribution of OpenTelemetry (EDOT) extends [OpenTelemetry language SDKs](https://opentelemetry.io/docs/languages/) for multiple languages:

* [EDOT Java](https://github.com/elastic/elastic-otel-java)
* [EDOT .NET](https://github.com/elastic/elastic-otel-dotnet)
* [EDOT Node.js](https://github.com/elastic/elastic-otel-node)
* [EDOT Python](https://github.com/elastic/elastic-otel-python)
* [EDOT PHP](https://github.com/elastic/elastic-otel-php/)

In Kubernetes environments with the OpenTelemetry Operator, [**automatic (or zero-code) instrumentation**](https://opentelemetry.io/docs/kubernetes/operator/automatic/) simplifies the process by automatically injecting and configuring instrumentation libraries into the targeted Pods.

On the other hand, **manual instrumentation** with OpenTelemetry involves adding specific OpenTelemetry SDKs and APIs directly into your application’s code. This approach provides more granular control over what and how data is captured, allowing you to customize trace spans, metrics, and logging based on your application’s logic.

## Table of contents

- [Prerequisites](#prerequisites)
- [Auto-instrumentation basics](#auto-instrumentation-basics)
- [Configuring auto-instrumentation](#configuring-auto-instrumentation)
- [Advanced configuration](#advanced-configuration)
- [Manual instrumentation](#manual-instrumentation)

## Prerequisites

- Install the OpenTelemetry operator and EDOT collectors following the [getting started guide](./README.md).
- Ensure a valid `kind: Instrumentation` object exists in the cluster.

## Auto-instrumentation basics

Zero-code instrumenation is handled by the operator with the help of `Instrumenation` objects.

The process follows the usual OTel Operator steps for [auto-instrumentation injection](https://github.com/open-telemetry/opentelemetry-operator#opentelemetry-auto-instrumentation-injection), which is common to all supported languages:

  1. Install the OTel Operator into a k8s cluster.
  2. Create a `kind: Instrumentation` object with the appropriate config.
  3. Deploy a service/pod/deployment with the appropriate annotation.

During the installation of the Operator, an `Instrumentation` object with name `elastic-instrumentation` in namespace `opentelemetry-operator-system` should have been created, which means that you have to focus on applying `annotations` to the desired pods.

The `Instrumentation` object stores important parameters:

- The **exporter endpoint**: It represents the destination for the traces, in this case the HTTP receiver configured in the EDOT DaemonSet Collector. That endpoint has to be reachable by the Pods being instrumented.

```yaml
  exporter:
    endpoint: http://opentelemetry-kube-stack-daemon-collector.opentelemetry-operator-system.svc.cluster.local:4318
```

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

## Configuring auto-instrumentation

To enable auto-instrumentation, add the corresponding annotation to the pods of existing deployments (`spec.template.metadata.annotations`), or to the desired namespace (to auto-instrument all pods in the namespace):

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: myapp
spec:
  ...
  template:
    metadata:
      annotations:
        instrumentation.opentelemetry.io/inject-<LANGUAGE>: "opentelemetry-operator-system/elastic-instrumentation"
      ...
    spec:
      containers:
      - image: myapplication-image
        name: app
      ...        
```

where <LANGUAGE> is one of: `go` , `java`, `nodejs`, `python`, `dotnet`

If you followed the proposed installation of the Operator with the provided `values.yaml`, the previous value (`"opentelemetry-operator-system/elastic-instrumentation"`) should be the right one in the environment.

The possible values for the annotation are documented [here](https://opentelemetry.io/docs/kubernetes/operator/automatic/#add-annotations-to-existing-deployments):

- `"true"`: to inject Instrumentation resource with default name from the current namespace.
- `"my-instrumentation"`: to inject Instrumentation CR instance with name "my-instrumentation" in the current namespace.
- `"my-other-namespace/my-instrumentation"`: to inject Instrumentation CR instance with name "my-instrumentation" from another namespace "my-other-namespace".
- `"false"`: do not inject.

> [!NOTE]
> After adding annotations to Pods or Namespaces the applications need to be restarted for the injection to occur.

### Namespace based annotations example

The following example creates a namespace with an annotation to instrument all pods of the namespace with the `java` SDK.

```
kubectl create namespace java-apps

#Annotate app namespace
kubectl annotate namespace java-apps instrumentation.opentelemetry.io/inject-java="opentelemetry-operator-system/elastic-instrumentation"

# Run a java example application in the namespace
kubectl run otel-test -n java-apps --env OTEL_INSTRUMENTATION_METHODS_INCLUDE="test.Testing[methodB]" --image docker.elastic.co/demos/apm/k8s-webhook-test
```

## Advanced configuration

You can apply configuration at two different levels:
- At Pod/container level, by using OTEL related environment variables.
- At `Instrumentation` object level.

Use cases:
- Change the library to be injected.
- Change the exporter endpoint.
- Apply certain logging level settings (OTEL_LOG_LEVEL).


## Manual instrumentation

This process is more complicated and requires changes in your workload definitions.
(TBD)Also your application containers should be prepared for OTEL.
