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
  - id: edot-sdk
---

# Troubleshooting the EDOT Java Agent

Use the information in this section to troubleshoot common problems. As a first step, make sure your stack is compatible with the [supported technologies](./supported-technologies.md) for EDOT Java and the OpenTelemetry SDK.

If you need help and you're an existing Elastic customer with a support contract, create a ticket in the [Elastic Support portal](https://support.elastic.co/customers/s/login/). Other users can post in the [APM discuss forum](https://discuss.elastic.co/c/apm) or [open a GitHub issue](https://github.com/elastic/elastic-otel-node/issues)

## General troubleshooting

Make you have set a service name, for example `-Dotel.service.name=Service1` or the environment variable `OTEL_SERVICE_NAME` set to `Service1`. Otherwise, by default the data will be sent to `unknown_service_java`. You may be getting data but it may all be under that service.

## Connectivity to endpoint

Check from the host, VM, pod, container, or image running the app that connectivity is available to the Collector.

The following examples use a default URL, `http://127.0.0.1:4318/, which you should replace with the endpoint you are using:

- OpenTelemetry or EDOT Collector without authentication: `curl -i http://127.0.0.1:4318/v1/traces -X POST -d '{}' -H content-type:application/json`
- OpenTelemetry or EDOT Collector with API key authentication: `curl -i http://127.0.0.1:4318/v1/traces -X POST -d '{}' -H content-type:application/json -H "Authorization:ApiKey <api_key>"`

The Collector should produce output similar to the following:

```
{"partialSuccess":{}}
```

## Agent troubleshooting

Determine if the issue is related to the agent by following these steps:

1. Start the application with no agent and see if the issue is not present. Observe if the issue is again present when restarting with the agent.
2. Check end-to-end connectivity without the agent by running one or more of the example apps in https://github.com/elastic/elastic-otel-java/blob/main/examples/troubleshooting/README.md . These use the OpenTelemetry SDK rather than the auto-instrumentation. They can confirm that the issue is specific to the agent or can otherwise identify that the issue is something else.

## Agent debug output

Turn on debug output with `-Dotel.javaagent.debug=true` or by setting the `OTEL_JAVAAGENT_DEBUG` environment variable to `true`. That adds noticeable overhead. A lower overhead option is to set the `otel.traces.exporter` JVM property or the `OTEL_TRACES_EXPORTER` environment variable to the value `otlp,logging-otlp`. This will configure the agent to send the traces both to the collector and to also print it to the standardoutput in JSON format.

After debug is activated, look for:

- Errors and exceptions.
- For the expected traces or metrics, or the lack of them. Perhaps the [technology isn't instrumented](https://github.com/open-telemetry/opentelemetry-java-instrumentation/blob/main/docs/supported-libraries.md).

## Access or modification of application code

The agent modifies the Java application binaries in bytecode form and does not requires original code nor recompiling or re-packaging the application.

## How to deactivate the agent

There are two ways to deactivate the instrumentation agent:

- Remove the `-javaagent:` JVM argument.
- Set the `OTEL_JAVAAGENT_ENABLED` environment variable or the `otel.javaagent.enabled` Java system property to `false`.

In both cases you need to restart the JVM.

## Partial activation or deactivation of the agent

You can partially deactivate the agent, or only selectively activate a limited set of instrumentations by following instructions in the [upstream documentation](https://opentelemetry.io/docs/zero-code/java/agent/disable/).

## Check if EDOT is attached to a running JVM

There are a few ways you can detect if the agent has been attached to a JVM:

- In JVM logs, agent startup log message might be included.
- In JVM arguments, Run `ps -ef|grep javaagent`.
- In environment variables, for example `JAVA_TOOL_OPTIONS`. Check by inspecting the output of `export|grep javaagent`.

## Identify the version of EDOT agent

When the agent starts, a log message in the standard error provides the agent version: 

```
INFO io.opentelemetry.javaagent.tooling.VersionLogger - opentelemetry-javaagent - version: 1.2.3
```

In addition, the `-javaagent:` JVM argument can provide the path to the agent file name, which might also contain
the agent version, for example `-javaagent:elastic-otel-javaagent-1.2.3.jar`.

Executing the agent jar as an application with `java -jar elastic-otel-javaagent.jar` provides the agent version on standard output, which could be relevant to use when the jar file has been renamed.

Also, you can inspect the `Implementation-Version` entry in `META-INF/MANIFEST.MF` file of the agent jar, for example with `unzip -p elastic-otel-javaagent.jar META-INF/MANIFEST.MF|grep 'Implementation-Version'`.

## Versions of the OpenTelemetry upstream dependencies

Because EDOT Java is a distribution of [OpenTelemetry Java instrumentation](https://github.com/open-telemetry/opentelemetry-java-instrumentation), it includes the following dependencies:

- [OpenTelemetry Java Instrumentation](https://github.com/open-telemetry/opentelemetry-java-instrumentation)
- [OpenTelemetry Java SDK](https://github.com/open-telemetry/opentelemetry-java)
- [Semantic Conventions Java mappings](https://github.com/open-telemetry/semantic-conventions-java)
- [OpenTelemetry Java Contrib](https://github.com/open-telemetry/opentelemetry-java-contrib)

The versions of those included in EDOT are usually aligned with the OpenTelemetry Java Instrumentation. For reference, check the [release notes](https://github.com/elastic/elastic-otel-java/releases) details of versions included in each release.

## When and how to update EDOT

The general recommendation is to update EDOT agent to the latest version when possible to benefit from:

- Bug fixes and technical improvements.
- Support of new features and instrumentation.
- Evolution of semantic conventions.
- Frequent and regular updates usually makes reviewing and handling changes easier.

Updating to the latest EDOT version involves reviewing changes of the included dependencies:

- [OpenTelemetry Java Instrumentation](https://github.com/open-telemetry/opentelemetry-java-instrumentation)
- [OpenTelemetry Java SDK](https://github.com/open-telemetry/opentelemetry-java)
- [Semantic Conventions Java mappings](https://github.com/open-telemetry/semantic-conventions-java)
- [OpenTelemetry Java Contrib](https://github.com/open-telemetry/opentelemetry-java-contrib)

To review each of those individually, you can use the [EDOT release notes](https://github.com/elastic/elastic-otel-java/releases) for links to the respective versions of each component.

### OpenTelemetry API/SDK update

To implement manual instrumentation, some applications use the OpenTelemetry API and/or SDK which allows them to capture custom spans, metrics or even send data without any instrumentation agent.

Updates of the OpenTelemetry API/SDK in the application and the EDOT Java agent can be done independently.

- EDOT Java is backward-compatible with all previous versions of OpenTelemetry API/SDK.
- Using a more recent version of API/SDK than the one in EDOT should usually work without problem, however to ensure maximum compatibility keeping OpenTelemetry API/SDK version ≤ EDOT OpenTelemetry API/SDK version is recommended.

### How to update

Updating EDOT Java agent is done by replacing the agent binary `.jar` that has been [added during setup](./setup/index.md).


