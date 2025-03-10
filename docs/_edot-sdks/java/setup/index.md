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

In order to send your data to Elastic using EDOT Java, you need to have the following prerequisites
- an [Elastic](/quickstart/) deployment
- an [EDOT collector](/edot-collector/) deployment

TODO: how to create an API key for the OTEL SDK ? Should probably be distinct from the collector API key.

## Run

Use the `-javaagent:` JVM argument with the path to agent jar.

```bash
java \
  -javaagent:/path/to/agent.jar \
  -jar myapp.jar
```

## Configuration

By default, the instrumentation agent sends data to `http://localhost:4318` OTLP endpoint using HTTP protocol.

Unless such a local endpoint is available on the host, you will need to configure the following environment variables:

* `OTEL_EXPORTER_OTLP_ENDPOINT`: The full URL of the endpoint where data will be sent.
* `OTEL_EXPORTER_OTLP_HEADERS`: A comma-separated list of `key=value` pairs that will
  be added to the headers of every request. This is typically used for authentication information.

The values of those configuration options should be retrieved from the Elastic deployment as part of the prerequisites.
- `OTEL_EXPORTER_OTLP_ENDPOINT` should be set to the OTLP endpoint of the EDOT collector endpoint
- `OTEL_EXPORTER_OTLP_HEADERS` should be set/modified to include authentication API key.

For example:

```shell
export OTEL_EXPORTER_OTLP_ENDPOINT=https://my-deployment.apm.us-west1.gcp.cloud.es.io
export OTEL_EXPORTER_OTLP_HEADERS="Authorization=Bearer P....l"
```

For more advanced configuration, see [Configuration](../configuration.md) section.