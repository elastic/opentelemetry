# Instrumenting Java applications with EDOT SDKs on Kubernetes

This document focuses on instrumenting Java applications on Kubernetes, using the OpenTelemetry Operator, EDOT Collectors and the [Elastic Distribution of OpenTelemetry Java](https://github.com/elastic/elastic-otel-java) SDK (EDOT Java).

- For general knowledge about the EDOT Java SDK, refer to the [getting started guide](https://github.com/elastic/elastic-otel-java/blob/main/docs/get-started.md).
- For Java auto-instrumentation specifics, refer to [OpenTelemetry Operator Java auto-instrumentation](https://opentelemetry.io/docs/kubernetes/operator/automatic/#java)
- For general information about instrumenting applications on kubernetes, refer to [instrumenting applications](./instrumenting-applications.md)

## Java agent extensions consideration

The operator supports a configuration that installs [Java agent extensions](https://opentelemetry.io/docs/zero-code/java/agent/extensions/) in `Instrumentation` objects. The extension needs to be available in an image. Refer to [using extensions with the OpenTelemetry Java agent](https://www.elastic.co/observability-labs/blog/using-the-otel-operator-for-injecting-elastic-agents#using-an-extension-with-the-opentelemetry-java-agent) for an example of adding an extension to an agent.

## Guided example to instrument a Java app with EDOT Java SDK on Kubernetes

In this section you will learn how to:

- Enable auto-instrumentation of a Java application following any of the supported methods, such as:
  - Adding an annotation to the deployment pods.
  - Adding an annotation to the namespace.
- Verify that auto-instrumentation libraries are injected and configured correctly.
- Confirm data is flowing to **Kibana Observability**.

For demonstration purposes, we assume the application to be instrumented is a deployment named `java-app` running in the `java-ns` namespace.

1. Ensure you have successfully [installed the OpenTelemetry Operator](./README.md), and confirm that the following `Instrumentation` object exists in the system:

```bash
$ kubectl get instrumentation -n opentelemetry-operator-system
NAME                      AGE    ENDPOINT                                                                                                
elastic-instrumentation   107s   http://opentelemetry-kube-stack-daemon-collector.opentelemetry-operator-system.svc.cluster.local:4318
```
> [!NOTE]
> If your `Instrumentation` object has a different name or is created in a different namespace, you will have to adapt the annotation value in the next step.

2. Enable auto-instrumentation of your Java application using one of the following methods:

  - Edit your application workload definition and include the annotation under `spec.template.metadata.annotations`:

    ```yaml
    kind: Deployment
    metadata:
      name: java-app
      namespace: java-ns
    spec:
    ...
      template:
        metadata:
    ...
          annotations:
            instrumentation.opentelemetry.io/inject-java: opentelemetry-operator-system/elastic-instrumentation
    ...
    ```

  - Alternatively, add the annotation at namespace level to apply auto-instrumentation in all Pods of the namespace:

    ```bash
    kubectl annotate namespace java-ns instrumentation.opentelemetry.io/inject-java=opentelemetry-operator-system/elastic-instrumentation
    ```

3. Restart application

  Once the annotation has been set, the Pods need to be recreated for the instrumentation libraries to be injected.

    ```bash
    kubectl rollout restart deployment java-app -n java
    ```

4. Verify the [auto-instrumentation resources](./instrumenting-applications.md#how-auto-instrumentation-works) are injected in the Pod:

  Run a `kubectl describe` of one of your application Pods and check:

  - There should be an init container named `opentelemetry-auto-instrumentation-java` in the Pod:

    ```bash
    $ kubectl describe pod java-app-8d84c47b8-8h5z2 -n java
    Name:             java-app-8d84c47b8-8h5z2
    Namespace:        java-ns
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

5. Confirm data is flowing to **Kibana**:

  - Open **Observability** -> **Applications** -> **Service inventory**, and determine if:
    - The application appears in the list of services.
    - The application shows transactions and metrics.
  
  - For application container logs, open **Kibana Discover** and filter for your Pod's logs. In the provided example, we could filter for them with either of the following:
    - `k8s.deployment.name: "java-app"` (**adapt the query filter to your use case**)
    - `k8s.pod.name: java-app*` (**adapt the query filter to your use case**)

  Note that the application logs are not provided by the instrumentation library, but by the DaemonSet collector deployed as part of the [operator installation](./README.md).

## Troubleshooting

- Refer to [troubleshoot auto-instrumentation](./troubleshoot-auto-instrumentation.md) for further analysis.
