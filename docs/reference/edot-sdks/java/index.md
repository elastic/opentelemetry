---
navigation_title: EDOT Java
description: Introduction to the Elastic Distribution of OpenTelemetry (EDOT) Java Agent, a customized version of the OpenTelemetry Java agent for capturing traces, metrics, and logs.
applies_to:
  stack:
  serverless:
    observability:
  product:
    edot_java: ga
products:
  - id: cloud-serverless
  - id: observability
  - id: edot-sdk
---

# Elastic Distribution of OpenTelemetry Java

The {{edot}} (EDOT) Java is a customized version of the [OpenTelemetry Java agent](https://github.com/open-telemetry/opentelemetry-java-instrumentation), configured for the best experience with Elastic Observability. 

Use EDOT Java to start the OpenTelemetry SDK with your Java application, and automatically capture tracing data, performance metrics, and logs. Traces, metrics, and logs can be sent to any OpenTelemetry Protocol (OTLP) Collector you choose.

A goal of this distribution is to avoid introducing proprietary concepts in addition to those defined by the wider OpenTelemetry community. For any additional features introduced, Elastic aims at contributing them back to the OpenTelemetry project.

## Features [edot-sdks-java-features]

In addition to all the features of OpenTelemetry Java, with EDOT Java you have access to the following:

* Improvements and bug fixes contributed by the Elastic team before the changes are available in OpenTelemetry repositories.
* Optional features that can enhance OpenTelemetry data that is being sent to Elastic.
* Elastic-specific processors that ensure optimal compatibility when exporting OpenTelemetry signal data to an Elastic backend like an Elastic Observability deployment.
* Preconfigured collection of tracing and metrics signals, applying some opinionated defaults, such as which sources are collected by default.
* Compatibility with APM Agent Central Configuration to modify the settings of the EDOT Java agent without having to restart the application.

Follow the step-by-step instructions in [Setup](/reference/edot-sdks/java/setup/index.md) to get started.

## Release notes [edot-sdks-java-release-notes]

For the latest release notes, including known issues, deprecations, and breaking changes, refer to [EDOT Java release notes](elastic-otel-java://release-notes/index.md)