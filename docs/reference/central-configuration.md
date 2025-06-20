---
navigation_title: Central configuration
description: Reference documentation for the central configuration of EDOT SDKs.
applies_to:
  deployment:
      ess: preview 9.1
  stack: preview 9.1
products:
  - id: cloud
  - id: observability
  - id: kibana
---

# Central configuration for EDOT SDKs

You can manage {{edot}} (EDOT) SDKs through the APM central configuration feature in the Applications UI. Changes are automatically propagated to the deployed [EDOT SDKs](./edot-sdks/index.md). Refer to [APM central configuration](docs-content://solutions/observability/apm/apm-agent-central-configuration.md) for more information.

## Prerequisites

To use central configuration for EDOT SDKs, you need:

* An Elastic self-managed or {{ecloud}} deployment, version 9.1 or higher.
* [EDOT Collector](./edot-collector/index.md) in standalone mode.
* [EDOT SDKs](./edot-sdks/index.md) instrumenting your application.

The following versions of EDOT support central configuration:

| Component | Minimum Version |
|-----------|----------------|
| EDOT Collector | 9.1 / 8.19 or higher |
| EDOT Java | 1.5.0 or higher |
| EDOT Node.js | 1.2.0 or higher |
| EDOT PHP | 1.1.0 or higher |
| EDOT Python | 1.4.0 or higher |

::::{note}
Serverless deployments are not currently supported.
::::

## Activate central management

To activate central management for EDOT SDKs, follow these steps.

:::::{stepper}

::::{step} Edit the EDOT Collector configuration

Edit the EDOT Collector configuration file to use central configuration. Refer to [EDOT Collector configuration](./edot-collector/config/default-config-standalone.md#central-configuration).

Restart the Elastic Agent to apply the changes.

::::

::::{step} Edit the EDOT SDK configuration

Edit the EDOT SDK configuration file to use central configuration. Refer to each EDOT SDK documentation for more information:

- [EDOT Java](./edot-sdks/java/configuration.md#central-configuration)
- [EDOT Node.js](./edot-sdks/nodejs/configuration.md#central-configuration)
- [EDOT PHP](./edot-sdks/php/configuration.md#central-configuration)
- [EDOT Python](./edot-sdks/python/configuration.md#central-configuration)

Restart the instrumented application to apply the changes.

::::

::::{step} Check that the EDOT SDK appears in central configuration

After some minutes, go to Kibana and check that the EDOT SDK appears in central configuration.

1. Go to **Kibana** → **Observability** → **Applications** and select a service.
2. Select **Settings** and go to **Agent Configuration**.

::::

:::::{stepper}
