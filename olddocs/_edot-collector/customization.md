---
title: Customization
layout: default
nav_order: 5
---

# Customization

The EDOT Collector comes with a [curated list](./components) of OTel Collector components and some opinionated [configuration samples](https://github.com/elastic/elastic-agent/tree/v{{ site.edot_versions.collector }}/internal/pkg/otel/samples).

If your use case requires additional components, you have two options:

1. [Build your custom, EDOT-like collector](./custom-collector) 
2. [Open a request](https://github.com/elastic/opentelemetry/issues/new/choose) to add those components to EDOT 

Requests for adding new components to the EDOT Collector will be reviewed and decided on the basis of the popularity of the requests, technical suitability and other criteria. 

{: .note }
> Custom collector builds are *not* covered through [Elastic's Support](https://www.elastic.co/support_policy).
