---
title: Troubleshooting
layout: default
nav_order: 5
parent: EDOT Java
---

# Troubleshooting the EDOT Java Agent

The sections below are in the order you should follow, unless you have already identified the section you need.

This guide assumes you have tested the other components in the route from application+agent to Elastic Observability (eg collector, Elasticsearch, and Kibana) and that the problem has been isolated to the application+agent.

## General

Ensure you have set a service name (eg `-Dotel.service.name=Service1` or environment variable `OTEL_SERVICE_NAME` set to `Service1`) otherwise by default the data (traces, metrics, logs) will be sent to `unknown_service_java` - you may be getting data but it may all be under that service

## Connectivity to endpoint

Check _from_ the host/VM/pod/container/image running the app, that connectivity is available to the collector.

The examples here use a default URL `http://127.0.0.1:4318/, which you should replace with the endpoint you are using:

- OpenTelemetry or EDOT collector without authentication: `curl -i http://127.0.0.1:4318/v1/traces -X POST -d '{}' -H content-type:application/json`
- OpenTelemetry or EDOT collector with API key authentication: `curl -i http://127.0.0.1:4318/v1/traces -X POST -d '{}' -H content-type:application/json -H "Authorization:ApiKey <api_key>"`

The collector should produce output similar to
```
{"partialSuccess":{}}
```

## Is it the agent?

Determine if the issue is related to the agent by

1. Starting the application with no agent and seeing if the issue is not present, but then the issue is again present when restarting with the agent
2. Check end-to-end connectivity without the agent by running one or more of the example apps in https://github.com/elastic/elastic-otel-java/blob/main/examples/troubleshooting/README.md . These use the OpenTelemetry SDK rather than the auto-instrumentation, ie there is no agent present, and create traces, metrics and logs, so provide confirmation that the issue is specific to the agent or can otherwise identify that the issue is something else

## Agent DEBUG

Debug output is enabled with `-Dotel.javaagent.debug=true` or environment variable `OTEL_JAVAAGENT_DEBUG` to `true`. 

Once debug is enabled, look for:
- Errors and exceptions
- For the expected traces or metrics - or lack of them (maybe the [technology isn't instrumented?](https://github.com/open-telemetry/opentelemetry-java-instrumentation/blob/main/docs/supported-libraries.md))


