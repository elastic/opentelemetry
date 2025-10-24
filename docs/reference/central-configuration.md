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

Manage {{edot}} (EDOT) SDKs through the {{product.apm-agent}} Central Configuration feature in the Applications UI. Changes are automatically propagated to the deployed EDOT SDKs. Refer to [{{product.apm-agent}} Central Configuration](docs-content://solutions/observability/apm/apm-agent-central-configuration.md) for more information.

This feature implements the Open Agent Management Protocol (OpAMP). Refer to [Open Agent Management Protocol
](https://opentelemetry.io/docs/specs/opamp/) for more information.

## Architecture

The central configuration architecture for the {{edot}} (EDOT) provides a robust and scalable mechanism for managing fleets of EDOT SDKs remotely. The data flow, illustrated in this diagram, ensures that configuration changes are efficiently propagated from a central management point to each individual agent.

:::{image} ./images/central-config-edot.png
:alt: Diagram of Central config architecture
:::

The process starts within {{product.kibana}}, where administrators create and manage settings for the EDOT SDKs. Once defined, settings are written to and persisted in {{es}}, which acts as the single source of truth. The EDOT Collector, when configured in Gateway mode, includes the Elastic {{product.apm}} Config Extension, which reads the SDK settings from {{product.elasticsearch}}, making them available for distribution.

Each EDOT SDK contains an embedded OpAMP Client. Following the Open Agent Management Protocol (OpAMP), these clients periodically poll the OpAMP server, bundled with the Collector's {{product.apm}} Config Extension, over HTTP. This polling action allows the SDKs to retrieve the latest configuration updates, enabling dynamic and centralized control over their behavior without requiring manual intervention or redeployment.

## Prerequisites

To use {{product.apm-agent}} Central Configuration for EDOT SDKs, you need:

* An Elastic self-managed or {{ecloud}} deployment, version 9.1 or higher.
* A standalone [EDOT Collector](elastic-agent://reference/edot-collector/index.md), in either Agent or Collector mode.
* EDOT SDKs instrumenting your application.

The following versions of EDOT and {{stack}} support central configuration:

| Component | Minimum version |
|-----------|----------------|
| {{kib}} | 9.1 or higher |
| EDOT Collector | 8.19, 9.1 or higher |
| EDOT Android | 1.2.0 or higher |
| EDOT iOS | 1.4.0 or higher |
| EDOT Java | 1.5.0 or higher |
| EDOT Node.js | 1.2.0 or higher |
| EDOT PHP | 1.1.1 or higher |
| EDOT Python | 1.4.0 or higher |

::::{note}
Serverless deployments are not currently supported.
::::

## Activate central configuration

To activate {{product.apm-agent}} Central Configuration for EDOT SDKs, follow these steps.

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

Refer to [Secure connection](elastic-agent://reference/edot-collector/config/default-config-standalone.md#secure-connection) if you need to secure the connection between the EDOT Collector and Elastic using TLS or mutual TLS.

:::::

:::::{step} Set the environment variables for the SDKs

Activate the central configuration feature in the SDKs by setting the `ELASTIC_OTEL_OPAMP_ENDPOINT` environment variable to the URL endpoint of the `apmconfig` extension that you configured in the previous step. For example:

```sh
export ELASTIC_OTEL_OPAMP_ENDPOINT="http://localhost:4320/v1/opamp"
```

If the OpAMP server in the Collector requires authentication set the `ELASTIC_OTEL_OPAMP_HEADERS` environment variable.

```sh
export ELASTIC_OTEL_OPAMP_HEADERS="Authorization=ApiKey an_api_key"
```

Restart the instrumented application to apply the changes.

:::{important}
Support for the `ELASTIC_OTEL_OPAMP_HEADERS` environment variable depends on each SDK. Refer to the configuration reference of each EDOT SDK for more information.
:::

:::::

:::::{step} Check that the EDOT SDK shows up

Wait some time for the EDOT SDK to appear in {{kib}} under Agent Configuration.

1. Go to **{{kib}}** → **Observability** → **Applications** and select a service.
2. Select **Settings** and go to **Agent Configuration**.

Your application must produce and send telemetry data for the EDOT SDK to appear in Agent Configuration. This is because central configuration requires an application name as the key, which can't be defined until the application name is associated with the EDOT SDK agent after receiveing telemetry.

:::{note}
Central configuration uses the `service.name` and `deployment.environment.name` OpenTelemetry resource attributes to target specific instances with a configuration. If no environment is specified, the central configuration feature will match `All` as the environment.
:::

:::::

::::::

## Supported settings

For a list of settings that you can configure through {{product.apm-agent}} Central Configuration, refer to the configuration reference of each EDOT SDK:

- [EDOT Android](apm-agent-android://reference/edot-android/configuration.md#central-configuration)
- [EDOT iOS](apm-agent-ios://reference/edot-ios/configuration.md#central-configuration-edot)
- [EDOT Java](elastic-otel-java://reference/edot-java/configuration.md#central-configuration)
- [EDOT Node.js](elastic-otel-node://reference/edot-node/configuration.md#central-configuration)
- [EDOT PHP](elastic-otel-php://reference/edot-php/configuration.md#central-configuration)
- [EDOT Python](elastic-otel-python://reference/edot-python/configuration.md#central-configuration)

## Advanced configuration

```{applies_to}
stack: preview 9.2
```

The **Advanced Configuration** feature allows you to define custom configuration options as key-value pairs. Settings are passed directly to your EDOT SDK.

:::{warning}
Use this feature with caution. An incorrect or incompatible setting might affect the behavior of the EDOT SDK.
:::

## Deactivate central configuration

To deactivate central configuration, remove the `ELASTIC_OTEL_OPAMP_ENDPOINT` environment variable.

Restart the instrumented application to apply the changes.
