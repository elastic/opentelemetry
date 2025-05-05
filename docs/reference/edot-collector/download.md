---
navigation_title: Download
description: Direct download links for EDOT Collector binaries for various operating systems and architectures.
applies_to:
  stack:
  serverless:
---

# Download the EDOT Collector Binaries

EDOT is embedded in the Elastic Agent package, it is a separate binary that invokes only OpenTelemetry collector components.
Below are the direct download links for **EDOT Collector version <COLLECTOR_VERSION>** for different operating systems and architectures.

| Platform      | Architecture | Download Link |
|--------------|--------------|---------------|
| Windows      | x86_64       | [Download](https://artifacts.elastic.co/downloads/beats/elastic-agent/elastic-agent-<COLLECTOR_VERSION>-windows-x86_64.zip) |
| macOS        | x86_64       | [Download](https://artifacts.elastic.co/downloads/beats/elastic-agent/elastic-agent-<COLLECTOR_VERSION>-darwin-x86_64.tar.gz) |
| macOS        | aarch64      | [Download](https://artifacts.elastic.co/downloads/beats/elastic-agent/elastic-agent-<COLLECTOR_VERSION>-darwin-aarch64.tar.gz) |
| Linux        | x86_64       | [Download](https://artifacts.elastic.co/downloads/beats/elastic-agent/elastic-agent-<COLLECTOR_VERSION>-linux-x86_64.tar.gz) |
| Linux        | aarch64      | [Download](https://artifacts.elastic.co/downloads/beats/elastic-agent/elastic-agent-<COLLECTOR_VERSION>-linux-arm64.tar.gz) |
| Linux (DEB)  | x86_64       | [Download](https://artifacts.elastic.co/downloads/beats/elastic-agent/elastic-agent-<COLLECTOR_VERSION>-amd64.deb) |
| Linux (DEB)  | aarch64      | [Download](https://artifacts.elastic.co/downloads/beats/elastic-agent/elastic-agent-<COLLECTOR_VERSION>-arm64.deb) |
| Linux (RPM)  | x86_64       | [Download](https://artifacts.elastic.co/downloads/beats/elastic-agent/elastic-agent-<COLLECTOR_VERSION>-x86_64.rpm) |
| Linux (RPM)  | aarch64      | [Download](https://artifacts.elastic.co/downloads/beats/elastic-agent/elastic-agent-<COLLECTOR_VERSION>-aarch64.rpm) |

Once downloaded you can get EDOT Collector running with the below command.
```
sudo ./otelcol --config otel.yml
```

For use case specific configuration follow the [Quickstart guide](../quickstart) or visit the [EDOT Collector Configuration](./config/index.md) page for more details.