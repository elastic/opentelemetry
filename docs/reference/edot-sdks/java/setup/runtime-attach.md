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

# Instrumenting Java applications using the EDOT Java runtime attach

:::{warning}
This feature is currently in *tech preview*.
:::

Runtime attach includes the EDOT instrumentation agent in the application binary. This allows deploying the agent when access to JVM arguments or configuration is not possible, for example, with some managed services. The application development team can control the agent deployment and update cycle without having to modify the execution environment. Runtime attach only requires a minor modification of the application main entry point and one additional dependency.

## Limitations

The following limitations apply:

- Runtime attach can't be used with multiple applications that share a JVM, for example, with web-applications and application servers. In this case, only the `-javaagent` setup option is supported.
- Agent update is tied to the application development and deployment lifecycle. You can't update application and agent independently.
- Agent can only be attached at application start; it can't be used to attach later during application runtime.
- Recent JVMs issue [warnings in standard error](#jvm-runtime-attach-warnings) and the feature might require explicit opt-in with JVM settings in the future.

## Instrument a Java app

Follow these steps to instrument your Java application using runtime attach.

::::::{stepper}

:::::{step} Add runtime attach to application dependencies

::::{tab-set}

:::{tab-item} Maven
```xml
<dependency>
  <groupId>co.elastic.otel</groupId>
  <artifactId>elastic-otel-runtime-attach</artifactId>
  <version>1.4.1</version>
</dependency>
```
:::

:::{tab-item} Gradle
```kotlin
implementation("co.elastic.otel:elastic-otel-runtime-attach:1.4.1")
```
:::

::::
:::::

:::::{step} Modify the main method

Add a single call to `RuntimeAttach.attachJavaagentToCurrentJvm()` at the start of the `main` method body. Here is an example of a simple spring-boot application:

```java
@SpringBootApplication
public class MyApplication {

    public static void main(String[] args) {
        RuntimeAttach.attachJavaagentToCurrentJvm();
        SpringApplication.run(MyApplication.class, args);
    }
}
```
:::::

:::::{step} Package and redeploy the application

After you've added the new dependency and modified the `main` method, package and redeploy your application.

:::::
::::::

## JVM runtime attach warnings

The following warning might appear in the process standard error output:

```
WARNING: A Java agent has been loaded dynamically (/tmp/otel-agent6227828786286549290/agent.jar)
WARNING: If a serviceability tool is in use, please run with -XX:+EnableDynamicAgentLoading to hide this warning
WARNING: If a serviceability tool is not in use, please run with -Djdk.instrument.traceUsage for more information
WARNING: Dynamic loading of agents will be disallowed by default in a future release
```

This message indicates that the dynamic agent attachment will be disabled by in the future. Add `-XX:+EnableDynamicAgentLoading` to the JVM arguments, or to the `JAVA_TOOL_OPTIONS` environment variable, to silence it.

The runtime attach feature will be turned off by default in future JVM versions. Until then, you can ignore the warning.
