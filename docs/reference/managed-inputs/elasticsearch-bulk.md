---
navigation_title: "Managed Elasticsearch _bulk endpoint"
description: "Ingest log data from Elasticsearch _bulk shippers through the Elastic Cloud Managed Elasticsearch _bulk endpoint, and decide when to choose direct Elasticsearch instead."
applies_to:
  serverless:
    observability: ga
    security: ga
  deployment:
    ech: ga
products:
  - id: cloud-serverless
  - id: cloud-hosted
  - id: observability
  - id: security
---

# Ingest data with the Managed {{es}} _bulk endpoint [elasticsearch-bulk]

The Managed {{es}} _bulk endpoint ingests data sent in the [{{es}} `_bulk` API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-bulk) format. It accepts `_bulk` traffic natively, so shippers that already write to {{es}} can send data through [managed inputs](index.md) by pointing their existing {{es}} output at the endpoint. It's a dedicated managed input exposed on the `/_es` path of the same ingest host as the [Managed OTLP Endpoint](managed-otlp-endpoint.md) and the [Managed Prometheus Remote Write endpoint](prometheus-remote-write.md).

The endpoint is {{es}}-compatible: it emulates a subset of the `_bulk` API, so most shippers need only a new endpoint and credentials to start sending data. The managed input buffers the data and then indexes it into {{es}} asynchronously. Only log data is supported, and bulk actions must use the `create` action.

## When to use the Managed {{es}} _bulk endpoint [when-to-use]

The Managed {{es}} _bulk endpoint accepts the same requests as {{es}}, but it isn't a drop-in replacement for sending `_bulk` requests directly to {{es}}. Because data is buffered before it's indexed, the endpoint acknowledges data earlier, reports failures differently, and adds latency. Use the following comparison to decide which endpoint fits your workload.

The managed endpoint is a good fit when:

- You send log data from standalone {{product.elastic-agent}}, {{product.logstash}}, or another `_bulk` shipper that writes to log data streams, and want to use the same ingest endpoint and API key as your other [managed inputs](index.md).
- Your ingest volume varies sharply, with spikes well above the usual rate, and you'd rather have the managed endpoint absorb them than tune the output settings of every shipper.
- Your shippers have little or no local buffering, and a delay in indexing is acceptable.

Send data directly to {{es}} when:

