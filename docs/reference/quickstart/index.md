---
navigation_title: Quickstart
description: Learn how to set up the Elastic Distributions for OpenTelemetry (EDOT) to monitor Kubernetes, applications, and hosts. The guides cover installing the EDOT Collector, enabling auto-instrumentation, and configuring data collection for metrics, logs, and traces in Elastic Observability.
applies_to:
   stack:
   serverless:
    observability:
products:
  - id: cloud-serverless
  - id: observability
---

# Quickstart guides

Learn how to set up the Elastic Distributions for OpenTelemetry (EDOT) to monitor Kubernetes, applications, and hosts.

## Add data from the UI

You can quickly add data from hosts, Kubernetes, applications, and cloud services from the Observability UI.

1. Open Elastic Observability.
2. Go to **Add data**.
3. Select what you want to monitor.
4. Follow the instructions.

## Manual installation guides

The guides cover how to install the EDOT Collector, turn on auto-instrumentation, and configure data collection for metrics, logs, and traces in Elastic Observability.

Select a guide based on the environment of your target system and your Elastic deployment model.

| Deployment Model       | Kubernetes                              | Docker                                  | Hosts or VMs                          |
|-------------------------|-----------------------------------------|-----------------------------------------|---------------------------------------|
| Self-managed Elastic Stack | [Kubernetes on self-managed](./self-managed/k8s.md) | [Docker on self-managed](./self-managed/docker.md) | [Hosts or VMs on self-managed](./self-managed/hosts_vms.md) |
| Elastic Cloud Serverless  | [Kubernetes on serverless](./serverless/k8s.md)     | [Docker on serverless](./serverless/docker.md)     | [Hosts or VMs on serverless](./serverless/hosts_vms.md)     |
| Elastic Cloud Hosted      | [Kubernetes on hosted](./ech/k8s.md)               | [Docker on hosted](./ech/docker.md)               | [Hosts or VMs on hosted](./ech/hosts_vms.md)               |
