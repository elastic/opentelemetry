---
navigation_title: Docker
description: Learn how to set up the EDOT Collector and EDOT SDKs in a Docker environment to collect host metrics, logs and application traces.
applies_to:
  stack:
  serverless:
    observability:
  product:
    edot_collector: ga
products:
  - id: cloud-serverless
  - id: observability
  - id: edot-collector
---

# Quickstart for Docker on self-managed deployments

Learn how to set up the EDOT Collector and EDOT SDKs in a Docker environment to collect host metrics, logs and application traces.

## Prerequisites

Make sure the following requirements are present:

- Docker installed and running.
- The **[System](integration-docs://reference/system/index.md)** integration is installed in {{kib}}. Select **Add integration only** to skip the agent installation, as only the integration assets are required.

## Guided setup

:::{include} ../../_snippets/guided-instructions.md
:::

## Manual installation

Follow these steps to deploy the EDOT Collector and EDOT OTel SDKs in Docker.

:::::{stepper}

::::{step} Create the config file

Create the `otel-collector-config.yml` file with your EDOT Collector configuration. Refer to the [configuration reference](/reference/edot-collector/config/default-config-standalone.md).
::::

::::{step} Retrieve your settings

Retrieve your [{{es}} endpoint](docs-content://solutions/search/search-connection-details.md) and [API key](docs-content://deploy-manage/api-keys/elasticsearch-api-keys.md).
::::

::::{step} Create the .env file

Create an `.env` file with the following content. Replace the placeholder values with your Elastic Cloud credentials:

```bash subs=true
HOST_FILESYSTEM=/
DOCKER_SOCK=/var/run/docker.sock
ELASTIC_AGENT_OTEL=true
COLLECTOR_CONTRIB_IMAGE=elastic/elastic-agent:{{edot-collector-version}}
ELASTIC_API_KEY=<your_api_key_here>
ELASTIC_ENDPOINT=<your_endpoint_here>
OTEL_COLLECTOR_CONFIG=/path/to/otel-collector-config.yml
   ```
::::

::::{step} Create the compose file

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
::::

::::{step} Start the Collector

Start the Collector by running the following command:

```bash
docker compose up -d
```
::::

::::{step} (Optional) Instrument your applications

If you want to collect telemetry from applications running on the host where you installed the EDOT Collector, instrument your target applications:

- [.NET](/reference/edot-sdks/dotnet/setup/index.md)
- [Java](/reference/edot-sdks/java/setup/index.md)
- [Node.js](/reference/edot-sdks/nodejs/setup/index.md)
- [PHP](/reference/edot-sdks/php/setup/index.md)
- [Python](/reference/edot-sdks/python/setup/index.md)

Configure your SDKs to send the data to the local EDOT Collector using OTLP/gRPC (`http://localhost:4317`) or OTLP/HTTP (`http://localhost:4318`).
::::
:::::
