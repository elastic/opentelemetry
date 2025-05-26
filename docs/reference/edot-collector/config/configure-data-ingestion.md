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

## ECS mode

ECS mode is not officially supported.

## What do users need to do if they only want certain logs / certain metrics / certain application telemetry

Enable / disable exporters on SDKs.

## Add / remove pipelines in the collector

Add / remove pipelines in the collector.