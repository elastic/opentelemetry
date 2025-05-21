---
navigation_title: Runtime attach Setup
description: Guide on instrumenting Java applications using EDOT Java runtime attach.
applies_to:
  stack:
  serverless:
    observability:
products:
  - id: cloud-serverless
  - id: observability
  - id: edot-sdk
---

# Instrumenting Java applications with EDOT Java runtime attach

% TODO do we have a global definition of what "tech preview" means that we could link to ?

:::{warning}
This feature is currently in *tech preview*.
:::

Runtime attach allows including the EDOT instrumentation agent in the application binary, doing so provides some setup [features](#features)
and also comes with [limitations](#limitations) that must be reviewed beforehand.

Adding runtime attach to an application is a 3-step process:
- [add runtime attach to the application dependencies](#adding-runtime-attach-to-application-dependencies)
- [minor code modification of the application main method](#minor-code-modification)
- package and re-deploy the application

## Features

- Allows deploying the agent when access to JVM arguments or configuration is not possible, for example, with some managed services.
- Agent deployment and update cycle can be controlled by the application development team, without needing modifications to the run environment.

## Limitations

- It can't be used with multiple applications that share a JVM, for example, with web-applications and application servers, in this case only the `-javaagent` setup option is supported
- Agent update is tied to the application development and deployment lifecycle, it is not possible to update application and agent independently.
- It requires minor modification of the application main entry point and adding one extra dependency.
- Agent can only be attached at application start, it can't be used to attach later during application runtime.
- Recent JVMs issue [warnings in standard error](#jvm-runtime-attach-warnings) and the feature might require explicit opt-in with JVM settings in the future
 
## Adding runtime attach to application dependencies

% TODO: can we replace ${VERSION} with the actual latest published version for an easier copy/paste experience ? 

::::{tab-set}

:::{tab-item} Maven
```xml
<dependency>
  <groupId>co.elastic.otel</groupId>
  <artifactId>elastic-otel-runtime-attach</artifactId>
  <version>${VERSION}</version>
</dependency>
```
:::

:::{tab-item} Gradle
```kotlin
implementation("co.elastic.otel:elastic-otel-runtime-attach:${VERSION}")
```
:::

::::

## Minor code modification

A single call to `RuntimeAttach.attachJavaagentToCurrentJvm()` must be added early at the start of the `main` method body. Here is an example of a simple spring-boot application:

```java
@SpringBootApplication
public class MyApplication {

    public static void main(String[] args) {
        RuntimeAttach.attachJavaagentToCurrentJvm();
        SpringApplication.run(MyApplication.class, args);
    }
}
```

## JVM Runtime attach warnings

With recent JVMs, the following warning may be issued in the process standard error output:

```
WARNING: A Java agent has been loaded dynamically (/tmp/otel-agent6227828786286549290/agent.jar)
WARNING: If a serviceability tool is in use, please run with -XX:+EnableDynamicAgentLoading to hide this warning
WARNING: If a serviceability tool is not in use, please run with -Djdk.instrument.traceUsage for more information
WARNING: Dynamic loading of agents will be disallowed by default in a future release
```

This message indicates that the dynamic agent attachment will be disabled by in the future, adding `-XX:+EnableDynamicAgentLoading` to the JVM arguments (or `JAVA_TOOL_OPTIONS` env variable) will allow to get rid of it.

It is also safe to ignore it until the runtime attach feature is disabled by default in a newer JVM version and the JVM version used to run the application is updated to it.
