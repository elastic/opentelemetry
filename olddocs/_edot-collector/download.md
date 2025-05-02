---
title: Download
layout: default
nav_order: 2
---

# Download the EDOT Collector Binaries

EDOT is embedded in the Elastic Agent package, it is a separate binary that invokes only OpenTelemetry collector components.
Below are the direct download links for **EDOT Collector version {{ site.edot_versions.collector }}** for different operating systems and architectures.

| Platform      | Architecture | Download Link |
|--------------|--------------|---------------|
| Windows      | x86_64       | [Download](https://artifacts.elastic.co/downloads/beats/elastic-agent/elastic-agent-{{ site.edot_versions.collector }}-windows-x86_64.zip) |
| macOS        | x86_64       | [Download](https://artifacts.elastic.co/downloads/beats/elastic-agent/elastic-agent-{{ site.edot_versions.collector }}-darwin-x86_64.tar.gz) |
| macOS        | aarch64      | [Download](https://artifacts.elastic.co/downloads/beats/elastic-agent/elastic-agent-{{ site.edot_versions.collector }}-darwin-aarch64.tar.gz) |
| Linux        | x86_64       | [Download](https://artifacts.elastic.co/downloads/beats/elastic-agent/elastic-agent-{{ site.edot_versions.collector }}-linux-x86_64.tar.gz) |
| Linux        | aarch64      | [Download](https://artifacts.elastic.co/downloads/beats/elastic-agent/elastic-agent-{{ site.edot_versions.collector }}-linux-arm64.tar.gz) |
| Linux (DEB)  | x86_64       | [Download](https://artifacts.elastic.co/downloads/beats/elastic-agent/elastic-agent-{{ site.edot_versions.collector }}-amd64.deb) |
| Linux (DEB)  | aarch64      | [Download](https://artifacts.elastic.co/downloads/beats/elastic-agent/elastic-agent-{{ site.edot_versions.collector }}-arm64.deb) |
| Linux (RPM)  | x86_64       | [Download](https://artifacts.elastic.co/downloads/beats/elastic-agent/elastic-agent-{{ site.edot_versions.collector }}-x86_64.rpm) |
| Linux (RPM)  | aarch64      | [Download](https://artifacts.elastic.co/downloads/beats/elastic-agent/elastic-agent-{{ site.edot_versions.collector }}-aarch64.rpm) |

Once downloaded you can get EDOT Collector running with the below command.
```
sudo ./otelcol --config otel.yml
```

For use case specific configuration follow the [Quickstart guide](../quickstart) or visit the [EDOT Collector Configuration](./config/index) page for more details.