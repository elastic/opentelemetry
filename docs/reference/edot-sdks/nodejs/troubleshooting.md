---
navigation_title: Troubleshooting
description: Troubleshooting guide for the Elastic Distribution of OpenTelemetry Node.js (EDOT Node.js).
applies_to:
  stack:
  serverless:
    observability:
products:
  - id: cloud-serverless
  - id: observability
  - id: edot-nodejs
---

# Troubleshooting the EDOT Node.js SDK

Use the information on this page to troubleshoot issues using EDOT Node.js.

If you need help and you're an existing Elastic customer with a support contract, please create a ticket in the [Elastic Support portal](https://support.elastic.co/customers/s/login/). Other users can post in the [APM discuss forum](https://discuss.elastic.co/c/apm) or [open a GitHub issue](https://github.com/elastic/elastic-otel-node/issues).


## Is your app compatible with the SDK's supported technologies?

First, review the [supported technologies](./supported-technologies.md) to ensure your application is supported by the SDK. Are you using a Node.js version that the SDK supports? Are the versions of your dependencies in the [supported version range](./supported-technologies.md#instrumentations) to be instrumented?


## Have you set a service name?

Ensure you have set a service name (via `OTEL_SERVICE_NAME=my-service`, or via `OTEL_RESOURCE_ATTRIBUTES=service.name=my-service`) otherwise by default the data (traces, metrics, logs) will be sent to the `unknown_service:node` service -- you may be getting data but it may all be under that service.


## Can the application reach the OTLP endpoint?

Check *from* the host/VM/pod/container running your application, that connectivity is available to the collector.
Run:

```bash
curl -i $ELASTIC_OTLP_ENDPOINT \
    -X POST -d "{}" -H content-type:application/json \
    -H "Authorization: ApiKey $ELASTIC_API_KEY"
```

For example, if you [configured](./configuration.md#basic-configuration) EDOT Node.js with:

```bash
export OTEL_EXPORTER_OTLP_ENDPOINT="https://my-deployment-abc123.ingest.us-west-2.aws.elastic.cloud"
export OTEL_EXPORTER_OTLP_HEADERS="Authorization=ApiKey Zm9vO...mJhcg=="
...
```

then you would run:

```bash
curl -i https://my-deployment-abc123.ingest.us-west-2.aws.elastic.cloud \
    -X POST -d "{}" -H content-type:application/json \
    -H "Authorization: ApiKey Zm9vO...mJhcg=="
```

If that works correctly, you should expect to see output similar to:

```
HTTP/1.1 200 OK
Content-Type: application/json
Date: Thu, 27 Mar 2025 23:07:09 GMT
Content-Length: 21

{"partialSuccess":{}}
```


## Is the SDK causing an application issue?

If your application has an issue, but you are not sure if the EDOT Node.js SDK
could be the cause, try disabling the SDK.

You can exclude the SDK by not starting it with your application:

```bash
node my-app.js   # instead of 'node --import @elastic/opentelemetry-node my-app.js'
```

or by setting the `OTEL_SDK_DISABLED` environment variable:

```bash
export OTEL_SDK_DISABLED=true
node --import @elastic/opentelemetry-node my-app.js
```


## SDK diagnostic logs [sdk-diagnostic-logs]

Next, enable verbose diagnostic / debug logging from EDOT Node.js:

1. Set the `OTEL_LOG_LEVEL` environment varible to `verbose`.
2. Restart your application, and reproduce the issue. (Note: If the issue is about not seeing telemetry that you expect to see, be sure to exercise your application -- e.g. send it HTTP requests -- so that telemetry data is generated.)
3. Gather *the full verbose log from application start* until after the issue was reproduced.

The start of the diagnostic log will look something like this:

```
% OTEL_LOG_LEVEL=verbose node --import @elastic/opentelemetry-node my-app.js
{"name":"elastic-otel-node","level":10,"msg":"import.mjs: registering module hook","time":"2025-03-27T23:29:12.075Z"}
{"name":"elastic-otel-node","level":10,"msg":"ElasticNodeSDK opts: {}","time":"2025-03-27T23:29:12.392Z"}
{"name":"elastic-otel-node","level":20,"msg":"@opentelemetry/api: Registered a global for diag v1.9.0.","time":"2025-03-27T23:29:12.392Z"}
{"name":"elastic-otel-node","level":20,"msg":"Enabling instrumentation \"@elastic/opentelemetry-instrumentation-openai\"","time":"2025-03-27T23:29:12.393Z"}
{"name":"elastic-otel-node","level":20,"msg":"Enabling instrumentation \"@opentelemetry/instrumentation-amqplib\"","time":"2025-03-27T23:29:12.394Z"}
{"name":"elastic-otel-node","level":20,"msg":"Enabling instrumentation \"@opentelemetry/instrumentation-aws-sdk\"","time":"2025-03-27T23:29:12.395Z"}
...
{"name":"elastic-otel-node","level":10,"msg":"Metrics exporter protocol set to http/protobuf","time":"2025-03-27T23:29:12.408Z"}
{"name":"elastic-otel-node","level":30,"preamble":true,"distroVersion":"0.7.0","env":{"os":"darwin 24.3.0","arch":"arm64","runtime":"Node.js v18.20.4"},"msg":"start Elastic Distribution of OpenTelemetry Node.js","time":"2025-03-27T23:29:12.409Z"}
...
```

Look for warnings (`"level":40`) or errors (`"level":50`) in the log output that might indicate an issue.
(This log output will be invaluable in Elastic support requests or for developers in support requests.)


## Getting support

If you are stuck, you can ask for help.  If you're an existing Elastic customer with a support contract, please create a ticket in the [Elastic Support portal](https://support.elastic.co/customers/s/login/). Other users can post in the [APM discuss forum](https://discuss.elastic.co/c/apm) or [open a GitHub issue](https://github.com/elastic/elastic-otel-node/issues).

When opening an issue:

1. By far the best way to help get a quick resolution of your issue is if you can provide a small **reproduction** case. For example, create a small GitHub repository that reproduces the same problem you are seeing. We understand that creating a small reproduction is not always possible.
2. **Describe your application/service/system architecture** as accurately as possible.
3. Include as much **[diagnostic log output](#sdk-diagnostic-logs)** as possible.

:::warning
Though an effort is made to avoid it, verbose/debug diagnostic logs **can include sensitive information**. Therefore it is **not** recommended that the full log is included in public forums or GitHub issues. (This is less of a concern for private Elastic customer support.)
:::

## How to disable the SDK?

Set the `OTEL_SDK_DISABLED` environment variable to `true`, and restart your application.

## How to disable an instrumentation?

Set the [`OTEL_NODE_DISABLED_INSTRUMENTATIONS`](./configuration.md#otel_node_disabledenabled_instrumentations-details) environment variable.

For example, to disable `@opentelemetry/instrumentation-net` and `@opentelemetry/instrumentation-dns`:

```bash
export OTEL_NODE_DISABLED_INSTRUMENTATIONS=dns,net
...
node --import @elastic/opentelemetry-node my-app.js
```

## How to tell if EDOT Node.js is running?

Look for "start Elastic Distribution of OpenTelemetry Node.js" in the application log.

As it is starting, EDOT Node.js always logs (at the "info" level) a preamble to indicate that it has started. For example, it looks like this:

```json
{"name":"elastic-otel-node","level":30,"preamble":true,"distroVersion":"0.7.0","env":{"os":"darwin 24.3.0","arch":"arm64","runtime":"Node.js v18.20.4"},"msg":"start Elastic Distribution of OpenTelemetry Node.js","time":"2025-03-27T22:14:08.288Z"}
...
```

The `distroVersion` field also indicates which version of EDOT Node.js is being used.


