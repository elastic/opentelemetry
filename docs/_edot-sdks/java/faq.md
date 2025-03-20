---
title: Frequently Asked Questions
layout: default
nav_order: 7
parent: EDOT Java
---

# Frequently Asked Questions on EDOT Java

## Does agent requires access to or modification of application code ?

TODO

## How to disable the agent ?

TODO

- remove `-javaagent:` JVM argument
- use configuration

## How to partially disable the agent

TODO

## How to know if EDOT is attached to a running JVM ?

TODO
- check JVM logs, agent startup log message might be included
- check JVM arguments `ps -ef|grep javaagent`

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