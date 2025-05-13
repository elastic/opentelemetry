---
navigation_title: Setup
description: Set up the Elastic Distribution of OpenTelemetry PHP to instrument your PHP application.
applies_to:
  stack:
  serverless:
    observability:
products:
  - id: cloud-serverless
  - id: observability
  - id: edot-php
---

# Setting up EDOT PHP

This guide shows you how to use the Elastic Distribution of OpenTelemetry PHP (EDOT PHP) to instrument your PHP application and send OpenTelemetry data to an Elastic Observability deployment.

**Already familiar with OpenTelemetry?** It's an explicit goal of this distribution to introduce _no new concepts_ outside those defined by the wider OpenTelemetry community.

**New to OpenTelemetry?** This section will guide you through the _minimal_ configuration options to get EDOT PHP set up in your application. You do _not_ need any existing experience with OpenTelemetry to set up EDOT PHP initially. If you need more control over your configuration after getting set up, you can learn more in the [OpenTelemetry documentation](https://opentelemetry.io/docs/languages/php/).

## 1. Prerequisites

Before you begin, make sure you have a destination for the telemetry data collected by EDOT PHP.
While EDOT PHP can export data to any OpenTelemetry Protocol (OTLP)–compatible endpoint, this guide focuses on using [Elastic Observability](https://www.elastic.co/observability) as the backend.
You can either use an existing Elastic Cloud deployment or create a new one.

To quickly get up and running, follow the [Elastic OpenTelemetry Quickstart guide](../../../quickstart/index.md), which walks you through:

- Creating a free Elastic Cloud deployment
- Configuring your OpenTelemetry agent
- Exploring traces and metrics in Kibana

### Operating system and PHP version

Please refer to the [supported technologies](../supported-technologies.md) page for details about currently supported operating systems and PHP versions.

### Other limitations
See [limitations](./limitations.md) about other limitations of EDOT PHP.

## 2. Download and install packages

To install EDOT PHP download one of the [packages for supported platforms](https://github.com/elastic/elastic-otel-php/releases/latest).

### Install RPM package (RHEL/CentOS, Fedora)

    rpm -ivh <package-file>.rpm

### Install DEB package (Debian, Ubuntu 18+)

    dpkg -i <package-file>.deb

### Install APK package (Alpine)

    apk add --allow-untrusted <package-file>.apk

## 3. Send data to Elastic

After installing EDOT PHP, configure and initialize it to start sending data to Elastic.

### Configure EDOT PHP

To configure EDOT PHP, at a minimum you'll need your Elastic Observability cloud deployment's OTLP endpoint and
authorization data to set a few `OTLP_*` environment variables that will be available when running EDOT PHP:

* `OTEL_EXPORTER_OTLP_ENDPOINT`: The full URL of the endpoint where data will be sent.
* `OTEL_EXPORTER_OTLP_HEADERS`: A comma-separated list of `key=value` pairs that will
be added to the headers of every request. This is typically used for authentication information.

Here's an example how to connect to Serverless environment:

```sh
export OTEL_EXPORTER_OTLP_ENDPOINT=https://my-deployment.ingest.us-west-2.aws.elastic.cloud:443/
export OTEL_EXPORTER_OTLP_HEADERS="Authorization=ApiKey P....=="
```

### Run EDOT PHP

:::warning
After completing the configuration, you should restart the PHP process. If you are using PHP as an Apache Webserver module or PHP-FPM, you need to perform a **full** process restart to ensure that the extension with the agent is loaded correctly.
:::

## 4. Confirm that EDOT PHP is working

To confirm that EDOT PHP has successfully connected to Elastic:

1. Go to **APM** → **Traces**.
1. You should see the name of the service to which you just added EDOT PHP. It can take several minutes after initializing EDOT PHP for the service to show up in this list.
1. Click on the name in the list to see trace data.

:::note
There may be no trace data to visualize unless you have _used_ your application since initializing EDOT PHP.
:::

## 5. Next steps

* Reference all available [configuration options](../configuration.md).
* Learn more about viewing and interpreting data in the [Observability guide](https://www.elastic.co/guide/en/observability/current/apm.html).
