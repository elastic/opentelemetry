---
navigation_title: Setup
description: Instructions for setting up the Elastic Distribution of OpenTelemetry (EDOT) Java Agent in various environments, including Kubernetes and others.
---
# Setting up the EDOT Java Agent

**Kubernetes**

For Kubernetes we recommend using the OTel Kubernetes Operator that also manages the auto-instrumentation of Java applications. Follow the [Quickstart Guide](../../../quickstart/index.md) for Kubernetes or learn more about [instrumentation details on Kubernetes for Java](./k8s). 

**All other environments**

Follow the Java setup guide below for all other environments.

## Download

You can download the latest release version or snapshot version of the EDOT Java Agent from the following links:

| Latest Release | Latest Snapshot |
|:---:|:---:|
| [![Maven Central](https://img.shields.io/maven-central/v/co.elastic.otel/elastic-otel-javaagent?label=elastic-otel-javaagent&style=for-the-badge)](https://mvnrepository.com/artifact/co.elastic.otel/elastic-otel-javaagent/latest) | [![Sonatype Nexus](https://img.shields.io/nexus/s/co.elastic.otel/elastic-otel-javaagent?server=https%3A%2F%2Foss.sonatype.org&label=elastic-otel-javaagent&style=for-the-badge)](https://oss.sonatype.org/service/local/artifact/maven/redirect?r=snapshots&g=co.elastic.otel&a=elastic-otel-javaagent&v=LATEST) |

## Prerequisites

You need to have completed the steps in the [Quickstart](/quickstart/) section that corresponds to your Elastic deployment model.

##  Configure the Java agent

The minimal configuration to send data involves setting the values for `OTEL_EXPORTER_OTLP_ENDPOINT` and `OTEL_EXPORTER_OTLP_HEADERS` environment variables.

We also recommend setting the `service.name` resource attribute explicitly with `OTEL_SERVICE_NAME` as it allows to qualify captured data and group multiple service instances together.

Here is an example to set `OTEL_EXPORTER_OTLP_ENDPOINT`, `OTEL_EXPORTER_OTLP_HEADERS` and `OTEL_SERVICE_NAME` environment variables:

```sh
export OTEL_EXPORTER_OTLP_ENDPOINT=https://my-deployment.apm.us-west1.gcp.cloud.es.io
export OTEL_EXPORTER_OTLP_HEADERS="Authorization=ApiKey P....l"
export OTEL_SERVICE_NAME="my-awesome-service"
```

For more advanced configuration, see [Configuration](../configuration) section.

Configuration of those environment values depends on the deployment model:

### Local EDOT Collector

EDOT Collector is accessible with `http://localhost:4318` without authentication, no further configuration is required.
The `OTEL_EXPORTER_OTLP_ENDPOINT` and `OTEL_EXPORTER_OTLP_HEADERS` environment variables do not have to be set.

**Self-managed EDOT Collector**

`OTEL_EXPORTER_OTLP_ENDPOINT` should be set to the OTLP endpoint of your selfmanaged EDOT Collector.
    
If EDOT Collector requires authentication, `OTEL_EXPORTER_OTLP_HEADERS` should be set to include `Authorization=ApiKey <ELASTIC_API_KEY>` (comma-separated key=value list).

### Elastic Managed OTLP endpoint

Use [these guides](../../../quickstart/serverless/index.md) to retrieve the `<ELASTIC_OTLP_ENDPOINT>` and the `<ELASTIC_API_KEY>`.

- `OTEL_EXPORTER_OTLP_ENDPOINT` should be set to `<ELASTIC_OTLP_ENDPOINT>`
- `OTEL_EXPORTER_OTLP_HEADERS` should be set to include `Authorization=ApiKey <ELASTIC_API_KEY>` (comma-separated key=value list).

### Kubernetes

Connection to the EDOT Collector is managed by the OTel Kubernetes Operator, [follow the Quickstart Guides](../../../quickstart/index.md) for Kubernetes.

## Run the Java agent

Use the `-javaagent:` JVM argument with the path to agent jar, this requires to modify the JVM arguments and restart
the application.

```sh
java \
-javaagent:/path/to/agent.jar \
-jar myapp.jar
```

When modifying the JVM command line arguments is not possible, the `JAVA_TOOL_OPTIONS` environment variable can be used
to provide the `-javaagent:` argument or JVM system properties. When `JAVA_TOOL_OPTIONS` is set, all JVMs will automatically 
use it, thus special care should be taken to limit the scope to the relevant JVMs.

Also, some application servers require manual steps or modification of their configuration files, see [dedicated instructions](https://opentelemetry.io/docs/zero-code/java/agent/server-config/) for more details.

For applications deployed with Kubernetes, we recommend using [OpenTelemetry Operator](./k8s).
