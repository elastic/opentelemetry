---
navigation_title: Automatic instrumentation
description: Instrument Android applications automatically using EDOT Android.
applies_to:
  stack:
  serverless:
    observability:
products:
  - id: cloud-serverless
  - id: observability
  - id: edot-sdk
mapped_pages:
  - https://www.elastic.co/guide/en/apm/agent/android/current/supported-technologies.html
---

# Automatic instrumentation

The SDK can automatically generate telemetry on your behalf. This allows you to get telemetry data for supported targets without having to write [manual instrumentation](manual-instrumentation.md).

## Installation

The first step is to install the automatic instrumentations you'd like to use. Specific targets are supported for automatic instrumentation, each with its own Gradle plugin for installation. 

To install a supported automatic instrumentation, follow these steps:

1. Choose a [supported instrumentation](#supported-instrumentations).
2. Add its Gradle plugin to your project in the same location where the [agent](getting-started.md#gradle-setup) is added.
3. [Initialize the agent](getting-started.md#agent-setup) the same way you would without using automatic instrumentation.

Automatic instrumentations will get installed during the SDK initialization.

## Compilation behavior

Some automatic instrumentations perform bytecode instrumentation, where your application's code, including code from the libraries it uses, is modified at compile-time. This automates code changes that you would otherwise need to make manually.

Bytecode instrumentation is a common technique which may already be used in your project for use cases such as [code optimization](https://developer.android.com/build/shrink-code#optimization) through R8. While useful, bytecode instrumentation can make compilation take longer to complete. Because of this, the agent provides [a way to exclude](#automatic-instrumentation-configuration) specific build types in your app from byte code changes.

## Configuration [automatic-instrumentation-configuration]

For large projects, you can avoid the added compilation time caused by the [compilation behavior](#compilation-behavior) by excluding build types that don't need the functionality. 

Use the following configuration to exclude build types:

```kotlin
// Your app's build.gradle.kts file
plugins {
    // ...
    id("co.elastic.otel.android.agent")
}

// ...

elasticAgent {
    bytecodeInstrumentation.disableForBuildTypes.set(listOf("debug")) // <1>
}
```

1. By default, the `disableForBuildTypes` list is empty. Add any [build type](https://developer.android.com/build/build-variants#build-types) names for which you want to turn off byte code instrumentation.

:::{note}
Disabling byte code instrumentation will cause the [automatic instrumentations](#supported-instrumentations) that need it to fail for the affected build type. This only affects the agent's ability to automatically collect telemetry.
:::

## Supported instrumentations

The following automatic instrumentations are supported.

### OkHttp

Creates spans for outgoing HTTP requests that are made using the [OkHttp](https://square.github.io/okhttp/) library. This also includes tools that rely on OkHttp to work, such as [Retrofit](https://square.github.io/retrofit/).

#### Gradle plugin

```kotlin
plugins {
    id("co.elastic.otel.android.instrumentation.okhttp") version "[latest_version]" // <1>
}
```

1. You can find the latest version [here](https://plugins.gradle.org/plugin/co.elastic.otel.android.instrumentation.okhttp).
