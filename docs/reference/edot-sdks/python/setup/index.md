---
navigation_title: Setup
description: Learn how to set up and configure the Elastic Distribution of OpenTelemetry (EDOT) Python to instrument your application or service.
applies_to:
  stack:
  serverless:
    observability:
  product:
    edot_python: ga
products:
  - id: cloud-serverless
  - id: observability
  - id: edot-sdk
---

# Set up the EDOT Python agent

Learn how to set up the {{edot}} (EDOT) Python in various environments, including Kubernetes and others.

Follow these steps to get started.

::::::{stepper}

::::{step} Install the distribution
Install EDOT Python by running pip:

```bash
pip install elastic-opentelemetry
```
::::

::::{step} Install the available instrumentation
EDOT Python doesn't install any instrumentation package by default. Instead, it relies on the `edot-bootstrap` command to scan the installed packages and install the available instrumentation. The following command installs all the instrumentations available for libraries installed in your environment:

```bash
edot-bootstrap --action=install
```

:::{note}
Add this command every time you deploy an updated version of your application. Also add it to your container image build process.
:::
::::

::::{step} Configure EDOT Python
Refer to [Observability quickstart](/reference/quickstart/index.md) documentation on how to setup your environment.

To configure EDOT Python you need to set a few `OTLP_*` environment variables that are available when running EDOT Python:

* `OTEL_RESOURCE_ATTRIBUTES`: Use this to add a `service.name` and `deployment.environment`. This makes it easier to recognize your application when reviewing data sent to Elastic.

The following environment variables are not required if you are sending data through a local EDOT Collector but are provided in the Elastic Observability platform onboarding:

* `OTEL_EXPORTER_OTLP_ENDPOINT`: The full URL of the endpoint where data will be sent.
* `OTEL_EXPORTER_OTLP_HEADERS`: A comma-separated list of `key=value` pairs that will be added to the headers of every request. This is typically used for authentication information.
::::

::::{step} Run EDOT Python
Wrap your service invocation with `opentelemetry-instrument`, which is the wrapper that provides automatic instrumentation. For example, a web service running with gunicorn might look like this:

```bash
opentelemetry-instrument gunicorn main:app
```
::::

::::{step} Confirm that EDOT Python is working
To confirm that EDOT Python has successfully connected to Elastic:

1. Go to **Observability** → **Applications** → **Service Inventory**
2. Find the name of the service to which you just added EDOT Python. It can take several minutes after initializing EDOT Python for the service to show up in this list.
3. Select the name in the list to see trace data.

:::{note}
There might be no trace data to visualize unless you have invoked your application since initializing EDOT Python.
:::
::::

::::::

## Troubleshooting

For help with common setup issues, refer to the [EDOT Python troubleshooting guide](/troubleshooting/edot-sdks/python/index.md).