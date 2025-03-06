---
title: Quick Start
layout: default
nav_order: 2
---

# 🚀 EDOT Quickstart Guide

This guide helps you set up Elastic Distributions for OpenTelemetry (EDOT) to monitor Kubernetes, applications, and hosts. It covers installing the EDOT Collector, enabling auto-instrumentation, and configuring data collection for metrics, logs, and traces in Elastic Observability. 

> 🏁 *By the end of this guide, you’ll have a fully operational EDOT-powered monitoring pipeline sending data to Elastic Observability.*

Choose the Quick Start guide based on the environment of your target system (`Kubernetes`, `Docker` or plain `Hosts / VMs`) and your Elastic deployment model (`Self-managed`, `Elastic Cloud Serverless`, `Elastic Cloud Hosted`):

|                                 | ☸️ **Kubernetes**            | 🐳 **Docker**                 | 🖥 **Hosts / VMs**           |
|---------------------------------|:-------------------------:|:--------------------------:|:-------------------------:|
| 🆂 **Self-managed Elastic Stack**  | [Quick Start 🆂 ☸️]        | [Quick Start 🆂 🐳 ]        | [Quick Start 🆂 🖥 ] |
| ☁️ **Elastic Cloud Serverless**    |  [Quick Start ☁️ ☸️]        | [Quick Start ☁️ 🐳 ]        | [Quick Start ☁️ 🖥 ] |
| 🗄️ **Elastic Cloud Hosted**        |  [Quick Start 🗄️ ☸️]       |   [Quick Start 🗄️ 🐳 ]      | [Quick Start 🗄️ 🖥 ] |

## Troubleshooting
- [EDOT Collector Troubleshooting](_edot-collector/edot-collector-troubleshoot.md)
- [Auto-instrumentation Troubleshooting](_kubernetes/operator/troubleshoot-auto-instrumentation.md).


[Quick Start 🆂 ☸️]: ./self-managed/k8s
[Quick Start ☁️ ☸️]: ./serverless/k8s
[Quick Start 🗄️ ☸️]: ./ech/k8s
[Quick Start 🆂 🐳 ]: ./self-managed/docker
[Quick Start ☁️ 🐳 ]: ./serverless/docker
[Quick Start 🗄️ 🐳 ]: ./ech/docker
[Quick Start 🆂 🖥 ]: ./self-managed/hosts_vms
[Quick Start ☁️ 🖥 ]: ./serverless/hosts_vms
[Quick Start 🗄️ 🖥 ]: ./ech/hosts_vms