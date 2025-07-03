---
navigation_title: Docker
description: Learn how to set up the EDOT Collector and EDOT SDKs in a Docker environment with {{serverless-full}} to collect host metrics, logs, and application traces.
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

# Quickstart for Docker on Elastic Cloud Serverless

Learn how to set up the EDOT Collector and EDOT SDKs in a Docker environment with {{serverless-full}} to collect host metrics, logs, and application traces.

## Prerequisites

Make sure the following requirements are present:

- Docker installed and running.
- The **[System](integration-docs://reference/system/index.md)** integration is installed in {{kib}}. Select **Add integration only** to skip the agent installation, as only the integration assets are required.

## Guided setup

:::{include} ../../_snippets/guided-instructions.md
:::

## Manual installation

Follow these steps to deploy the EDOT Collector and EDOT OTel SDKs in Docker with {{serverless-full}}.

:::::{stepper}

::::{step} Create the config file

Create a `otel-collector-config.yml` file with your EDOT collector configuration. For more details, refer to the [configuration reference](/reference/edot-collector/config/default-config-standalone.md) for {{motlp}}.

::::

::::{step}  Retrieve your settings

:::{include} ../../_snippets/serverless-endpoint-api.md
:::

::::

::::{step} Create the .env file

Create a `.env` file with the following content, replacing the placeholder values with your actual Elastic Cloud credentials:

```bash subs=true
HOST_FILESYSTEM=/
DOCKER_SOCK=/var/run/docker.sock
ELASTIC_AGENT_OTEL=true
COLLECTOR_CONTRIB_IMAGE=elastic/elastic-agent:{{edot-collector-version}}
ELASTIC_API_KEY=<your_api_key_here>
ELASTIC_OTLP_ENDPOINT=<your_endpoint_here>
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
      - ELASTIC_OTLP_ENDPOINT
      - STORAGE_DIR=/usr/share/elastic-agent
```

::::

::::{step}  Start the Collector

Start the collector by running:

```bash
docker compose up -d
```

::::

::::{step} (Optional) Instrument your applications

To collect telemetry from applications running on the host where you installed the EDOT Collector, instrument your target applications:

- [.NET](/reference/edot-sdks/dotnet/setup/index.md)
- [Java](/reference/edot-sdks/java/setup/index.md)
- [Node.js](/reference/edot-sdks/nodejs/setup/index.md)
- [PHP](/reference/edot-sdks/php/setup/index.md)
- [Python](/reference/edot-sdks/python/setup/index.md)

Configure your SDKs to send the data to the local EDOT Collector using OTLP/gRPC (`http://localhost:4317`) or OTLP/HTTP (`http://localhost:4318`).

::::
:::::

## Troubleshooting

The following issues might occur.

### API Key prefix not found

The following error is due to an improperly formatted API key:

```txt
Exporting failed. Dropping data.
{"kind": "exporter", "data_type": }
"Unauthenticated desc = ApiKey prefix not found"
```

Format your API key as `"Authorization": "ApiKey <api-key-value-here>"` or `"Authorization=ApiKey <api-key>"` depending on whether you're using a Collector or SDK.

### Error: too many requests

The managed endpoint has per-project rate limits in place. If you reach this limit, contact our [support team](https://support.elastic.co).