- Your shipper must know that data was indexed before it marks the data as sent. The managed endpoint returns success when data is buffered, and delivery to {{es}} completes later, within limits. Refer to [Delivery behavior](#delivery-behavior).
- You need data in {{es}} within a predictable time, for example for alerting. The managed endpoint adds latency, and the delay grows when {{es}} is slow or unavailable.
- You rely on your shipper's own metrics for successful and failed events to monitor ingestion. With the managed endpoint, those metrics only tell you whether data was buffered, and managed inputs don't expose ingestion health or throughput metrics to you.
- You ship metrics, traces, or any data other than logs.
- You tune output settings such as batch size, flush interval, or worker count. You can't configure batching or retries on the managed side.
- Your {{product.elastic-agent}}s are managed by {{product.fleet}}. {{product.fleet}}-managed outputs can't use the endpoint.
- On {{ech}}, you use IP filters or private connectivity. Refer to [{{ech}} limitations](authentication-delivery-and-failure-handling.md#ech-limitations).

For the full list of constraints, refer to [Limitations](#limitations).

If you switch an existing shipper to the managed endpoint, compare document counts between the source and the destination data stream for a period after the switch, and monitor the destination with [Data Set Quality](docs-content://solutions/observability/data-set-quality-monitoring.md).

## Prerequisites [prerequisites]

- An {{serverless-full}} Observability or Security project, or an {{ech}} deployment on {{stack}} version 9.0 or later.
- A `_bulk`-compatible shipper that sends `create` actions to log data streams, such as standalone {{product.elastic-agent}}, {{product.logstash}}, or another shipper with an {{es}} output.
- An API key with the `event:write` privilege for the `apm` application. Refer to [Authentication](authentication-delivery-and-failure-handling.md#authentication) for the required key format and generation steps.
- Any {{es}} index templates and {{kib}} assets your shipper relies on, installed beforehand. The endpoint doesn't install them for you. Refer to [Limitations](#limitations).

## Set up the Managed {{es}} _bulk endpoint [set-up]

The Managed {{es}} _bulk endpoint uses the same ingest host as the [Managed OTLP Endpoint](managed-otlp-endpoint.md), with the `/_es` path appended. Its exact format depends on your deployment type. Copy the exact value from the {{ecloud}} Console, as described in the following steps.

::::::{stepper}

:::::{step} Find your endpoint

To find your Managed {{es}} _bulk endpoint:

1. Log in to the {{ecloud}} Console.
2. Do one of the following:
   - **{{serverless-full}}**: Find your project and select **Manage**.
   - **{{ech}}**: Find your deployment in **Hosted deployments** and select **Manage**.
3. In the **Application endpoints, cluster and component IDs** section, select **{{es}}**, then copy the **_bulk endpoint** value.

This endpoint value is shown as `<managed-_bulk-endpoint>` in the examples that follow. Your shipper appends the `_bulk` path (and any target index path) itself, so requests are sent to `POST <managed-_bulk-endpoint>/_bulk`.

:::::

:::::{step} Authenticate

Create an API key suitable for managed inputs as described in [Authentication](authentication-delivery-and-failure-handling.md#authentication). Send this key in each request's `Authorization` header as `ApiKey <api-key>`:

```http
Authorization: ApiKey <api-key>
```

Shippers that call `GET /_es` or `GET /_es/_license` at startup can use the same API key. You don't need to grant additional privileges for those requests.

:::::

:::::{step} Configure your shipper and send data

To send data, configure your shipper's {{es}} output with the following:

- **Endpoint**: Use your Managed {{es}} _bulk endpoint value (`<managed-_bulk-endpoint>`) in the host format for your deployment type. If your shipper has a separate path or URL-prefix setting, set it to `/_es` instead of including it in the host.
- **Authentication**: The API key you created for the managed inputs, sent as the HTTP header `Authorization: ApiKey <api-key>`.
- **Action**: Use `create`. Shippers that write to data streams already use this action.

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

A standalone {{product.elastic-agent}} configures its {{es}} output the same way, with one difference in how the API key is passed. The `api_key` setting takes the key as `<id>:<api_key>`, and {{product.elastic-agent}} encodes it itself. Don't use the encoded value from the **Add data** flow, which results in `401` errors. Instead, copy the **Beats** format from the {{kib}} **API keys** page, or join the `id` and `api_key` fields from the Create API key API response with a colon:

```yaml
outputs:
  default:
    type: elasticsearch
    hosts: ["<managed-_bulk-endpoint>"]
    api_key: "<id>:<api_key>"
```

If your shipper uses the `index`, `update`, or `delete` action, switch to `create` or target a data stream. Refer to [Limitations](#limitations).

To confirm your setup is working, check that your shipper reports successful (`2xx`) responses with no authentication errors, then open **Discover** and verify that new documents are landing in your target data stream.

If documents don't appear, they might have failed during asynchronous indexing. These errors aren't reported in the bulk response, so use [Data Set Quality](docs-content://solutions/observability/data-set-quality-monitoring.md) to monitor and triage indexing issues. For more details, refer to [Indexing errors and the failure store](authentication-delivery-and-failure-handling.md#failure-store).

:::::

::::::

## How _bulk data appears in {{es}} [data-mapping]

Each action in a `_bulk` request can specify its target through the `_index` field, so data lands in the data stream that your shipper already targets. For example, a shipper writing nginx access logs to `logs-nginx.access-default` continues to land there. If your shipper sets a fallback target in the request path (`/_es/<target>/_bulk`), that target is used for actions that omit `_index`. Only log data streams are supported targets. Refer to [Limitations](#limitations).

## Delivery behavior [delivery-behavior]

The Managed {{es}} _bulk endpoint emulates the {{es}} `_bulk` API, but because it ingests through managed inputs, it behaves differently from indexing directly into {{es}}. Keep the following in mind:

- **Batches are atomic.** The endpoint either enqueues the entire batch and returns success, or rejects the entire request. There's no per-document partial success or failure. If a valid batch can't be enqueued, the whole request fails with `503 Service Unavailable`. Malformed requests, unsupported actions, or missing targets fail with `400 Bad Request`.
- **A success response means the data is enqueued, not indexed.** A successful response returns an {{es}}-compatible body in which each item reports a `201` status. This confirms the managed input accepted the document, not that {{es}} has indexed it. Errors that occur later during indexing, such as mapping conflicts, happen asynchronously and aren't reported in the bulk response. Your shipper counts these documents as sent.
- **Delivery is retried, within limits.** The managed input retries indexing while {{es}} is temporarily unavailable or rejecting requests, which covers typical short interruptions. Retries and buffer retention are limited, so if {{es}} can't accept data for an extended period, data that couldn't be delivered in time is discarded. Because it never reached {{es}}, it isn't recorded in the failure store either.
- **Delivery time depends on {{es}}.** Buffered data is indexed as fast as {{es}} accepts it, so the delay grows when {{es}} is slow or unavailable, without any change visible to your shipper. Direct `_bulk` requests, by contrast, slow down or fail when {{es}} is under pressure, which your shipper can see and react to.
- **`require_data_stream` and `require_alias` are ignored.** The endpoint doesn't enforce these query parameters, so they don't protect you from writing to an unintended target type the way they do with {{es}}.
- **Compressed requests are supported.** The endpoint accepts `Content-Encoding: gzip` request bodies.

For shared buffering and delivery behavior across managed inputs, refer to [Buffering and delivery](authentication-delivery-and-failure-handling.md#delivery).

## Indexing errors and rate limiting [indexing-errors-and-rate-limiting]

Because indexing happens asynchronously, indexing failures such as mapping conflicts aren't reported in the bulk response, and the endpoint doesn't provide client-side visibility into them. To confirm your data was indexed, verify that documents landed in the destination data stream and use [Data Set Quality](docs-content://solutions/observability/data-set-quality-monitoring.md) to monitor indexing issues. For more detail on how indexing errors are handled, refer to [Indexing errors and the failure store](authentication-delivery-and-failure-handling.md#failure-store).

Under load, or when the service can't accept more data, the endpoint can respond with `429 Too Many Requests` or `503 Service Unavailable`. Configure your shipper to retry these responses with backoff and to queue data locally during transient rejections. For how rate limiting works and how it differs between {{serverless-full}} and {{ech}}, refer to [Managed inputs rate limiting](rate-limiting.md).

## Limitations [limitations]

The following limitations apply when using the Managed {{es}} _bulk endpoint:

- **Only log data is supported.** It must target `logs-*`, `logs.*`, or `logs` data streams, for example `logs-my_dataset-default` or the `logs.otel` wired stream. The endpoint doesn't reject other data or other targets: those requests still return success, and any failures after that aren't reported to your shipper. To send metrics and traces, use the direct {{es}} endpoint. For OpenTelemetry data, use the [Managed OTLP Endpoint](managed-otlp-endpoint.md).
- **{{product.beats}} aren't supported with their default settings.** They write to `<beat>-*` indices such as `filebeat-*` by default, which the endpoint accepts but never indexes.
- **Only `create` actions are supported.** Requests that use `index`, `update`, or `delete` actions are rejected with `400 Bad Request`. Features that depend on other actions, such as scripted upserts, aren't supported.
- **`require_data_stream` and `require_alias` aren't enforced.** Refer to [Delivery behavior](#delivery-behavior).
- **Duplicate detection isn't applied.** The endpoint doesn't deduplicate documents by `_id`, so client retries can produce duplicate documents.
- **Indexing outcomes aren't reported to your shipper.** The bulk response confirms that data was enqueued, not indexed, so errors such as mapping conflicts never reach your shipper. Managed inputs don't expose ingestion health metrics either, so monitor indexing with [Data Set Quality](docs-content://solutions/observability/data-set-quality-monitoring.md).
- **Delivery settings on the managed side aren't configurable.** Batching, flush intervals, retries, and worker counts are fixed, unlike the equivalent settings of a shipper's {{es}} output.
- **{{product.fleet}}-managed {{product.elastic-agent}} outputs can't use the endpoint.** {{product.fleet}} issues its agents {{es}} API keys with index privileges, which the endpoint doesn't accept. Only shippers you configure yourself, such as standalone {{product.elastic-agent}} and {{product.logstash}}, can use an API key for managed inputs.
- **Index templates, index lifecycle management (ILM) policies, and {{kib}} assets can't be installed through the endpoint.** It serves only the root (`/_es`), license (`/_es/_license`), and `_bulk` paths (`/_es/_bulk` and `/_es/<target>/_bulk`). {{product.elastic-agent}} and {{product.logstash}} setup steps that create index templates or load dashboards must run against {{es}} and {{kib}} directly before you send data.
- **{{ech}} network limitations apply.** IP filters don't apply to managed endpoints, and the endpoints aren't available over private connections. Refer to [{{ech}} limitations](authentication-delivery-and-failure-handling.md#ech-limitations).

## Related pages [related-pages]

- [Authentication, delivery, and failure handling with managed inputs](authentication-delivery-and-failure-handling.md): Shared authentication, buffering and delivery, and indexing-error handling across all managed inputs.
- [Managed inputs rate limiting](rate-limiting.md): How `429` responses work and how capacity limits differ between {{serverless-full}} and {{ech}}.
