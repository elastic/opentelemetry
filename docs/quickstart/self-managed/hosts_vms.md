---
title: Hosts / VMs
layout: default
nav_order: 2
parent: Self-managed
---

# Quickstart

🖥 Hosts / VMs
{: .label .label-red }

🆂 Self-managed Elastic Stack
{: .label .label-yellow }

The quick start for Hosts / VMs with a self-managed Elastic Stack will guide you through setting up the EDOT Collector and EDOT SDKs to collect host metrics, logs and application traces.

1. **Download the EDOT Collector**

    [Download the EDOT Collector](../../edot-collector/download) for your operating system, extract the archive and move to the extracted directory.

2. **Configure the EDOT Collector**

    Retrieve your [Elasticsearch endpoint](https://www.elastic.co/guide/en/kibana/current/search-space-connection-details.html){:target="_blank"} and [API key](https://www.elastic.co/guide/en/kibana/current/api-keys.html){:target="_blank"} and replace `<ELASTICSEARCH_ENDPOINT>` and `<ELASTIC_API_KEY>` before applying the below command.

    *Linux*

    ```bash
    ELASTICSEARCH_ENDPOINT=<ELASTICSEARCH_ENDPOINT> \
    ELASTIC_API_KEY=<ELASTIC_API_KEY> \
    rm ./otel.yml && cp ./otel_samples/logs_metrics_traces.yml ./otel.yml && mkdir -p ./data/otelcol && sed -i 's#\${env:STORAGE_DIR}#'"$PWD"/data/otelcol'#g' ./otel.yml && sed -i 's#\${env:ELASTIC_ENDPOINT}#$ELASTICSEARCH_ENDPOINT' ./otel.yml && sed -i 's/\${env:ELASTIC_API_KEY}/$ELASTIC_API_KEY/g' ./otel.yml
    ```

    *MacOS*

    ```bash
    ELASTICSEARCH_ENDPOINT=<ELASTICSEARCH_ENDPOINT> \
    ELASTIC_API_KEY=<ELASTIC_API_KEY> \
    rm ./otel.yml && cp ./otel_samples/logs_metrics_traces.yml ./otel.yml && mkdir -p ./data/otelcol && sed -i '' 's#\${env:STORAGE_DIR}#'"$PWD"/data/otelcol'#g' ./otel.yml && sed -i '' 's#\${env:ELASTIC_ENDPOINT}#'"$ELASTICSEARCH_ENDPOINT"'#g' ./otel.yml && sed -i '' 's#\${env:ELASTIC_API_KEY}#'"$ELASTIC_API_KEY"'#g' ./otel.yml
    ```

    *Windows*

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

3. **Run the EDOT Collector**

    Execute the following command to run the EDOT Collector. 
    
    {: .note }
    The Collector will open the ports `4317` and `4318` to receive application data from locally running OTel SDKs.

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
