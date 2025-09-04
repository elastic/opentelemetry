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

The [Elastic Distributions of OpenTelemetry (EDOT)](/reference/index.md) are based on the contrib OpenTelemetry project but include additional features and configurations that are specific to the Elastic ecosystem. Each EDOT component is carefully selected and tested to ensure it works seamlessly with Elastic Stack components.

Here are some key differences and considerations when using EDOT compared to contrib OpenTelemetry Collector:

| Feature | EDOT | Contrib |
|---------|------|------------------------|
| Configuration | Configured for Elastic Observability. | Requires manual configuration.|
| Support | Official Elastic support with SLAs. | Community support only. |
| Integration | Seamless integration with Elastic Stack. | Requires additional configuration for Elastic. |
| Components | Curated list of components for Elastic Observability. | Generic components that may not support all Elastic features. |
| Deployment | Easier to deploy with Elastic Stack. | Requires manual setup and configuration. |
| Central management | Central management of OTel SDKs and Collectors. | No central management. |
| Compatibility | Fully compatible with Elastic Stack components. | Compatible but may require additional configuration. |
| Self-managed/ECH | Required for full functionality. | Compatible but without guaranteed support. |
| Updates | Future updates aligned with Elastic Stack releases. | Updates depend on contrib OpenTelemetry release cycle. |
| EDOT-specific components | Includes custom components optimized for Elastic. | Uses standard OpenTelemetry components. |

EDOT offers a streamlined experience with less configuration burden compared to contrib OpenTelemetry Collector. While you can use contrib components with Elastic, these components aren't covered under official Elastic support SLAs.

## EDOT Collector compared to contrib OpenTelemetry Collector

The OpenTelemetry project does not provide a single, recommended distribution of the OpenTelemetry Collector for production use. Instead, it offers a variety of components that can be assembled into a custom Collector. Using the contrib Collector requires careful selection and configuration of components, which can be complex and time-consuming.

EDOT Collector is a curated version of the OpenTelemetry Collector that includes specific components and configurations optimized for Elastic Observability. It is designed to work seamlessly with Elastic Stack components, such as Elasticsearch and Kibana, and provides additional features that are not available in the contrib OpenTelemetry Collector.

For a complete list of components included in the EDOT Collector, refer to [EDOT Collector components](/reference/edot-collector/components.md).
