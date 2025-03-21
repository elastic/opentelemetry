---
title: LLM Observability
layout: default
nav_order: 5
parent: Use Cases
---
# LLM Observability with EDOT

Applications make more and more use of Generative Artificial Intelligence (GenAI). Telemetry data in terms of spans, metrics and logs when communicating with the GenAI APIs becomes more and more important to operate the application in production and understand the application's behavior and health state.

We currently support LLM observability with our EDOT Java, EDOT Node.js and EDOT Python as tech preview. In the following, the supported technologies are listed as well as quickstart instructions to instrument your application to get telemetry data.

# Supported Technologies

| Technology | EDOT Java | EDOT Node.js | EDOT Python |
|:---------|:---------|:---------|:---------|
| OpenAI Client | :white_check_mark: | :white_check_mark: | :white_check_mark: |
| AWS Bedrock | :x: | :x: | :white_check_mark: |

See the [Supported Technologies section in the corresponding EDOT SDK](../../_edot-sdks/index) for detailed information on supported versions.

# Quickstart

This quick start describes the setup and collection of OpenTelemetry data for LLM applications.

1. **Setup**

Choose the environment and target system from the [quick start overview](../../quickstart/index) and follow the setup instructions to instrument your LLM application. The instrumentation for the supported technologies is enabled by default.

2. **Configuration**

See the [Configuration section in the corresponding EDOT SDK](../../_edot-sdks/index) to enable and disable specific instrumentations and to see what instrumentation is enabled by default.

When you finish the setup and the configuration of the EDOT SDK and there is a workload on your application, you should start to see telemetry data in Kibana. If there is no telemetry data showing up, please see the troubleshooting of the EDOT SDK,