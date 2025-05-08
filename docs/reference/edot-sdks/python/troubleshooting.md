---
navigation_title: Troubleshooting
description: Troubleshooting the EDOT Python Agent.
applies_to:
  stack:
  serverless:
    observability:
products:
  - cloud-serverless
  - observability
  - edot-python
---

# Troubleshooting the EDOT Python Agent

Below are some resources and tips for troubleshooting and debugging the Elastic Distribution of OpenTelemetry Python (EDOT Python).

- [Easy Fixes](#easy-fixes)
- [Disable EDOT](#easy-fixes)

## Easy Fixes

Before you try anything else, go through the following sections to ensure that
EDOT Python is configured correctly. This is not an exhaustive list, but rather
a list of common problems that users run into.

### Debug and development modes

Most frameworks support a debug mode. Generally, this mode is intended for
non-production environments and provides detailed error messages and logging of
potentially sensitive data. So enabling instrumentation in debug mode is not advised and may pose privacy and security issues in recording
sensitive data.

#### Django

Django applications running with the Django `runserver` need to use the `--noreload` parameter in order to be instrumented with `opentelemetry-instrument`.
Remember that you also need to set the `DJANGO_SETTINGS_MODULE` environment variable pointing to the application settings module.

#### FastAPI

FastAPI application started with `fastapi dev` requires the reloader to be disabled with `--no-reload` in order to be instrumented with `opentelemetry-instrument`.

#### Flask

Flask applications running in debug mode will require to disable the reloader in order to being traced, see [OpenTelemetry zero code documentation](https://opentelemetry.io/docs/zero-code/python/example/#instrumentation-while-debugging).

## Disable EDOT

In the unlikely event EDOT Python causes disruptions to a production application, you can disable it while you troubleshoot.

To disable the underlying OpenTelemetry SDK you set the following environment variable `OTEL_SDK_DISABLED=true`.

If only a subset of instrumentation are causing disruptions you can disable them with the `OTEL_PYTHON_DISABLED_INSTRUMENTATIONS`
environment variable. It accepts a list of comma separated instrumentations to disable, see [OpenTelemetry zero code documentation](https://opentelemetry.io/docs/zero-code/python/configuration/#disabling-specific-instrumentations)

## Missing logs

Enabling the Python logging module auto-instrumentation with `OTEL_PYTHON_LOGGING_AUTO_INSTRUMENTATION_ENABLED=true` calls the
[logging.basicConfig](https://docs.python.org/3/library/logging.html#logging.basicConfig) method that will make your own application calls
to it a no-op. The side effect of this is that you won't see your application logs in the console anymore.

If you are already shipping logs by other means you don't need to enable this.

## Are semantic convention stable yet?

Unfortunately not yet and so you should expect some changes between versions in order to stabilize them. For some semantic conventions
like HTTP there is a migration path but the conversion to stable HTTP semantic conventions is not done yet for all the instrumentations.

## Does EDOT Python require access to or modification of application code ?

EDOT Python is distributed as a Python package and so must be installed in the same environment as your application. Once it is
available in the path we can auto-instrument your application without changing the application code.
