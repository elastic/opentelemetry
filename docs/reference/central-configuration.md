---
navigation_title: Central configuration
description: Reference documentation for the central configuration of EDOT SDKs.
applies_to:
  deployment:
      ess: preview 9.1
  stack: preview 9.1
  serverless: unavailable
products:
  - id: observability
  - id: kibana
  - id: edot-collector
---

# Central configuration for EDOT SDKs

Manage {{edot}} (EDOT) SDKs through the APM Agent Central Configuration feature in the Applications UI. Changes are automatically propagated to the deployed [EDOT SDKs](/reference/edot-sdks/index.md). Refer to [APM Agent Central Configuration](docs-content://solutions/observability/apm/apm-agent-central-configuration.md) for more information.

This feature implements the Open Agent Management Protocol (OpAMP). Refer to [Open Agent Management Protocol
](https://opentelemetry.io/docs/specs/opamp/) for more information.

## Prerequisites

To use APM Agent Central Configuration for EDOT SDKs, you need:

* An Elastic self-managed or {{ecloud}} deployment, version 9.1 or higher.
* A standalone [EDOT Collector](/reference/edot-collector/index.md), in either Agent or Collector mode.
* [EDOT SDKs](/reference/edot-sdks/index.md) instrumenting your application.

The following versions of EDOT and {{stack}} support central configuration:

| Component | Minimum version |
|-----------|----------------|
| Kibana | 9.1 or higher |
| EDOT Collector | 8.19, 9.1 or higher |
| EDOT Android | 1.2.0 or higher |
| EDOT Java | 1.5.0 or higher |
| EDOT Node.js | 1.2.0 or higher |
| EDOT PHP | 1.1.1 or higher |
| EDOT Python | 1.4.0 or higher |

::::{note}
Serverless deployments are not currently supported.
::::

## Activate central configuration

To activate APM Agent Central Configuration for EDOT SDKs, follow these steps.

:::::{stepper}

::::{step} Edit the EDOT Collector configuration

Edit the EDOT Collector configuration file to use the `apmconfig` extension. You need a valid {{es}} API key to authenticate to the {{es}} endpoint. 

:::{include} _snippets/retrieve-credentials.md
:::

The example configuration is:

```yaml
extensions:
  bearertokenauth:
    scheme: "APIKey"
    token: "<ENCODED_ELASTICSEARCH_APIKEY>"

  apmconfig:
    opamp:
      protocols:
        http:
          # Default is localhost:4320
          # endpoint: "<CUSTOM_OPAMP_ENDPOINT>"
    source:
      elasticsearch:
        endpoint: "<ELASTICSEARCH_ENDPOINT>"
        auth:
          authenticator: bearertokenauth
```

Restart the Elastic Agent to also restart the Collector and apply the changes. Refer to [EDOT Collector configuration](/reference/edot-collector/config/default-config-standalone.md#central-configuration) for more information.

::::

::::{step} Set the environment variable for the SDKs

Activate the central configuration feature in the SDKs by setting the `ELASTIC_OTEL_OPAMP_ENDPOINT` environment variable to the URL endpoint of the `apmconfig` extension that you configured in the previous step. For example:

```sh
export ELASTIC_OTEL_OPAMP_ENDPOINT="http://localhost:4320/v1/opamp"
```

Restart the instrumented application to apply the changes.

:::{note}
Central configuration uses the `service.name` and `deployment.environment.name` OpenTelemetry resource attributes to target specific instances with a configuration. If no environment is specified, the central configuration feature will match `All` as the environment.
:::

::::

::::{step} Check that the EDOT SDK appears in central configuration

Wait some time for the EDOT SDK to appear in {{kib}} under Agent Configuration.

1. Go to **{{kib}}** → **Observability** → **Applications** and select a service.
2. Select **Settings** and go to **Agent Configuration**.

:::{note}
Your application must produce and send telemetry data for the EDOT SDK to appear in Agent Configuration.
:::

::::

:::::{stepper}

## Supported settings

For a list of settings that you can configure through APM Agent Central Configuration, refer to the configuration reference of each EDOT SDK:

- [EDOT Android](/reference/edot-sdks/android/configuration.md#central-configuration)
- [EDOT Java](/reference/edot-sdks/java/configuration.md#central-configuration)
- [EDOT Node.js](/reference/edot-sdks/nodejs/configuration.md#central-configuration)
- [EDOT PHP](/reference/edot-sdks/php/configuration.md#central-configuration)
- [EDOT Python](/reference/edot-sdks/python/configuration.md#central-configuration)

EDOT iOS currently supports APM Agent Central Configuration through APM Server. Refer to [EDOT iOS configuration](/reference/edot-sdks/ios/configuration.md) for more details.