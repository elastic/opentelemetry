# Instrumenting Python applications with EDOT SDKs on Kubernetes

This document focuses on instrumenting Python applications on Kubernetes, using the OpenTelemetry Operator, EDOT Collectors and the [EDOT Python](https://github.com/elastic/elastic-otel-python) SDK.

For general knowledge about the EDOT Python SDK, refer to the [getting started guide](https://github.com/elastic/elastic-otel-python/blob/main/docs/get-started.md).

For general information about instrumenting applications on kubernetes, refer to [instrumenting applications](./instrumenting-applications.md)

## Guided example to instrument a Python app with EDOT Python SDK on Kubernetes

In the following example you will learn how to:

- Deploy an example Python app in a dedicated namespace.
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

1. Create a `python` namespace and run a deployment named `python-app`:

    ```bash
    # Python Namespace and Deployment
    kubectl create namespace python
    kubectl apply -f - <<EOF
    apiVersion: apps/v1
    kind: Deployment
    metadata:
      labels:
        app: python-app
      name: python-app
      namespace: python
    spec:
      replicas: 1
      selector:
        matchLabels:
          app: python-app
      template:
        metadata:
          name: python-app
          labels:
            app: python-app
        spec:
          containers:
            - image: andrewgizas/python-otel-auto:latest
              imagePullPolicy: Always
              name: python-app
              env: 
              - name: OTEL_LOG_LEVEL
                value: "debug"
              - name: AGENT_HAS_STARTED_IF_YOU_SEE
                value: "Exception while exporting metrics HTTPConnectionPool"
    EOF
    ```


2. Enable auto-instrumentation of the Python application using one of the following methods:

  - Add an annotation at namespace level:

    ```bash
    kubectl annotate namespace python instrumentation.opentelemetry.io/inject-python=opentelemetry-operator-system/elastic-instrumentation
    ```

  - Alternatively, edit the `python-app` deployment to include the annotation under `spec.template.metadata.annotations`:

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

3. Restart application

    ```bash
    kubectl rollout restart deployment python-app -n python
    ```

3. Verify the auto-instrumentation resources are injected in the Pod:

  Python apps are instrumented by the OpenTelemetry Operator with the following actions:

    - It adds an init container in the Pod with the objective of copying the SDK to a shared volume.
    - Defines an `emptyDir volume` mounted in both containers.
    - Adds `PYTHONPATH` and other OTEL related environment variables.

  Run `kubectl describe pod python-app-xxxx` and check:

  - There should be an init container named `opentelemetry-auto-instrumentation-python` in the Pod:

    ```bash
    $ kubectl describe pod java-app-8d84c47b8-8h5z2 -n java
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
          OTEL_RESOURCE_ATTRIBUTES_POD_NAME:   python-app-6dc5fdf699-qwnbs (v1:metadata.name)
          OTEL_PROPAGATORS:                    tracecontext,baggage,b3
          OTEL_TRACES_SAMPLER:                 parentbased_traceidratio
          OTEL_TRACES_SAMPLER_ARG:             1.0
    ```

  - The Pod has an `EmptyDir` volume named `opentelemetry-auto-instrumentation-python` mounted in both the main and the init containers in path `/otel-auto-instrumentation-python`:

  Ensure the environment variable `OTEL_EXPORTER_OTLP_ENDPOINT` points to a valid endpoint and there's network communication between the Pod and the endpoint.

4. Confirm data is flowing through in **Kibana**:

  - Open Observability -> Applications -> Service Inventory, and determine if:
    - The application appears in the list of services.
    - The application shows transactions and metrics.
  
  - For application logs, open **Kibana Discovery** and filter for your pods log, with any of:
    - `k8s.deployment.name: "python-app"`
    - `k8s.pod.name: python-app*`

  Note that the application logs are not provided by the instrumentation library, but by the DaemonSet collector deployed as part of the [operator installation](./README.md)

## Troubleshooting

- Refer to [troubleshoot auto-instrumentation](./troubleshoot-auto-instrumentation.md) for further analysis.
