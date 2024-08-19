# Build a custom collector or configure the OpenTelemetry Collector Contrib distribution

You can build and configure a [custom collector](https://opentelemetry.io/docs/collector/custom-collector/) or extend the [OpenTelemetry Collector Contrib ](https://github.com/open-telemetry/opentelemetry-collector-contrib) distribution to collect logs and metrics and send them to Elastic Observability.

For a more seamless experience, use the Elastic Distribution of the OpenTelemetry Collector.
Refer to the [guided onboarding](guided-onboarding.md) docs or the [manual configuration](manual-configuration.md) docs for more on configuring the Elastic Distribution of the OpenTelemetry Collector.

## Upstream collector configuration examples

Use the Elastic [example configurations](https://github.com/elastic/elastic-agent/tree/main/internal/pkg/otel/samples) as a reference when configuring your upstream collector.

## Build a custom collector for MacOS or Linux

To build a custom collector to collect your telemetry data from a MacOS or Linux system and send it to Elastic Observability, complete the following steps.

### Step 1. Install the OpenTelemetry Collector builder
Install the OpenTelemetry Collector builder (ocb) using the following command:

`go install go.opentelemetry.io/collector/cmd/builder@latest
`

### Step 2. Create a builder configuration file
Create a builder configuration file (for example, `builder-config.yml`) that defines your custom collector. This file specifies the components (receivers, exporters, processors, and extensions) included in your custom collector.

Refer to the following example `builder-config.yml`:

``` yaml
dist:
  name: "custom-otel-collector"
  description: "Custom OpenTelemetry Collector"
  output_path: "./build"

receivers:
  - gomod: "github.com/open-telemetry/opentelemetry-collector-contrib/receiver/hostmetricsreceiver v0.103.0"
  - gomod: "github.com/open-telemetry/opentelemetry-collector-contrib/receiver/filelogreceiver v0.103.0"

processors:
  - gomod:  "github.com/open-telemetry/opentelemetry-collector-contrib/processor/resourcedetectionprocessor v0.103.0"
  - gomod:  "github.com/elastic/opentelemetry-collector-components/processor/elasticinframetricsprocessor v0.5.1"
  - gomod: "github.com/open-telemetry/opentelemetry-collector-contrib/processor/resourceprocessor v0.103.0"
  - gomod: "github.com/open-telemetry/opentelemetry-collector-contrib/processor/attributesprocessor v0.103.0"

exporters:
  - gomod: "go.opentelemetry.io/collector/exporter/otlphttpexporter v0.103.0"
  - gomod: "go.opentelemetry.io/collector/exporter/loggingexporter v0.103.0"
  - gomod: "github.com/open-telemetry/opentelemetry-collector-contrib/exporter/elasticsearchexporter v0.103.0"

```

### Step 3. Build the Collector
Build your custom collector using the ocb toll and the configuration file by running the following command:

`builder --config builder-config.yml`

This command generates a new collector in the specified output path (for example, ./build). The generated collector includes onnly the components you specified in the configuration file.

## Build a custom collector for Kubernetes

To build a custom collector to collect your telemetry data from a Kubernetes system and send it to Elastic Observability, complete the following steps.