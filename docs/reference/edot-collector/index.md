---
navigation_title: EDOT Collector
description: Introduction to the Elastic Distribution of OpenTelemetry (EDOT) Collector, a curated and supported distribution of the OpenTelemetry Collector.
applies_to:
  stack:
  serverless:
    observability:
products:
  - cloud-serverless
  - observability
  - edot-collector
---

# Elastic Distribution of OpenTelemetry Collector

The Elastic Distribution of OpenTelemetry (EDOT) Collector is an open-source distribution of the OpenTelemetry Collector. 

## Get started

To install the EDOT Collector with basic settings in your environment, follow the [quickstart guides](../quickstart/index.md).

## Configure the Collector

You can configure the EDOT Collector to use the standard OTel collector configuration file or `values.yml` file if you have deployed it using Helm.

For full details on each option, see [Configuration](./config/index.md)

## Collector components

Built on OpenTelemetry’s modular architecture, the EDOT Collector offers a curated and fully supported selection of components designed for production-grade reliability.

Refer to [Components](./components.md) for the full list of components embedded in the EDOT Collector.

To request a component to be added to EDOT Collector, submit a [GitHub issue here](https://github.com/elastic/elastic-agent/issues/new/choose).

## Limitations 

The EDOT collector inherits the same limitations from the upstream components. Refer to [Limitations](../compatibility/limitations.md) for a complete list.

## License

For details on the EDOT Collector license, see the [LICENSE.txt](https://github.com/elastic/elastic-agent/blob/main/LICENSE.txt) file.