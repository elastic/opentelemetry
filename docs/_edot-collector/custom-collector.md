---
title: Custom Collector
layout: default
nav_order: 2
parent: Customization
---

# Build a Custom EDOT-like Collector

You can build and configure a [custom collector](https://opentelemetry.io/docs/collector/custom-collector/) or extend the [OpenTelemetry Collector Contrib ](https://github.com/open-telemetry/opentelemetry-collector-contrib) distribution to collect logs and metrics and send them to Elastic Observability.

For a more seamless experience, use the Elastic Distribution of the OpenTelemetry Collector.
Refer to the [configuration](./config/index) docs for more on configuring the EDOT Collector.

## Build a custom collector

To build a custom collector to collect your telemetry data and send it to Elastic Observability, you need to:

1. Install the OpenTelemetry Collector builder (ocb).
1. Create a builder configuration file.
1. Build the collector.

Refer to the following sections to complete these steps.

### Step 1. Install the OpenTelemetry Collector builder
Install the ocb using the command that aligns with you system from the [OpenTelemetry building a custom collector documentation](https://opentelemetry.io/docs/collector/custom-collector/#step-1---install-the-builder).

### Step 2. Create a builder configuration file
Create a builder configuration file,`builder-config.yml`, to define the custom collector. This file specifies the components (extensions, exporters, processors, receivers, and connectors) included in your custom collector.

The following example `builder-config.yml` file contains the components needed to send your telemetry data to Elastic Observability. For more information on these components, refer to the [components](./components) documentation. Keep or remove components from the example configuration file to fit your needs.

<!-- DO NOT DELETE THIS SECTION, TAGS ARE REQUIRED FOR GENERATION-->
<!-- start:edot-collector-components-ocb -->
``` yaml
dist:
  name: otelcol-dev
  description: Basic OTel Collector distribution for Developers
  output_path: ./otelcol-dev
  otelcol_version: 0.120.0

extensions:
  - gomod: github.com/open-telemetry/opentelemetry-collector-contrib/extension/storage/filestorage v0.120.1
  - gomod: github.com/open-telemetry/opentelemetry-collector-contrib/extension/healthcheckextension v0.120.1
  - gomod: github.com/open-telemetry/opentelemetry-collector-contrib/extension/observer/k8sobserver v0.120.1
  - gomod: go.opentelemetry.io/collector/extension/memorylimiterextension v0.120.0
  - gomod: github.com/open-telemetry/opentelemetry-collector-contrib/extension/pprofextension v0.120.1

receivers:
  - gomod: github.com/open-telemetry/opentelemetry-collector-contrib/receiver/filelogreceiver v0.120.1
  - gomod: github.com/open-telemetry/opentelemetry-collector-contrib/receiver/hostmetricsreceiver v0.120.1
  - gomod: github.com/open-telemetry/opentelemetry-collector-contrib/receiver/httpcheckreceiver v0.120.1
  - gomod: github.com/open-telemetry/opentelemetry-collector-contrib/receiver/jaegerreceiver v0.120.1
  - gomod: github.com/open-telemetry/opentelemetry-collector-contrib/receiver/jmxreceiver v0.120.1
  - gomod: github.com/open-telemetry/opentelemetry-collector-contrib/receiver/k8sclusterreceiver v0.120.1
  - gomod: github.com/open-telemetry/opentelemetry-collector-contrib/receiver/k8sobjectsreceiver v0.120.1
  - gomod: github.com/open-telemetry/opentelemetry-collector-contrib/receiver/kafkareceiver v0.120.1
  - gomod: github.com/open-telemetry/opentelemetry-collector-contrib/receiver/kubeletstatsreceiver v0.120.1
  - gomod: github.com/open-telemetry/opentelemetry-collector-contrib/receiver/nginxreceiver v0.120.1
  - gomod: go.opentelemetry.io/collector/receiver/nopreceiver v0.119.0
  - gomod: go.opentelemetry.io/collector/receiver/otlpreceiver v0.120.0
  - gomod: github.com/open-telemetry/opentelemetry-collector-contrib/receiver/prometheusreceiver v0.120.1
  - gomod: github.com/open-telemetry/opentelemetry-collector-contrib/receiver/receivercreator v0.120.1
  - gomod: github.com/open-telemetry/opentelemetry-collector-contrib/receiver/redisreceiver v0.120.1
  - gomod: github.com/open-telemetry/opentelemetry-collector-contrib/receiver/zipkinreceiver v0.120.1

exporters:
  - gomod: go.opentelemetry.io/collector/exporter/debugexporter v0.120.0
  - gomod: github.com/open-telemetry/opentelemetry-collector-contrib/exporter/elasticsearchexporter v0.120.1
  - gomod: github.com/open-telemetry/opentelemetry-collector-contrib/exporter/fileexporter v0.120.1
  - gomod: github.com/open-telemetry/opentelemetry-collector-contrib/exporter/kafkaexporter v0.120.1
  - gomod: github.com/open-telemetry/opentelemetry-collector-contrib/exporter/loadbalancingexporter v0.120.1
  - gomod: go.opentelemetry.io/collector/exporter/otlpexporter v0.120.0
  - gomod: go.opentelemetry.io/collector/exporter/otlphttpexporter v0.120.0

processors:
  - gomod: github.com/open-telemetry/opentelemetry-collector-contrib/processor/attributesprocessor v0.120.1
  - gomod: go.opentelemetry.io/collector/processor/batchprocessor v0.120.0
  - gomod: github.com/elastic/opentelemetry-collector-components/processor/elasticinframetricsprocessor v0.13.0
  - gomod: github.com/elastic/opentelemetry-collector-components/processor/elastictraceprocessor v0.4.1
  - gomod: github.com/open-telemetry/opentelemetry-collector-contrib/processor/filterprocessor v0.120.1
  - gomod: github.com/open-telemetry/opentelemetry-collector-contrib/processor/geoipprocessor v0.120.1
  - gomod: github.com/open-telemetry/opentelemetry-collector-contrib/processor/k8sattributesprocessor v0.120.1
  - gomod: go.opentelemetry.io/collector/processor/memorylimiterprocessor v0.119.0
  - gomod: github.com/open-telemetry/opentelemetry-collector-contrib/processor/resourcedetectionprocessor v0.120.1
  - gomod: github.com/open-telemetry/opentelemetry-collector-contrib/processor/resourceprocessor v0.120.1
  - gomod: github.com/open-telemetry/opentelemetry-collector-contrib/processor/transformprocessor v0.120.1

connectors:
  - gomod: github.com/elastic/opentelemetry-collector-components/connector/elasticapmconnector v0.2.0
  - gomod: github.com/open-telemetry/opentelemetry-collector-contrib/connector/routingconnector v0.120.1
  - gomod: github.com/open-telemetry/opentelemetry-collector-contrib/connector/spanmetricsconnector v0.120.1

providers:
  - gomod: go.opentelemetry.io/collector/confmap/provider/envprovider v1.26.0
  - gomod: go.opentelemetry.io/collector/confmap/provider/fileprovider v1.26.0
  - gomod: go.opentelemetry.io/collector/confmap/provider/httpprovider v1.26.0
  - gomod: go.opentelemetry.io/collector/confmap/provider/httpsprovider v1.26.0
  - gomod: go.opentelemetry.io/collector/confmap/provider/yamlprovider v1.26.0
```
<!-- end:edot-collector-components-ocb -->

### Step 3. Build the Collector
Build your custom collector using the ocb tool and the configuration file by running the following command:

`builder --config builder-config.yml`

This command generates a new collector in the specified output path, `otelcol-dev`. The generated collector includes the components you specified in the configuration file.

For general information on building a custom collector, refer to the [OpenTelemetry documentation](https://opentelemetry.io/docs/collector/custom-collector/#step-1---install-the-builder).
