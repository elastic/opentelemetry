# Configure a custom collector or the OpenTelemetry Collector Contrib distribution

You can build and configure a [custom collector](https://opentelemetry.io/docs/collector/custom-collector/) or extend the [OpenTelemetry Collector Contrib ](https://github.com/open-telemetry/opentelemetry-collector-contrib) distribution to collect logs and metrics and send them to Elastic Observability.

For a more seamless experience, use the Elastic Distribution for the OpenTelemetry Collector.
Refer to the [guided onboarding](guided-onboarding.md) docs or the [manual configuration](manual-configuration.md) docs for more on configuring the Elastic Distribution for the OpenTelemetry Collector.

## Upstream collector configuration examples
Refer to the OpenTelemetry documentation on [building a custom collector](https://opentelemetry.io/docs/collector/custom-collector/) for more on creating an upstream collector.
Use the Elastic [example configurations](https://github.com/elastic/elastic-agent/tree/main/internal/pkg/otel/samples) as a reference when configuring your upstream collector.