# Build a custom collector or configure the OpenTelemetry Collector Contrib distribution

You can build and configure a [custom collector](https://opentelemetry.io/docs/collector/custom-collector/) or extend the [OpenTelemetry Collector Contrib ](https://github.com/open-telemetry/opentelemetry-collector-contrib) distribution to collect logs and metrics and send them to Elastic Observability.

For a more seamless experience, use the Elastic Distribution of the OpenTelemetry Collector.
Refer to the [guided onboarding](guided-onboarding.md) docs or the [manual configuration](manual-configuration.md) docs for more on configuring the Elastic Distribution of the OpenTelemetry Collector.

## Upstream collector configuration examples

Use the Elastic [example configurations](https://github.com/elastic/elastic-agent/tree/main/internal/pkg/otel/samples) as a reference when configuring your upstream collector.

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

The following example `builder-config.yml` file contains the components needed to send your telemetry data to Elastic Observability. For more information on these components, refer to the [components](collector-components.md) documentation. Keep or remove components from the example configuration file to fit your needs.

``` yaml
dist:
  name: otelcol-dev
  description: Basic OTel Collector distribution for Developers
  output_path: ./otelcol-dev
  otelcol_version: 0.107.0

extensions:
  - gomod: github.com/open-telemetry/opentelemetry-collector-contrib/extension/healthcheckextension v0.106.1
  - gomod: github.com/open-telemetry/opentelemetry-collector-contrib/extension/storage/filestorage v0.106.1
  - gomod: go.opentelemetry.io/collector/extension/memorylimiterextension v0.106.1

exporters:
  - gomod: github.com/open-telemetry/opentelemetry-collector-contrib/exporter/elasticsearchexporter v0.106.1
  - gomod: github.com/open-telemetry/opentelemetry-collector-contrib/exporter/fileexporter v0.106.1
  - gomod: go.opentelemetry.io/collector/exporter/debugexporter v0.106.1
  - gomod: go.opentelemetry.io/collector/exporter/otlpexporter v0.106.1
  - gomod: go.opentelemetry.io/collector/exporter/otlphttpexporter v0.106.1

processors:
  - gomod: go.opentelemetry.io/collector/processor/memorylimiterprocessor v0.106.1
  - gomod: github.com/open-telemetry/opentelemetry-collector-contrib/processor/attributesprocessor v0.106.1
  - gomod: github.com/open-telemetry/opentelemetry-collector-contrib/processor/filterprocessor v0.106.1
  - gomod: github.com/open-telemetry/opentelemetry-collector-contrib/processor/k8sattributesprocessor v0.106.1
  - gomod: github.com/open-telemetry/opentelemetry-collector-contrib/processor/resourcedetectionprocessor v0.106.1
  - gomod: github.com/open-telemetry/opentelemetry-collector-contrib/processor/resourceprocessor v0.106.1
  - gomod: github.com/open-telemetry/opentelemetry-collector-contrib/processor/transformprocessor v0.106.1
  - gomod: go.opentelemetry.io/collector/processor/batchprocessor v0.106.1

receivers:
  - gomod: github.com/open-telemetry/opentelemetry-collector-contrib/receiver/jaegerreceiver v0.106.1
  - gomod: github.com/open-telemetry/opentelemetry-collector-contrib/receiver/prometheusreceiver v0.106.1
  - gomod: github.com/open-telemetry/opentelemetry-collector-contrib/receiver/zipkinreceiver v0.106.1
  - gomod: github.com/open-telemetry/opentelemetry-collector-contrib/receiver/filelogreceiver v0.106.1
  - gomod: github.com/open-telemetry/opentelemetry-collector-contrib/receiver/hostmetricsreceiver v0.106.1
  - gomod: github.com/open-telemetry/opentelemetry-collector-contrib/receiver/httpcheckreceiver v0.106.1
  - gomod: github.com/open-telemetry/opentelemetry-collector-contrib/receiver/k8sclusterreceiver v0.106.1
  - gomod: github.com/open-telemetry/opentelemetry-collector-contrib/receiver/k8sobjectsreceiver v0.106.1
  - gomod: github.com/open-telemetry/opentelemetry-collector-contrib/receiver/kubeletstatsreceiver v0.106.1
  - gomod: go.opentelemetry.io/collector/receiver/otlpreceiver v0.106.1

connectors:
  - gomod: 	github.com/open-telemetry/opentelemetry-collector-contrib/connector/spanmetricsconnector v0.106.1
```

### Step 3. Build the Collector
Build your custom collector using the ocb tool and the configuration file by running the following command:

`builder --config builder-config.yml`

This command generates a new collector in the specified output path, `otelcol-dev`. The generated collector includes the components you specified in the configuration file.

For general information on building a custom collector, refer to the [OpenTelemetry documentation](https://opentelemetry.io/docs/collector/custom-collector/#step-1---install-the-builder).