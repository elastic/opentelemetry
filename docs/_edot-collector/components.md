---
title: Components
layout: default
nav_order: 1
parent: Customization
---

# Components included in the EDOT Collector

The EDOT Collector comes with embedded Collector components from the [OTel Collector Core](https://github.com/open-telemetry/opentelemetry-collector), 
[OTel Collector Contrib](https://github.com/open-telemetry/opentelemetry-collector-contrib) and the [Elastic Collector Components](https://github.com/elastic/opentelemetry-collector-components) repositories. 

The components included in the EDOT Collector are categorized into **[Core]** and **[Extended]** components.

| Component | GitHub Repo | Version | EDOT Collector 9.x |
|:---|:---|:---|:---|
|***Receivers***||||
| [filelogreceiver ](https://github.com/open-telemetry/opentelemetry-collector-contrib/tree/main/receiver/filelogreceiver) | [OTel Contrib Repo](https://github.com/open-telemetry/opentelemetry-collector-contrib) | v0.120.1 | ✅ [Core] (since 9.0) |
| [hostmetricsreceiver ](https://github.com/open-telemetry/opentelemetry-collector-contrib/tree/main/receiver/hostmetricsreceiver) | [OTel Contrib Repo](https://github.com/open-telemetry/opentelemetry-collector-contrib) | v0.120.1 | ✅ [Core] (since 9.0) |
| [httpcheckreceiver ](https://github.com/open-telemetry/opentelemetry-collector-contrib/tree/main/receiver/httpcheckreceiver) | [OTel Contrib Repo](https://github.com/open-telemetry/opentelemetry-collector-contrib) | v0.120.1 | 🟡 [Extended] |
| [jaegerreceiver ](https://github.com/open-telemetry/opentelemetry-collector-contrib/tree/main/receiver/jaegerreceiver) | [OTel Contrib Repo](https://github.com/open-telemetry/opentelemetry-collector-contrib) | v0.120.1 | 🟡 [Extended] |
| [jmxreceiver ](https://github.com/open-telemetry/opentelemetry-collector-contrib/tree/main/receiver/jmxreceiver) | [OTel Contrib Repo](https://github.com/open-telemetry/opentelemetry-collector-contrib) | v0.120.1 | 🟡 [Extended] |
| [k8sclusterreceiver ](https://github.com/open-telemetry/opentelemetry-collector-contrib/tree/main/receiver/k8sclusterreceiver) | [OTel Contrib Repo](https://github.com/open-telemetry/opentelemetry-collector-contrib) | v0.120.1 | ✅ [Core] (since 9.0) |
| [k8sobjectsreceiver ](https://github.com/open-telemetry/opentelemetry-collector-contrib/tree/main/receiver/k8sobjectsreceiver) | [OTel Contrib Repo](https://github.com/open-telemetry/opentelemetry-collector-contrib) | v0.120.1 | ✅ [Core] (since 9.0) |
| [kafkareceiver ](https://github.com/open-telemetry/opentelemetry-collector-contrib/tree/main/receiver/kafkareceiver) | [OTel Contrib Repo](https://github.com/open-telemetry/opentelemetry-collector-contrib) | v0.120.1 | 🟡 [Extended] |
| [kubeletstatsreceiver ](https://github.com/open-telemetry/opentelemetry-collector-contrib/tree/main/receiver/kubeletstatsreceiver) | [OTel Contrib Repo](https://github.com/open-telemetry/opentelemetry-collector-contrib) | v0.120.1 | ✅ [Core] (since 9.0) |
| [nginxreceiver ](https://github.com/open-telemetry/opentelemetry-collector-contrib/tree/main/receiver/nginxreceiver) | [OTel Contrib Repo](https://github.com/open-telemetry/opentelemetry-collector-contrib) | v0.120.1 | 🟡 [Extended] |
| [nopreceiver ](https://github.com/open-telemetry/opentelemetry-collector/tree/main/receiver/nopreceiver) | [OTel Core Repo](https://github.com/open-telemetry/opentelemetry-collector) | v0.119.0 | 🟡 [Extended] |
| [otlpreceiver ](https://github.com/open-telemetry/opentelemetry-collector/tree/main/receiver/otlpreceiver) | [OTel Core Repo](https://github.com/open-telemetry/opentelemetry-collector) | v0.120.0 | ✅ [Core] (since 9.0) |
| [prometheusreceiver ](https://github.com/open-telemetry/opentelemetry-collector-contrib/tree/main/receiver/prometheusreceiver) | [OTel Contrib Repo](https://github.com/open-telemetry/opentelemetry-collector-contrib) | v0.120.1 | 🟡 [Extended] |
| [receivercreator ](https://github.com/open-telemetry/opentelemetry-collector-contrib/tree/main/receiver/receivercreator) | [OTel Contrib Repo](https://github.com/open-telemetry/opentelemetry-collector-contrib) | v0.120.1 | 🟡 [Extended] |
| [redisreceiver ](https://github.com/open-telemetry/opentelemetry-collector-contrib/tree/main/receiver/redisreceiver) | [OTel Contrib Repo](https://github.com/open-telemetry/opentelemetry-collector-contrib) | v0.120.1 | 🟡 [Extended] |
| [zipkinreceiver ](https://github.com/open-telemetry/opentelemetry-collector-contrib/tree/main/receiver/zipkinreceiver) | [OTel Contrib Repo](https://github.com/open-telemetry/opentelemetry-collector-contrib) | v0.120.1 | 🟡 [Extended] |
|***Exporters***||||
| [debugexporter ](https://github.com/open-telemetry/opentelemetry-collector/tree/main/exporter/debugexporter) | [OTel Core Repo](https://github.com/open-telemetry/opentelemetry-collector) | v0.120.0 | 🟡 [Extended] |
| [elasticsearchexporter ](https://github.com/open-telemetry/opentelemetry-collector-contrib/tree/main/exporter/elasticsearchexporter) | [OTel Contrib Repo](https://github.com/open-telemetry/opentelemetry-collector-contrib) | v0.120.1 | ✅ [Core] (since 9.0) |
| [fileexporter ](https://github.com/open-telemetry/opentelemetry-collector-contrib/tree/main/exporter/fileexporter) | [OTel Contrib Repo](https://github.com/open-telemetry/opentelemetry-collector-contrib) | v0.120.1 | 🟡 [Extended] |
| [kafkaexporter ](https://github.com/open-telemetry/opentelemetry-collector-contrib/tree/main/exporter/kafkaexporter) | [OTel Contrib Repo](https://github.com/open-telemetry/opentelemetry-collector-contrib) | v0.120.1 | 🟡 [Extended] |
| [loadbalancingexporter ](https://github.com/open-telemetry/opentelemetry-collector-contrib/tree/main/exporter/loadbalancingexporter) | [OTel Contrib Repo](https://github.com/open-telemetry/opentelemetry-collector-contrib) | v0.120.1 | 🟡 [Extended] |
| [otlpexporter ](https://github.com/open-telemetry/opentelemetry-collector/tree/main/exporter/otlpexporter) | [OTel Core Repo](https://github.com/open-telemetry/opentelemetry-collector) | v0.120.0 | ✅ [Core] (since 9.0) |
| [otlphttpexporter ](https://github.com/open-telemetry/opentelemetry-collector/tree/main/exporter/otlphttpexporter) | [OTel Core Repo](https://github.com/open-telemetry/opentelemetry-collector) | v0.120.0 | ✅ [Core] (since 9.0) |
|***Processors***||||
| [attributesprocessor ](https://github.com/open-telemetry/opentelemetry-collector-contrib/tree/main/processor/attributesprocessor) | [OTel Contrib Repo](https://github.com/open-telemetry/opentelemetry-collector-contrib) | v0.120.1 | ✅ [Core] (since 9.0) |
| [batchprocessor ](https://github.com/open-telemetry/opentelemetry-collector/tree/main/processor/batchprocessor) | [OTel Core Repo](https://github.com/open-telemetry/opentelemetry-collector) | v0.120.0 | ✅ [Core] (since 9.0) |
| [elasticinframetricsprocessor ](https://github.com/elastic/opentelemetry-collector-components/tree/main/processor/elasticinframetricsprocessor) | [Elastic Repo](https://github.com/elastic/opentelemetry-collector-components) | v0.13.0 | ✅ [Core] (since 9.0) |
| [elastictraceprocessor ](https://github.com/elastic/opentelemetry-collector-components/tree/main/processor/elastictraceprocessor) | [Elastic Repo](https://github.com/elastic/opentelemetry-collector-components) | v0.4.1 | ✅ [Core] (since 9.0) |
| [filterprocessor ](https://github.com/open-telemetry/opentelemetry-collector-contrib/tree/main/processor/filterprocessor) | [OTel Contrib Repo](https://github.com/open-telemetry/opentelemetry-collector-contrib) | v0.120.1 | 🟡 [Extended] |
| [geoipprocessor ](https://github.com/open-telemetry/opentelemetry-collector-contrib/tree/main/processor/geoipprocessor) | [OTel Contrib Repo](https://github.com/open-telemetry/opentelemetry-collector-contrib) | v0.120.1 | 🟡 [Extended] |
| [k8sattributesprocessor ](https://github.com/open-telemetry/opentelemetry-collector-contrib/tree/main/processor/k8sattributesprocessor) | [OTel Contrib Repo](https://github.com/open-telemetry/opentelemetry-collector-contrib) | v0.120.1 | ✅ [Core] (since 9.0) |
| [memorylimiterprocessor ](https://github.com/open-telemetry/opentelemetry-collector/tree/main/processor/memorylimiterprocessor) | [OTel Core Repo](https://github.com/open-telemetry/opentelemetry-collector) | v0.119.0 | 🟡 [Extended] |
| [resourcedetectionprocessor ](https://github.com/open-telemetry/opentelemetry-collector-contrib/tree/main/processor/resourcedetectionprocessor) | [OTel Contrib Repo](https://github.com/open-telemetry/opentelemetry-collector-contrib) | v0.120.1 | ✅ [Core] (since 9.0) |
| [resourceprocessor ](https://github.com/open-telemetry/opentelemetry-collector-contrib/tree/main/processor/resourceprocessor) | [OTel Contrib Repo](https://github.com/open-telemetry/opentelemetry-collector-contrib) | v0.120.1 | ✅ [Core] (since 9.0) |
| [transformprocessor ](https://github.com/open-telemetry/opentelemetry-collector-contrib/tree/main/processor/transformprocessor) | [OTel Contrib Repo](https://github.com/open-telemetry/opentelemetry-collector-contrib) | v0.120.1 | ✅ [Core] (since 9.0) |
|***Connectors***||||
| [elasticapmconnector ](https://github.com/elastic/opentelemetry-collector-components/tree/main/connector/elasticapmconnector) | [Elastic Repo](https://github.com/elastic/opentelemetry-collector-components) | v0.2.0 | ✅ [Core] (since 9.0) |
| [routingconnector ](https://github.com/open-telemetry/opentelemetry-collector-contrib/tree/main/connector/routingconnector) | [OTel Contrib Repo](https://github.com/open-telemetry/opentelemetry-collector-contrib) | v0.120.1 | ✅ [Core] (since 9.0) |
| [spanmetricsconnector ](https://github.com/open-telemetry/opentelemetry-collector-contrib/tree/main/connector/spanmetricsconnector) | [OTel Contrib Repo](https://github.com/open-telemetry/opentelemetry-collector-contrib) | v0.120.1 | 🟡 [Extended] |
|***Extensions***||||
| [filestorage ](https://github.com/open-telemetry/opentelemetry-collector-contrib/tree/main/extension/storage/filestorage) | [OTel Contrib Repo](https://github.com/open-telemetry/opentelemetry-collector-contrib) | v0.120.1 | |
| [healthcheckextension ](https://github.com/open-telemetry/opentelemetry-collector-contrib/tree/main/extension/healthcheckextension) | [OTel Contrib Repo](https://github.com/open-telemetry/opentelemetry-collector-contrib) | v0.120.1 | |
| [k8sobserver ](https://github.com/open-telemetry/opentelemetry-collector-contrib/tree/main/extension/observer/k8sobserver) | [OTel Contrib Repo](https://github.com/open-telemetry/opentelemetry-collector-contrib) | v0.120.1 | |
| [memorylimiterextension ](https://github.com/open-telemetry/opentelemetry-collector/tree/main/extension/memorylimiterextension) | [OTel Core Repo](https://github.com/open-telemetry/opentelemetry-collector) | v0.120.0 | |
| [pprofextension ](https://github.com/open-telemetry/opentelemetry-collector-contrib/tree/main/extension/pprofextension) | [OTel Contrib Repo](https://github.com/open-telemetry/opentelemetry-collector-contrib) | v0.120.1 | |
|***Providers***||||
| [envprovider ](https://github.com/open-telemetry/opentelemetry-collector/tree/main/confmap/provider/envprovider) | [OTel Core Repo](https://github.com/open-telemetry/opentelemetry-collector) | v1.26.0 | |
| [fileprovider ](https://github.com/open-telemetry/opentelemetry-collector/tree/main/confmap/provider/fileprovider) | [OTel Core Repo](https://github.com/open-telemetry/opentelemetry-collector) | v1.26.0 | |
| [httpprovider ](https://github.com/open-telemetry/opentelemetry-collector/tree/main/confmap/provider/httpprovider) | [OTel Core Repo](https://github.com/open-telemetry/opentelemetry-collector) | v1.26.0 | |
| [httpsprovider ](https://github.com/open-telemetry/opentelemetry-collector/tree/main/confmap/provider/httpsprovider) | [OTel Core Repo](https://github.com/open-telemetry/opentelemetry-collector) | v1.26.0 | |
| [yamlprovider ](https://github.com/open-telemetry/opentelemetry-collector/tree/main/confmap/provider/yamlprovider) | [OTel Core Repo](https://github.com/open-telemetry/opentelemetry-collector) | v1.26.0 | |

[Extended]: ./nomenclature#extended-components
[Core]: ./nomenclature#core-components