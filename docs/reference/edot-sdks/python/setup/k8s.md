---
navigation_title: Kubernetes
description: Instrumenting Python applications with EDOT SDKs on Kubernetes.
applies_to:
  stack:
  serverless:
    observability:
products:
  - cloud-serverless
  - observability
  - edot-python
---

# Instrumenting Python applications with EDOT SDKs on Kubernetes

This document focuses on instrumenting Python applications on Kubernetes, using the OpenTelemetry Operator, Elastic Distribution of OpenTelemetry (EDOT) Collectors, and the EDOT Python SDK.

- For general knowledge about the EDOT Python SDK, refer to the [EDOT Java Intro page](../index.md).
- For Python auto-instrumentation specifics, refer to [OpenTelemetry Operator Python auto-instrumentation](https://opentelemetry.io/docs/kubernetes/operator/automatic/#python).
- To manually instrument your Python application code (by customizing spans and metrics), refer to [EDOT Python manual instrumentation](./manual-instrumentation.md).
- For general information about instrumenting applications on Kubernetes, refer to [instrumenting applications on Kubernetes](../../../use-cases/kubernetes/instrumenting-applications.md).

## Supported environments and configuration

- EDOT Python container image supports `glibc` and `musl` based auto-instrumentation for Python 3.12.
- `musl` based containers instrumentation requires an [extra annotation](https://opentelemetry.io/docs/kubernetes/operator/automatic/#annotations-python-musl) and operator v0.113.0+.
- To enable logs auto-instrumentation, refer to [auto-instrument python logs](https://opentelemetry.io/docs/kubernetes/operator/automatic/#auto-instrumenting-python-logs).
- To disable specific instrumentation libraries, refer to [excluding auto-instrumentation](https://opentelemetry.io/docs/kubernetes/operator/automatic/#python-excluding-auto-instrumentation).
- For a full list of configuration options, refer to [Python specific configuration](https://opentelemetry.io/docs/zero-code/python/configuration/#python-specific-configuration).
- For Python specific limitations when using the OpenTelemetry operator, refer to [Python-specific topics](https://opentelemetry.io/docs/zero-code/python/operator/#python-specific-topics).

## Instrument a Python app with EDOT Python SDK on Kubernetes

In this example, you'll learn how to:

- Enable auto-instrumentation of a Python application using one of the following supported methods:
  - Adding an annotation to the deployment Pods.
  - Adding an annotation to the namespace.
- Verify that auto-instrumentation libraries are injected and configured correctly.
- Confirm data is flowing to **Kibana Observability**.

For this example, we assume the application you're instrumenting is a deployment named `python-app` running in the `python-ns` namespace.

1. Ensure you have successfully [installed the OpenTelemetry Operator](../../../use-cases/kubernetes/deployment.md), and confirm that the following `Instrumentation` object exists in the system:

    ```bash
    $ kubectl get instrumentation -n opentelemetry-operator-system
    NAME                      AGE    ENDPOINT
    elastic-instrumentation   107s   http://opentelemetry-kube-stack-daemon-collector.opentelemetry-operator-system.svc.cluster.local:4318
    ```

    :::{note}
    > If your `Instrumentation` object has a different name or is created in a different namespace, you will have to adapt the annotation value in the next step.
    :::

2. Enable auto-instrumentation of the Python application using one of the following methods:

    - Edit your application workload definition and include the annotation under `spec.template.metadata.annotations`:

        ```yaml
        spec:
        # ...
        template:
            metadata:
            labels:
                app: python-app
            annotations:
                instrumentation.opentelemetry.io/inject-python: opentelemetry-operator-system/elastic-instrumentation
        # ...
        ```

    - Alternatively, add the annotation at namespace level to apply auto-instrumentation in all Pods of the namespace:

        ```bash
        kubectl annotate namespace python-ns instrumentation.opentelemetry.io/inject-python=opentelemetry-operator-system/elastic-instrumentation
        ```

3. Restart application:

    Once the annotation has been set, restart the application to create new Pods and inject the instrumentation libraries:

        ```bash
        kubectl rollout restart deployment python-app -n python-ns
        ```

4. Verify the [auto-instrumentation resources](../../../use-cases/kubernetes/instrumenting-applications#how-auto-instrumentation-works) are injected in the Pod:

    Run a `kubectl describe` of one of your application pods and check:

    - There should be an init container named `opentelemetry-auto-instrumentation-python` in the Pod:

        ```bash
        $ kubectl describe pod python-app-8d84c47b8-8h5z2 -n python-ns
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

    - The main container has new environment variables, including `PYTHONPATH`:

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

        ```bash
        Init Containers:
        opentelemetry-auto-instrumentation-python:
        ...
            Mounts:
            /otel-auto-instrumentation-python from opentelemetry-auto-instrumentation-python (rw)
        Containers:
        python-app:
        ...
            Mounts:
            /otel-auto-instrumentation-python from opentelemetry-auto-instrumentation-python (rw)
        ...
        Volumes:
        ...
        opentelemetry-auto-instrumentation-python:
            Type:        EmptyDir (a temporary directory that shares a pod's lifetime)
        ```

    Ensure the environment variable `OTEL_EXPORTER_OTLP_ENDPOINT` points to a valid endpoint and there's network communication between the Pod and the endpoint.

5. Confirm data is flowing to **Kibana**:

    - Open **Observability** -> **Applications** -> **Service inventory**, and determine if:
        - The application appears in the list of services.
        - The application shows transactions and metrics.
        - If [python logs instrumentation](https://opentelemetry.io/docs/kubernetes/operator/automatic/#auto-instrumenting-python-logs) is enabled, the application logs should  appear in the Logs tab.

    - For application container logs, open **Kibana Discover** and filter for your Pods' logs. In the provided example, we could filter for them with either of the following:
        - `k8s.deployment.name: "python-app"` (**adapt the query filter to your use case**)
        - `k8s.pod.name: python-app*` (**adapt the query filter to your use case**)

    Note that the container logs are not provided by the instrumentation library, but by the DaemonSet collector deployed as part of the [operator installation](../../../use-cases/kubernetes/deployment.md).

## Troubleshooting

- Refer to [troubleshoot auto-instrumentation](../../../use-cases/kubernetes/instrumenting-applications.md#troubleshooting-auto-instrumentation) for further analysis.
