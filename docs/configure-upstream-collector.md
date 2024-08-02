# Configure an upstream collector

You can configure an upstream collector, like a [custom collector](https://opentelemetry.io/docs/collector/custom-collector/) or [contrib](https://github.com/open-telemetry/opentelemetry-collector-contrib) distribution for the collector, to collect logs and metrics and send them to Elastic Observability.

For a more seamless experience, use the Elastic distribution for the OpenTelemetry collector.
Refer to the [guided onboarding](guided-onboarding.md) docs or the [manual configuration](manual-configuration.md) docs for more on configuring the Elastic distribution.

## Upstream collector configuration examples
Refer to the OpenTelemetry documentation on [building a custom collector](https://opentelemetry.io/docs/collector/custom-collector/) for more on creating an upstream collector.
Use the Elastic [example configurations](https://github.com/elastic/elastic-agent/tree/main/internal/pkg/otel/samples) as a reference when configuring your upstream collector.