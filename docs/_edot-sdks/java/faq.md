---
title: Frequently Asked Questions
layout: default
nav_order: 7
parent: EDOT Java
---

# Frequently Asked Questions on EDOT Java

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
the agent version, for example `-javaagent:elastic-otel-javaagent-1.2.3.jar`

When the original agent jar file has been renamed, it is still possible to inspect the `Implementation-Version` entry in `META-INF/MANIFEST.MF` file of the agent jar,
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

Updating EDOT Java agent is done by replacing the agent binary `.jar` that has been [added during setup](./setup/).
