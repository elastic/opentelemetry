## 🇪 EDOT Collector

The **Elastic Distribution of OpenTelemetry (EDOT) Collector** is an open-source distribution of the [OpenTelemetry Collector](https://github.com/open-telemetry/opentelemetry-collector).

Built on OpenTelemetry’s modular [architecture](https://opentelemetry.io/docs/collector/), the EDOT Collector offers a curated and fully supported selection of Receivers, Processors, Exporters, and Extensions. Designed for production-grade reliability. 

### Get started
The quickest way to get started with EDOT is to follow our [quick start guide](https://github.com/elastic/opentelemetry/blob/miguel-docs/quickstart-guide.md).

### 🧩 EDOT Collector components

The Elastic Distribution of OpenTelemetry (EDOT) Collector is built on OpenTelemetry’s modular architecture, integrating a carefully curated selection of Receivers, Processors, Exporters, and Extensions to ensure stability, scalability, and seamless observability. The table below categorizes these components into Core and Extended groups, highlighting the supported and production-tested components included in EDOT.

<table style="border-collapse: collapse; width: 100%;">
    <tr>
        <th style="text-align: left;">Category</th>
        <th style="text-align: left;">Component Type</th>
        <th style="text-align: left;">Component Name</th>
    </tr>
    <!-- Core Components -->
    <tr>
        <td rowspan="14"><strong>Core</strong></td>
        <td rowspan="2"><strong>Exporter</strong></td>
        <td><a href="https://github.com/open-telemetry/opentelemetry-collector-contrib/tree/main/exporter/elasticsearchexporter">elasticsearch</a></td>
    </tr>
    <tr>
        <td><a href="https://github.com/open-telemetry/opentelemetry-collector/tree/main/exporter/otlpexporter">otlp</a></td>
    </tr>
    <tr>
        <td rowspan="6"><strong>Processor</strong></td>
        <td><a href="https://github.com/open-telemetry/opentelemetry-collector-contrib/tree/main/processor/attributesprocessor">attributes</a></td>
    </tr>
    <tr>
        <td><a href="https://github.com/open-telemetry/opentelemetry-collector/tree/main/processor/batchprocessor">batch</a></td>
    </tr>
    <tr>
        <td><a href="https://github.com/open-telemetry/opentelemetry-collector-contrib/tree/main/processor/elasticinframetricsprocessor">elasticinframetrics</a></td>
    </tr>
    <tr>
        <td><a href="https://github.com/open-telemetry/opentelemetry-collector-contrib/tree/main/processor/k8sattributesprocessor">k8sattributes</a></td>
    </tr>
    <tr>
        <td><a href="https://github.com/open-telemetry/opentelemetry-collector/tree/main/processor/resourceprocessor">resource</a></td>
    </tr>
    <tr>
        <td><a href="https://github.com/open-telemetry/opentelemetry-collector-contrib/tree/main/processor/resourcedetectionprocessor">resourcedetection</a></td>
    </tr>
    <tr>
        <td rowspan="6"><strong>Receiver</strong></td>
        <td><a href="https://github.com/open-telemetry/opentelemetry-collector-contrib/tree/main/receiver/filelogreceiver">filelog</a></td>
    </tr>
    <tr>
        <td><a href="https://github.com/open-telemetry/opentelemetry-collector-contrib/tree/main/receiver/hostmetricsreceiver">hostmetrics</a></td>
    </tr>
    <tr>
        <td><a href="https://github.com/open-telemetry/opentelemetry-collector-contrib/tree/main/receiver/k8sclusterreceiver">k8s_cluster</a></td>
    </tr>
    <tr>
        <td><a href="https://github.com/open-telemetry/opentelemetry-collector-contrib/tree/main/receiver/k8sobjectsreceiver">k8sobjects</a></td>
    </tr>
    <tr>
        <td><a href="https://github.com/open-telemetry/opentelemetry-collector-contrib/tree/main/receiver/kubeletstatsreceiver">kubeletstats</a></td>
    </tr>
    <tr>
        <td><a href="https://github.com/open-telemetry/opentelemetry-collector/tree/main/receiver/otlpreceiver">otlp</a></td>
    </tr>
    <!-- Extended Components -->
    <tr>
        <td rowspan="4"><strong>Extended</strong></td>
        <td><strong>Exporter</strong></td>
        <td><a href="https://github.com/elastic/elastic-agent/tree/main/internal/pkg/otel#exporters">Full List</a></td>
    </tr>
    <tr>
        <td><strong>Receiver</strong></td>
        <td><a href="https://github.com/elastic/elastic-agent/tree/main/internal/pkg/otel#receivers">Full List</a></td>
    </tr>
    <tr>
        <td><strong>Processor</strong></td>
        <td><a href="https://github.com/elastic/elastic-agent/tree/main/internal/pkg/otel#processors">Full List</a></td>
    </tr>
    <tr>
        <td><strong>Connector</strong></td>
        <td><a href="https://github.com/elastic/elastic-agent/tree/main/internal/pkg/otel#connectors">Full List</a></td>
    </tr>
</table>

#### Core Components
The Core category includes production-grade, tested, and supported components selected for their stability and key observability use cases. These components ensure efficient telemetry collection, processing, and export for production environments. Each links to its respective OpenTelemetry Contrib repository for detailed functionality and configuration.

#### Extended Components
The Extended category offers additional Exporters, Processors, Receivers, and Connectors for specialized observability needs. While included by default in EDOT, these components are not covered under our SLAs.

#### Request a component to be added
To request a component to be added to EDOT Collector, please submit a [github issue](https://github.com/elastic/opentelemetry/issues/new/choose).

### 🩺 Troubleshooting Quick Reference

* **Check Logs**: Review the Collector’s logs for error messages.
* **Validate Configuration:** Use the `--dry-run` option to test configurations.
* Enable Debug Logging: Run the Collector with `--log-level=debug` for detailed logs.
* **Check Service Status:** Ensure the Collector is running with `systemctl status <collector-service>` (Linux) or `tasklist` (Windows).
* **Test Connectivity:** Use `telnet <endpoint> <port>` or `curl` to verify backend availability.
* **Check Open Ports:** Run netstat `-tulnp or lsof -i` to confirm the Collector is listening.
* **Monitor Resource Usage:** Use top/htop (Linux) or Task Manager (Windows) to check CPU & memory.
* **Validate Exporters:** Ensure exporters are properly configured and reachable.
* **Verify Pipelines:** Use `otelctl` diagnose (if available) to check pipeline health.
* **Check Permissions:** Ensure the Collector has the right file and network permissions.
* **Review Recent Changes:** Roll back recent config updates if the issue started after changes.

For in-depth details on troubleshooting, refer to the OpenTelemetry Collector troubleshooting documentation.

For in-depth details on troubleshooting refer to the [OpenTelemetry Collector troubleshooting documentation](https://opentelemetry.io/docs/collector/troubleshooting/)