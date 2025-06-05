---
navigation_title: Get started
description: Set up the Elastic Distribution of OpenTelemetry Android (EDOT Android) to send data to Elastic.
applies_to:
  stack:
  serverless:
    observability:
products:
  - id: cloud-serverless
  - id: observability
  - id: edot-sdk
mapped_pages:
  - https://www.elastic.co/guide/en/apm/agent/android/current/setup.html
---

# Get started with EDOT Android

Set up the Elastic Distribution of OpenTelemetry Android (EDOT Android) in your app and explore your app's data in {{kib}}.

## Requirements

| Requirement                                       | Minimum version                                                                                           |
|---------------------------------------------------|-----------------------------------------------------------------------------------------------------------|
| [{{stack}}](https://www.elastic.co/elastic-stack) | 8.18                                                                                                      |
| Android Gradle plugin                             | 7.4.0                                                                                                     |
| Android API level                                 | 26 (or 21 with [desugaring](https://developer.android.com/studio/write/java8-support#library-desugaring)) |

:::{important}
If your application's [minSdk](https://developer.android.com/studio/publish/versioning#minsdk) value is lower than 26, you must add [Java 8 desugaring support](https://developer.android.com/studio/write/java8-support#library-desugaring). Refer to the [FAQ](troubleshooting.md#why-desugaring) for more information.
:::

## Gradle setup

Add the [Elastic OTel Agent plugin](https://plugins.gradle.org/plugin/co.elastic.otel.android.agent) to your application’s `build.gradle[.kts]` file:

```kotlin
plugins {
    id("com.android.application")
    id("co.elastic.otel.android.agent") version "[latest_version]" // <1>
}
```

1. You can find the latest version in [Gradle](https://plugins.gradle.org/plugin/co.elastic.otel.android.agent).

## Agent setup

After you've configured Gradle, initialize the agent within your app's code:

```kotlin
val agent = ElasticApmAgent.builder(application) // <1>
    .setServiceName("My app name") // <2>
    .setExportUrl("http://10.0.2.2:4318") // <3>
    .setExportAuthentication(Authentication.ApiKey("my-api-key")) // <4>
    .build()
```

1. Your [Application](https://developer.android.com/reference/android/app/Application) object. [Get your application object](#get-application).
2. In OpenTelemetry, _service_ means _an entity that produces telemetry_, so this is where your application name should go. Refer to [Troubleshooting](troubleshooting.md#why-service).
3. This is the Elastic endpoint where all your telemetry will be exported. [Get your Elastic endpoint](#get-export-endpoint).
4. Use an API key to connect the agent to the {{stack}}. [Create an API key](#create-api-key).

:::{tip}
If you'd like to provide these values from outside of your code, using an environment variable or a properties file for example, refer to [Provide config values outside of your code](configuration.md#provide-config-values-from-outside-of-your-code).
:::


### Get your Android application instance [get-application]

Your [Application](https://developer.android.com/reference/android/app/Application) instance is needed to initialize the agent. There are a couple of ways you can get yours.

#### From within your custom Application implementation (Recommended)

The agent should get initialized as soon as your application is launched to make sure that it can start collecting telemetry from the very beginning.

An ideal place to do so is from within your own custom [Application.onCreate](https://developer.android.com/reference/android/app/Application#onCreate()) method implementation, as shown in the following snippet:

```kotlin
package my.app

class MyApp : Application() {
    override fun onCreate() {
        super.onCreate()
        val agent = ElasticApmAgent.builder(this) // <1>
            //...
            .build()
    }
}
```
1. `this` is your application.

:::{important}
You must register your custom application in your `AndroidManifest.xml` file, like so:

```xml
<?xml version="1.0" encoding="utf-8"?>
<manifest xmlns:android="http://schemas.android.com/apk/res/android">
    <application
        android:name="my.app.MyApp"
        ...
    </application>
</manifest>
```
:::

#### From an Activity

You can get your application from an [Activity](https://developer.android.com/reference/android/app/Activity) by calling its [getApplication()](https://developer.android.com/reference/android/app/Activity#getApplication()) method.

#### From a Fragment

From a [Fragment](https://developer.android.com/reference/androidx/fragment/app/Fragment.html) instance, you can get the [Activity](https://developer.android.com/reference/android/app/Activity) that it is associated to by calling its [requireActivity()](https://developer.android.com/reference/androidx/fragment/app/Fragment.html#requireActivity()) method. After you get the Activity object, you can get your application from it as [explained above](#from-an-activity).

### Get your {{stack}} export endpoint [get-export-endpoint]

The export endpoint is where your app's telemetry is sent. The endpoint is required to initialize the agent. The way to find the endpoint in your {{stack}} depends on the type of deployment you use.

#### Serverless deployments

On a [Serverless deployment](https://www.elastic.co/guide/en/serverless/current/intro.html), follow these steps:

1. Open {{kib}} and find **Add data** in the main menu. Alternatively, you can use the [global search field](docs-content://explore-analyze/find-and-organize/find-apps-and-objects.md) and search for `Observability Onboarding`.
2. Select **Application**, **OpenTelemetry**.
3. Select the **OpenTelemetry** tab, followed by **Managed OTLP Endpoint** under **Configure the OpenTelemetry SDK**.

Your export endpoint URL is the value for the `OTEL_EXPORTER_OTLP_ENDPOINT` configuration setting.

#### Cloud hosted and self-managed deployments

For Elastic Cloud Hosted (ECH) and self-managed deployments, the export endpoint, also known as [EDOT Collector](../../edot-collector/index.md), is not available out of the box at the moment. You can still create your own service by following [creating and configuring a standalone EDOT Collector](../../edot-collector/config/default-config-standalone.md).

### Create an API key [create-api-key]

API keys are the recommended way of authenticating the agent with your {{stack}}. There's a couple of ways you can create one.

#### Use {{kib}}'s Applications UI

Follow [this quick guide](docs-content://solutions/observability/apm/api-keys.md#apm-create-an-api-key) and leave all the settings with their default values.

#### Use REST APIs

Follow [this guide](https://www.elastic.co/docs/api/doc/kibana/operation/operation-createagentkey) to create an API Key with a set of privileges that are scoped for the APM Agent use case only.

## Start sending telemetry

With the SDK fully initialized, you can start sending telemetry to your {{stack}}.

### Generate telemetry

The following snippet shows how to generate telemetry through [manual instrumentation](manual-instrumentation.md):

```kotlin
val agent = ElasticApmAgent.builder(application)
    .setServiceName("My app name")
    //...
    .build()


agent.span("My Span") {
    Thread.sleep(500) // <1>
    agent.span("My nested Span") { // <2>
        Thread.sleep(500)
    }
}
```
1. Simulates some code execution for which we want to measure the time it takes to complete.
2. Demonstrates what span hierarchies look like in {{kib}}.

### Visualize telemetry

After your app has sent telemetry data, either [manually](manual-instrumentation.md) or [automatically](automatic-instrumentation.md), view it in {{kib}} by navigating to **Applications**, **Service Inventory**, or by searching for `Service Inventory` in the [global search field](docs-content://explore-analyze/find-and-organize/find-apps-and-objects.md). You should find your application listed there.

:::{image} images/span-visualization/1.png
:alt: Services
:width: 350px
:::

When you open it, go to the **Transactions** tab, where you should see your app's "outermost" spans listed.

:::{image} images/span-visualization/2.png
:alt: Transactions tab
:width: 350px
:::

After clicking on the span, you should see it in detail.

:::{image} images/span-visualization/3.png
:alt: Trace sample
:width: 350px
:::
