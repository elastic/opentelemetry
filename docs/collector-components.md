# Elastic Distribution of OpenTelemetry Collector components

The OpenTelemetry Collector uses the following components to receive, process, and export telemetry data:

- [Receivers](collector-components.md#receivers): Collect telemetry from your host.
- [Processors](collector-components.md#processors): Modify or transform telemetry data before sending it to the exporters.
- [Exporters](collector-components.md#exporters): Send data to the backends or destinations.
- [Extensions](collector-components.md#extensions): Provide additional functionalities and capabilities.

The default configurations of the Elastic Distribution of the OpenTelemetry (EDOT) Collector follows these flows:

**MacOS and Linux host metrics**

![Flow for MacOS and Linux Host metrics](images/macos-and-linux-host-metrics.png)

**MacOS and Linux logs**

![Flow for MacOS and Linux logs](images/macos-and-linux-logs.png)

**Kubernetes metrics**

![Flow for Kubernetes metrics](images/kubernetes-metrics.png)

**Kubernetes, MacOS, and Linux logs**

![Flow for Kubernetes, MacOS, and Linux logs](images/kubernetes-macos-and-linux-logs.png)

Refer to the [Elastic Distribution for OpenTelemetry Collector docs](https://github.com/elastic/elastic-agent/blob/main/internal/pkg/otel/README.md#components) for more information on the components included in the EDOT Collector.
Follow the links for OpenTelemetry documentation with more configuration details for each component.
To set up the EDOT Collector, get started using the [guided onboarding](guided-onboarding.md) docs or the [manual configuration](manual-configuration.md) docs.
