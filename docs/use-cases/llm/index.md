# LLM Observability with EDOT

We currently support LLM observability with our EDOT Java, EDOT Node.js and EDOT Python as tech preview.

# Supported Technologies

| Technology | EDOT Java | EDOT Node.js | EDOT Python |
|:---------|:---------|:---------|:---------|
| OpenAI Client | :red_circle: | :red_circle: | :red_circle: |
| AWS Bedrock | :red_circle: | :red_circle: | :red_circle: |

See the [Supported Technologies section in the corresponding EDOT SDK](../../_edot-sdks/) for detailed information on supported versions.

# Quickstart Kubernetes

This quick start describes the setup and collection of OpenTelemetry data for applications running on Kubernetes with Elastic Cloud Serverless. For other options see the [quick start overview](../../quickstart/) and choose your prefered environment and target system.

1. **Setup Elastic Cloud Serverless**

Follow the instructions to [setup your Elastic Cloud serverless project](../../quickstart/serverless/index.md).

2. **Collect Data**

Setup the collection of OpenTelemetry data for applications running on Kubernetes following the [quickstart for Kubernetes](../../quickstart/serverless/k8s.md).

3. **Configuration**

See the [Configuration section in the corresponding EDOT SDK](../../_edot-sdks/) to enable and disable specific instrumentations and to what instrumentation is enabled by default.