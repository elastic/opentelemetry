---
title: Hosts & VMs
layout: default
nav_order: 2
parent: Elastic Cloud Serverless
---

# Quickstart

🖥 Hosts / VMs
{: .label .label-red }

☁️ Elastic Cloud Serverless
{: .label .label-green }

The quick start for Hosts / VMs with Elastic Cloud Serverless will guide you through setting up the EDOT Collector and EDOT SDKs to collect host metrics,
logs and application traces and send the data through OTLP to your Elastic Serverless Porject.

1. **Download the EDOT Collector**

    [Download the EDOT Collector](../../edot-collector/download) for your operating system.

2. **Configure the EDOT Collector**

    Retrieve the `Elastic OTLP Endpoint` and the `Elastic API Key` for your Serverless Project by [following these instructions](./#retrieving-connection-details-for-your-serverless-project).

    Replace `<ELASTIC_OTLP_ENDPOINT>` and `<ELASTIC_API_KEY>` before applying the command below.

    *Linux*

    ```bash
    ELASTIC_OTLP_ENDPOINT=<ELASTIC_OTLP_ENDPOINT> && \
    ELASTIC_API_KEY=<ELASTIC_API_KEY> && \
    cp ./otel_samples/managed_otlp/logs_metrics_traces.yml ./otel.yml && \
    mkdir -p ./data/otelcol && \
    sed -i "s#\${env:STORAGE_DIR}#${PWD}/data/otelcol#g" ./otel.yml && \
    sed -i "s#\${env:ELASTIC_OTLP_ENDPOINT}#${ELASTIC_OTLP_ENDPOINT}#g" ./otel.yml && \
    sed -i "s#\${env:ELASTIC_API_KEY}#${ELASTIC_API_KEY}#g" ./otel.yml
    ```

    *MacOS*

    ```bash
    ELASTIC_OTLP_ENDPOINT=<ELASTIC_OTLP_ENDPOINT> && \
    ELASTIC_API_KEY=<ELASTIC_API_KEY> && \
    cp ./otel_samples/managed_otlp/logs_metrics_traces.yml ./otel.yml && \
    mkdir -p ./data/otelcol && \
    sed -i '' "s#\${env:STORAGE_DIR}#${PWD}/data/otelcol#g" ./otel.yml && \
    sed -i '' "s#\${env:ELASTIC_OTLP_ENDPOINT}#${ELASTIC_OTLP_ENDPOINT}#g" ./otel.yml && \
    sed -i '' "s#\${env:ELASTIC_API_KEY}#${ELASTIC_API_KEY}#g" ./otel.yml
    ```

    *Windows*

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

3. **Run the EDOT Collector**
    
    {: .note }
    The Collector will open the ports `4317` and `4318` to receive application data from locally running OTel SDKs without authentication.
    This allows the SDKs to send data without any further configuration needed as they use this endpoint by default.

   Execute the following command to run the EDOT Collector.

    *Linux / MacOS*

    ```bash
    sudo ./otelcol --config otel.yml
    ```

    *Windows*

    ```powershell
    .\elastic-agent.exe otel --config otel.yml
    ```

4. **(Optional) Instrument your applications**

    If you would like to collect telemetry from applications running on the host where you installed the EDOT Collector,
    you need to instrument your target applications according to the setup instructions for corresponding EDOT SDKs:

    - [.NET](../../edot-sdks/dotnet/setup)
    - [Java](../../edot-sdks/java/setup)
    - [Node.js](../../edot-sdks/nodejs/setup)
    - [PHP](../../edot-sdks/php/setup)
    - [Python](../../edot-sdks/python/setup)

    Configure your SDKs to send the data to the local EDOT Collector using OTLP/gRPC (`http://localhost:4317`) or OTLP/HTTP (`http://localhost:4318`).
