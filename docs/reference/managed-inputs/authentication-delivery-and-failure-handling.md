---
navigation_title: Authentication, delivery, and failure handling
description: Learn how Elastic Cloud managed inputs share authentication, buffering and delivery, the failure store, and Elastic Cloud Hosted network limitations.
type: overview
applies_to:
  serverless: ga
  deployment:
    ech: ga
products:
  - id: cloud-serverless
  - id: cloud-hosted
  - id: observability
  - id: security
---

# Authentication, delivery, and failure handling with managed inputs [authentication-delivery-and-failure-handling]

This page covers what all managed inputs share: how you authenticate, how data is buffered and delivered, what happens when indexing fails, and network limitations on {{ech}}. For protocol-specific setup, choose your endpoint in [Next steps](#next-steps).

## Authentication [authentication]

You can create an API key in the {{ecloud}} Console (for example from an **Add data** flow) or with the [{{es}} Create API key API](docs-content://deploy-manage/api-keys/elasticsearch-api-keys.md). The [Send data to the {{motlp}}](docs-content://solutions/observability/get-started/quickstart-elastic-cloud-otel-endpoint.md) quickstart walks through generating a pre-configured key. That same key works for all managed inputs.

To send data to any managed input, your API key must include the `event:write` privilege for the `apm` application. You use the same privilege for every managed input endpoint, including OpenTelemetry Protocol (OTLP), Prometheus Remote Write, and `_bulk`.

The following example creates a `managed_inputs_writer` role with the required privilege:

```json
{
  "managed_inputs_writer": {
    "applications": [
      {
        "application": "apm",
        "resources": ["*"],
        "privileges": ["event:write"]
      }
    ]
  }
}
```

Send the key in each request's `Authorization` header as `ApiKey <api-key>`.

:::{note}
Index-level privilege scoping is not supported for managed inputs. API keys restricted to specific index-level privileges return a `PermissionDenied` error.
:::

## Buffering and delivery [delivery]

Managed inputs provide a durable ingest layer in front of {{es}}:

- Incoming data is buffered before it reaches your {{es}} cluster.
- When the service can't accept more data, endpoints apply back-pressure and respond with `429 Too Many Requests` so clients can retry. Refer to [Managed inputs rate limiting](rate-limiting.md).
- A successful accept response means managed inputs durably accepted the data for processing, not that {{es}} has finished indexing it.

:::{note}
For the Managed {{es}} _bulk endpoint, a batch is atomic: the endpoint accepts or rejects the whole batch, and a `201` per item means the data is durably enqueued, not indexed. For details, refer to [Delivery behavior](elasticsearch-bulk.md#delivery-behavior).
:::

## Indexing errors and the failure store [failure-store]

A successful accept response from a managed input means the data was durably accepted for processing, not that {{es}} has indexed it. Indexing errors, such as mapping conflicts or ingest pipeline errors, can happen asynchronously after the data is accepted, and aren't reported back to the client.

Managed inputs don't enable or manage the [failure store](docs-content://manage-data/data-store/data-streams/failure-store.md). The failure store is an {{es}} data stream setting, so if the destination data stream has it enabled, documents that fail indexing are written there; otherwise, they aren't captured.

To confirm your data was indexed, verify that documents landed in the destination data stream, and use [Data Set Quality](docs-content://solutions/observability/data-set-quality-monitoring.md) to monitor and triage indexing issues.

## {{ech}} limitations [ech-limitations]

```{applies_to}
ech:
```

In {{ech}} deployments, the following limitations apply to managed inputs:

- [IP filters](docs-content://deploy-manage/security/ip-filtering-cloud.md) do not apply to managed endpoints.
- Managed endpoints are not available over a [private connection](docs-content://deploy-manage/security/private-connectivity.md). When private connectivity is configured, the public managed endpoint is still available.

## Next steps [next-steps]

After you understand authentication and delivery, configure the endpoint for your protocol:

- [Ingest OpenTelemetry data with the Managed OTLP endpoint](managed-otlp-endpoint.md)
- [Ingest Prometheus metrics with the Managed Prometheus Remote Write endpoint](prometheus-remote-write.md)
- [Ingest data with the Managed {{es}} _bulk endpoint](elasticsearch-bulk.md)

For `429` responses and capacity guidance, refer to [Managed inputs rate limiting](rate-limiting.md).
