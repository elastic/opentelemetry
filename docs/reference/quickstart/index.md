---
navigation_title: Quickstart
description: This guide helps you set up Elastic Distributions for OpenTelemetry (EDOT) to monitor Kubernetes, applications, and hosts. It covers installing the EDOT Collector, enabling auto-instrumentation, and configuring data collection for metrics, logs, and traces in Elastic Observability.
---

# EDOT Quickstart Guide

This guide helps you set up Elastic Distributions for OpenTelemetry (EDOT) to monitor Kubernetes, applications, and hosts. It covers installing the EDOT Collector, enabling auto-instrumentation, and configuring data collection for metrics, logs, and traces in Elastic Observability.

:::note
*By the end of this guide, you’ll have a fully operational EDOT-powered monitoring pipeline sending data to Elastic Observability.*
:::

Choose the Quickstart guide based on the environment of your target system (`Kubernetes`, `Docker` or plain `Hosts / VMs`) and your Elastic deployment model (`Self-managed Elastic Stack`, `Elastic Cloud Serverless` or `Elastic Cloud Hosted`):

|                                    | ☸️ **Kubernetes**            | 🐳 **Docker**                 | 🖥 **Hosts / VMs**           |
|------------------------------------|:---------------------------:|:-----------------------------:|:---------------------------:|
| 🆂 **Self-managed Elastic Stack**  | [Quickstart 🆂 ☸️]   | [Quickstart 🆂 🐳 ]  | [Quickstart 🆂 🖥 ] |
| ☁️ **Elastic Cloud Serverless**     | [Quickstart ☁️ ☸️]   | [Quickstart ☁️ 🐳 ]   | [Quickstart ☁️ 🖥 ]  |
| 🗄️ **Elastic Cloud Hosted**        | [Quickstart 🗄️ ☸️]   | [Quickstart 🗄️ 🐳 ]  | [Quickstart 🗄️ 🖥 ] |

[Quickstart 🆂 ☸️]: ./self-managed/k8s
[Quickstart ☁️ ☸️]: ./serverless/k8s
[Quickstart 🗄️ ☸️]: ./ech/k8s
[Quickstart 🆂 🐳 ]: ./self-managed/docker
[Quickstart ☁️ 🐳 ]: ./serverless/docker
[Quickstart 🗄️ 🐳 ]: ./ech/docker
[Quickstart 🆂 🖥 ]: ./self-managed/hosts_vms
[Quickstart ☁️ 🖥 ]: ./serverless/hosts_vms
[Quickstart 🗄️ 🖥 ]: ./ech/hosts_vms