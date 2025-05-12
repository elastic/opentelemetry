---
navigation_title: Troubleshooting
description: Troubleshooting guide for the Elastic Distribution of OpenTelemetry (EDOT) Java Agent, covering connectivity, agent identification, and debugging.
applies_to:
  stack:
  serverless:
    observability:
products:
  - id: cloud-serverless
  - id: observability
  - id: edot-java
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

## Does agent requires access to or modification of application code ?

No, the agent modifies the Java application binaries in bytecode form and does not requires original code nor
recompiling or re-packaging the application.

## How to disable the agent ?

There are two ways to disable the instrumentation agent:

- remove `-javaagent:` JVM argument
- set `OTEL_JAVAAGENT_ENABLED` environment variable or `otel.javaagent.enabled` Java system property to `false`

In both cases you need to restart the JVM.

## How to partially enable or disable the agent ?

It is possible to partially disable the agent, or to only selectively enable a limited set of instrumentations
by following instructions in the [upstream documentation](https://opentelemetry.io/docs/zero-code/java/agent/disable/).

## How to know if EDOT is attached to a running JVM ?

There are a few ways we can detect if the agent has been attached to a JVM
- in JVM logs, agent startup log message (see [below](#how-to-identify-the-version-of-edot-agent-)) might be included
- in JVM arguments `ps -ef|grep javaagent`
- in environment variables, for example `JAVA_TOOL_OPTIONS`, for example by inspecting the output of `export|grep javaagent`

## How to identify the version of EDOT agent ?

When the agent starts, a log message in the standard error provides the agent version: 
```
INFO io.opentelemetry.javaagent.tooling.VersionLogger - opentelemetry-javaagent - version: 1.2.3
```

In addition, the `-javaagent:` JVM argument can provide the path to the agent file name, which _might_ also contain
the agent version, for example `-javaagent:elastic-otel-javaagent-1.2.3.jar`.

Executing the agent jar as an application with `java -jar elastic-otel-javaagent.jar` will provide the agent version on standard output,
which could be relevant to use when the jar file has been renamed.

Also, it is also possible to inspect the `Implementation-Version` entry in `META-INF/MANIFEST.MF` file of the agent jar,
for example with `unzip -p elastic-otel-javaagent.jar META-INF/MANIFEST.MF|grep 'Implementation-Version'`

## What are the versions of the OpenTelemetry upstream dependencies ?

Because EDOT Java is a distribution of [OpenTelemetry Java instrumentation](https://github.com/open-telemetry/opentelemetry-java-instrumentation),
it includes the following dependencies:

- [OpenTelemetry Java Instrumentation](https://github.com/open-telemetry/opentelemetry-java-instrumentation)
- [OpenTelemetry Java SDK](https://github.com/open-telemetry/opentelemetry-java)
- [Semantic Conventions Java mappings](https://github.com/open-telemetry/semantic-conventions-java)
- [OpenTelemetry Java Contrib](https://github.com/open-telemetry/opentelemetry-java-contrib)

The versions of those included in EDOT is usually aligned with the OpenTelemetry Java Instrumentation, for reference we
provide in the [release notes](https://github.com/elastic/elastic-otel-java/releases) details of versions included in each release.

## When and how to update EDOT

The general recommendation is to update EDOT agent to the latest version when possible to benefit from:
- bug fixes and technical improvements
- support of new features and instrumentation
- evolution of semantic conventions
- frequent and regular updates usually makes reviewing and handling changes easier.

Updating to the latest EDOT version involves reviewing changes of the included dependencies:

- [OpenTelemetry Java Instrumentation](https://github.com/open-telemetry/opentelemetry-java-instrumentation)
- [OpenTelemetry Java SDK](https://github.com/open-telemetry/opentelemetry-java)
- [Semantic Conventions Java mappings](https://github.com/open-telemetry/semantic-conventions-java)
- [OpenTelemetry Java Contrib](https://github.com/open-telemetry/opentelemetry-java-contrib)

In order to review each of those individually, you can use the [EDOT release notes](https://github.com/elastic/elastic-otel-java/releases) 
for links to the respective versions of each component.

### OpenTelemetry API/SDK update

In order to implement manual instrumentation, some applications use the OpenTelemetry API and/or SDK which allows them
to capture custom spans, metrics or even send data without any instrumentation agent.

Updates of the OpenTelemetry API/SDK in the application and the EDOT Java agent can be done independently.
- EDOT Java is backward-compatible with all previous versions of OpenTelemetry API/SDK
- Using a more recent version of API/SDK than the one in EDOT should usually work without problem, however to ensure maximum compatibility keeping OpenTelemetry API/SDK version ≤ EDOT OpenTelemetry API/SDK version is recommended.

### How to update

Updating EDOT Java agent is done by replacing the agent binary `.jar` that has been [added during setup](./setup/index.md).


