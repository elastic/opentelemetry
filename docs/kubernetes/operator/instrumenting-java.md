# Instrumenting Java applications with EDOT SDKs on Kubernetes

This document focuses on instrumenting Java applications on Kubernetes, using the OpenTelemetry Operator, EDOT Collectors and the [EDOT Java](https://github.com/elastic/elastic-otel-java) SDK.

For general knowledge about the EDOT Java SDK, refer to the [getting started guide](https://github.com/elastic/elastic-otel-java/blob/main/docs/get-started.md).

For general information about instrumenting applications on kubernetes, refer to [instrumenting applications](./instrumenting-applications.md).

## Java agent extensions consideration

The operator supports configuration that installs [Java agent extensions](https://opentelemetry.io/docs/zero-code/java/agent/extensions/) in `Instrumentation` objects. The extension needs to be available in an image. Refer to [using extensions with the OpenTelemetry Java agent](https://www.elastic.co/observability-labs/blog/using-the-otel-operator-for-injecting-elastic-agents#using-an-extension-with-the-opentelemetry-java-agent) for an example of adding an extension to an agent.

## Guided example to instrument a Java app with EDOT Java SDK on Kubernetes

In the following example you will learn how to:

- Deploy an example Java app in a dedicated namespace.
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

1. Create a `java` namespace and run a deployment named `java-app`:

    ```bash
    # Java Namespace and Deployment
    kubectl create namespace java
    kubectl apply -f - <<EOF
    apiVersion: apps/v1
    kind: Deployment
    metadata:
      labels:
        app: java-app
      name: java-app
      namespace: java
    spec:
      replicas: 1
      selector:
        matchLabels:
          app: java-app
      template:
        metadata:
          labels:
            app: java-app
        spec:
          containers:
          - name: java-app
            image: docker.elastic.co/demos/apm/k8s-webhook-test
            env:
            - name: OTEL_INSTRUMENTATION_METHODS_INCLUDE
              value: "test.Testing[methodB]"
    EOF
    ```

2. Enable auto-instrumentation of the Java application using one of the following methods:

  - Add an annotation at namespace level:

    ```bash
    kubectl annotate namespace java instrumentation.opentelemetry.io/inject-java=opentelemetry-operator-system/elastic-instrumentation
    ```

  - Alternatively, edit the `java-app` deployment to include the annotation under `spec.template.metadata.annotations`:

    ```yaml
    spec:
    ...
      template:
        metadata:
          labels:
            app: java-app
          annotations:
            instrumentation.opentelemetry.io/inject-java: opentelemetry-operator-system/elastic-instrumentation
    ...
    ```

3. Restart application

    ```bash
    kubectl rollout restart deployment java-app -n java
    ```

3. Verify the auto-instrumentation resources are injected in the Pod:

  Java apps are instrumented by the OpenTelemetry Operator with the following actions:
    - It adds an init container in the Pod with the objective of copying the SDK and making it available for the main container.
    - Defines and mount an emptyDir volume 
    - Configures the main container to use the SDK as a `java agent`.

  Run `kubectl describe pod java-app-xxxx` and check:

  - There should be an init container named `opentelemetry-auto-instrumentation-java` in the Pod:

    ```bash
    $ kubectl describe pod java-app-8d84c47b8-8h5z2 -n java
    Name:             java-app-8d84c47b8-8h5z2
    Namespace:        java
    ...
    ...
    Init Containers:
      opentelemetry-auto-instrumentation-java:
        Container ID:  containerd://cbf67d7ca1bd62c25614b905a11e81405bed6fd215f2df21f84b90fd0279230b
        Image:         docker.elastic.co/observability/elastic-otel-javaagent:1.0.0
        Image ID:      docker.elastic.co/observability/elastic-otel-javaagent@sha256:28d65d04a329c8d5545ed579d6c17f0d74800b7b1c5875e75e0efd29e210566a
        Port:          <none>
        Host Port:     <none>
        Command:
          cp
          /javaagent.jar
          /otel-auto-instrumentation-java/javaagent.jar
        State:          Terminated
          Reason:       Completed
          Exit Code:    0
          Started:      Wed, 13 Nov 2024 15:47:02 +0100
          Finished:     Wed, 13 Nov 2024 15:47:03 +0100
        Ready:          True
        Restart Count:  0
        Environment:    <none>
        Mounts:
          /otel-auto-instrumentation-java from opentelemetry-auto-instrumentation-java (rw)
          /var/run/secrets/kubernetes.io/serviceaccount from kube-api-access-swhn5 (ro)
    ```

  - The main container of the deployment is using the SDK as `javaagent`: 

    ```bash
    ...
    Containers:
      java-app:
        Environment:
    ...
          OTEL_INSTRUMENTATION_METHODS_INCLUDE:  test.Testing[methodB]
          JAVA_TOOL_OPTIONS:                      -javaagent:/otel-auto-instrumentation-java/javaagent.jar
          OTEL_SERVICE_NAME:                     java-app
          OTEL_EXPORTER_OTLP_ENDPOINT:           http://opentelemetry-kube-stack-daemon-collector.opentelemetry-operator-system.svc.cluster.local:4318
    ...
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
    - `k8s.deployment.name: "java-app"`
    - `k8s.pod.name: java-app*`

  Note that the application logs are not provided by the instrumentation library, but by the DaemonSet collector deployed as part of the [operator installation](./README.md)

## Troubleshooting

- Refer to [troubleshoot auto-instrumentation](./troubleshoot-auto-instrumentation.md) for further analysis.
