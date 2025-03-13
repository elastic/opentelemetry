---
title: Components
layout: default
nav_order: 1
parent: Customization
---

# Components included in the EDOT Collector

The EDOT Collector comes with embedded Collector components from the [OTel Collector Core](https://github.com/open-telemetry/opentelemetry-collector), 
[OTel Collector Contrib](https://github.com/open-telemetry/opentelemetry-collector-contrib) and the [Elastic Collector Components](https://github.com/elastic/opentelemetry-collector-components) repositories. 

<!-- DO NOT DELETE THIS SECTION, TAGS ARE REQUIRED FOR GENERATION-->
<!-- start:edot-collector-components-table -->

| Component | GitHub Repo | Version |
|:---|:---|:---|
|***Receivers***|||
| [filelogreceiver ](https://github.com/open-telemetry/opentelemetry-collector-contrib/tree/main/receiver/filelogreceiver) | [Contrib](https://github.com/open-telemetry/opentelemetry-collector-contrib) | v0.119.0 |
| [hostmetricsreceiver ](https://github.com/open-telemetry/opentelemetry-collector-contrib/tree/main/receiver/hostmetricsreceiver) | [Contrib](https://github.com/open-telemetry/opentelemetry-collector-contrib) | v0.119.0 |
| [httpcheckreceiver ](https://github.com/open-telemetry/opentelemetry-collector-contrib/tree/main/receiver/httpcheckreceiver) | [Contrib](https://github.com/open-telemetry/opentelemetry-collector-contrib) | v0.119.0 |
| [jaegerreceiver ](https://github.com/open-telemetry/opentelemetry-collector-contrib/tree/main/receiver/jaegerreceiver) | [Contrib](https://github.com/open-telemetry/opentelemetry-collector-contrib) | v0.119.0 |
| [k8sclusterreceiver ](https://github.com/open-telemetry/opentelemetry-collector-contrib/tree/main/receiver/k8sclusterreceiver) | [Contrib](https://github.com/open-telemetry/opentelemetry-collector-contrib) | v0.119.0 |
| [k8sobjectsreceiver ](https://github.com/open-telemetry/opentelemetry-collector-contrib/tree/main/receiver/k8sobjectsreceiver) | [Contrib](https://github.com/open-telemetry/opentelemetry-collector-contrib) | v0.119.0 |
| [kubeletstatsreceiver ](https://github.com/open-telemetry/opentelemetry-collector-contrib/tree/main/receiver/kubeletstatsreceiver) | [Contrib](https://github.com/open-telemetry/opentelemetry-collector-contrib) | v0.119.0 |
| [otlpreceiver ](https://github.com/open-telemetry/opentelemetry-collector/tree/main/receiver/otlpreceiver) | [Core](https://github.com/open-telemetry/opentelemetry-collector) | v0.119.0 |
| [prometheusreceiver ](https://github.com/open-telemetry/opentelemetry-collector-contrib/tree/main/receiver/prometheusreceiver) | [Contrib](https://github.com/open-telemetry/opentelemetry-collector-contrib) | v0.119.0 |
| [zipkinreceiver ](https://github.com/open-telemetry/opentelemetry-collector-contrib/tree/main/receiver/zipkinreceiver) | [Contrib](https://github.com/open-telemetry/opentelemetry-collector-contrib) | v0.119.0 |
|***Exporters***|||
| [debugexporter ](https://github.com/open-telemetry/opentelemetry-collector/tree/main/exporter/debugexporter) | [Core](https://github.com/open-telemetry/opentelemetry-collector) | v0.119.0 |
| [elasticsearchexporter ](https://github.com/open-telemetry/opentelemetry-collector-contrib/tree/main/exporter/elasticsearchexporter) | [Contrib](https://github.com/open-telemetry/opentelemetry-collector-contrib) | v0.119.0 |
| [fileexporter ](https://github.com/open-telemetry/opentelemetry-collector-contrib/tree/main/exporter/fileexporter) | [Contrib](https://github.com/open-telemetry/opentelemetry-collector-contrib) | v0.119.0 |
| [loadbalancingexporter ](https://github.com/open-telemetry/opentelemetry-collector-contrib/tree/main/exporter/loadbalancingexporter) | [Contrib](https://github.com/open-telemetry/opentelemetry-collector-contrib) | v0.119.0 |
| [otlpexporter ](https://github.com/open-telemetry/opentelemetry-collector/tree/main/exporter/otlpexporter) | [Core](https://github.com/open-telemetry/opentelemetry-collector) | v0.119.0 |
| [otlphttpexporter ](https://github.com/open-telemetry/opentelemetry-collector/tree/main/exporter/otlphttpexporter) | [Core](https://github.com/open-telemetry/opentelemetry-collector) | v0.119.0 |
|***Processors***|||
| [attributesprocessor ](https://github.com/open-telemetry/opentelemetry-collector-contrib/tree/main/processor/attributesprocessor) | [Contrib](https://github.com/open-telemetry/opentelemetry-collector-contrib) | v0.119.0 |
| [batchprocessor ](https://github.com/open-telemetry/opentelemetry-collector/tree/main/processor/batchprocessor) | [Core](https://github.com/open-telemetry/opentelemetry-collector) | v0.119.0 |
| [elasticinframetricsprocessor ](https://github.com/elastic/opentelemetry-collector-components/tree/main/processor/elasticinframetricsprocessor) | [Elastic](https://github.com/elastic/opentelemetry-collector-components) | v0.13.0 |
| [elastictraceprocessor ](https://github.com/elastic/opentelemetry-collector-components/tree/main/processor/elastictraceprocessor) | [Elastic](https://github.com/elastic/opentelemetry-collector-components) | v0.3.0 |
| [filterprocessor ](https://github.com/open-telemetry/opentelemetry-collector-contrib/tree/main/processor/filterprocessor) | [Contrib](https://github.com/open-telemetry/opentelemetry-collector-contrib) | v0.119.0 |
| [k8sattributesprocessor ](https://github.com/open-telemetry/opentelemetry-collector-contrib/tree/main/processor/k8sattributesprocessor) | [Contrib](https://github.com/open-telemetry/opentelemetry-collector-contrib) | v0.119.0 |
| [lsmintervalprocessor ](https://github.com/elastic/opentelemetry-collector-components/tree/main/processor/lsmintervalprocessor) | [Elastic](https://github.com/elastic/opentelemetry-collector-components) | v0.3.0 |
| [memorylimiterprocessor ](https://github.com/open-telemetry/opentelemetry-collector/tree/main/processor/memorylimiterprocessor) | [Core](https://github.com/open-telemetry/opentelemetry-collector) | v0.119.0 |
| [resourcedetectionprocessor ](https://github.com/open-telemetry/opentelemetry-collector-contrib/tree/main/processor/resourcedetectionprocessor) | [Contrib](https://github.com/open-telemetry/opentelemetry-collector-contrib) | v0.119.0 |
| [resourceprocessor ](https://github.com/open-telemetry/opentelemetry-collector-contrib/tree/main/processor/resourceprocessor) | [Contrib](https://github.com/open-telemetry/opentelemetry-collector-contrib) | v0.119.0 |
| [transformprocessor ](https://github.com/open-telemetry/opentelemetry-collector-contrib/tree/main/processor/transformprocessor) | [Contrib](https://github.com/open-telemetry/opentelemetry-collector-contrib) | v0.119.0 |
|***Connectors***|||
| [routingconnector ](https://github.com/open-telemetry/opentelemetry-collector-contrib/tree/main/connector/routingconnector) | [Contrib](https://github.com/open-telemetry/opentelemetry-collector-contrib) | v0.119.0 |
| [signaltometricsconnector ](https://github.com/elastic/opentelemetry-collector-components/tree/main/connector/signaltometricsconnector) | [Elastic](https://github.com/elastic/opentelemetry-collector-components) | v0.3.0 |
| [spanmetricsconnector ](https://github.com/open-telemetry/opentelemetry-collector-contrib/tree/main/connector/spanmetricsconnector) | [Contrib](https://github.com/open-telemetry/opentelemetry-collector-contrib) | v0.119.0 |
|***Extensions***|||
| [filestorage ](https://github.com/open-telemetry/opentelemetry-collector-contrib/tree/main/extension/storage/filestorage) | [Contrib](https://github.com/open-telemetry/opentelemetry-collector-contrib) | v0.119.0 |
| [healthcheckextension ](https://github.com/open-telemetry/opentelemetry-collector-contrib/tree/main/extension/healthcheckextension) | [Contrib](https://github.com/open-telemetry/opentelemetry-collector-contrib) | v0.119.0 |
| [memorylimiterextension ](https://github.com/open-telemetry/opentelemetry-collector/tree/main/extension/memorylimiterextension) | [Core](https://github.com/open-telemetry/opentelemetry-collector) | v0.119.0 |
| [pprofextension ](https://github.com/open-telemetry/opentelemetry-collector-contrib/tree/main/extension/pprofextension) | [Contrib](https://github.com/open-telemetry/opentelemetry-collector-contrib) | v0.119.0 |

<!-- end:edot-collector-components-table -->