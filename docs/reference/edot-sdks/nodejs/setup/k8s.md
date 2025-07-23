---
navigation_title: Kubernetes
description: How to instrument Node.js applications on Kubernetes using the Elastic Distribution of OpenTelemetry (EDOT).
applies_to:
  stack:
  serverless:
    observability:
  product:
    edot_node: ga
products:
  - id: cloud-serverless
  - id: observability
  - id: edot-sdk
---

# Instrumenting Node.js applications with EDOT SDKs on Kubernetes

Learn how to instrument Node.js applications on Kubernetes, using the OpenTelemetry Operator, the {{edot}} (EDOT) Collectors, and the EDOT Node.js SDK.

- For general knowledge about the EDOT Node.js SDK, refer to the [EDOT Node.js Intro page](/reference/edot-sdks/nodejs/index.md) and [Configuration](/reference/edot-sdks/nodejs/configuration.md).
- For Node.js auto-instrumentation specifics, refer to [OpenTelemetry Operator Node.js auto-instrumentation](https://opentelemetry.io/docs/kubernetes/operator/automatic/#nodejs).
- For general information about instrumenting applications on Kubernetes, refer to [instrumenting applications on Kubernetes](/reference/use-cases/kubernetes/instrumenting-applications.md).

## Instrument a Node.js app on Kubernetes

::::::{stepper}

::::{step} Ensure the OpenTelemetry Operator and Instrumentation object exist
Ensure you have successfully [installed the OpenTelemetry Operator](/reference/use-cases/kubernetes/deployment.md), and confirm that the following `Instrumentation` object exists in the system:

```bash
$ kubectl get instrumentation -n opentelemetry-operator-system
NAME                      AGE    ENDPOINT
elastic-instrumentation   107s   http://opentelemetry-kube-stack-daemon-collector.opentelemetry-operator-system.svc.cluster.local:4318
```

:::{note}
If your `Instrumentation` object has a different name or is created in a different namespace, you will have to adapt the annotation value in the next step.
:::
::::

::::{step} Enable auto-instrumentation for your Node.js application
Enable auto-instrumentation of your Node.js application using one of the following methods:

- Edit your application workload definition and include the annotation under `spec.template.metadata.annotations`:

  ```yaml
  kind: Deployment
  metadata:
    name: nodejs-app
    namespace: nodejs-ns
  spec:
  ...
    template:
      metadata:
  ...
        annotations:
          instrumentation.opentelemetry.io/inject-nodejs: opentelemetry-operator-system/elastic-instrumentation
  ...
  ```

- Alternatively, add the annotation at namespace level to apply auto-instrumentation in all Pods of the namespace:

  ```bash
  kubectl annotate namespace nodejs-ns instrumentation.opentelemetry.io/inject-nodejs=opentelemetry-operator-system/elastic-instrumentation
  ```
::::

::::{step} Restart your application
Once the annotation has been set, restart the application to create new Pods and inject the instrumentation libraries:

  ```bash
  kubectl rollout restart deployment nodejs-app -n nodejs-ns
  ```
::::

::::{step} Verify auto-instrumentation resources in the Pods
Verify the [auto-instrumentation resources](/reference/use-cases/kubernetes/instrumenting-applications.md#how-auto-instrumentation-works) are injected in the Pods:

Run a `kubectl describe` of one of your application Pods and check:

- There should be an init container named `opentelemetry-auto-instrumentation-nodejs` in the Pod. For example:

  ```bash
  $ kubectl describe pod nodejs-app-8d84c47b8-8h5z2 -n nodejs-ns
  Name:             nodejs-app-8d84c47b8-8h5z2
  Namespace:        nodejs-ns
  ...
  ...
  Init Containers:
    opentelemetry-auto-instrumentation-nodejs:
      Container ID:  containerd://cbf67d7ca1bd62c25614b905a11e81405bed6fd215f2df21f84b90fd0279230b
      Image:         docker.elastic.co/observability/elastic-otel-node:0.5.0
      Command:
        cp
        -r
        /autoinstrumentation/.
        /otel-auto-instrumentation-nodejs
      State:          Terminated
        Reason:       Completed
        Exit Code:    0
        Started:      Wed, 13 Nov 2024 15:47:02 +0100
        Finished:     Wed, 13 Nov 2024 15:47:03 +0100
      Ready:          True
      Restart Count:  0
      Environment:    <none>
      Mounts:
        /otel-auto-instrumentation-nodejs from opentelemetry-auto-instrumentation-nodejs (rw)
        /var/run/secrets/kubernetes.io/serviceaccount from kube-api-access-swhn5 (ro)
  ```

- The main container of the deployment loads the SDK through the `NODE_OPTIONS` environment variable:

  ```bash
  ...
  Containers:
    nodejs-app:
      Environment:
  ...
        NODE_OPTIONS:                           --require /otel-auto-instrumentation-nodejs/autoinstrumentation.js
        OTEL_SERVICE_NAME:                     nodejs-app
        OTEL_EXPORTER_OTLP_ENDPOINT:           http://opentelemetry-kube-stack-daemon-collector.opentelemetry-operator-system.svc.cluster.local:4318
  ...
  ```

  Ensure the environment variable `OTEL_EXPORTER_OTLP_ENDPOINT` points to a valid endpoint and there's network communication between the Pod and the endpoint.

- The Pod has an `EmptyDir` volume named `opentelemetry-auto-instrumentation-nodejs` mounted in both the main and the init containers in path `/otel-auto-instrumentation-nodejs`.

  ```bash
  Init Containers:
    opentelemetry-auto-instrumentation-nodejs:
  ...
      Mounts:
        /otel-auto-instrumentation-nodejs from opentelemetry-auto-instrumentation-nodejs (rw)
  Containers:
    nodejs-app:
  ...
      Mounts:
        /otel-auto-instrumentation-nodejs from opentelemetry-auto-instrumentation-nodejs (rw)
  ...
  Volumes:
  ...
    opentelemetry-auto-instrumentation-nodejs:
      Type:        EmptyDir (a temporary directory that shares a pod's lifetime)
  ```
::::

::::{step} Confirm data is flowing to {{kib}}
Confirm data is flowing to **{{kib}}**:

- Open **Observability** → **Applications** → **Service inventory**, and determine if:
    - The application appears in the list of services (`nodejs-app` in the example).
    - The application shows transactions and metrics.

    :::{note}
    You may need to generate traffic to your application to see spans and metrics.
    :::

- For application container logs, open **{{kib}} Discover** and filter for your Pods' logs. In the provided example, you could filter for them with either of the following:
    - `k8s.deployment.name: "nodejs-app"` (adapt the query filter to your use case).
    - `k8s.pod.name: nodejs-app*` (adapt the query filter to your use case).

Note that the container logs are not provided by the instrumentation library, but by the DaemonSet collector deployed as part of the [operator installation](/reference/use-cases/kubernetes/deployment.md).
::::

::::::

## Troubleshooting

Refer to [troubleshoot auto-instrumentation](/reference/use-cases/kubernetes/instrumenting-applications.md#troubleshooting-auto-instrumentation) for further analysis.
