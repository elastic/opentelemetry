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

![EDOT Cloud Forwarder GCP overview](../images/edot-cloud-forwarder-gcp-overview.png)

### Data flow

- Ingestion: Logs are sent to a Pub/Sub topic (either directly or using a GCS bucket notification).
- Processing: A push subscription triggers the Cloud Run service, where an OpenTelemetry collector is running.
- Forwarding: The service processes the data and exports it to {{ecloud}} using the {{motlp}}.
- Failure Handling: If processing or forwarding still fails after retries, the failed messages are routed to a dead-letter topic and archived in a GCS bucket for future analysis.

## Supported log types

Currently, {{edot-cf}} for GCP supports the following log types:

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

You should have the following permissions on your Google Cloud project:

<DocAccordion buttonContent="Project IAM Admin" initialIsOpen> 
The principal should be granted the built-in `roles/resourcemanager.projectIamAdmin` role, allowing them to manage IAM policies and roles at the project level.
</DocAccordion>

<DocAccordion buttonContent="Storage" initialIsOpen>
The following permissions are needed for Cloud Storage management: 
- `storage.buckets.create` 
- `storage.buckets.delete` 
- `storage.buckets.get` 
- `storage.buckets.getIamPolicy`
- `storage.buckets.setIamPolicy`
- `storage.buckets.update`
</DocAccordion>

<DocAccordion buttonContent="Secret Manager" initialIsOpen>
The following permissions are needed for Secret Manager management: 
- `secretmanager.secrets.create` 
- `secretmanager.secrets.delete` 
- `secretmanager.secrets.get` 
- `secretmanager.secrets.getIamPolicy` 
- `secretmanager.secrets.setIamPolicy` 
- `secretmanager.secrets.update` 
- `secretmanager.versions.access` 
- `secretmanager.versions.add` 
- `secretmanager.versions.destroy` 
- `secretmanager.versions.enable` 
- `secretmanager.versions.get` 
</DocAccordion>

<DocAccordion buttonContent="Pub/Sub" initialIsOpen> 
The following permissions are needed for Pub/Sub management: 
- `pubsub.subscriptions.create` 
- `pubsub.subscriptions.delete` 
- `pubsub.subscriptions.get` 
- `pubsub.subscriptions.getIamPolicy` 
- `pubsub.subscriptions.list` 
- `pubsub.subscriptions.setIamPolicy` 
- `pubsub.subscriptions.update` 
- `pubsub.topics.attachSubscription` 
- `pubsub.topics.create` 
- `pubsub.topics.delete` 
- `pubsub.topics.detachSubscription` 
- `pubsub.topics.get` 
- `pubsub.topics.getIamPolicy` 
- `pubsub.topics.setIamPolicy` 
- `pubsub.topics.update` 
</DocAccordion>

<DocAccordion buttonContent="Cloud Run" initialIsOpen> 
The following permissions are needed for Cloud Run management: 
- `run.operations.get` 
- `run.services.create` 
- `run.services.delete` 
- `run.services.get` 
- `run.services.getIamPolicy` 
- `run.services.setIamPolicy` 
- `run.services.update` 
</DocAccordion>

<DocAccordion buttonContent="Service Account" initialIsOpen> 
The following permissions are needed for Service Account management: 
- `iam.serviceAccountKeys.create` 
- `iam.serviceAccountKeys.get` 
- `iam.serviceAccounts.create` 
- `iam.serviceAccounts.delete` 
- `iam.serviceAccounts.get` 
- `iam.serviceAccounts.update` 
- `iam.serviceAccounts.actAs` 
</DocAccordion>

<DocAccordion buttonContent="Artifact Registry" initialIsOpen> 
The following permissions are needed: 
- `artifactregistry.repositories.create` 
- `artifactregistry.repositories.delete` 
- `artifactregistry.repositories.get` 
- `artifactregistry.repositories.getIamPolicy` 
- `artifactregistry.repositories.setIamPolicy` 
- `artifactregistry.repositories.update` 
- `artifactregistry.repositories.downloadArtifacts` 
</DocAccordion>


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

The current retry logic treats all failures the same way, whether they're temporary or permanent errors like an invalid log format. This means a message that can't ever be processed correctly will still go through all configured retries before finally being sent to the dead-letter topic and archived in the GCS bucket. While this ensures resilience against transient failures, it does mean you might incur unnecessary processing costs for messages that were never going to succeed.

## Changelog

% How to link the CHANGELOG.md file if it is in a private repository?
% https://github.com/elastic/edot-cloud-forwarder-gcp/blob/main/CHANGELOG.md

