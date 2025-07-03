---
navigation_title: Download
description: Direct download links for EDOT Collector binaries for various operating systems and architectures.
applies_to:
  stack:
  serverless:
    observability:
products:
  - id: cloud-serverless
  - id: observability
  - id: edot-collector
---

# Download the EDOT Collector

The {{edot}} (EDOT) Collector is embedded in the {{agent}} package as a separate binary that invokes OpenTelemetry Collector components.

The following table contains direct download links for the latest EDOT Collector version for different operating systems and architectures.

| Platform      | Architecture | Download link |
|--------------|--------------|---------------|
| Windows      | x86_64       | [Download (Zip)](https://artifacts.elastic.co/downloads/beats/elastic-agent/elastic-agent-{{edot-collector-version}}-windows-x86_64.zip) |
| macOS        | x86_64       | [Download (Tar.gz)](https://artifacts.elastic.co/downloads/beats/elastic-agent/elastic-agent-{{edot-collector-version}}-darwin-x86_64.tar.gz) |
| macOS        | aarch64      | [Download (Tar.gz)](https://artifacts.elastic.co/downloads/beats/elastic-agent/elastic-agent-{{edot-collector-version}}-darwin-aarch64.tar.gz) |
| Linux        | x86_64       | [Download (Tar.gz)](https://artifacts.elastic.co/downloads/beats/elastic-agent/elastic-agent-{{edot-collector-version}}-linux-x86_64.tar.gz) |
| Linux        | aarch64      | [Download (Tar.gz)](https://artifacts.elastic.co/downloads/beats/elastic-agent/elastic-agent-{{edot-collector-version}}-linux-arm64.tar.gz) |
| Linux (DEB)  | x86_64       | [Download (Deb)](https://artifacts.elastic.co/downloads/beats/elastic-agent/elastic-agent-{{edot-collector-version}}-amd64.deb) |
| Linux (DEB)  | aarch64      | [Download (Deb)](https://artifacts.elastic.co/downloads/beats/elastic-agent/elastic-agent-{{edot-collector-version}}-arm64.deb) |
| Linux (RPM)  | x86_64       | [Download (Rpm)](https://artifacts.elastic.co/downloads/beats/elastic-agent/elastic-agent-{{edot-collector-version}}-x86_64.rpm) |
| Linux (RPM)  | aarch64      | [Download (Rpm)](https://artifacts.elastic.co/downloads/beats/elastic-agent/elastic-agent-{{edot-collector-version}}-aarch64.rpm) |

After you've downloaded and uncompressed the file, you can get EDOT Collector running with the following command:

```
sudo ./otelcol --config otel.yml
```

For specific configuration, refer to the [Quickstart guides](/reference/quickstart/index.md) or refer to [Configuration](/reference/edot-collector/config/index.md).