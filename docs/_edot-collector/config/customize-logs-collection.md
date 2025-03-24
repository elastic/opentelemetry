---
title: Customize Logs
parent: Configuration
layout: default
nav_order: 3
---

# Customize Logs Collection

🚧 Coming soon

## Pre-processing Logs

- limitation: (as of 9.0) Elasticsearch Ingest Pipelinges are not (yet) applicable to OTel-native data
- pre-processing of logs needs to happen in OTel collectors

### Parsing JSON logs

```yaml
# ...
receivers:
  filelog:
    # ...
    operators:
      # Parse body as JSON https://github.com/open-telemetry/opentelemetry-collector-contrib/blob/main/pkg/stanza/docs/operators/json_parser.md
      - type: json_parser
        on_error: send_quiet
        parse_from: body
        parse_to: body

    # ...
``` 

### Setting custom fields

## Customizing logs parsing on Kubernetes

TODO: use K8s pods annotation to configure logs parsing, link Blog post

Daemonset collector config:

```yaml
receivers:
  receiver_creator/logs:
    watch_observers: [k8s_observer]
    discovery:
      enabled: true
    receivers:

# ...

extensions:
  k8s_observer:

# ...

service:
  extensions: [k8s_observer]
  pipelines:
```

- Make sure to remove / comment out the static file log receiver (or restrict the log file pattern) to avoid log duplication

Annotation of the pod

```yaml
# ...
metadata:
  annotations:
  io.opentelemetry.discovery.logs/enabled: "true"
  io.opentelemetry.discovery.logs/config: |
    operators:
      - id: container-parser
        type: container
      - id: json-parser
        type: json_parser
        on_error: send_quiet
        parse_from: body
        parse_to: body
      - id: custom-value
        type: add
        field: attributes.tag
        value: custom-value
spec:
    containers:
    # ...
```

## Using Processors / OTTL for Logs processing