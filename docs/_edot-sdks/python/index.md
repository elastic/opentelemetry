---
title: EDOT Python
layout: default
nav_order: 6
---

# EDOT Python

The [Elastic Distribution of OpenTelemetry Python (EDOT Python)](https://github.com/elastic/elastic-otel-python) is a customized version of [OpenTelemetry Python](https://opentelemetry.io/docs/languages/python).
EDOT Python makes it easier to get started using OpenTelemetry in your Python applications through strictly OpenTelemetry native means, while also providing a smooth and rich out of the box experience with [Elastic Observability](https://www.elastic.co/observability). It's an explicit goal of this distribution **to avoid introducing proprietary concepts** in addition to those defined by the wider OpenTelemetry community. For any additional features introduced we aim for contributing them back to the upstream OpenTelemetry Python project.

With EDOT Python you have access to all the features of the OpenTelemetry Python agent plus:

* Access to improvements and bug fixes contributed by the Elastic team _before_ the changes are available upstream in OpenTelemetry repositories.
* Access to optional features that can enhance OpenTelemetry data that is being sent to Elastic.
* Elastic-specific processors that ensure optimal compatibility when exporting OpenTelemetry signal data to an Elastic backend like an Elastic Observability deployment.
* Preconfigured collection of tracing and metrics signals, applying some opinionated defaults, such as which sources are collected by default.

**Ready to try out EDOT Python?** Follow the step-by-step instructions in [Setup](./setup/index).

## Compatibility matrix

Data can be exported in the OpenTelemetry-native [OTLP (OpenTelemetry protocol)](https://opentelemetry.io/docs/specs/otlp) format via gRPC (default)
and HTTP to self-managed, Elastic Cloud Hosted or Elastic Cloud Serverless observability backends.

For the best (and supported) experience, we recommend exporting data from EDOT Python via the [EDOT Collector](https://elastic.github.io/opentelemetry/edot-collector/index).

| EDOT Python | Elastic Stack 8.x | Elastic Stack 9.x | Serverless |
| ----------- | ----------------- | ----------------- | ---------- |
| 1.0.0       | 8.18.0+¹          | 9.0.0+¹           | ✅ ²       |

***1.** Via the EDOT Collector.*

***2.** Via the OTel-native ingest endpoint.*
