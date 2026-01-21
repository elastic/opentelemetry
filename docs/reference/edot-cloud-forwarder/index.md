---
navigation_title: EDOT Cloud Forwarder
description: Introduction to the EDOT Cloud Forwarder, the Elastic Distribution of OpenTelemetry (EDOT) Collector for Cloud providers. Send your telemetry data to Elastic Stack from AWS, GCP, and Azure.
applies_to:
  serverless:
    observability: preview
  deployment:
    ess: preview
products:
  - id: cloud-serverless
  - id: observability
  - id: edot-cf
---

# EDOT Cloud Forwarder

The Elastic Distribution of OpenTelemetry (EDOT) Cloud Forwarder provides the EDOT Collector as a function to collect and send your telemetry data to Elastic Observability from AWS, GCP, and Azure. {{edot-cf}} can collect telemetry data from object storage and cloud services.

{{edot-cf}} sends the data it collects directly to the [Managed OTLP endpoint](docs-content://solutions/observability/get-started/quickstart-elastic-cloud-otel-endpoint.md) of {{serverless-full}}.

## Supported cloud providers and services

{{edot-cf}} is available for the following cloud providers and services:

| Cloud provider | Cloud service           | Availability                                   |
|----------------|-------------------------|------------------------------------------------|
| AWS            | S3, CloudWatch          | [EDOT Cloud Forwarder for AWS](edot-cloud-forwarder-aws://reference/edot-cf-aws/index.md)     |
| Azure          | Blob Storage, Event Hub | [EDOT Cloud Forwarder for Azure](azure.md) |
| GCP            | GCS, Operations         | [EDOT Cloud Forwarder for GCP](gcp.md)     |

## Get started

To get started with {{edot-cf}}, select the setup guide for your cloud provider:

- [AWS](edot-cloud-forwarder-aws://reference/edot-cf-aws/index.md)
- [Azure](azure.md)
- [GCP](gcp.md)


