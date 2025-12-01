---
navigation_title: GCP
description: Set up the EDOT Cloud Forwarder for GCP to bring your GCP logs to Elastic Observability.
applies_to:
  serverless:
    observability: preview
  deployment:
    ess: preview
  product:
    edot_cf_gcp: preview
products:
  - id: cloud-serverless
  - id: observability
  - id: edot-cf
---

# EDOT Cloud Forwarder for GCP

{{edot-cf}} for GCP provides a serverless, scalable way to ingest Google Cloud Platform logs into Elastic. It deploys the EDOT Collector as a Google Cloud Run service that listens for Pub/Sub push subscriptions, processes the logs, and forwards them to {{motlp}}.

## Architecture overview

The architecture for the {{edot-cf}} GCP is as pictured:

![EDOT Cloud Forwarder GCP overview](../images/edot-cloud-forwarder-gcp-overview.svg)

### Data flow

- Ingestion: Logs are sent to a Pub/Sub topic (either directly or via GCS Bucket notifications).
- Processing: A push subscription triggers the Cloud Run service, where the {{edot-cf}} is running.
- Forwarding: The service processes the data and exports it to Elastic via the {{motlp}}.
- Failure Handling: If processing fails (after retries), messages are routed to a dead letter topic and archived in a GCS Bucket for future analysis.

## Supported log types

Currently, {{edot-cf}} for GCP supports the following log types:

% TODO constanca-m MAYBE add permalink to otel version we will use in ECF GCP image in the table

| Log             | OTel mapping    |
|-----------------|-----------------|
| Cloud Audit Log | Cloud Audit Log |
| VPC Flow Log    | Access logs     |

:::{note}
We are working to support other popular log types and sources. [Contact us](docs-content://troubleshoot/ingest/opentelemetry/contact-support.md) to let us know of any specific requirements that could influence our plans.
:::


## Prerequisites

### Elastic requirements

- Access to {{motlp}} endpoint.
- Valid API key with ingest permissions.

You can refer to [Send data to Elastic](../motlp.md#send-data-to-elastic) documentation for more details.


### GCP permissions

% TODO constanca-m joecompute https://github.com/elastic/edot-cloud-forwarder-gcp/pull/225


## Quick start

% TODO Publish https://github.com/elastic/terraform-google-edot-cloud-forwarder on terraform public registry


## Features

The {{edot-cf}} is designed for reliability and observability.

### Flexible ingestion

Logs can be sent:

- Directly to a Pub/Sub topic.
- To a file placed in a GCS bucket. This will trigger an event notification to Pub/Sub which in turn will trigger the {{edot-cf}}.

### Reliability & Recovery

- Dead letter queue (DLQ): If a log entry fails to process or send to Elastic after the configured retries, it is not lost. The
  {{edot-cf}} automatically routes failed messages to a dedicated GCS bucket for later analysis.
- Smart retries: Built-in exponential backoff for transient network issues.

### Observability & Metadata

- Self-telemetry: You can configure the collector to send its own internal telemetry to the {{motlp}}.
- Enrich metadata: You can enable `include_metadata` to enrich your logs with context from the transport layer, including:
  - `bucket`
  - `object`
  - `subscription`
  - `message_id`
  - `delivery_attempt`

## Performance

% TODO

## Limitations

% TODO Add information on: permanent errors don't stop the retries

## Changelog

% How to link the CHANGELOG.md file if it is in a private repository?
% https://github.com/elastic/edot-cloud-forwarder-gcp/blob/main/CHANGELOG.md

