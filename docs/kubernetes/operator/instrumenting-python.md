# Instrumenting Python applications with EDOT SDKs on Kubernetes

This document focuses on instrumenting Python applications on Kubernetes, using [Elastic Distribution of OpenTelemetry Python (EDOT Python)](https://github.com/elastic/elastic-otel-python) together with the OpenTelemetry Operator and the EDOT Collectors described in the [getting started](./README.md) guide.

- For general knowledge about the EDOT Python SDK, refer to the [EDOT Python docs](https://github.com/elastic/elastic-otel-python/blob/main/docs/get-started.md).

- For general information about instrumenting applications on kubernetes, refer to [instrumenting applications](./instrumenting-applications.md).

- To manually instrument your Python application code (by customizing transactions, traces, and spans), refer to [EDOT Python manual instrumentation](https://github.com/elastic/elastic-otel-python/blob/main/docs/manual-instrumentation.md#Manually-instrument-your-Python-application).

## Supported environments and configuration

- EDOT Python container image supports `glibc` and `musl` based auto-instrumentation for Python 3.12.
- `musl` based containers instrumentation requires an [extra annotation](https://opentelemetry.io/docs/kubernetes/operator/automatic/#annotations-python-musl) and operator v0.113.0+.
- To enable logs auto-instrumentation, refer to [auto-instrument python logs](https://opentelemetry.io/docs/kubernetes/operator/automatic/#auto-instrumenting-python-logs).
- To disable specific instrumentation libraries, refer to [excluding auto-instrumentation](https://opentelemetry.io/docs/kubernetes/operator/automatic/#python-excluding-auto-instrumentation).
- For a full list of configuration options, refer to [Python specific configuration](https://opentelemetry.io/docs/zero-code/python/configuration/#python-specific-configuration).
- For Python specific limitations when using the OpenTelemetry operator, refer to [Python-specific topics](https://opentelemetry.io/docs/zero-code/python/operator/#python-specific-topics).

## Guided example to instrument a Python app with EDOT Python SDK on Kubernetes

In this section you will learn how to:

- Enable auto-instrumentation of a Python application following any of the supported methods, such as:
  - Adding an annotation to the deployment pods.
  - Adding an annotation to the namespace.
- Verify that auto-instrumentation libraries are injected and configured correctly.
- Confirm data is flowing to **Kibana Observability**.

For demonstration purposes, we assume the application to be instrumented is a deployment named `python-app` running in the `python-ns` namespace.

1. Ensure you have successfully [installed the OpenTelemetry Operator](./README.md), and confirm that the following `Instrumentation` object exists in the system:

```bash
$ kubectl get instrumentation -n opentelemetry-operator-system
NAME                      AGE    ENDPOINT                                                                                                
elastic-instrumentation   107s   http://opentelemetry-kube-stack-daemon-collector.opentelemetry-operator-system.svc.cluster.local:4318
```
> [!NOTE]
> If your `Instrumentation` object has a different name or is created in a different namespace, you will have to adapt the annotation value in the next step.

2. Enable auto-instrumentation of the Python application using one of the following methods:

  - Edit the `python-app` workload definition and include the annotation under `spec.template.metadata.annotations`:

    ```yaml
    spec:
    ...
      template:
        metadata:
          labels:
            app: python-app
          annotations:
            instrumentation.opentelemetry.io/inject-python: opentelemetry-operator-system/elastic-instrumentation
    ...
    ```

  - Alternatively, add the annotation at namespace level to apply auto-instrumentation in all Pods of the namespace:

    ```bash
    kubectl annotate namespace python-ns instrumentation.opentelemetry.io/inject-python=opentelemetry-operator-system/elastic-instrumentation
    ```

3. Restart application:

  Once the annotation has been set, the Pods need to be recreated for the instrumentation libraries to be injected.

    ```bash
    kubectl rollout restart deployment python-app -n python
    ```

4. Verify the auto-instrumentation resources are injected in the Pod:

  Python apps are instrumented by the OpenTelemetry Operator with the following actions:

  - It adds an init container in the Pod with the objective of copying the SDK to a shared volume.

  - Defines an `emptyDir volume` mounted in both containers.

  - Adds `PYTHONPATH` and other OTEL related environment variables.

  Run a `kubectl describe` of one of your application pods and check:

  - There should be an init container named `opentelemetry-auto-instrumentation-python` in the Pod:

    ```bash
    $ kubectl describe pod python-app-8d84c47b8-8h5z2 -n python
    ...
    ...
    Init Containers:
      opentelemetry-auto-instrumentation-python:
        Container ID:  containerd://fdc86b3191e34ef5ec872853b14a950d0af1e36b0bc207f3d59bd50dd3caafe9
        Image:         docker.elastic.co/observability/elastic-otel-python:0.3.0
        Image ID:      docker.elastic.co/observability/elastic-otel-python@sha256:de7b5cce7514a10081a00820a05097931190567ec6e18a384ff7c148bad0695e
        Port:          <none>
        Host Port:     <none>
        Command:
          cp
          -r
          /autoinstrumentation/.
          /otel-auto-instrumentation-python
        State:          Terminated
          Reason:       Completed
    ...
    ```

  - The main container has new environment variables: 

    ```bash
    ...
    Containers:
      python-app:
    ...
        Environment:
    ...
          PYTHONPATH:                          /otel-auto-instrumentation-python/opentelemetry/instrumentation/auto_instrumentation:/otel-auto-instrumentation-python
          OTEL_EXPORTER_OTLP_PROTOCOL:         http/protobuf
          OTEL_TRACES_EXPORTER:                otlp
          OTEL_METRICS_EXPORTER:               otlp
          OTEL_SERVICE_NAME:                   python-app
          OTEL_EXPORTER_OTLP_ENDPOINT:         http://opentelemetry-kube-stack-daemon-collector.opentelemetry-operator-system.svc.cluster.local:4318
    ...
    ```

  - The Pod has an `EmptyDir` volume named `opentelemetry-auto-instrumentation-python` mounted in both the main and the init containers in path `/otel-auto-instrumentation-python`:

  Ensure the environment variable `OTEL_EXPORTER_OTLP_ENDPOINT` points to a valid endpoint and there's network communication between the Pod and the endpoint.

5. Confirm data is flowing through in **Kibana**:

  - Open Observability -> Applications -> Service Inventory, and determine if:
    - The application appears in the list of services.
    - The application shows transactions and metrics.
    - If [python logs instrumentation](https://opentelemetry.io/docs/kubernetes/operator/automatic/#auto-instrumenting-python-logs) is enabled, the application logs should  appear in the Logs tab.
  
  - For application container logs, open **Kibana Discover** and filter for your pods logs. In the provided example we could filter them with any of:
    - `k8s.deployment.name: "python-app"` (**adapt the query filter to your use case**)
    - `k8s.pod.name: python-app*` (**adapt the query filter to your use case**)

    Note that the container logs are not provided by the instrumentation library, but by the DaemonSet collector deployed as part of the [operator installation](./README.md).

## Troubleshooting

- Refer to [troubleshoot auto-instrumentation](./troubleshoot-auto-instrumentation.md) for further analysis.
