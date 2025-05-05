---
navigation_title: Customization
description: Options for customizing the EDOT Collector, including building a custom collector or requesting new components.
applies_to:
  stack:
  serverless:
---

# Customization

The EDOT Collector comes with a [curated list](./components) of OTel Collector components and some opinionated [configuration samples](https://github.com/elastic/elastic-agent/tree/v{{ site.edot_versions.collector }}/internal/pkg/otel/samples).

If your use case requires additional components, you have two options:

1. [Build your custom, EDOT-like collector](./custom-collector)
2. [Open a request](https://github.com/elastic/opentelemetry/issues/new/choose) to add those components to EDOT

Requests for adding new components to the EDOT Collector will be reviewed and decided on the basis of the popularity of the requests, technical suitability and other criteria.

:::{note}
Custom collector builds are *not* covered through [Elastic's Support](https://www.elastic.co/support_policy).
:::

:::{note}
For more information on building a custom collector, refer to the [OpenTelemetry documentation](https://opentelemetry.io/docs/collector/custom-collector/).
:::
