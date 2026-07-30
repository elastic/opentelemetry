---
navigation_title: Authentication, delivery, and failure handling
description: Learn how managed inputs share authentication, buffering and delivery, failure handling, and Elastic Cloud Hosted network limitations.
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

This page covers what all managed inputs share: how you authenticate, how data is briefly stored and delivered, what happens when indexing fails, and network limitations on {{ech}}. For protocol-specific setup, choose your endpoint in [Next steps](#next-steps).

## Authentication [authentication]

Managed inputs authenticate with an {{es}} API key that includes the `event:write` privilege for the `apm` application. The same `event:write` / `apm` privilege applies to every managed endpoint, including the OTLP, Prometheus Remote Write, and _bulk endpoints.

You can create this API key in one of the following ways:

:::{dropdown} From the Add data flow
:applies_to: {"serverless": {"observability": "ga"}, "ech": "ga"}

1. Select **Add data** in the navigation menu of your Serverless Observability project or {{ech}} deployment.
2. In the **Connect directly to the endpoint** section, select the managed endpoint for which you want to create an API key.
3. Select **Create key**, then copy the encoded value from the **API key** field.
:::

:::{dropdown} From the API keys management page in {{kib}}
1. Go to the **API keys** management page in the navigation menu or use the [global search field](docs-content://explore-analyze/find-and-organize/find-apps-and-objects.md).
2. Select **Create API key**, enter a name for the key, and enable **Control security privileges**.
3. In the role descriptors box, enter the following privileges:

    ```json
    {
      "managed-inputs-writer": {
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

4. Select **Create API key** and copy the encoded value.

For more details, refer to [Elasticsearch API keys](docs-content://deploy-manage/api-keys/elasticsearch-api-keys.md) and [Serverless project API keys](docs-content://deploy-manage/api-keys/serverless-project-api-keys.md).
:::

:::{dropdown} Using the Create API key API
Use the [Create API key API](https://www.elastic.co/docs/api/doc/elasticsearch-serverless/operation/operation-security-create-api-key). The same request works for both {{serverless-full}} and {{ech}}. For example, to create an API key named `managed-inputs-api-key`:

```console
POST /_security/api_key
{
  "name": "managed-inputs-api-key",
  "role_descriptors": {
    "managed-inputs-writer": {
      "applications": [
        {
          "application": "apm",
          "resources": ["*"],
          "privileges": ["event:write"]
        }
      ]
    }
  }
}
```
:::

Send the API key in the `Authorization` header of each request to the managed endpoint as `ApiKey <api-key>`. For example:

```http
Authorization: ApiKey <api-key>
```

:::{note}
Index-level privilege scoping is not supported for managed inputs.
:::

## Buffering and delivery [delivery]

Managed inputs provide a durable ingest layer in front of {{es}}:

- Incoming data is briefly stored (buffered) in a durable ingest layer before it reaches your {{es}} cluster. Buffered data is held for a limited time before it must be delivered.
- When the service can't accept more data, endpoints apply back-pressure and respond with `429 Too Many Requests` so clients can retry. Refer to [Managed inputs rate limiting](rate-limiting.md).

:::{note}
For the Managed {{es}} _bulk endpoint, a batch is atomic: the endpoint accepts or rejects the whole batch, and a `201` per item means the data is durably enqueued, not indexed. For details, refer to [Delivery behavior](elasticsearch-bulk.md#delivery-behavior).
:::

## Indexing errors and the failure store [failure-store]

To confirm your data was indexed, verify that documents landed in the destination data stream, and use [Data Set Quality](docs-content://solutions/observability/data-set-quality-monitoring.md) to monitor and triage indexing issues.

A successful accept response from a managed input means the data was durably accepted for processing, not that {{es}} has indexed it. Indexing errors, such as mapping conflicts or ingest pipeline errors, can happen asynchronously after the data is accepted, and aren't reported back to the client.

Managed inputs don't enable or manage the [failure store](docs-content://manage-data/data-store/data-streams/failure-store.md). The failure store is an {{es}} data stream setting. If the destination data stream has it enabled, documents that fail indexing are written there. If it isn't enabled, those documents aren't captured.

:::{warning}
If a document fails indexing and the destination data stream doesn't have the failure store enabled, the document is dropped. Because indexing errors happen after the data is accepted, your shipper still reports success, so this data loss is silent.
:::

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
