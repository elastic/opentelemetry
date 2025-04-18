---
title: Docker
layout: default
nav_order: 3
parent: Elastic Cloud Hosted
---

# Quickstart - Docker - Hosted

🐳 Docker
{: .label .label-blue }

🗄️ Elastic Cloud Hosted
{: .label .label-blue }

The quick start for Docker with with Elastic Cloud Hosted will guide you through setting up the EDOT Collector and EDOT SDKs to collect host metrics, logs and application traces.

## Instructions

1. Create a `otel-collector-config.yml` file with your EDOT collector configuration. See the [configuration reference](../../_edot-collector/config/default-config-standalone.md) for "Direct ingestion into Elasticsearch" for more details.

2. Retrieve the `Elasticsearch Endpoint` and the `Elastic API Key` for your Elastic Cloud deployment by [following these instructions](./#retrieving-connection-details-for-your-elastic-cloud-deployment).

3. Create a `.env` file with the following content, replacing the placeholder values with your actual Elastic Cloud credentials:
   
   ```bash
   HOST_FILESYSTEM=/
   DOCKER_SOCK=/var/run/docker.sock
   ELASTIC_AGENT_OTEL=true
   COLLECTOR_CONTRIB_IMAGE=elastic/elastic-agent:9.0.0
   ELASTIC_API_KEY=<your_api_key_here>
   ELASTIC_ENDPOINT=<your_endpoint_here>
   OTEL_COLLECTOR_CONFIG=/path/to/otel-collector-config.yml
   ```

4. Create a `compose.yml` file with the following content:

   ```yaml
   services:
    otel-collector:
      image: ${COLLECTOR_CONTRIB_IMAGE}
      container_name: otel-collector
      deploy:
        resources:
          limits:
            memory: 1.5G
      restart: unless-stopped
      command: ["--config", "/etc/otelcol-config.yml" ]
      network_mode: host
      user: 0:0
      volumes:
        - ${HOST_FILESYSTEM}:/hostfs:ro
        - ${DOCKER_SOCK}:/var/run/docker.sock:ro
        - ${OTEL_COLLECTOR_CONFIG}:/etc/otelcol-config.yml
      environment:
        - HOST_FILESYSTEM
        - ELASTIC_API_KEY
        - ELASTIC_ENDPOINT
        - STORAGE_DIR=/usr/share/elastic-agent
   ```

5. Start the collector by running:

   ```bash
   docker compose up -d
   ```

6. **(Optional) Instrument your applications**

    If you would like to collect telemetry from applications running on the host where you installed the EDOT Collector,
    you need to instrument your target applications according to the setup instructions for corresponding EDOT SDKs:

    - [.NET](../../edot-sdks/dotnet/setup)
    - [Java](../../edot-sdks/java/setup)
    - [Node.js](../../edot-sdks/nodejs/setup)
    - [PHP](../../edot-sdks/php/setup)
    - [Python](../../edot-sdks/python/setup)

    Configure your SDKs to send the data to the local EDOT Collector using OTLP/gRPC (`http://localhost:4317`) or OTLP/HTTP (`http://localhost:4318`).





