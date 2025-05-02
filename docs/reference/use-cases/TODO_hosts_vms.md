---
description: "Quick start guide for setting up EDOT Collector on Hosts/VMs with a self-managed Elastic Stack."
applies_to:
  serverless: all
---

# Quickstart

The quick start for Hosts / VMs with a self-managed Elastic Stack will guide you through setting up the EDOT Collector and to collect host metrics, logs and application traces using an OpenTelemetry configuration. You’ll download the appropriate package for your system, configure authentication, and run the collector. Optional steps allow you to customize log collection paths and set up application monitoring.
![EDOT-host-metrics-logs](../../images/edot-host-metrics-logs.png)

## Run EDOT Collector for Host Metrics and Log collection

These instructions will download EDOT collector including an OpenTelemetry collector configuration that will:

* Collect metrics from your host
* Collect logs from a set of locations in your host
Run the below commands to download the EDOT Collector package relevant to your system's architecture.

### Linux

Download EDOT Collector

```bash
arch=$(if ([[ $(arch) == "arm" || $(arch) == "aarch64" ]]); then echo "arm64"; else echo $(arch); fi)

curl --output elastic-distro-8.17.2-linux-$arch.tar.gz --url https://artifacts.elastic.co/downloads/beats/elastic-agent/elastic-agent-8.17.2-linux-$arch.tar.gz --proto '=https' --tlsv1.2 -fOL && mkdir -p elastic-distro-8.17.2-linux-$arch && tar -xvf elastic-distro-8.17.2-linux-$arch.tar.gz -C "elastic-distro-8.17.2-linux-$arch" --strip-components=1 && cd elastic-distro-8.17.2-linux-$arch
```

Replace the collector configuration with a preset for logs and host metrics collection and inject your credentials into the EDOT collector default configuration.

Retrieve your [Elasticsearch endpoint](https://www.elastic.co/guide/en/kibana/current/search-space-connection-details.html) and [API key](https://www.elastic.co/guide/en/kibana/current/api-keys.html) and replace `<ELASTICSEARCH_ENDPOINT>` and `<BASE64_APIKEY>` before applying the below command.

```bash
rm ./otel.yml && cp ./otel_samples/platformlogs_hostmetrics.yml ./otel.yml && mkdir -p ./data/otelcol && sed -i 's#\${env:STORAGE_DIR}#'"$PWD"/data/otelcol'#g' ./otel.yml && sed -i 's#\${env:ELASTIC_ENDPOINT}#<ELASTICSEARCH_ENDPOINT>' ./otel.yml && sed -i 's/\${env:ELASTIC_API_KEY}/<BASE64_APIKEY>/g' ./otel.yml
```

Run EDOT collector

```bash
sudo ./otelcol --config otel.yml
```

### MacOS

Download EDOT Collector

```bash
arch=$(if ([[ $(arch) == "arm" || $(arch) == "aarch64" ]]); then echo "arm64"; else echo $(arch); fi)

curl --output elastic-distro-8.17.2-darwin-$arch.tar.gz --url https://artifacts.elastic.co/downloads/beats/elastic-agent/elastic-agent-8.17.2-darwin-$arch.tar.gz --proto '=https' --tlsv1.2 -fOL && mkdir -p "elastic-distro-8.17.2-darwin-$arch" && tar -xvf elastic-distro-8.17.2-darwin-$arch.tar.gz -C "elastic-distro-8.17.2-darwin-$arch" --strip-components=1 && cd elastic-distro-8.17.2-darwin-$arch
```

Replace the collector configuration with a preset for logs and host metrics collection and inject your credentials into the EDOT collector default configuration.

Retrieve your [Elasticsearch endpoint](https://www.elastic.co/guide/en/kibana/current/search-space-connection-details.html) and [API key](https://www.elastic.co/guide/en/kibana/current/api-keys.html) and replace `<ELASTICSEARCH_ENDPOINT>` and `<BASE64_APIKEY>` before applying the below command.

```bash
rm ./otel.yml && cp ./otel_samples/platformlogs_hostmetrics.yml ./otel.yml && mkdir -p ./data/otelcol && sed -i 's#\${env:STORAGE_DIR}#'"$PWD"/data/otelcol'#g' ./otel.yml && sed -i 's#\${env:ELASTIC_ENDPOINT}#<ELASTICSEARCH_ENDPOINT>' ./otel.yml && sed -i 's/\${env:ELASTIC_API_KEY}/<BASE64_APIKEY>/g' ./otel.yml
```

Run EDOT collector

```bash
sudo ./otelcol --config otel.yml
```

### Windows
Download EDOT Collector

```powershell
# Download and extract
$distroPath = "elastic-distro-8.17.2-windows-x86_64";$zipFile = "$distroPath.zip"
```

This step disables the progress bar which might slow down the download

```powershell
$ProgressPreference = 'SilentlyContinue';Invoke-WebRequest -Uri "https://artifacts.elastic.co/downloads/beats/elastic-agent/elastic-agent-8.17.2-windows-x86_64.zip" -OutFile $zipFile;
New-Item -ItemType Directory -Force -Path $distroPath | Out-Null
Expand-Archive -Path $zipFile -DestinationPath $distroPath
Move-Item -Path "$distroPath\elastic-agent-8.17.2-windows-x86_64\*" -Destination $distroPath
Remove-Item -Path "$distroPath\elastic-agent-8.17.2-windows-x86_64" -Recurse
Remove-Item -Path $zipFile
Set-Location $distroPath
```

This command replaces the collector configuration with a preset for logs and host metrics collection

```powershell
Remove-Item -Path .\otel.yml -ErrorAction SilentlyContinue
Copy-Item .\otel_samples\platformlogs_hostmetrics.yml .\otel.yml
New-Item -ItemType Directory -Force -Path .\data\otelcol | Out-Null
```

Replace environment variables in otel.yml

```powershell
$content = Get-Content .\otel.yml
$content = $content -replace '\${env:STORAGE_DIR}', "$PWD\data\otelcol"
$content = $content -replace '\${env:ELASTIC_ENDPOINT}', "https://sample.eu-west-1.aws.qa.cld.elstc.co:443"
$content = $content -replace '\${env:ELASTIC_API_KEY}', "sampleApiKey=="
$content | Set-Content .\otel.yml
```

## Changing Log Collection Configuration (optional)
New log messages are collected from the setup onward.
The default log path is `/var/log/*`. You can change this or include other paths in the EDOT collector configuration, for advanced settings visit [filelog receiver documentation.](https://github.com/open-telemetry/opentelemetry-collector-contrib/tree/main/receiver/filelogreceiver)

To change log collection settings edit the below section of the `otel.yml` collector configuration file.
```yaml
receivers:
  # Receiver for platform specific log files
  filelog/platformlogs:
    include: [ /var/log/*.log ]
    retry_on_failure:
      enabled: true
    start_at: end
    storage: file_storage
```

## Collect application telemetry

TODO