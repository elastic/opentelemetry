---
title: LLM Observability
layout: default
nav_order: 5
parent: Use Cases
---
# LLM Observability with EDOT

We currently support LLM observability with our EDOT Java, EDOT Node.js and EDOT Python as tech preview.

# Supported Technologies

| Technology | EDOT Java | EDOT Node.js | EDOT Python |
|:---------|:---------|:---------|:---------|
| OpenAI Client | :red_circle: | :red_circle: | :red_circle: |
| AWS Bedrock | :red_circle: | :red_circle: | :red_circle: |

See the [Supported Technologies section in the corresponding EDOT SDK](../../_edot-sdks/index) for detailed information on supported versions.

# Quickstart

This quick start describes the setup and collection of OpenTelemetry data for LLM applications.

1. **Setup**

Choose the environment and target system from the [quick start overview](../../quickstart/index) and follow the setup instructions to instrument your LLM application. The instrumentation for the supported technologies is enabled by default.

2. **Configuration**

See the [Configuration section in the corresponding EDOT SDK](../../_edot-sdks/index) to enable and disable specific instrumentations and to see what instrumentation is enabled by default.