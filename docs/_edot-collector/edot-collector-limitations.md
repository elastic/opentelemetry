---
title: Limitations
layout: default
nav_order: 4
---

# EDOT Collector Limitations

The Elastic Distribution of the OpenTelemetry (EDOT) Collector has the following limitations:

- **Host network panels do not display data in some Elastic Observability UIs**  
  Due to an upstream limitation, `host.network.*` metrics are not available from OpenTelemetry.  

- **Process state is unavailable in OpenTelemetry host metrics**  
  The `process.state` metric is not present and is assigned a dummy value of **Unknown** in the **State** column of the host processes table.  

- **Host OS version and operating system may show as "N/A"**  
  Although the Elasticsearch exporter processes resource attributes, it may not populate these values.  

- **Normalized Load data is missing unless the CPU scraper is enabled**  
  The `systm.load.cores` metric is required for the **Normalized Load** column in the **Hosts** table and the **Normalized Load** visualization in the host detailed view.  

- **MacOS collectors do not support CPU and disk metrics**  
  The [`hostmetrics receiver`](https://github.com/open-telemetry/opentelemetry-collector-contrib/tree/main/receiver/hostmetricsreceiver) does not collect these metrics on MacOS, leaving related fields empty.  

- **Permission issues may cause error logs for process metrics**  
  The [`hostmetrics receiver`](https://github.com/open-telemetry/opentelemetry-collector-contrib/tree/main/receiver/hostmetricsreceiver) logs errors if it cannot access certain process information due to insufficient permissions.  

- **Mapping errors appear temporarily in the console**  
  Initial mapping errors occur until the system completes the mapping process.

- **Ingest Pipelines with OTel-native Data**

- **Histograms only supported in delta temporality**