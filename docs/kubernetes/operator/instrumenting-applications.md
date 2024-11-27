# Instrumenting applications with EDOT SDKs on Kubernetes

Elastic Distributions of OpenTelemetry (EDOT) SDKs cover multiple languages:

* [EDOT Java](https://github.com/elastic/elastic-otel-java)
* [EDOT .NET](https://github.com/elastic/elastic-otel-dotnet)
* [EDOT Node.js](https://github.com/elastic/elastic-otel-node)
* [EDOT Python](https://github.com/elastic/elastic-otel-python)
* [EDOT PHP](https://github.com/elastic/elastic-otel-php/)

This section provides guidance and examples for applications instrumentation in a Kubernetes environment for all supported languages.

In Kubernetes environments with the OpenTelemetry Operator, [**automatic (or zero-code) instrumentation**](https://opentelemetry.io/docs/kubernetes/operator/automatic/) simplifies the process by injecting and configuring instrumentation libraries into the targeted Pods.

On the other hand, **manual instrumentation** with OpenTelemetry allows you to customize trace spans, metrics, and logging directly in your application’s code. This approach provides more granular control over what and how data is captured.

## Table of contents

- [Supported languages](#supported-languages)
- [Prerequisites](#prerequisites)
- [Auto-instrumentation basics](#auto-instrumentation-basics)
- [Configuring auto-instrumentation](#configuring-auto-instrumentation)
- [How auto-instrumentation works](#how-auto-instrumentation-works)
- [Advanced configuration](#advanced-configuration)
- [Manual instrumentation](#manual-instrumentation)

## Supported languages

The following table illustrates the different languages supported by OpenTelemetry (OTel) and the Elastic Stack, the type of SDK/API used for instrumentation (either zero-code or source code dependencies), and the corresponding deployment types (on-premises, ESS, or serverless) for each language.

| Language   | OTel SDK/API Type                                       | Deployment Model Support             |
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

Zero-code instrumentation is handled by the operator through `Instrumentation` objects, used to automatically inject the necessary SDKs and configuration into application workloads.

If you followed the [getting started guide](./README.md) to install the operator, there should be an `Instrumentation` object with name `elastic-instrumentation` in namespace `opentelemetry-operator-system`:

```bash
kubectl get instrumentation -A
NAMESPACE                       NAME                      AGE     ENDPOINT                                                                                                SAMPLER                    SAMPLER ARG
opentelemetry-operator-system   elastic-instrumentation   5d20h   http://opentelemetry-kube-stack-daemon-collector.opentelemetry-operator-system.svc.cluster.local:4318   parentbased_traceidratio   1.0
```

The `Instrumentation` object stores important parameters:

- The **exporter endpoint** represents the destination for the traces, in this case the HTTP receiver configured in the EDOT DaemonSet Collector. That endpoint has to be reachable by the Pods being instrumented.

```yaml
  exporter:
    endpoint: http://opentelemetry-kube-stack-daemon-collector.opentelemetry-operator-system.svc.cluster.local:4318
```

- Language-specific **images** used by the operator to inject the appropriate library into each Pod.

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

To enable auto-instrumentation, add the corresponding language annotation to the **Pods** template (`spec.template.metadata.annotations`) in your Deployment or relevant workload object (StatefulSet, Job, CronJob, etc.).

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

where ``<LANGUAGE>`` is one of: `go` , `java`, `nodejs`, `python`, `dotnet`

> [!NOTE]
> Ensure you add the annotations at Pod level and not directly at the workload `spec` level (Deployment, Job, etc.).
> Ensure the annotation value points to an existing `Instrumentation` object.

Alternatively, you can enable auto-instrumentation by adding the annotation at **namespace level**. This approach automatically applies instrumentation to all Pods within the specified namespace.

```yaml
apiVersion: v1
kind: Namespace
metadata:
  name: mynamespace
  annotations:
    instrumentation.opentelemetry.io/inject-<LANGUAGE>: "opentelemetry-operator-system/elastic-instrumentation"
```

After adding annotations to Pods or Namespaces, the applications must be restarted for the instrumentation injection to take effect:

```bash
kubectl rollout restart deployment/my-deployment
```

In case you have multiple Instrumentation objects with different settings or images, ensure you point your Pods to the the desired `Instrumentation` objects in the annotations.

The possible values for the annotation are detailed in the [Operator documentation](https://opentelemetry.io/docs/kubernetes/operator/automatic/#add-annotations-to-existing-deployments). For reference purposes, the values are:

- `"true"`: to inject Instrumentation instance with `default` name from the current namespace.
- `"my-instrumentation"`: to inject Instrumentation instance with name `"my-instrumentation"` in the current namespace.
- `"my-other-namespace/my-instrumentation"`: to inject Instrumentation instance with name `"my-instrumentation"` from another namespace `"my-other-namespace"`.
- `"false"`: do not inject.

For details on instrumenting specific languages, refer to:

- [Instrumenting Java](./instrumenting-java.md)
- [Instrumenting Python](./instrumenting-python.md)
- [Instrumenting Dotnet](./instrumenting-dotnet.md)

### Namespace based annotations example

The following example creates a namespace with an annotation to instrument all Pods of the namespace with `java` libraries.

```
kubectl create namespace java-apps

#Annotate app namespace
kubectl annotate namespace java-apps instrumentation.opentelemetry.io/inject-java="opentelemetry-operator-system/elastic-instrumentation"

# Run a java example application in the namespace
kubectl run otel-test -n java-apps --env OTEL_INSTRUMENTATION_METHODS_INCLUDE="test.Testing[methodB]" --image docker.elastic.co/demos/apm/k8s-webhook-test
```

## Verify auto-instrumentation

After adding the annotation and restarting the Pods, run `kubectl describe` on your application Pod to verify the SDK has been properly attached.

Ensure that the `init container`, `volume`, and `environment variables` described in [how auto-instrumentation works](#how-auto-instrumentation-works) have been successfully injected into the Pod.

## How auto-instrumentation works

The OpenTelemetry Operator automates the process of instrumenting applications by injecting the necessary libraries and configuration into the application Pods.
The process may vary slightly depending on the language, but it generally involves the following steps:

- **Adding an init container**:

  The operator adds an init container into the Pod. This container is responsible for copying the OpenTelemetry instrumentation library and make it accessible to the main application container.

- **Creating a shared volume**:

  The operator creates an `emptyDir` shared volume within the Pod, and mounts it in both containers. This volume serves as the medium for sharing the instrumentation library between the init container and the application container.

- **Configuring the main container**:

  The operator injects environment variables into the main application container to configure OpenTelemetry settings (for example, `OTEL_EXPORTER_OTLP_ENDPOINT` or `OTEL_TRACES_SAMPLER`). Additionally, it links the instrumentation library to the application using mechanisms specific to the language runtime, such as:
    - **For Java**: The library is linked through the `javaagent` option.
    - **For Node.js**: The library is linked through the `NODE_OPTIONS` environment variable.

## Advanced configuration

You can apply OTEL specific configuration to your applications at two different levels:
- At Pod/container level, by using OTEL related environment variables.
- At `Instrumentation` object level, for example configuring different settings per language.

Use cases:
- Change the library to be injected.
- Change the exporter endpoint.
- Apply certain logging level settings (OTEL_LOG_LEVEL).

### Adding extra Instrumentation objects

Consider also the creation of different `Instrumentation` objects for different purposes, such as:

- Different configuration options for certain languages.
- Trying out different versions of the SDKs.

(TBD: add instructions and references about Instrumentation objects)


## Manual instrumentation
(TBD, in-progress)

The manual instrumentation...
Configuration requirements (does every language has its own requirements)?
Exporter destination? HTTP vs OTLP? does each EDOT SDK support different protocols?

