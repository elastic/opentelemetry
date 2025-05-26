---
navigation_title: Configure data routing
description: Learn how to configure and customize data routing through the Elastic Distribution of OpenTelemetry Collector. 
applies_to:
  stack:
  serverless:
    observability:
products:
  - id: cloud-serverless
  - id: observability
  - id: edot-collector
---

# Configure data routing

Learn how to configure and customize data routing through the Elastic Distribution of OpenTelemetry Collector. 

## Data routing

You can route data to different data streams based on different criteria. For example, you can split data by K8s namespace into different data streams.

## What do users need to do if they only want certain logs / certain metrics / certain application telemetry

Enable / disable exporters on SDKs.

## Add / remove pipelines in the collector

Add / remove pipelines in the collector.

Data filtering at receiver level (for example, collected metrics).
Metrics filtering at processor level.
Logs processing / filtering for things like PII redaction.
Metric type conversion.
ECS use cases.