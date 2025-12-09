---
navigation_title: EDOT compared to contrib Collector
description: Differences between Elastic Distributions of OpenTelemetry (EDOT) and contrib OpenTelemetry Collector.
applies_to:
  stack:
  serverless:
    observability:
products:
  - id: cloud-serverless
  - id: observability
  - id: edot-collector
  - id: edot-sdk
---

# EDOT compared to contrib OpenTelemetry Collector

The [Elastic Distributions of OpenTelemetry (EDOT)](/reference/index.md) are built using components from the Contrib OpenTelemetry project. The EDOT Collector includes additional features and configurations that enable a smoother experience when collecting and forwarding telemetry to the Elastic ecosystem. Each OpenTelemetry component that is selected for EDOT is carefully tested to ensure it works seamlessly with Elastic Stack components.

When working with OpenTelemetry and Elastic, **EDOT is optional and never required for data collection on the edge machines**. Elastic remains vendor agnostic because users can run any upstream or third-party collector. EDOT is available for teams that want supported, production grade packaging without changing their existing architecture.

Here are some key differences and considerations when using EDOT compared to contrib OpenTelemetry Collector:

| Feature | EDOT | Contrib |
|---------|------|------------------------|
| Configuration | Configured for Elastic Observability. | Requires manual configuration.|
| Support | Official Elastic support with SLAs. | Community support only. |
| Integration | Seamless integration with Elastic Stack. | Requires additional configuration for Elastic. |
| Components | Curated list of components for Elastic Observability. | Components that may not be mature or introduce potential unwanted code or features. |
| Deployment | Same methods of deployment as upstream, including configuration. | Requires manual setup and configuration. |
| Central management | Central management of OTel SDKs and Collectors. | No central management. |
| Compatibility | Fully tested with Elastic Stack components. | Components might be compatible but are not tested for guaranteed support. |
| Updates | Future updates aligned with Elastic Stack releases. | Updates depend on contrib OpenTelemetry release cycle. |

## EDOT Collector compared to contrib OpenTelemetry Collector

The OpenTelemetry project does not provide a single, recommended distribution of the OpenTelemetry Collector for production use. Instead, it offers a variety of components that can be assembled into a custom Collector. Using the contrib Collector requires careful selection and configuration of components, which can be complex and time-consuming.

EDOT Collector is a curated version of the OpenTelemetry Collector that includes specific components and configurations optimized for Elastic Observability. It is designed to work seamlessly with Elastic Stack components, such as Elasticsearch and Kibana, and provides additional features that aren't currently available in the Contrib Collector. Most of these features will be contributed to upstream in the future.

For a complete list of components included in the EDOT Collector, refer to [EDOT Collector components](elastic-agent://reference/edot-collector/components.md).
