---
navigation_title: Configure Logs Collection


applies_to:
  stack:
  serverless:
    observability:
products:
  - cloud-serverless
  - observability
---

# Configure Logs Collection

This page contains example and references for customizing logs collection.

:::{note}
As of Elastic Stack version <COLLECTOR_VERSION> Elasticsearch Ingest Pipelines are not (yet) applicable to OTel-native data, see [corresponding limitation documentation](../../compatibility/limitations#centralized-parsing-and-processing-of-data).
Hence, we recommend using OTel collector processing pipelines for pre-processing and parsing of logs.
:::


## Parsing JSON logs

Parsing logs that come in json format can be achieved through
[filelog](https://github.com/open-telemetry/opentelemetry-collector-contrib/blob/v0.123.0/receiver/filelogreceiver/README.md)
receiver's operators. Specifically, the
[`router`](https://github.com/open-telemetry/opentelemetry-collector-contrib/blob/v0.123.0/pkg/stanza/docs/operators/router.md)
operator can be used in order to check if the format is json and route the logs to
[`json-parser`](https://github.com/open-telemetry/opentelemetry-collector-contrib/blob/v0.123.0/pkg/stanza/docs/operators/json_parser.md):

```yaml
# ...
receivers:
  filelog:
    # ...
    operators:
      # Check if format is json and route properly
      - id: get-format
        routes:
        - expr: body matches "^\\{"
          output: json-parser
        type: router
      # Parse body as JSON https://github.com/open-telemetry/opentelemetry-collector-contrib/blob/main/pkg/stanza/docs/operators/json_parser.md
      - type: json_parser
        id: json-parser
        on_error: send_quiet
        parse_from: body
        parse_to: body

    # ...
```

## Parsing multiline logs

Parsing mutliline logs can be achieved using the
[`multiline`](https://github.com/open-telemetry/opentelemetry-collector-contrib/blob/v0.123.0/receiver/filelogreceiver/README.md#multiline-configuration)
option as in the following example:

```yaml
receivers:
  filelog:
    include:
    - /var/log/example/multiline.log
    multiline:
      line_start_pattern: ^Exception
```

The above configuration can parse the following logs that span across multiple lines and recombine them
properly into one single log message:

```log
Exception in thread 1 "main" java.lang.NullPointerException
        at com.example.myproject.Book.getTitle(Book.java:16)
        at com.example.myproject.Author.getBookTitles(Author.java:25)
        at com.example.myproject.Bootstrap.main(Bootstrap.java:14)
Exception in thread 2 "main" java.lang.NullPointerException
        at com.example.myproject.Book.getTitle(Book.java:16)
        at com.example.myproject.Author.getBookTitles(Author.java:25)
        at com.example.myproject.Bootstrap.main(Bootstrap.java:44)
```

## Parsing OTLP logs in JSON format

Applications instrumented with OpenTelemetry SDKs can be tuned to write their logs in `OTLP/JSON` format
in files that are stored on the disk. With that, the
[filelog](https://github.com/open-telemetry/opentelemetry-collector-contrib/blob/v0.123.0/receiver/filelogreceiver/README.md)
receiver can be used to collect and parse these logs and
forward them to the
[`otlpjson`](https://github.com/open-telemetry/opentelemetry-collector-contrib/tree/v0.123.0/connector/otlpjsonconnector)
connector which extracts the `OTLP` logs from the `OTLP/JSON` log lines.
An example `OTLP/JSON` is the following:

```json
{
  "resourceLogs": [
    {
      "resource": {
        "attributes": [
          {
            "key": "deployment.environment.name",
            "value": {
              "stringValue": "staging"
            }
          },
          {
            "key": "service.instance.id",
            "value": {
              "stringValue": "6ad88e10-238c-4fb7-bf97-38df19053366"
            }
          },
          {
            "key": "service.name",
            "value": {
              "stringValue": "checkout"
            }
          },
          {
            "key": "service.namespace",
            "value": {
              "stringValue": "shop"
            }
          },
          {
            "key": "service.version",
            "value": {
              "stringValue": "1.1"
            }
          }
        ]
      },
      "scopeLogs": [
        {
          "scope": {
            "name": "com.mycompany.checkout.CheckoutServiceServer$CheckoutServiceImpl",
            "attributes": []
          },
          "logRecords": [
            {
              "timeUnixNano": "1730435085776869000",
              "observedTimeUnixNano": "1730435085776944000",
              "severityNumber": 9,
              "severityText": "INFO",
              "body": {
                "stringValue": "Order order-12035 successfully placed"
              },
              "attributes": [
                {
                  "key": "customerId",
                  "value": {
                    "stringValue": "customer-49"
                  }
                },
                {
                  "key": "thread.id",
                  "value": {
                    "intValue": "44"
                  }
                },
                {
                  "key": "thread.name",
                  "value": {
                    "stringValue": "grpc-default-executor-1"
                  }
                }
              ],
              "flags": 1,
              "traceId": "42de1f0dd124e27619a9f3c10bccac1c",
              "spanId": "270984d03e94bb8b"
            }
          ]
        }
      ],
      "schemaUrl": "https://opentelemetry.io/schemas/1.24.0"
    }
  ]
}
```

The following configuration can be used to properly parse and extract the `OTLP` content from these log lines:

```yaml
receivers:
  filelog/otlpjson:
    include: [/path/to/myapp/otlpjson.log]

connectors:
  otlpjson:

service:
  pipelines:
    logs/otlpjson:
      receivers: [filelog/otlpjson]
      processors: []
      exporters: [otlpjson]
    logs:
      receivers: [otlp, otlpjson]
      processors: []
      exporters: [debug]
...
```

## Parsing apache logs

Parsing logs of a known technology, like Apache logs, can be achieved through filelog receiver's operators.
Specifically, the
[`regex_parser`](https://github.com/open-telemetry/opentelemetry-collector-contrib/blob/v0.123.0/pkg/stanza/docs/operators/regex_parser.md)
operator can be used in order to parse the logs that follow the specific pattern:

```yaml
receivers:
  # Receiver to read the Apache logs
  filelog:
    include:
    - /var/log/*apache*.log
    start_at: end
    operators:
    # Operator to parse the Apache logs
    # This operator uses a regex to parse the logs
    - id: apache-logs
      type: regex_parser
      regex: ^(?P<source_ip>\d+\.\d+.\d+\.\d+)\s+-\s+-\s+\[(?P<timestamp_log>\d+/\w+/\d+:\d+:\d+:\d+\s+\+\d+)\]\s"(?P<http_method>\w+)\s+(?P<http_path>.*)\s+(?P<http_version>.*)"\s+(?P<http_code>\d+)\s+(?P<http_size>\d+)$
```

## Customizing logs parsing on Kubernetes

The OpenTelemetry Collector also supports enabling log's collection dynamically for Kubernetes Pods
by defining properly specific Pod's annotations.

Detailed examples can be found in the respective [blog post](https://www.elastic.co/observability-labs/blog/k8s-discovery-with-EDOT-collector)
and the
[Collector's documentation](https://github.com/open-telemetry/opentelemetry-collector-contrib/blob/main/receiver/receivercreator/README.md#supported-logs-annotations).

The collector configuration should enable the
[`k8s_observer`](https://github.com/open-telemetry/opentelemetry-collector-contrib/tree/v0.123.0/extension/observer/k8sobserver)
and the
[`receiver_creator`](https://github.com/open-telemetry/opentelemetry-collector-contrib/tree/v0.123.0/receiver/receivercreator)
properly:

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
    logs:
      receivers: [ receiver_creator/logs]
```

In addition, make sure to remove / comment out any static filelog receiver (or restrict the log file pattern) to avoid log duplication.

Then annotating the pod will enable custom log collection targeted only for this specific Pod.

```yaml
# ...
metadata:
  annotations:
    io.opentelemetry.discovery.logs/enabled: "true"
    io.opentelemetry.discovery.logs/config: |
      operators:
      - id: container-parser
        type: container
      # Check if format is json and route properly
      - id: get-format
        routes:
        - expr: body matches "^\\{"
          output: json-parser
        type: router
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

Targeting a single container's scope is also possible by scoping the annotation using containers' names
like `io.opentelemetry.discovery.logs.my-container/enabled: "true"`.
Visit [Collector's documentation](https://github.com/open-telemetry/opentelemetry-collector-contrib/blob/main/receiver/receivercreator/README.md#supported-logs-annotations)
for additional information.

### Collecting Apache logs using annotations discovery

The following example can be used in order to collect and parse Apache logs by annotating Apache containers:

```yaml
metadata:
  annotations:
    io.opentelemetry.discovery.logs.apache/enabled: "true"
    io.opentelemetry.discovery.logs.apache/config: |
      operators:
        - type: container
          id: container-parser
        - id: apache-logs
          type: regex_parser
          regex: ^(?P<source_ip>\d+\.\d+.\d+\.\d+)\s+-\s+-\s+\[(?P<timestamp_log>\d+/\w+/\d+:\d+:\d+:\d+\s+\+\d+)\]\s"(?P<http_method>\w+)\s+(?P<http_path>.*)\s+(?P<http_version>.*)"\s+(?P<http_code>\d+)\s+(?P<http_size>\d+)$
spec:
    containers:
      - name: apache
      # ...
```

## Using Processors / OTTL for Logs processing

OTTL functions can be used in the transform processor to parse logs of a specific format or logs
that follow a specific pattern. 

### Parsing JSON logs using OTTL

The following
[`transform`](https://github.com/open-telemetry/opentelemetry-collector-contrib/tree/v0.123.0/processor/transformprocessor)
processor can be used to parse logs that come in `JSON` format:

```yaml
processors:
  transform:
    error_mode: ignore
    log_statements:
      - context: log
        statements:
          # Parse body as JSON and merge the resulting map with the cache map, ignoring non-json bodies.
          # cache is a field exposed by OTTL that is a temporary storage place for complex operations.
          - merge_maps(cache, ParseJSON(body), "upsert") where IsMatch(body, "^\\{")
          - set(body,cache["log"]) where cache["log"] != nil
```

### Parsing Apache logs using OTTL

The following configuration can parse Apache access log using OTTL and the transform processor:

```yaml
exporters:
  debug:
    verbosity: detailed
receivers:
  filelog:
    include:
      - /Users/chrismark/otelcol/log/apache.log


processors:
  transform/apache_logs:
    error_mode: ignore
    log_statements:
      - context: log
        statements:
          - 'merge_maps(attributes, ExtractPatterns(body, "^(?P<source_ip>\\d+\\.\\d+.\\d+\\.\\d+)\\s+-\\s+-\\s+\\[(?P<timestamp_log>\\d+/\\w+/\\d+:\\d+:\\d+:\\d+\\s+\\+\\d+)\\]\\s\"(?P<http_method>\\w+)\\s+(?P<http_path>.*)\\s+(?P<http_version>.*)\"\\s+(?P<http_code>\\d+)\\s+(?P<http_size>\\d+)$"), "upsert")'
service:
  pipelines:
    logs:
      receivers: [filelog]
      processors: [transform/apache_logs]
      exporters: [debug]


```

A more detailed example about using OTTL and the transform processor can be found at the
[nginx_ingress_controller_otel](https://github.com/elastic/integrations/blob/main/packages/nginx_ingress_controller_otel/docs/README.md)
integration.
