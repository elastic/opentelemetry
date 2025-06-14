---
navigation_title: Elastic Distributions of OpenTelemetry (EDOT)
description: Reference documentation for the Elastic Distributions of OpenTelemetry (EDOT).
applies_to:
  stack:
  serverless:
    observability:
products:
  - id: cloud-serverless
  - id: observability
---

# Elastic Distributions of OpenTelemetry

Elastic Distributions of OpenTelemetry (EDOT) is an open-source ecosystem of [OpenTelemetry distributions](https://opentelemetry.io/docs/concepts/distributions/) tailored to Elastic. They include a customized OpenTelemetry Collector and several OpenTelemetry Language SDKs.

![EDOT-Distributions](images/EDOT-SDKs-Collector.png)

Each EDOT distribution is assembled with selected OpenTelemetry components and tested to ensure production readiness. This provides a reliable and optimized OpenTelemetry experience, enabling seamless adoption with confidence and expert support.

[OpenTelemetry](https://opentelemetry.io/docs/) is a vendor-neutral observability framework for collecting, processing, and exporting telemetry data. If you are new to OpenTelemetry, refer to OpenTelemetry [concepts](https://opentelemetry.io/docs/concepts/) and [components](https://opentelemetry.io/docs/concepts/components/). Refer to [EDOT compared to upstream OpenTelemetry](./compatibility/edot-vs-upstream.md) for more information on how EDOT differs from upstream OpenTelemetry.


## Available OpenTelemetry distributions

The following Elastic OpenTelemetry distributions are available:

| Distribution | Version | Status |
| ------------ | ------- | ------ |
| [EDOT Collector](./edot-collector/index.md) | {{edot-collector-version}} | GA |
| [EDOT .NET](./edot-sdks/dotnet/index.md) | {{edot-dotnet-version}} | GA |
| [EDOT Java](./edot-sdks/java/index.md) | {{edot-java-version}} | GA |
| [EDOT Node.js](./edot-sdks/nodejs/index.md) | {{edot-nodejs-version}} | GA |
| [EDOT PHP](./edot-sdks/php/index.md) | {{edot-php-version}} | GA |
| [EDOT Python](./edot-sdks/python/index.md) | {{edot-python-version}} | GA |
| [EDOT Android](apm-agent-android://reference/index.md) | {{edot-android-version}} | GA |
| [EDOT iOS](apm-agent-ios://reference/index.md) | {{edot-ios-version}} | GA |

Each EDOT distribution undergoes production-grade testing before being declared Generally Available (GA). Elastic provides full support for GA releases in accordance with our [support matrix](https://www.elastic.co/support/matrix) and SLAs.

Technical Preview distributions receive best-effort support and are not covered under standard SLAs.

## Get started

Pick the right [Quickstart guide](./quickstart/index.md) for your environment or select an observability use case:

- [Monitoring on Kubernetes](./use-cases/kubernetes/index.md)
- [LLM Observability](./use-cases/llms/index.md)

## EDOT Demo environment

A demo environment that showcases EDOT capabilities is available in the [opentelemetry-demo repository](https://github.com/elastic/opentelemetry-demo).

The EDOT demo includes:

*   Sample applications instrumented with OpenTelemetry SDKs.
*   EDOT Collector configured for various scenarios. For example, Kubernetes and hosts.
*   Integration with an Elastic Stack deployment, such as {{es}} and {{kib}}.

Follow the instructions in the demo repository to set up and run the demo.

## Report an issue or provide feedback

To report an issue or provide feedback on EDOT, [submit a GitHub issue](https://github.com/elastic/opentelemetry/issues/new/choose).
