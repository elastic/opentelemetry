---
title: Components Description
layout: default
nav_order: 2
parent: Monitoring on Kubernetes
grand_parent: Use Cases
---

# Components description

Getting started with OpenTelemetry for Kubernetes observability requires an understanding of the following components, their functions, and interactions: OpenTelemetry Operator, Collectors, kube-stack Helm Chart, and auto-instrumentation resources.

## OpenTelemetry Operator

The OpenTelemetry Operator is a [Kubernetes Operator](https://kubernetes.io/docs/concepts/extend-kubernetes/operator/) implementation designed to manage OpenTelemetry resources in a Kubernetes environment. It defines and oversees the following Custom Resource Definitions (CRDs):

- [OpenTelemetry Collectors](https://github.com/open-telemetry/opentelemetry-collector): Agents responsible for receiving, processing, and exporting telemetry data such as logs, metrics, and traces.
- [Instrumentation](https://opentelemetry.io/docs/kubernetes/operator/automatic): Leverages OpenTelemetry instrumentation libraries to automatically instrument workloads.

All signals including logs, metrics, and traces are processed by the collectors and sent directly to Elasticsearch using the ES exporter. A collector's processor pipeline replaces the traditional APM server functionality for handling application traces.

## Kube-stack Helm Chart

The [kube-stack Helm chart](https://github.com/open-telemetry/opentelemetry-helm-charts/tree/main/charts/opentelemetry-kube-stack) is used to manage the installation of the operator (including its CRDs), and to configure a suite of collectors, which instrument various Kubernetes components to enable comprehensive observability and monitoring.

The chart is installed with a provided default `values.yaml` file that can be customized when needed.

## DaemonSet collectors

The OpenTelemetry components deployed within the DaemonSet collectors are responsible for observing specific signals from each node. To ensure complete data collection, these components must be deployed on every node in the cluster. Failing to do so will result in partial and potentially incomplete data.

The DaemonSet collectors handle the following data:

- Host Metrics: Collects host metrics (hostmetrics receiver) specific to each node.
- Kubernetes Metrics: Captures metrics related to the Kubernetes infrastructure on each node.
- Logs: Utilizes a filelog receiver to gather logs from all Pods running on the respective node.
- OTLP Traces Receiver: Opens an HTTP and a GRPC port on the node to receive OTLP trace data.

## Deployment collector

The OpenTelemetry components deployed within a Deployment collector focus on gathering data at the cluster level rather than at individual nodes. Unlike DaemonSet collectors, which need to be deployed on every node, a Deployment collector operates as a standalone instance.

The Deployment collector handles the following data:

- Kubernetes Events: Monitors and collects events occurring across the entire Kubernetes cluster.
- Cluster Metrics: Captures metrics that provide insights into the overall health and performance of the Kubernetes cluster.

## Auto-instrumentation

The Helm chart is configured to enable zero-code instrumentation using the [Operator's Instrumentation resource](https://github.com/open-telemetry/opentelemetry-operator/?tab=readme-ov-file#opentelemetry-auto-instrumentation-injection) for the following programming languages:

- Go
- Java
- Node.js
- Python
- .NET