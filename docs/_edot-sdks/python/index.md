---
title: EDOT Python
layout: default
nav_order: 6
---

## EDOT Python

The [Elastic Distribution of OpenTelemetry Python (EDOT Python)](https://github.com/elastic/elastic-otel-python) is a customized version of [OpenTelemetry Python](https://opentelemetry.io/docs/languages/python).
EDOT Python makes it easier to get started using OpenTelemetry in your Python applications through strictly OpenTelemetry native means, while also providing a smooth and rich out of the box experience with [Elastic Observability](https://www.elastic.co/observability). It's an explicit goal of this distribution **to avoid introducing proprietary concepts** in addition to those defined by the wider OpenTelemetry community. For any additional features introduced we aim for contributing them back to the upstream OpenTelemetry Python project.

With EDOT Python you have access to all the features of the OpenTelemetry Python agent plus:

* Access to improvements and bug fixes contributed by the Elastic team _before_ the changes are available upstream in OpenTelemetry repositories.
* Access to optional features that can enhance OpenTelemetry data that is being sent to Elastic.
* Elastic-specific processors that ensure optimal compatibility when exporting OpenTelemetry signal data to an Elastic backend like an Elastic Observability deployment.
* Preconfigured collection of tracing and metrics signals, applying some opinionated defaults, such as which sources are collected by default.

**Ready to try out EDOT Python?** Follow the step-by-step instructions in [Setup](./setup/index).

## Read the docs

* [Setup](./setup/index)
* [Setup on Kubernetes](./setup/k8s)
* [Supported technologies](./supported-technologies)
* [Manual instrumentation](./setup/manual-instrumentation)
* [Configuration](./configuration)
* [Migrating from Elastic APM Python Agent](./migration)
* [Troubleshooting](./troubleshooting)
* [FAQ](./faq)
* [Release notes](./release)
