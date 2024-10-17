# Troubleshooting auto-instrumentation

1. Check the operator is running, eg
```
$ kubectl get pods -n opentelemetry-operator-system
NAME                                                              READY   STATUS             RESTARTS      AGE
opentelemetry-kube-stack-opentelemetry-operator-7b8684cfbdbv4hj   2/2     Running            0             58s
...
```

2. Check the `Instrumentation` object has been deployed, eg
```
$ kubectl describe Instrumentation -n opentelemetry-operator-system
Name:         elastic-instrumentation
Namespace:    opentelemetry-operator-system
  ...
Kind:         Instrumentation
Metadata:
  ...
Spec:
  Dotnet:
    Image:  docker.elastic.co/observability/elastic-otel-dotnet:edge
  Go:
    Image:  ghcr.io/open-telemetry/opentelemetry-go-instrumentation/autoinstrumentation-go:v0.14.0-alpha
  Java:
    Image:  docker.elastic.co/observability/elastic-otel-javaagent:1.0.0
  Nodejs:
    Image:  docker.elastic.co/observability/elastic-otel-node:edge
  Python:
    Image:  docker.elastic.co/observability/elastic-otel-python:edge
  ...
```

3. Check your pod is running, eg (using example running in banana namespace)
```
$ kubectl get pods -n banana
NAME               READY   STATUS    RESTARTS   AGE
example-otel-app   1/1     Running   0          104s
```

4. Check the pod has had the instrumentation initcontainer installed (for golang, container not initcontainer) and that the events show the docker image was successfully pulled and containers started
```
$ kubectl describe pod/example-otel-app -n banana
Name:             example-otel-app
Namespace:        banana
...
Annotations:      instrumentation.opentelemetry.io/inject-java: opentelemetry-operator-system/elastic-instrumentation
Init Containers:
  opentelemetry-auto-instrumentation-java:
    Container ID:  docker://7ecdf3954263d591b994ed1c0519d16322479b1515b58c1fbbe51d3066210d99
    Image:         docker.elastic.co/observability/elastic-otel-javaagent:1.0.0
    Image ID:      docker-pullable://docker.elastic.co/observability/elastic-otel-javaagent@sha256:28d65d04a329c8d5545ed579d6c17f0d74800b7b1c5875e75e0efd29e210566a
    ...
Containers:
  example-otel-app:
...
Events:
  Type    Reason     Age   From               Message
  ----    ------     ----  ----               -------
  Normal  Scheduled  5m3s  default-scheduler  Successfully assigned banana/example-otel-app to docker-desktop
  Normal  Pulled     5m3s  kubelet            Container image "docker.elastic.co/observability/elastic-otel-javaagent:1.0.0" already present on machine
  Normal  Created    5m3s  kubelet            Created container opentelemetry-auto-instrumentation-java
  Normal  Started    5m3s  kubelet            Started container opentelemetry-auto-instrumentation-java
  Normal  Pulling    5m2s  kubelet            Pulling image "docker.elastic.co/demos/apm/k8s-webhook-test"
  Normal  Pulled     5m1s  kubelet            Successfully pulled image "docker.elastic.co/demos/apm/k8s-webhook-test" in 1.139s (1.139s including waiting). Image size: 406961626 bytes.
  Normal  Created    5m1s  kubelet            Created container example-otel-app
  Normal  Started    5m1s  kubelet            Started container example-otel-app
```

5.(a) check your pod logs - look for agent output eg
```
$ kubectl logs example-otel-app -n banana
...
[otel.javaagent 2024-10-11 13:32:44:127 +0000] [main] INFO io.opentelemetry.javaagent.tooling.VersionLogger - opentelemetry-javaagent - version: 1.0.0
...
```

5.(b) if there is no obvious agent log output, restart the pod with agent log level set to debug and look for agent debug output. Setting the agent to debug is different for the different language agents.
- All langs: add/set environment variable OTEL_LOG_LEVEL set to debug, eg
```
      env:
      - name: OTEL_LOG_LEVEL
        value: "debug"
```
- Java: add/set environment variable OTEL_JAVAAGENT_DEBUG set to true
