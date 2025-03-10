---
title: Setup
layout: default
nav_order: 1
parent: EDOT Java
---

# Setting up the EDOT Java Agent

## Download

Latest release: [![Maven Central](https://img.shields.io/maven-central/v/co.elastic.otel/elastic-otel-javaagent?label=elastic-otel-javaagent)](https://mvnrepository.com/artifact/co.elastic.otel/elastic-otel-javaagent/latest)

Latest snapshot: [![Sonatype Nexus](https://img.shields.io/nexus/s/co.elastic.otel/elastic-otel-javaagent?server=https%3A%2F%2Foss.sonatype.org&label=elastic-otel-javaagent)](https://oss.sonatype.org/service/local/artifact/maven/redirect?r=snapshots&g=co.elastic.otel&a=elastic-otel-javaagent&v=LATEST)

## Prerequisites

You need to have completed the steps in the [Quickstart](/quickstart/) section that corresponds to your Elastic deployment model.

## Run

Use the `-javaagent:` JVM argument with the path to agent jar, this requires to modify the JVM arguments and restart
the application.

```bash
java \
  -javaagent:/path/to/agent.jar \
  -jar myapp.jar
```

For applications deployed with Kubernetes, we recommend using [OpenTelemetry Operator](./k8s).

## Minimal configuration

The minimal configuration to send data involves setting the values for `OTEL_EXPORTER_OTLP_ENDPOINT` and `OTEL_EXPORTER_OTLP_HEADERS` environment variables.

Configuration of those environment values depends on the deployment model:
- EDOT Collector running on the application host, accessible with `http://localhost:4318` without authentication, no further configuration is required.
- EDOT Collector managed by the OpenTelemetry Kubernetes Operator: environment variables are automatically provided by the Operator, no further configuration is required.
- Elastic Managed OTLP endpoint (Elastic Cloud Serverless):
  - `OTEL_EXPORTER_OTLP_ENDPOINT` should be set to `<ELASTIC_OTLP_ENDPOINT>`
  - `OTEL_EXPORTER_OTLP_HEADERS` should be set to include `Authorization=ApiKey <ELASTIC_API_KEY>` (comma-separated key=value list).
- Self-managed EDOT Collector:
  - `OTEL_EXPORTER_OTLP_ENDPOINT` should be set to the OTLP endpoint of EDOT Collector
  - `OTEL_EXPORTER_OTLP_HEADERS` should be set to include `Authorization=ApiKey <ELASTIC_API_KEY>` (comma-separated key=value list).

For example:

```shell
export OTEL_EXPORTER_OTLP_ENDPOINT=https://my-deployment.apm.us-west1.gcp.cloud.es.io
export OTEL_EXPORTER_OTLP_HEADERS="Authorization=ApiKey P....l"
```

For more advanced configuration, see [Configuration](../configuration) section.