---
navigation_title: "Managed {{es}} _bulk endpoint"
description: "Ingest data from {{es}} _bulk shippers such as Beats, Elastic Agent, and Logstash through the Elastic Cloud Managed {{es}} _bulk endpoint."
applies_to:
  serverless: ga
  deployment:
    ech: ga
products:
  - id: cloud-serverless
  - id: cloud-hosted
  - id: elasticsearch
  - id: observability
  - id: security
---

# Ingest _bulk data with managed inputs [elasticsearch-bulk]

The Managed {{es}} _bulk endpoint ingests data sent in the [{{es}} `_bulk` API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-bulk) format. It accepts `_bulk` traffic natively, so shippers that already write to {{es}} can send data through [managed inputs](index.md) by pointing their existing {{es}} output at the endpoint. It's a dedicated managed input exposed on the `/_es` path of the same ingest host as the [Managed OTLP Endpoint](managed-otlp-endpoint.md) and the [Managed Prometheus Remote Write endpoint](prometheus-remote-write.md).

The endpoint is {{es}}-compatible: it emulates a subset of the `_bulk` API, so most shippers need only a new endpoint and credentials to start sending data. The managed input then durably buffers the data and routes it into {{es}}. Documents must use the `create` action. Refer to [Limitations](#limitations) for additional constraints.

## When to use the Managed {{es}} _bulk endpoint [when-to-use]

Use the Managed {{es}} _bulk endpoint to bring data shippers that rely on the {{es}} `_bulk` API into managed ingestion, including:

- {{product.beats}}
- {{product.elastic-agent}}
- {{product.logstash}}
- {{edot-cf}}
- Any other shipper that sends data using the {{es}} `_bulk` API.

Compared to sending `_bulk` requests directly to {{es}}, the Managed {{es}} _bulk endpoint provides:

- A single ingest endpoint and API key shared with the other [managed inputs](index.md).
- Durable buffering, back-pressure, and automatic retries before data reaches {{es}}.
- A low-friction path for existing {{product.beats}}, {{product.elastic-agent}}, and {{product.logstash}} deployments to adopt managed ingestion without re-architecting their pipelines.

:::{tip}
On {{serverless-full}} and {{ech}}, prefer the Managed {{es}} _bulk endpoint over sending `_bulk` requests directly to {{es}}. Direct ingest bypasses managed inputs, so it has no durable buffering or managed processing before data reaches {{es}}, and it authenticates with {{es}} credentials or an API key with index privileges instead of a managed inputs API key.
:::

## Prerequisites [prerequisites]

- An {{serverless-full}} project, or an {{ech}} deployment on {{stack}} version 9.0 or later.
- A `_bulk`-compatible shipper, such as {{product.beats}}, {{product.elastic-agent}}, {{product.logstash}}, or another shipper with an {{es}} output.
- A managed inputs API key with the `event:write` privilege for the `apm` application. Refer to [Authentication](managed-otlp-endpoint.md#authentication) for the required key format and generation steps.

## Find your Managed {{es}} _bulk endpoint [find-endpoint]

The Managed {{es}} _bulk endpoint uses the same ingest host as the [Managed OTLP Endpoint](managed-otlp-endpoint.md), with the `/_es` path appended, and looks similar to `https://<project>.ingest.<region>.<csp>.elastic.cloud/_es`.

To find your Managed {{es}} _bulk endpoint:

:::::{applies-switch}
::::{applies-item} serverless:
1. Log in to the {{ecloud}} Console.
2. Find your project and select **Manage**.
3. In the **Application endpoints, cluster and component IDs** section, select **{{es}}**, then copy the **_bulk endpoint** value.
::::

::::{applies-item} ech:
1. Log in to the {{ecloud}} Console.
2. Find your deployment in **Hosted deployments** and select **Manage**.
3. In the **Application endpoints, cluster and component IDs** section, select **{{es}}**, then copy the **_bulk endpoint** value.
::::
:::::

Configure your shipper's {{es}} output with this endpoint value, shown as `<managed-_bulk-endpoint>` in the examples that follow. Your shipper appends the `_bulk` path (and any target index path) itself, so requests are sent to `POST <managed-_bulk-endpoint>/_bulk`.

## Authentication [authentication]

The Managed {{es}} _bulk endpoint uses the same authentication as the other managed inputs: a managed inputs API key with the `event:write` privilege for the `apm` application. Refer to [Authentication](managed-otlp-endpoint.md#authentication) for the required key format and generation steps. Send the key in each request's `Authorization` header as `ApiKey <api-key>`.

Shippers that call `GET /_es` or `GET /_es/_license` at startup can use the same managed inputs API key. You don't need to grant additional privileges for those requests.

## Send _bulk data through managed inputs [send-data]

To send data, configure your shipper's {{es}} output with the following:

- **Endpoint**: your Managed {{es}} _bulk endpoint value (`<managed-_bulk-endpoint>`), similar to `https://<project>.ingest.<region>.<csp>.elastic.cloud/_es`. If your shipper has a separate path or URL-prefix setting, set it to `/_es` instead of including it in the host.
- **Authentication**: your managed inputs API key, sent as the HTTP header `Authorization: ApiKey <api-key>`. Refer to [Authentication](#authentication) for details.
- **Action**: use `create`. Shippers that write to data streams already use this action.

The following example configures a {{product.logstash}} `elasticsearch` output. Setting names and the exact way to pass credentials vary by shipper and version, so validate the configuration for your shipper:

```ruby
output {
  elasticsearch {
    hosts => ["<managed-_bulk-endpoint>"]
    custom_headers => {
      "Authorization" => "ApiKey <api-key>"
    }
    action => "create"
  }
}
```

{{product.beats}} and {{product.elastic-agent}} configure their {{es}} output the same way: point the output hosts at `<managed-_bulk-endpoint>` and provide the managed inputs API key. If your shipper uses the `index`, `update`, or `delete` action, switch to `create` or target a data stream. Refer to [Limitations](#limitations).

## How _bulk data appears in {{es}} [data-mapping]

Each action in a `_bulk` request specifies its target through the `_index` field, so data lands in the data stream or index that your shipper already targets. For example, a shipper writing nginx access logs to `logs-nginx.access-default` continues to land there. If your shipper sets a fallback target in the request path (`/_es/<target>/_bulk`), that target is used for actions that omit `_index`.

## Delivery behavior [delivery-behavior]

The Managed {{es}} _bulk endpoint emulates the {{es}} `_bulk` API, but because it ingests through managed inputs, it behaves differently from indexing directly into {{es}}. Keep the following in mind:

- **Batches are atomic.** The endpoint either durably enqueues the entire batch and returns success, or rejects the entire batch. There's no per-document partial success or failure.
- **A success response means "durably enqueued", not "indexed".** A successful response returns an {{es}}-compatible body in which each item reports a `201` status. This confirms managed inputs durably accepted the document, not that {{es}} has indexed it. Errors that occur later during indexing, such as mapping conflicts, happen asynchronously and aren't reported in the bulk response.
- **Compressed requests are supported.** The endpoint accepts `Content-Encoding: gzip` request bodies.

## Handle back-pressure and errors [backpressure]

Under load, or when the service can't accept more data, the endpoint can respond with `429 Too Many Requests` or `503 Service Unavailable`. {{es}} output shippers such as {{product.beats}}, {{product.elastic-agent}}, and {{product.logstash}} retry these responses automatically with backoff, so transient rejections don't lose data as long as your shipper can queue it.

For how rate limiting works and how it differs between {{serverless-full}} and {{ech}}, refer to [Rate limiting](rate-limiting.md).

## Limitations [limitations]

The following limitations apply when using the Managed {{es}} _bulk endpoint:

- Only `create` actions are supported. Requests that use `index`, `update`, or `delete` actions are rejected with `400 Bad Request`. This suits append-only data streams, which is the typical target for logs and metrics.
- Duplicate detection isn't applied. The endpoint doesn't deduplicate documents by `_id`, so client retries can produce duplicate documents.
