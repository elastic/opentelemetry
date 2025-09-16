---
navigation_title: Central configuration
description: Reference documentation for the central configuration of EDOT SDKs.
applies_to:
  deployment:
      ess: preview 9.1
  stack: preview 9.1
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
* A standalone [EDOT Collector](elastic-agent://reference/edot-collector/index.md), in either Agent or Collector mode.
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

::::::{stepper}

:::::{step} Retrieve your credentials

You need a valid {{es}} API key to authenticate to the {{es}} endpoint. 

::::{include} _snippets/retrieve-credentials.md
::::

Make sure the API key has `config_agent:read` permissions and resources set to `-`.

::::{dropdown} Example JSON payload
```json
POST /_security/api_key
{
  "name": "apmconfig-opamp-test-sdk",
  "metadata": {
    "application": "apm"
  },
  "role_descriptors": {
    "apm": {
      "cluster": [],
      "indices": [],
      "applications": [
        {
          "application": "apm",
          "privileges": [
            "config_agent:read"
          ],
          "resources": [
            "*"
          ]
        }
      ],
      "run_as": [],
      "metadata": {}
    }
  }
}
```
::::

:::::

:::::{step} Edit the EDOT Collector configuration

Edit the [EDOT Collector configuration](elastic-agent://reference/edot-collector/config/default-config-standalone.md#central-configuration) to activate the central configuration feature:

:::{include} _snippets/edot-collector-auth.md
:::

Restart the Elastic Agent to also restart the Collector and apply the changes.

::::{note}
Refer to [Secure connection](elastic-agent://reference/edot-collector/config/default-config-standalone.md#secure-connection) if you need to secure the connection between the EDOT Collector and Elastic using TLS or mutual TLS.
::::
:::::

:::::{step} Set the environment variable for the SDKs

Activate the central configuration feature in the SDKs by setting the `ELASTIC_OTEL_OPAMP_ENDPOINT` environment variable to the URL endpoint of the `apmconfig` extension that you configured in the previous step. For example:

```sh
export ELASTIC_OTEL_OPAMP_ENDPOINT="http://localhost:4320/v1/opamp"
```

Restart the instrumented application to apply the changes.

:::{note}
Central configuration uses the `service.name` and `deployment.environment.name` OpenTelemetry resource attributes to target specific instances with a configuration. If no environment is specified, the central configuration feature will match `All` as the environment.
:::

:::::

:::::{step} Check that the EDOT SDK shows up

Wait some time for the EDOT SDK to appear in {{kib}} under Agent Configuration.

1. Go to **{{kib}}** → **Observability** → **Applications** and select a service.
2. Select **Settings** and go to **Agent Configuration**.

:::{note}
Your application must produce and send telemetry data for the EDOT SDK to appear in Agent Configuration. This is because central configuration requires an application name as the key, which can't be defined until the application name is associated with the EDOT SDK agent after receiveing telemetry. 
:::

:::::

::::::

## Supported settings

For a list of settings that you can configure through APM Agent Central Configuration, refer to the configuration reference of each EDOT SDK:

- [EDOT Android](apm-agent-android://reference/edot-android/configuration.md#central-configuration)
- [EDOT Java](elastic-otel-java://reference/edot-java/configuration.md#central-configuration)
- [EDOT Node.js](elastic-otel-node://reference/edot-node/configuration.md#central-configuration)
- [EDOT PHP](elastic-otel-php://reference/edot-php/configuration.md#central-configuration)
- [EDOT Python](elastic-otel-python://reference/edot-python/configuration.md#central-configuration)

EDOT iOS currently supports APM Agent Central Configuration through APM Server. Refer to [EDOT iOS configuration](apm-agent-ios://reference/configuration.md) for more details.

## Deactivate central configuration

To deactivate central configuration, remove the `ELASTIC_OTEL_OPAMP_ENDPOINT` environment variable.

Restart the instrumented application to apply the changes.
