---
navigation_title: Elastic Cloud Forwarder
description: Introduction to {{edot-cf}}, the {{edot}} Collector for Cloud providers. Send your telemetry data to Elastic Stack from AWS, GCP, and Azure.
applies_to:
  serverless:
    observability: preview
  deployment:
    ech: preview
products:
  - id: cloud-serverless
  - id: observability
  - id: edot-cf
---

# {{edot-cf}}

{{edot-cf}} provides the {{agent}} as a function to collect and send your telemetry data to Elastic Observability from AWS, GCP, and Azure. {{edot-cf}} can collect telemetry data from object storage and cloud services.

{{edot-cf}} sends the data it collects directly to the [Managed OTLP endpoint](docs-content://solutions/observability/get-started/quickstart-elastic-cloud-otel-endpoint.md) of {{serverless-full}}.

## Supported cloud providers and services

{{edot-cf}} is available for the following cloud providers and services:

| Cloud provider | Cloud service           | Availability                                   |
|----------------|-------------------------|------------------------------------------------|
| AWS            | S3, CloudWatch          | [{{edot-cf}} for AWS](edot-cloud-forwarder-aws://reference/edot-cf-aws/index.md)     |
| Azure          | Blob Storage, Event Hub | [{{edot-cf}} for Azure](edot-cloud-forwarder-azure://reference/edot-cf-azure/index.md) |
| GCP            | GCS, Operations         | [{{edot-cf}} for GCP](gcp/index.md)     |

## Get started

To get started with {{edot-cf}}, select the setup guide for your cloud provider:

- [AWS](edot-cloud-forwarder-aws://reference/edot-cf-aws/index.md)
- [Azure](edot-cloud-forwarder-azure://reference/edot-cf-azure/index.md)
- [GCP](gcp/index.md)


