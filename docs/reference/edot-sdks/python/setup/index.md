---
navigation_title: Setup
description: Setting up EDOT Python.
applies_to:
  stack:
  serverless:
    observability:
products:
  - cloud-serverless
  - observability
  - edot-python
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

:::{note}
Add this command every time you deploy an updated version of your application (in other words, add it to your container image build process).
:::

## Send data to Elastic

After installing EDOT Python, configure and initialize it to start sending data to Elastic.

### Configure EDOT Python

Refer to [Observability quickstart](https://elastic.github.io/opentelemetry/quickstart/) documentation on how to setup your environment.

To configure EDOT Python you need to set a few `OTLP_*` environment variables that will be available when running EDOT Python:

* `OTEL_RESOURCE_ATTRIBUTES`: Use this to add a `service.name` and `deployment.environment` that will make it easier to recognize your application when reviewing data sent to Elastic.

The following environment variables are not required if you are sending data through a local EDOT Collector but will be provided in the Elastic Observability platform onboarding:

* `OTEL_EXPORTER_OTLP_ENDPOINT`: The full URL of the endpoint where data will be sent.
* `OTEL_EXPORTER_OTLP_HEADERS`: A comma-separated list of `key=value` pairs that will be added to the headers of every request. This is typically used for authentication information.


### Run EDOT Python

Then wrap your service invocation with `opentelemetry-instrument`, which is the wrapper that provides _automatic instrumentation_:

```bash
opentelemetry-instrument <command to start your service>
```

For example, a web service running with gunicorn may look like this:

```bash
opentelemetry-instrument gunicorn main:app
```

## Confirm that EDOT Python is working

To confirm that EDOT Python has successfully connected to Elastic:

1. Go to **Observability** → **Applications** → **Service Inventory**
1. You should see the name of the service to which you just added EDOT Python. It can take several minutes after initializing EDOT Python for the service to show up in this list.
1. Click on the name in the list to see trace data.

:::{note}
There may be no trace data to visualize unless you have _invoked_ your application since initializing EDOT Python.
:::
