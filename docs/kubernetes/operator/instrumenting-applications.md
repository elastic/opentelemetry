# Instrumenting applications with EDOT on Kubernetes

Elastic Distribution of OpenTelemetry (EDOT) extends [OpenTelemetry language SDKs](https://opentelemetry.io/docs/languages/) for multiple languages:

* [EDOT Java](https://github.com/elastic/elastic-otel-java)
* [EDOT .NET](https://github.com/elastic/elastic-otel-dotnet)
* [EDOT Node.js](https://github.com/elastic/elastic-otel-node)
* [EDOT Python](https://github.com/elastic/elastic-otel-python)
* [EDOT PHP](https://github.com/elastic/elastic-otel-php/)

This section provides guidance and examples for applications instrumentation in a Kubernetes environment for all supported languages.

In Kubernetes environments with the OpenTelemetry Operator, [**automatic (or zero-code) instrumentation**](https://opentelemetry.io/docs/kubernetes/operator/automatic/) simplifies the process by automatically injecting and configuring instrumentation libraries into the targeted Pods.

On the other hand, **manual instrumentation** with OpenTelemetry involves adding specific OpenTelemetry SDKs and APIs directly into your application’s code. This approach provides more granular control over what and how data is captured, allowing you to customize trace spans, metrics, and logging based on your application’s logic.

## Table of contents

- [Supported languages](#supported-languages)
- [Prerequisites](#prerequisites)
- [Auto-instrumentation basics](#auto-instrumentation-basics)
- [Configuring auto-instrumentation](#configuring-auto-instrumentation)
- [Advanced configuration](#advanced-configuration)
- [Manual instrumentation](#manual-instrumentation)

## Supported languages

The following table illustrates the different languages supported by OpenTelemetry (OTel) and the Elastic Stack, the type of SDK/API used for instrumentation (either zero-code or source code dependencies), and the corresponding deployment types (on-premises, ESS, or serverless) for each language.

| Language   | OTel SDK/API Type                                       | Deployment Type Support             |
|------------|---------------------------------------------------------|-------------------------------------|
| Java       | EDOT Java - **zero-code instrumentation**               | All deployment types                |
| Node.js    | EDOT Node.js - **zero-code instrumentation**            | All deployment types                |
| .NET       | EDOT .NET - **zero-code instrumentation**               | All deployment types                |
| PHP        | EDOT PHP - source code dependencies                     | All deployment types                |
| Python     | EDOT Python - **zero-code instrumentation**             | All deployment types                |
| Swift      | EDOT Swift - source code dependencies                   | ESS, on-premises                    |
| Android    | EDOT Android - source code dependencies                 | ESS, on-premises                    |
| Javascript | Vanilla OTel RUM SDK/API - source code dependencies     | ESS, on-premises                    |
| Rust       | Vanilla OTel Rust SDK/API - source code dependencies    | All deployment types                |
| Ruby       | Vanilla OTel Ruby SDK/API - source code dependencies    | All deployment types                |
| Go         | Vanilla OTel Go SDK/API - **zero-code instrumentation** | All deployment types                |
| C++        | Vanilla OTel C++ SDK/API - source code dependencies     | All deployment types                |

## Prerequisites

Before starting with application auto-instrumentation, ensure the following prerequisites are in place for proper setup:
 
- Install the OpenTelemetry operator and EDOT collectors following the [getting started guide](./README.md).
- Ensure a valid `kind: Instrumentation` object exists in the cluster.

## Auto-instrumentation basics

Zero-code instrumenation is handled by the operator through `Instrumenation` objects.

The process is common to all supported languages, and it follows the usual OTel Operator steps for [auto-instrumentation injection](https://github.com/open-telemetry/opentelemetry-operator#opentelemetry-auto-instrumentation-injection):

  1. Install the OTel Operator into a k8s cluster.
  2. Create a `kind: Instrumentation` object with the appropriate config.
  3. Deploy a pod or deployment with the appropriate annotation.

If you followed the [getting started guide](./README.md) to install the operator, there should be an `Instrumentation` object with name `elastic-instrumentation` in namespace `opentelemetry-operator-system`. The `Instrumentation` object stores important parameters:

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
    image: docker.elastic.co/observability/elastic-otel-node:0.4.1
  python:
    image: docker.elastic.co/observability/elastic-otel-python:0.3.0
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

where `<LANGUAGE>` is one of: `go` , `java`, `nodejs`, `python`, `dotnet`

> [!NOTE]
> Ensure you add the annotations at Pod level and not directly at the workload `spec` level (Deployment, Job, etc.)
> After adding annotations to Pods or Namespaces, the applications must be restarted for the instrumentation injection to take effect.

If you followed the proposed installation of the Operator using the provided `values.yaml`, the previous value (`"opentelemetry-operator-system/elastic-instrumentation"`) should be correct for the environment.

In case you have multiple Instrumentation objects with different settings or images, ensure you point your pods to the the desired `Instrumentation` objects in the annotations.

The possible values for the annotation are documented in the [Operator documentation](https://opentelemetry.io/docs/kubernetes/operator/automatic/#add-annotations-to-existing-deployments). For reference purposes, the values are:

- `"true"`: to inject Instrumentation resource with default name from the current namespace.
- `"my-instrumentation"`: to inject Instrumentation CR instance with name `"my-instrumentation"` in the current namespace.
- `"my-other-namespace/my-instrumentation"`: to inject Instrumentation CR instance with name `"my-instrumentation"` from another namespace `"my-other-namespace"`.
- `"false"`: do not inject.

### Namespace based annotations example

The following example creates a namespace with an annotation to instrument all pods of the namespace with `java` libraries.

```
kubectl create namespace java-apps

#Annotate app namespace
kubectl annotate namespace java-apps instrumentation.opentelemetry.io/inject-java="opentelemetry-operator-system/elastic-instrumentation"

# Run a java example application in the namespace
kubectl run otel-test -n java-apps --env OTEL_INSTRUMENTATION_METHODS_INCLUDE="test.Testing[methodB]" --image docker.elastic.co/demos/apm/k8s-webhook-test
```

## Advanced configuration

You can apply OTEL specific configuration to your applications at two different levels:
- At Pod/container level, by using OTEL related environment variables.
- At `Instrumentation` object level, for example configuring different settings per language.

Consider also the creation of different `Instrumentation` objects for different purposes, such as:

- Different configuration options for certain languages.
- Trying out different versions of the SDKs.

Use cases:
- Change the library to be injected.
- Change the exporter endpoint.
- Apply certain logging level settings (OTEL_LOG_LEVEL).


## Manual instrumentation
(TBD, in-progress)

The manual instrumentation...
Configuration requirements (does every language has its own requirements)?
Exporter destination? HTTP vs OTLP? does each EDOT SDK support different protocols?

