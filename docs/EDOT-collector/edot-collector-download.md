## Download EDOT Collector

EDOT is embeded in the Elastic Agent package,  it is a separate binary that invokes only OpenTelemetry collector components.
Below are the direct download links for **EDOT Collector version 8.17.2** for different operating systems and architectures.

| Platform      | Architecture | Download Link |
|--------------|--------------|---------------|
| Windows      | x86_64       | [Download](https://artifacts.elastic.co/downloads/beats/elastic-agent/elastic-agent-8.17.2-windows-x86_64.zip) |
| Windows      | ARM64        | [Download](https://artifacts.elastic.co/downloads/beats/elastic-agent/elastic-agent-8.17.2-windows-arm64.zip) |
| macOS        | x86_64       | [Download](https://artifacts.elastic.co/downloads/beats/elastic-agent/elastic-agent-8.17.2-darwin-x86_64.tar.gz) |
| macOS        | ARM64        | [Download](https://artifacts.elastic.co/downloads/beats/elastic-agent/elastic-agent-8.17.2-darwin-arm64.tar.gz) |
| Linux        | x86_64       | [Download](https://artifacts.elastic.co/downloads/beats/elastic-agent/elastic-agent-8.17.2-linux-x86_64.tar.gz) |
| Linux        | ARM64        | [Download](https://artifacts.elastic.co/downloads/beats/elastic-agent/elastic-agent-8.17.2-linux-arm64.tar.gz) |
| Linux (DEB)  | x86_64       | [Download](https://artifacts.elastic.co/downloads/beats/elastic-agent/elastic-agent-8.17.2-amd64.deb) |
| Linux (RPM)  | x86_64       | [Download](https://artifacts.elastic.co/downloads/beats/elastic-agent/elastic-agent-8.17.2-x86_64.rpm) |

Once downloaded you can get EDOT Collector running with the below command.
```
sudo ./otelcol --config otel.yml
```

For use case specific configuration follow the [Quickstart guide](/Users/workspace/visualcode-github/opentelemetry/quickstart-guide.md) or visit the [EDOT Collector page](docs/EDOT-collector/README.md) for more details.