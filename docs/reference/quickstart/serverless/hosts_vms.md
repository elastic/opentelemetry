---
navigation_title: Hosts and VMs
description: Learn how to set up the EDOT Collector and EDOT SDKs in a Docker environment with {{serverless-full}} to collect host metrics, logs, and application traces. Send the data through OTLP to your Elastic Serverless Project.
applies_to:
  stack:
  serverless:
    observability:
products:
  - id: cloud-serverless
  - id: observability
---

#  Quickstart for hosts / VMs on Elastic Cloud Serverless

Learn how to set up the EDOT Collector and EDOT SDKs in a Docker environment with {{serverless-full}} to collect host metrics, logs, and application traces. Send the data through OTLP to your Elastic Serverless Project.

## Prerequisites

Make sure the following requirements are present:

- The **[System](integration-docs://reference/system/index.md)** integration is installed in {{kib}}. Select **Add integration only** to skip the agent installation, as only the integration assets are required.

## Guided setup

:::{include} ../../_snippets/guided-instructions.md
:::

## Manual installation

Follow these steps to deploy the EDOT Collector and EDOT OTel SDKs with {{serverless-full}}.

::::::{stepper}

:::::{step} Download the EDOT Collector

[Download the EDOT Collector](../../edot-collector/download.md) for your operating system.

:::::

:::::{step} Configure the EDOT Collector

Follow these steps to retrieve the [{{motlp}}](../../motlp.md) for your Serverless project:

1. In Elastic Cloud, open your Observability project.
2. Go to **Add data**, **Application**, **OpenTelemetry**.
3. Select **Managed OTLP Endpoint** in the second step.
4. Copy the OTLP endpoint configuration value.
5. Select Create API Key to generate an API key.

Replace `<ELASTIC_OTLP_ENDPOINT>` and `<ELASTIC_API_KEY>` before applying the following command.

::::{tab-set}

:::{tab-item} Linux
```bash
ELASTIC_OTLP_ENDPOINT=<ELASTIC_OTLP_ENDPOINT> && \
ELASTIC_API_KEY=<ELASTIC_API_KEY> && \
cp ./otel_samples/managed_otlp/logs_metrics_traces.yml ./otel.yml && \
mkdir -p ./data/otelcol && \
sed -i "s#\${env:STORAGE_DIR}#${PWD}/data/otelcol#g" ./otel.yml && \
sed -i "s#\${env:ELASTIC_OTLP_ENDPOINT}#${ELASTIC_OTLP_ENDPOINT}#g" ./otel.yml && \
sed -i "s#\${env:ELASTIC_API_KEY}#${ELASTIC_API_KEY}#g" ./otel.yml
```
:::

:::{tab-item} macOS
```bash
ELASTIC_OTLP_ENDPOINT=<ELASTIC_OTLP_ENDPOINT> && \
ELASTIC_API_KEY=<ELASTIC_API_KEY> && \
cp ./otel_samples/managed_otlp/logs_metrics_traces.yml ./otel.yml && \
mkdir -p ./data/otelcol && \
sed -i '' "s#\${env:STORAGE_DIR}#${PWD}/data/otelcol#g" ./otel.yml && \
sed -i '' "s#\${env:ELASTIC_OTLP_ENDPOINT}#${ELASTIC_OTLP_ENDPOINT}#g" ./otel.yml && \
sed -i '' "s#\${env:ELASTIC_API_KEY}#${ELASTIC_API_KEY}#g" ./otel.yml
```
:::

:::{tab-item} Windows
```powershell
Remove-Item -Path .\otel.yml -ErrorAction SilentlyContinue
Copy-Item .\otel_samples\managed_otlp\logs_metrics_traces.yml .\otel.yml
New-Item -ItemType Directory -Force -Path .\data\otelcol | Out-Null

$content = Get-Content .\otel.yml
$content = $content -replace '\${env:STORAGE_DIR}', "$PWD\data\otelcol"
$content = $content -replace '\${env:ELASTIC_OTLP_ENDPOINT}', "<ELASTIC_OTLP_ENDPOINT>"
$content = $content -replace '\${env:ELASTIC_API_KEY}', "<ELASTIC_API_KEY>"
$content | Set-Content .\otel.yml
```
:::
::::
:::::

:::::{step} Run the EDOT Collector
    
Run the following command to run the EDOT Collector.

::::{tab-set}

:::{tab-item} Linux and macOS

```bash
sudo ./otelcol --config otel.yml
```
:::

:::{tab-item} Windows
```powershell
.\elastic-agent.exe otel --config otel.yml
```
:::
::::

::::{note}
The Collector opens ports `4317` and `4318` to receive application data from locally running OTel SDKs without authentication. This allows the SDKs to send data without any further configuration needed as they use this endpoint by default.
::::
:::::

:::::{step} (Optional) Instrument your applications

If you want to collect telemetry from applications running on the host where you installed the EDOT Collector, instrument your target applications:

- [.NET](../../edot-sdks/dotnet/setup/index.md)
- [Java](../../edot-sdks/java/setup/index.md)
- [Node.js](../../edot-sdks/nodejs/setup/index.md)
- [PHP](../../edot-sdks/php/setup/index.md)
- [Python](../../edot-sdks/python/setup/index.md)

Configure your SDKs to send the data to the local EDOT Collector using OTLP/gRPC (`http://localhost:4317`) or OTLP/HTTP (`http://localhost:4318`).
:::::
::::::

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
