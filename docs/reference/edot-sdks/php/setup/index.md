---
navigation_title: Setup
description: Set up the Elastic Distribution of OpenTelemetry PHP to instrument your PHP application.
applies_to:
  stack:
  serverless:
    observability:
  product:
    edot_php: ga
products:
  - id: cloud-serverless
  - id: observability
  - id: edot-sdk
---

# Set up EDOT PHP

Learn how to use the {{edot}} PHP (EDOT PHP) to instrument your PHP application and send OpenTelemetry data to an Elastic Observability deployment.

## Prerequisites

Before you begin, make sure you have a destination for the telemetry data collected by EDOT PHP. While EDOT PHP can export data to any OpenTelemetry Protocol (OTLP)–compatible endpoint, this guide focuses on using [Elastic Observability](https://www.elastic.co/observability) as the backend. You can either use an existing Elastic Cloud deployment or create a new one.

To quickly get up and running, follow the [Elastic OpenTelemetry Quickstart guide](../../../quickstart/index.md), which walks you through:

- Creating a free Elastic Cloud deployment.
- Configuring your OpenTelemetry agent.
- Exploring traces and metrics in {{kib}}.

### Operating system and PHP version

Refer to [Supported technologies](../supported-technologies.md) for details about currently supported operating systems and PHP versions.

### Limitations

Refer to [Limitations](./limitations.md) to learn about the limitations of EDOT PHP.

## Download and install packages

To install EDOT PHP, download one of the [packages for supported platforms](https://github.com/elastic/elastic-otel-php/releases/latest).

::::{tab-set}

:::{tab-item} RPM (RHEL/CentOS, Fedora)
```bash
rpm -ivh <package-file>.rpm
```
:::

:::{tab-item} DEB (Debian, Ubuntu 18+)
```bash
dpkg -i <package-file>.deb
```
:::

:::{tab-item} APK (Alpine)
```bash
apk add --allow-untrusted <package-file>.apk
```
:::

::::

## Send data to Elastic

After installing EDOT PHP, configure and initialize it to start sending data to Elastic.

### Configure EDOT PHP

To configure EDOT PHP, at a minimum you need your Elastic Observability cloud deployment's OTLP endpoint and authorization data to set a few `OTLP_*` environment variables that will be available when running EDOT PHP:

* `OTEL_EXPORTER_OTLP_ENDPOINT`: The full URL of the endpoint where data will be sent.
* `OTEL_EXPORTER_OTLP_HEADERS`: A comma-separated list of `key=value` pairs that is added to the headers of every request. This is typically used for authentication information.

Here's an example how to connect to Serverless environment:

```sh
export OTEL_EXPORTER_OTLP_ENDPOINT=https://my-deployment.ingest.us-west-2.aws.elastic.cloud:443/
export OTEL_EXPORTER_OTLP_HEADERS="Authorization=ApiKey P....=="
```

### Run EDOT PHP

After completing the configuration, you should restart the PHP process. If you are using PHP as an Apache Webserver module or PHP-FPM, you need to perform a full process restart to ensure that the extension with the agent is loaded correctly.

## Confirm that EDOT PHP is working

To confirm that EDOT PHP has successfully connected to Elastic:

1. Go to **APM** → **Traces** in Elastic Observability.
2. Find the name of the service to which you just added EDOT PHP. It can take several minutes after initializing EDOT PHP for the service to show up in this list.
3. Select the name in the list to see trace data.

:::{note}
There might be no trace data to visualize unless you have used your application since initializing EDOT PHP.
:::
