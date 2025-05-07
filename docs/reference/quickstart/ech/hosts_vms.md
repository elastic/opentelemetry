---
navigation_title: Hosts and VMs
description: Learn how to set up the EDOT Collector and EDOT SDKs with Elastic Cloud Hosted to collect host metrics, logs and application traces.
applies_to:
  stack:
  serverless:
    observability:
products:
  - cloud-serverless
  - observability
---

# Quickstart for hosts and VMs on Elastic Cloud Hosted

Learn how to set up the EDOT Collector and EDOT SDKs with Elastic Cloud Hosted (ECH) to collect host metrics, logs and application traces.

## Instructions

Follow these steps to deploy the EDOT Collector and EDOT OTel SDKs with ECH.

::::::{stepper}

:::::{step} Download the EDOT Collector

[Download the EDOT Collector](../../edot-collector/download) for your operating system, extract the file, and change directory to the extracted files.

:::::

:::::{step} Configure the EDOT Collector

:::{include} ../../_snippets/retrieve-credentials.md
:::

Replace `<ELASTICSEARCH_ENDPOINT>` and `<ELASTIC_API_KEY>` before applying the following commands.

::::{tab-set}

:::{tab-item} Linux
```bash
ELASTICSEARCH_ENDPOINT=<ELASTICSEARCH_ENDPOINT> && \
ELASTIC_API_KEY=<ELASTIC_API_KEY> && \
cp ./otel_samples/logs_metrics_traces.yml ./otel.yml && \
mkdir -p ./data/otelcol && \
sed -i "s#\${env:STORAGE_DIR}#${PWD}/data/otelcol#g" ./otel.yml && \
sed -i "s#\${env:ELASTIC_ENDPOINT}#${ELASTICSEARCH_ENDPOINT}#g" ./otel.yml && \
sed -i "s#\${env:ELASTIC_API_KEY}#${ELASTIC_API_KEY}#g" ./otel.yml
```
:::

:::{tab-item} macOS
```bash
ELASTICSEARCH_ENDPOINT=<ELASTICSEARCH_ENDPOINT> && \
ELASTIC_API_KEY=<ELASTIC_API_KEY> && \
cp ./otel_samples/logs_metrics_traces.yml ./otel.yml && \
mkdir -p ./data/otelcol && \
sed -i '' "s#\${env:STORAGE_DIR}#${PWD}/data/otelcol#g" ./otel.yml && \
sed -i '' "s#\${env:ELASTIC_ENDPOINT}#${ELASTICSEARCH_ENDPOINT}#g" ./otel.yml && \
sed -i '' "s#\${env:ELASTIC_API_KEY}#${ELASTIC_API_KEY}#g" ./otel.yml
```
:::

:::{tab-item} Windows
```powershell
Remove-Item -Path .\otel.yml -ErrorAction SilentlyContinue
Copy-Item .\otel_samples\logs_metrics_traces.yml .\otel.yml
New-Item -ItemType Directory -Force -Path .\data\otelcol | Out-Null

$content = Get-Content .\otel.yml
$content = $content -replace '\${env:STORAGE_DIR}', "$PWD\data\otelcol"
$content = $content -replace '\${env:ELASTIC_ENDPOINT}', "<ELASTICSEARCH_ENDPOINT>"
$content = $content -replace '\${env:ELASTIC_API_KEY}', "<ELASTIC_API_KEY>"
$content | Set-Content .\otel.yml
```
:::
::::
:::::

:::::{step}  Run the EDOT Collector

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

:::{note}
By default, the Collector opens ports `4317` and `4318` to receive application data from locally running OTel SDKs.
:::

:::::

:::::{step} (Optional) Instrument your applications

If you want to collect telemetry from applications running on the host where you installed the EDOT Collector, instrument your target applications.

- [.NET](../../edot-sdks/dotnet/setup)
- [Java](../../edot-sdks/java/setup)
- [Node.js](../../edot-sdks/nodejs/setup)
- [PHP](../../edot-sdks/php/setup)
- [Python](../../edot-sdks/python/setup)

Configure your SDKs to send the data to the local EDOT Collector using OTLP/gRPC (`http://localhost:4317`) or OTLP/HTTP (`http://localhost:4318`).
:::::
::::::