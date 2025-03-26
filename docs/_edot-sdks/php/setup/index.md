---
title: Setup
layout: default
nav_order: 1
parent: EDOT PHP
---

<!-- TODO:
- where to download
- explicit description of basic setup here (even if it overlaps with upstream docs)
- link to upstream docs for more advanced setup use cases -->

# Setting up EDOT PHP

This guide shows you how to use the Elastic Distribution of OpenTelemetry PHP (EDOT PHP) to instrument your PHP application and send OpenTelemetry data to an Elastic Observability deployment.

**Already familiar with OpenTelemetry?** It's an explicit goal of this distribution to introduce _no new concepts_ outside those defined by the wider OpenTelemetry community.

**New to OpenTelemetry?** This section will guide you through the _minimal_ configuration options to get EDOT PHP set up in your application. You do _not_ need any existing experience with OpenTelemetry to set up EDOT PHP initially. If you need more control over your configuration after getting set up, you can learn more in the [OpenTelemetry documentation](https://opentelemetry.io/docs/languages/php/).

## Prerequisites

Before getting started, you'll need to send the gathered OpenTelemetry data somewhere so it can be viewed and analyzed. EDOT PHP supports sending data to any OpenTelemetry protocol (OTLP) endpoint, but this guide assumes you are sending data to an [Elastic Observability](https://www.elastic.co/observability) cloud deployment. You can use an existing one or set up a new one.

<details>
<summary><strong>Expand for setup instructions</strong></summary>

To create your first Elastic Observability deployment:

1. Sign up for a [free Elastic Cloud trial](https://cloud.elastic.co/registration) or sign into an existing account.
1. Go to <https://cloud.elastic.co/home>.
1. Click **Create deployment**.
1. When the deployment is ready, click **Open** to visit your Kibana home page (for example, `https://{DEPLOYMENT_NAME}.kb.{REGION}.cloud.es.io/app/home#/getting_started`).
</details>

## Install

### Prerequisites

#### Operating system

- **Linux**
  - Architectures: **x86_64** and **ARM64**
  - **glibc-based systems**: Packages available as **DEB** and **RPM**
  - **musl libc-based systems (Alpine Linux)**: Packages available as **APK**

#### PHP

Supported PHP versions are 8.1-8.4.
You can find more details in [supported technologies](../supported-technologies.md) doc.

### Other limitations
See [limitations](./limitations.md) about other limitations of EDOT PHP.

### Download and install packages

To install EDOT PHP download one of the [packages for supported platforms](https://github.com/elastic/elastic-otel-php/releases/latest).

#### Install RPM package (RHEL/CentOS, Fedora)

    rpm -ivh <package-file>.rpm

#### Install DEB package (Debian, Ubuntu 18+)

    dpkg -i <package-file>.deb

#### Install APK package (Alpine)

    apk add --allow-untrusted <package-file>.apk

<!-- Start-to-finish operation -->
## Send data to Elastic

After installing EDOT PHP, configure and initialize it to start sending data to Elastic.

### Configure EDOT PHP

To configure EDOT PHP, at a minimum you'll need your Elastic Observability cloud deployment's OTLP endpoint and
authorization data to set a few `OTLP_*` environment variables that will be available when running EDOT PHP:

* `OTEL_EXPORTER_OTLP_ENDPOINT`: The full URL of the endpoint where data will be sent.
* `OTEL_EXPORTER_OTLP_HEADERS`: A comma-separated list of `key=value` pairs that will
be added to the headers of every request. This is typically used for authentication information.

<!--
These are the instructions used in other distro docs, but in the README in this repo
it looks like you might be recommending using an API key rather than using the secret
token method used in the setup guides in Kibana.
-->
You can find the values of the endpoint and header variables in Kibana's APM tutorial. In Kibana:

1. Go to **Setup guides**.
1. Select **Observability**.
1. Select **Monitor my application performance**.
1. Scroll down and select the **OpenTelemetry** option.
1. The appropriate values for `OTEL_EXPORTER_OTLP_ENDPOINT` and `OTEL_EXPORTER_OTLP_HEADERS` are shown there.

Here's an example how to connect to Serverless environment:

```sh
export OTEL_EXPORTER_OTLP_ENDPOINT=https://my-deployment.ingest.us-west-2.aws.elastic.cloud:443/
export OTEL_EXPORTER_OTLP_HEADERS="Authorization=ApiKey P....=="
```

### Run EDOT PHP

:warning: After completing the configuration, you should restart the PHP process. If you are using PHP as an Apache Webserver module or PHP-FPM, you need to perform a **full** process restart to ensure that the extension with the agent is loaded correctly.

## Confirm that EDOT PHP is working

To confirm that EDOT PHP has successfully connected to Elastic:

1. Go to **APM** → **Traces**.
1. You should see the name of the service to which you just added EDOT PHP. It can take several minutes after initializing EDOT PHP for the service to show up in this list.
1. Click on the name in the list to see trace data.

> [!NOTE]
> There may be no trace data to visualize unless you have _used_ your application since initializing EDOT PHP.

## Next steps

* Reference all available [configuration options](../configuration.md).
* Learn more about viewing and interpreting data in the [Observability guide](https://www.elastic.co/guide/en/observability/current/apm.html).
