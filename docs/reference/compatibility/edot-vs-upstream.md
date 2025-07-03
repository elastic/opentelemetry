---
navigation_title: EDOT compared to upstream OTel
description: Differences between Elastic Distributions of OpenTelemetry (EDOT) and upstream OpenTelemetry.
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

# EDOT compared to upstream OpenTelemetry

The [Elastic Distributions of OpenTelemetry (EDOT)](/reference/index.md) are based on the upstream OpenTelemetry project but include additional features and configurations that are specific to the Elastic ecosystem. Each EDOT component is carefully selected and tested to ensure it works seamlessly with Elastic Stack components.

Here are some key differences and considerations when using EDOT compared to upstream OpenTelemetry:

| Feature | EDOT | Upstream OpenTelemetry |
|---------|------|------------------------|
| Configuration | Configured for Elastic Observability. | Requires manual configuration.|
| Support | Official Elastic support with SLAs. | Community support only. |
| Integration | Seamless integration with Elastic Stack. | Requires additional configuration for Elastic. |
| Components | Curated list of components for Elastic Observability. | Generic components that may not support all Elastic features. |
| Deployment | Easier to deploy with Elastic Stack. | Requires manual setup and configuration. |
| Compatibility | Fully compatible with Elastic Stack components. | Compatible but may require additional configuration. |
| Self-managed/ECH | Required for full functionality. | Compatible but without guaranteed support. |
| Updates | Future updates aligned with Elastic Stack releases. | Updates depend on upstream OpenTelemetry release cycle. |
| EDOT-specific components | Includes custom components optimized for Elastic. | Uses standard OpenTelemetry components. |

EDOT offers a streamlined experience with less configuration burden compared to upstream OpenTelemetry. While you can use upstream components with Elastic, these components aren't covered under official Elastic support SLAs.

## EDOT Collector compared to upstream OTel Collector

The OpenTelemetry project does not provide a single, recommended distribution of the OpenTelemetry Collector for production use. Instead, it offers a variety of components that can be assembled into a custom Collector. Using the upstream Collector requires careful selection and configuration of components, which can be complex and time-consuming.

EDOT Collector is a curated version of the OpenTelemetry Collector that includes specific components and configurations optimized for Elastic Observability. It is designed to work seamlessly with Elastic Stack components, such as Elasticsearch and Kibana, and provides additional features that are not available in the upstream OpenTelemetry Collector.

For a complete list of components included in the EDOT Collector, refer to [EDOT Collector components](/reference/edot-collector/components.md).
