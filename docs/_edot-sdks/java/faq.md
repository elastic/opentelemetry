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

## What are the versions of the OpenTelemetry upstream dependencies

TODO
- SDK
- Instrumentation
- Semantic conventions

link to release notes

## Updating EDOT

- general recommendation on updating to latest
- how to update

- updating EDOT does not require to update OpenTelemetry API/SDK in the application

## Is the agent compatible with other instrumentation agents ?

TODO

## How to instrument un-supported libraries/frameworks

TODO

- use configuration (but limited)
- use otel API with code modification
- write an instrumentation extension
- contribute instrumentation to upstream