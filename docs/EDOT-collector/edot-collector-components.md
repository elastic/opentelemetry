# EDOT Collector components

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

### Core Components
The Core category includes production-grade, tested, and supported components selected for their stability and key observability use cases. These components ensure efficient telemetry collection, processing, and export for production environments. Each links to its respective OpenTelemetry Contrib repository for detailed functionality and configuration.

### Extended Components
The Extended category offers additional Exporters, Processors, Receivers, and Connectors for specialized observability needs. While included by default in EDOT, these components are not covered under our SLAs.

### Request a component to be added
To request a component to be added to EDOT Collector, please submit a [github issue](https://github.com/elastic/opentelemetry/issues/new/choose).