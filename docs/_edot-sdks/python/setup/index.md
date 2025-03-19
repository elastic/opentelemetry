---
title: Setup
layout: default
nav_order: 1
parent: EDOT Python
---

# Setting up EDOT Python

## Install

### Install the distribution

Install EDOT Python:

```bash
pip install elastic-opentelemetry
```

### Install the available instrumentation

EDOT Python does not install any instrumentation package by default, instead it relies on the
`edot-bootstrap` command to scan the installed packages and install the available instrumentation.
The following command will install all the instrumentations available for libraries found installed
in your environment:

```bash
edot-bootstrap --action=install
```

> [!NOTE]
> Add this command every time you deploy an updated version of your application (in other words, add it to your container image build process).

<!-- ✅ Start-to-finish operation -->
## Send data to Elastic

After installing EDOT Python, configure and initialize it to start sending data to Elastic.

<!-- ✅ Provide _minimal_ configuration/setup -->
### Configure EDOT Python

To configure EDOT Python, at a minimum you'll need your Elastic Observability cloud OTLP endpoint and
authorization data to set a few `OTLP_*` environment variables that will be available when running EDOT Python:

* `OTEL_RESOURCE_ATTRIBUTES`: Use this to add a service name that will make it easier to recognize your application when reviewing data sent to Elastic.
* `OTEL_EXPORTER_OTLP_ENDPOINT`: The full URL of the endpoint where data will be sent.
* `OTEL_EXPORTER_OTLP_HEADERS`: A comma-separated list of `key=value` pairs that will
be added to the headers of every request. This is typically used for authentication information.

You can find the values of the endpoint and header variables in Kibana's APM tutorial. In Kibana:

1. Go to **Setup guides**.
1. Select **Observability**.
1. Select **Monitor my application performance**.
1. Scroll down and select the **OpenTelemetry** option.
1. The appropriate values for `OTEL_EXPORTER_OTLP_ENDPOINT` and `OTEL_EXPORTER_OTLP_HEADERS` are shown there.

Here's an example for sending data to an Elastic Cloud deployment:

```sh
export OTEL_RESOURCE_ATTRIBUTES=service.name=<app-name>,service.version=<app-version>,deployment.environment=production
export OTEL_EXPORTER_OTLP_ENDPOINT=https://my-deployment.apm.us-west1.gcp.cloud.es.io
export OTEL_EXPORTER_OTLP_HEADERS="Authorization=Bearer P....l"
```

And here's an example for sending data to an Elastic Cloud serverless project:

```sh
export OTEL_RESOURCE_ATTRIBUTES=service.name=<app-name>,service.version=<app-version>,deployment.environment=production
export OTEL_EXPORTER_OTLP_ENDPOINT=https://my-deployment.apm.us-west1.gcp.cloud.es.io
export OTEL_EXPORTER_OTLP_HEADERS="Authorization=ApiKey B....="
```

> [!NOTE]
> You'll be prompted to create an API key during the Elastic Cloud serverless project onboarding. Refer to the [Api keys documentation](https://www.elastic.co/guide/en/serverless/current/api-keys.html) on how to manage them.

### Run EDOT Python

Then wrap your service invocation with `opentelemetry-instrument`, which is the wrapper that provides _automatic instrumentation_:

```bash
opentelemetry-instrument <command to start your service>
```

For example, a web service running with gunicorn may look like this:

```bash
opentelemetry-instrument gunicorn main:app
```

<!--  ✅ What success looks like -->
## Confirm that EDOT Python is working

To confirm that EDOT Python has successfully connected to Elastic:

1. Go to **APM** → **Traces**.
1. You should see the name of the service to which you just added EDOT Python. It can take several minutes after initializing EDOT Python for the service to show up in this list.
1. Click on the name in the list to see trace data.

> [!NOTE]
> There may be no trace data to visualize unless you have _used_ your application since initializing EDOT Python.
