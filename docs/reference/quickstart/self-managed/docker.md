---
navigation_title: Docker
description: Learn how to set up the EDOT Collector and EDOT SDKs in a Docker environment to collect host metrics, logs and application traces.
applies_to:
  stack:
  serverless:
---

# Quickstart for Docker on self-managed deployments

Learn how to set up the EDOT Collector and EDOT SDKs in a Docker environment to collect host metrics, logs and application traces.

## Prerequisites

Make sure the following requirements are present:

- Docker installed and running.
- A Self-Managed Elasticsearch cluster up and running.

## Instructions

Follow these steps to deploy the EDOT Collector and EDOT OTel SDKs in Docker.

### Create the config file

Create the `otel-collector-config.yml` file with your EDOT Collector configuration. Refer to the [configuration reference](../../edot-collector/config/default-config-standalone.md).

### Retrieve your settings

Retrieve your [Elasticsearch endpoint](docs-content://solutions/search/search-connection-details) and [API key](docs-content://deploy-manage/api-keys/elasticsearch-api-keys).

### Create the .env file

Create an `.env` file with the following content. Replace the placeholder values with your Elastic Cloud credentials:

```bash
HOST_FILESYSTEM=/
DOCKER_SOCK=/var/run/docker.sock
ELASTIC_AGENT_OTEL=true
COLLECTOR_CONTRIB_IMAGE=elastic/elastic-agent:9.0.0
ELASTIC_API_KEY=<your_api_key_here>
ELASTIC_ENDPOINT=<your_endpoint_here>
OTEL_COLLECTOR_CONFIG=/path/to/otel-collector-config.yml
   ```

### Create the compose file

Create a `compose.yml` file with the following content:

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
      - ELASTIC_AGENT_OTEL
      - ELASTIC_API_KEY
      - ELASTIC_ENDPOINT
      - STORAGE_DIR=/usr/share/elastic-agent
```

### Start the Collector

Start the Collector by running the following command:

```bash
docker compose up -d
```

### (Optional) Instrument your applications

If you want to collect telemetry from applications running on the host where you installed the EDOT Collector, instrument your target applications:

- [.NET](../../edot-sdks/dotnet/setup)
- [Java](../../edot-sdks/java/setup)
- [Node.js](../../edot-sdks/nodejs/setup)
- [PHP](../../edot-sdks/php/setup)
- [Python](../../edot-sdks/python/setup)

Configure your SDKs to send the data to the local EDOT Collector using OTLP/gRPC (`http://localhost:4317`) or OTLP/HTTP (`http://localhost:4318`).