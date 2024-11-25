# Instrumenting Node.js applications with EDOT SDKs on Kubernetes

This document focuses on instrumenting Node.js applications on Kubernetes, using the OpenTelemetry Operator, EDOT Collectors and the [EDOT Node.js](https://github.com/elastic/elastic-otel-node) SDK.

For general knowledge about the EDOT Node.js SDK, refer to the [getting started guide](https://github.com/elastic/elastic-otel-node/blob/main/docs/get-started.md).

For general information about instrumenting applications on kubernetes, refer to [instrumenting applications](./instrumenting-applications.md).

(TBD / PENDING: extra topics or relevant details about Node.js specifics)

## Guided example to instrument a Node.js app with EDOT Node.js SDK on Kubernetes

In the following example you will learn how to:

- Deploy an example Node.js app in a dedicated namespace.
- Enable auto-instrumentation of the application following any of the supported methods, such as:
  - Adding an annotation to the namespace.
  - Adding an annotation to the deployment pods.
- Verify that auto-instrumentation libraries are injected and configured correctly.
- Confirm data is flowing to **Kibana Observability**.

Before continuing, ensure you have performed the [installation of the operator](./README.md), and confirm that the following `Instrumentation` object exists in the system:

```bash
$ kubectl get instrumentation -n opentelemetry-operator-system
NAME                      AGE    ENDPOINT                                                                                                
elastic-instrumentation   107s   http://opentelemetry-kube-stack-daemon-collector.opentelemetry-operator-system.svc.cluster.local:4318
```

Example auto-instrumentation steps:

1. Create a `nodejs` namespace and run a deployment named `nodejs-app`:

(TBD / PENDING EXAMPLE)

    ```bash
    ```

2. Enable auto-instrumentation of the Node.js application using one of the following methods:

  - Add an annotation at namespace level:

    ```bash
    kubectl annotate namespace nodejs instrumentation.opentelemetry.io/inject-nodejs=opentelemetry-operator-system/elastic-instrumentation
    ```

  - Alternatively, edit the `nodejs-app` deployment to include the annotation under `spec.template.metadata.annotations`:

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

3. Restart application

    ```bash
    kubectl rollout restart deployment nodejs-app -n nodejs
    ```

3. Verify the auto-instrumentation resources are injected in the Pod:

**FROM HERE ONWARDS WE HAVE TO REVIEW EVERYTHING**

  Node.js apps are instrumented by the OpenTelemetry Operator with the following actions:
  (TBD - REVIEW)
    - It adds an init container in the Pod with the objective of copying the SDK and making it available for the main container.
    - Defines and mount an emptyDir volume 
    - Configures the main container to use the SDK as a `java agent`.

  Run `kubectl describe pod nodejs-app-xxxx` and check:

  - There should be an init container named `opentelemetry-auto-instrumentation-nodejs` in the Pod:

    ```bash
    PENDING
    ```

  - The main container of the deployment is using the SDK (TBD)

    ```bash
PENDING
    ```

  - The Pod has an `EmptyDir` volume named `opentelemetry-auto-instrumentation-java` mounted in both the main and the init containers in path `/otel-auto-instrumentation-java`.

    ```bash
    Init Containers:
      opentelemetry-auto-instrumentation-java:
    ...
        Mounts:
          /otel-auto-instrumentation-java from opentelemetry-auto-instrumentation-java (rw)
    Containers:
      java-app:
    ...  
        Mounts:
          /otel-auto-instrumentation-java from opentelemetry-auto-instrumentation-java (rw)
    ...
    Volumes:
    ...
      opentelemetry-auto-instrumentation-java:
        Type:        EmptyDir (a temporary directory that shares a pod's lifetime)
    ```

  Ensure the environment variable `OTEL_EXPORTER_OTLP_ENDPOINT` points to a valid endpoint and there's network communication between the Pod and the endpoint.

4. Confirm data is flowing through in **Kibana**:

  - Open Observability -> Applications -> Service Inventory, and determine if:
    - The application appears in the list of services.
    - The application shows transactions and metrics.
  
  - For application logs, open **Kibana Discovery** and filter for your pods log, with any of:
    - `k8s.deployment.name: "nodejs-app"`
    - `k8s.pod.name: nodejs-app*`

  Note that the application logs are not provided by the instrumentation library, but by the DaemonSet collector deployed as part of the [operator installation](./README.md)

## Troubleshooting

- Refer to [troubleshoot auto-instrumentation](./troubleshoot-auto-instrumentation.md) for further analysis.
