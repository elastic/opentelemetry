---
mapped_pages:
  - https://www.elastic.co/guide/en/apm/agent/android/current/faq.html
---

# Troubleshooting

## General

The agent creates logs that enable you to see what it is working on and what might have failed at some point. You can find those in [logcat](https://developer.android.com/studio/debug/logcat), filtered by the tag `ELASTIC_AGENT`.

For more information about the agent's internal logs, as well as how to configure them, refer to the [internal logging policy](configuration.md#internal-logging-policy) configuration.

## Connectivity to the {{stack}}

If after following the [getting started](getting-started.md) guide and configuring your {{stack}} [endpoint parameters](configuration.md#export-connectivity), you can't see your application's data in {{kib}}, you can follow the following tips to try and figure out what could be wrong.

### Checking out logs

The agent prints debug logs, which can be seen in [logcat](https://developer.android.com/studio/debug/logcat), using the tag `ELASTIC_AGENT`, where you can have a look at your endpoint configuration parameters with a log that reads: _"Initializing connectivity with config [your endpoint configuration]"_. Take a look at those and make sure that the provided configuration matches your {{stack}} endpoint parameters.

### Inspecting network traffic

You can take a look at your app's outgoing network requests via Android Studio's [network inspector tool](http://developer.android.com/studio/debug/network-profiler). This tool can show you the agent's export requests, where you can see if they were successful or not, as well as the request body and the {{stack}} response body for when you need more details of the whole process. Apart from that, this tool also provides a way to export a file with the information of all of your app's HTTP requests, which you could share with our support team if needed.

### SSL/TLS error

Sometimes the request to the {{stack}} endpoint won't show up in the [network inspector](#inspecting-network-traffic). A common issue when this happens is that there is an SSL/TLS error that occurs when the agent tries to contact your {{stack}} endpoint. This is often the case when you work with an on-prem {{stack}} that doesn't have trusted CAs, for which you'd need to add custom security configurations to your app to make the export work. Take a look at [how to configure SSL/TLS](how-tos.md#how-ssl) for more information.

## Desugaring support [why-desugaring]

Android devices with an API level below 26 (older than [Android 8.0](https://developer.android.com/about/versions/oreo/android-8.0)) have limited support for Java 8 features and types, which can cause your app to crash when using those types while running on those older-than-8.0 devices. For example, if one of your app's dependencies uses the [Base64](https://docs.oracle.com/javase/8/docs/api/java/util/Base64.html) type ([added in API level 26](https://developer.android.com/reference/java/util/Base64)), and your app is installed on an Android device with OS version 7.0 ([API level 24](https://developer.android.com/about/versions/nougat/android-7.0)), a crash will happen when the code that uses said type is executed due to a "class not found" error.

To prevent these kinds of issues on devices using Android OS older than 8.0, you must add [Java 8 desugaring support](https://developer.android.com/studio/write/java8-support#library-desugaring) to your app. This requirement is inherited from the [OpenTelemetry Java SDK](https://github.com/open-telemetry/opentelemetry-java/blob/main/VERSIONING.md#language-version-compatibility), which this project is built upon, where several of the unsupported types for Android versions older than 8.0 are used.

## App referred to as service [why-service]

For historic reasons, `service` has been the default way of referring to "an entity that produces telemetry". This term made its way into OpenTelemetry to a point where it was marked as one of the first "stable" resource names, meaning that it was no longer possible/feasible to make a change to another name that would better represent any kind of telemetry source. This has been debated several times within the community. A recent discussion attempts to [explain the `service` description](https://github.com/open-telemetry/semantic-conventions/pull/630) and what it should represent in an effort to reduce confusion. However, there doesn't seem to be a consensus.