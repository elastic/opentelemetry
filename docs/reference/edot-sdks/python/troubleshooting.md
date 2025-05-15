---
navigation_title: Troubleshooting
description: Troubleshooting the EDOT Python Agent.
applies_to:
  stack:
  serverless:
    observability:
products:
  - id: cloud-serverless
  - id: observability
  - id: edot-sdk
---

# Troubleshooting the EDOT Python Agent

Use the information on this page to troubleshoot issues using EDOT Python.

If you need help and you're an existing Elastic customer with a support contract, create a ticket in the [Elastic Support portal](https://support.elastic.co/customers/s/login/). Other users can post in the [APM discuss forum](https://discuss.elastic.co/c/apm) or [open a GitHub issue](https://github.com/elastic/elastic-otel-node/issues).

As a first step, review the [supported technologies](./supported-technologies.md) to ensure your application is supported by the agent. Are you using a Python version that EDOT Python supports? Are the versions of your dependencies in the supported version range to be instrumented?

## General troubleshooting

Follow these recommended actions to make sure that EDOT Python is configured correctly.

### Debug and development modes

Most frameworks support a debug mode. This mode is intended for non-production environments and provides detailed error messages and logging of potentially sensitive data. Turning on instrumentation in debug mode is not advised and might pose privacy and security issues in recording sensitive data.

#### Django

Django applications running with the Django `runserver` must use the `--noreload` parameter to be instrumented with `opentelemetry-instrument`. You also need to set the `DJANGO_SETTINGS_MODULE` environment variable pointing to the application settings module.

#### FastAPI

FastAPI application started with `fastapi dev` requires the reloader to be turned off with `--no-reload` to be instrumented with `opentelemetry-instrument`.

#### Flask

Flask applications running in debug mode require to turn off the reloader to be traced. Refer to [OpenTelemetry zero code documentation](https://opentelemetry.io/docs/zero-code/python/example/#instrumentation-while-debugging).

## Turn off EDOT

In the unlikely event EDOT Python causes disruptions to a production application, you can turn it off while you troubleshoot. To turn off the underlying OpenTelemetry SDK, set the `OTEL_SDK_DISABLED` environment variable to `true`.

If only a subset of instrumentation are causing disruptions, turn them off using the `OTEL_PYTHON_DISABLED_INSTRUMENTATIONS` environment variable. The variable accepts a list of comma-separated instrumentations. Refer to [OpenTelemetry zero code documentation](https://opentelemetry.io/docs/zero-code/python/configuration/#disabling-specific-instrumentations).

## Missing logs

Activating the Python logging module auto-instrumentation with `OTEL_PYTHON_LOGGING_AUTO_INSTRUMENTATION_ENABLED=true` calls the [logging.basicConfig](https://docs.python.org/3/library/logging.html#logging.basicConfig) method that makes your own application calls to it a no-op. The side effect of this is that you won't see your application logs in the console. If you are already shipping logs by other means, you don't need to turn this on.

## Check stability of semantic conventions

For some semantic conventions, like HTTP, there is a migration path, but the conversion to stable HTTP semantic conventions is not done yet for all the instrumentations.

## Access or modification of application code

EDOT Python is distributed as a Python package and so must be installed in the same environment as your application. Once it is available in the path, it can auto-instrument your application without changing the application code.
