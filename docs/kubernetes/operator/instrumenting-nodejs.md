# Instrumenting Node.js applications with EDOT SDKs on Kubernetes

This document focuses on instrumenting Node.js applications on Kubernetes, using [Elastic Distribution of OpenTelemetry Node.js (EDOT Node.js)](https://github.com/elastic/elastic-otel-nodejs) together with the OpenTelemetry Operator and the EDOT Collectors described in the [getting started](./README.md) guide.

For general knowledge about the EDOT Node.js SDK, refer to the [getting started guide](https://github.com/elastic/elastic-otel-node/blob/main/packages/opentelemetry-node/docs/get-started.md) and [configuration](https://github.com/elastic/elastic-otel-node/blob/main/packages/opentelemetry-node/docs/configure.md).

For general information about instrumenting applications on kubernetes, refer to [instrumenting applications](./instrumenting-applications.md).

(TBD / PENDING: extra topics or relevant details about Node.js specifics for Kubernetes, if any).

## Guided example to instrument a Node.js app with EDOT Node.js SDK on Kubernetes

<!--
Useful links:
- Example: https://github.com/elastic/elastic-otel-node/tree/main/examples/otel-operator/ documented at https://github.com/elastic/elastic-otel-node/blob/main/DEVELOPMENT.md#testing-k8s-auto-instrumentation-with-otel-operator
(not user friendly, but we could use it in the future if we want to add a proper example here)
-->

In this section you will learn how to:

- Enable auto-instrumentation of a Node.js application following any of the supported methods, such as:
  - Adding an annotation to the deployment pods.
  - Adding an annotation to the namespace.
- Verify that auto-instrumentation libraries are injected and configured correctly.
- Confirm data is flowing to **Kibana Observability**.

For demonstration purposes, we assume the application to be instrumented is a deployment named `nodejs-app` running in the `nodejs-ns` namespace.

1. Ensure you have successfully [installed the OpenTelemetry Operator](./README.md), and confirm that the following `Instrumentation` object exists in the system:

```bash
$ kubectl get instrumentation -n opentelemetry-operator-system
NAME                      AGE    ENDPOINT                                                                                                
elastic-instrumentation   107s   http://opentelemetry-kube-stack-daemon-collector.opentelemetry-operator-system.svc.cluster.local:4318
```
> [!NOTE]
> If your `Instrumentation` object has a different name or is created in a different namespace, you will have to adapt the annotation value in the next step.

2. Enable auto-instrumentation of the Node.js application using one of the following methods:

  - Edit the workload definition and include the annotation under `spec.template.metadata.annotations`:

    ```yaml
    spec:
    ...
      template:
        metadata:
          labels:
            app: nodejs-app
          annotations:
            instrumentation.opentelemetry.io/inject-nodejs: opentelemetry-operator-system/elastic-instrumentation
    ...
    ```

  - Alternatively, add the annotation at namespace level to apply auto-instrumentation in all Pods of the namespace:

    ```bash
    kubectl annotate namespace nodejs-ns instrumentation.opentelemetry.io/inject-nodejs=opentelemetry-operator-system/elastic-instrumentation
    ```

3. Restart application:

  Once the annotation has been set, the Pods need to be recreated for the instrumentation libraries to be injected.

    ```bash
    kubectl rollout restart deployment nodejs-app -n nodejs
    ```

4. Verify the auto-instrumentation resources are injected in the Pod:

  Node.js apps are instrumented by the OpenTelemetry Operator with the following actions:
(TBD / WE NEED TO REVIEW HOW THIS IS DONE / NODE_OPTIONS env var?)

  - ??It adds an init container in the Pod with the objective of copying the SDK to a shared volume.

  - ??Defines an `emptyDir volume` mounted in both containers.

  - ??Adds `NODE_OPTIONS` and other OTEL related environment variables.

5. Confirm data is flowing through in **Kibana**:

  - Open Observability -> Applications -> Service Inventory, and determine if:
    - The application appears in the list of services.
    - The application shows transactions and metrics.
  
  - For application container logs, open **Kibana Discover** and filter for your pods logs. In the provided example we could filter them with any of:
    - `k8s.deployment.name: "nodejs-app"` (**adapt the query filter to your use case**)
    - `k8s.pod.name: nodejs-app*` (**adapt the query filter to your use case**)

    Note that the container logs are not provided by the instrumentation library, but by the DaemonSet collector deployed as part of the [operator installation](./README.md).

## Troubleshooting

- Refer to [troubleshoot auto-instrumentation](./troubleshoot-auto-instrumentation.md) for further analysis.
