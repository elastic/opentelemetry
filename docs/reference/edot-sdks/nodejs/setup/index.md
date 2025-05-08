---
navigation_title: Setup
description: How to set up the Elastic Distribution of OpenTelemetry Node.js (EDOT Node.js).
applies_to:
  stack:
  serverless:
    observability:
products:
  - cloud-serverless
  - observability
  - edot-nodejs
---

# Setting up EDOT Node.js

To monitor your service with the Elastic Distribution of OpenTelemetry Node.js (EDOT Node.js) you'll need to install it, configure it, and properly start it with your application. For example, this shows the minimal steps:

```bash
# Install it
npm install --save @elastic/opentelemetry-node

# Configure it
export OTEL_EXPORTER_OTLP_ENDPOINT="...your-ELASTIC_OTLP_ENDPOINT..."
export OTEL_EXPORTER_OTLP_HEADERS="Authorization=ApiKey ...your-ELASTIC_API_KEY..."
export OTEL_SERVICE_NAME="my-app"

# Start it with your application
node --import @elastic/opentelemetry-node my-app.js
```

This setup guide covers each of these steps. (If you are deploying in Kubernetes, see the [Kubernetes setup guide](./k8s.md).)


## Prerequisites

Before getting started, you'll need somewhere to send the gathered OpenTelemetry data, so it can be viewed and analyzed. This doc assumes you're using an Elastic Observability deployment. You can use an existing one or set up a new one.

Follow the EDOT [Quickstart guide](../../../quickstart/index.md) to get a deployment and gather the `ELASTIC_OTLP_ENDPOINT` and `ELASTIC_API_KEY` pieces of data that you'll need to configure the EDOT Node.js SDK.


## Installation

EDOT Node.js is published to npm as the [`@elastic/opentelemetry-node` package](https://www.npmjs.com/package/@elastic/opentelemetry-node). Install it with your chosen package manager:

```bash
npm install @elastic/opentelemetry-node  
yarn add @elastic/opentelemetry-node    
pnpm add @elastic/opentelemetry-node
```

## Configuration

EDOT Node.js is configured with environment variables beginning with `OTEL_` or `ELASTIC_OTEL_`. Any `OTEL_*` environment variables behave the same as with the upstream OpenTelemetry SDK. For example, all the OpenTelemetry [General SDK Configuration env vars](https://opentelemetry.io/docs/specs/otel/configuration/sdk-environment-variables/#general-sdk-configuration) are supported. If EDOT Node.js provides a configuration setting specific to the Elastic distribution, it will begin with `ELASTIC_OTEL_`.

### Basic configuration

To configure EDOT Node.js, as a typical minimum you will need:

* `OTEL_EXPORTER_OTLP_ENDPOINT`: The full URL of an OpenTelemetry Collector where data will be sent. When using Elastic Observability, this will be the "ingest" endpoint of an Elastic Cloud Serverless project or the URL of a deployed [EDOT Collector](../../../edot-collector/index.md) **Set this to the `ELASTIC_OTLP_ENDPOINT` value as described in the [EDOT Quickstart pages](../../../quickstart/index.md).**
* `OTEL_EXPORTER_OTLP_HEADERS`: A comma-separated list of HTTP headers used for exporting data, typically used to set the `Authorization` header with auth information. **Get an `ELASTIC_API_KEY` as described in the [EDOT Quickstart pages](../../../quickstart/index.md) and set this to `"Authorization=ApiKey ELASTIC_API_KEY"`.**
* `OTEL_SERVICE_NAME`: The name of your service, used to distinguish telemetry data from other services in your system. If not set, it will default to `unknown_service:node`.

:::note
In some environments, for example in some Kubernetes setups, a *local* OpenTelemetry Collector (e.g. EDOT Collector) is deployed with an endpoint of `http://localhost:4318`. This is the default exporter endpoint used by EDOT Node.js. In this case the `OTEL_EXPORTER_OTLP_ENDPOINT` environment variable does not need to be set.
:::

### Additional common configuration

Some other common configuration settings that are good to know:

* `OTEL_RESOURCE_ATTRIBUTES=service.version=<app-version>,deployment.environment=production`: This environment variable can be used to set additional [Resource attributes](https://opentelemetry.io/docs/languages/js/resources/). Setting `service.version` can be useful for correlating issues to different versions of your service. Setting `deployment.environment` can be useful for separating telemetry for development, test, qa, or production deployments of your services.
* `OTEL_NODE_DISABLED_INSTRUMENTATIONS=net,dns,...`: A comma-separated list of instrumentation names to disable. This can be useful if a particular instrumentation is unwanted for some reason.
* `OTEL_LOG_LEVEL=verbose`: This can be used to get more internal logging data from EDOT Node.js when investigating issues with telemetry.
* `OTEL_SDK_DISABLED=true`: This can be used to fully disable EDOT Node.js, perhaps when troubleshooting.

For more information on all the available configuration options, refer to [Configuration](../configuration.md).


## Start EDOT Node.js

For EDOT Node.js to automatically instrument modules used by your Node.js service, it must be started before you `require` or `import` your service code's dependencies -- for example, before `express` or `http` are loaded.

The recommended way to start EDOT Node.js is by using the `--import` Node.js [CLI option](https://nodejs.org/api/cli.html#--importmodule). This loads and starts the SDK in Node.js' "preload" phase, which ensures that it is started before any application modules.

```sh
node --import @elastic/opentelemetry-node my-app.js
```

This `--import` option can also be specified in the `NODE_OPTIONS` environment variable:

```bash
export NODE_OPTIONS="--import @elastic/opentelemetry-node"
node my-app.js
```

<!-- TODO: Refer to other ways to start the SDK when have ref for that. -->

EDOT Node.js will automatically instrument popular modules (listed in [Supported technologies](../supported-technologies.md)) used by your service, and send traces, metrics, and logs telemetry data (using OTLP) to your configured observability backend.

## Confirm instrumentation is working

To confirm that EDOT Node.js has be setup successfully:

1. Call your running service to ensure it has had some activity that EDOT Node.js can trace.
2. Go to **Applications** → **Service Inventory** in your Elastic deployment.
3. You should see the name of your service. (It can take a minute or two after starting your service with EDOT Node.js for the service to show up in this list.)

If you do not see your service, work through [the Troubleshooting guide](../troubleshooting.md).

