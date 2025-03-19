---
title: Migration
layout: default
nav_order: 5
parent: EDOT Python
---

# Migrating to EDOT Python from the Elastic APM Python Agent

This guide will highlight the major differences between the [Elastic APM Python agent](https://www.elastic.co/guide/en/apm/agent/python/current/getting-started.html) and the Elastic Distribution of OpenTelemetry Python (EDOT Python).
For step-by-step instructions on setting up EDOT Python refer to the [Setup](./setup/index).

## We are a distribution

As a distribution of OpenTelemetry, EDOT Python follows certain standards, but there is still some space for innovation.

## Bold on autoinstrumentation

We have chosen to make autoinstrumentation as simple as possible so you can just focus on your code; we favored an experience that requires minimal changes to your application code. The upstream OpenTelemetry configuration has more options than the distribution requires. Our default configuration is listed [here](https://github.com/elastic/elastic-otel-python?tab=readme-ov-file#configuration).

## Bring your own instrumentation

In EDOT Python we decided to not ship all the available instrumentations in order to accommodate environments where installing more packages than requested may be an issue.
We provide a tool to discover available instrumentations automatically that can be added to your build workflow. See [Get started](https://github.com/elastic/elastic-otel-python/blob/main/docs/get-started.md#install-the-available-instrumentation).

## Performance comparison

Any instrumentation agent will incur in a performance penalty for your application because more work will be done. How much really depends
on your application and on the instrumentations used.

While we can't provide generically applicable, accurate numbers about the performance penalty, here you can find some measurement taken
from a sample web application which allows to provide a comparison between agents and an order of magnitude of the effective overhead.

Those numbers are only provided as indicators, and you should not attempt to extrapolate them. You should however use
them as a framework to evaluate and measure the overhead on your applications.

The following table compares the response times of a sample web application without an agent, with Elastic APM Python Agent and with EDOT Python Agent in two situations: without data loaded and serialized to measure the minimal overhead of agents and with some data loaded and then serialized to provide a more common scenario.

|                                   | no agent  | EDOT Python instrumentation | Elastic APM Python agent |
|-----------------------------------|-----------|-----------------------------|--------------------------|
| No data: Time taken for tests     | 1.277 s   | 2.215 s                     | 2.313 s                  |
| Sample data: Time taken for tests | 4.546 s   | 6.401 s                     | 6.159 s                  |

## Limitations

### Central and Dynamic configuration

Currently EDOT Python does not have an equivalent of the [central configuration feature](https://www.elastic.co/guide/en/observability/current/apm-agent-configuration.html) that the Elastic APM Python agent supports. When using EDOT Python, all the configurations are static and should be provided to the application with other configurations, e.g. environment variables.

### AWS lambda

At the moment, we are not building a custom lambda layer for our Python distribution. You can refer to the upstream [Lambda Auto-Instrumentation](https://opentelemetry.io/docs/faas/lambda-auto-instrument/).

### Missing instrumentations

Not all instrumentations we have in Elastic APM Python Agent have an OpenTelemetry counterpart. But we may port them if they are requested by users.

At the time of writing these docs, the following libraries are missing an OpenTelemetry instrumentation:
- aiobotocore
- aiomysql
- aiopg
- aioredis
- Azure storage and Azure queue
- Graphene
- httplib2
- pylibmc
- pyodbc
- Sanic
- zlib

### Integration with structured logging

EDOT Python does not have any [structlog integration](https://www.elastic.co/guide/en/apm/agent/python/current/logs.html#structlog) at the moment.

### Span compression

EDOT Python does not implement [span compression](https://www.elastic.co/guide/en/observability/current/apm-data-model-spans.html#apm-spans-span-compression).

### Breakdown metrics

EDOT Python is not sending metrics that power the [Breakdown metrics](https://www.elastic.co/guide/en/apm/guide/current/data-model-metrics.html#_breakdown_metrics).
