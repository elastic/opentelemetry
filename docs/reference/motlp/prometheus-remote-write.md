---
navigation_title: "Prometheus Remote Write"
description: "Ingest Prometheus metrics into Elasticsearch using the Prometheus Remote Write protocol through the Elastic Cloud Managed Prometheus Remote Write Endpoint."
applies_to:
  serverless:
    observability: preview
products:
  - id: cloud-serverless
  - id: observability
---

# Ingest Prometheus metrics with Managed inputs [prometheus-remote-write]

The Managed Prometheus Remote Write Endpoint ingests metrics sent in the [Prometheus Remote Write v1](https://prometheus.io/docs/specs/remote_write_spec/) (PRW) protocol. It accepts Prometheus PRW traffic natively, so you don't need to convert metrics to OTLP, and it's a dedicated [Managed input](index.md) separate from the [Managed OTLP Endpoint](managed-otlp-endpoint.md). Metrics land in {{es}} time series data streams (TSDS), the same result as sending PRW directly to {{es}}.

## When to use the Managed Prometheus Remote Write Endpoint

For {{serverless-full}} projects, the Managed Prometheus Remote Write Endpoint is the recommended way to ingest Prometheus metrics. Compared to sending metrics directly to the [{{es}} Prometheus remote write endpoint](docs-content://manage-data/data-store/data-streams/tsds-ingest-prometheus-remote-write.md), it provides:

- A single ingest endpoint and API key shared with the other [Managed inputs](index.md).
- Durable buffering, back-pressure, and retry on `429 Too Many Requests`.
- The same Prometheus-to-TSDS mapping as the {{es}} PRW endpoint, so the resulting data is identical.

:::{warning}
On {{serverless-full}}, use the Managed Prometheus Remote Write Endpoint rather than sending metrics directly to the [{{es}} Prometheus remote write endpoint](docs-content://manage-data/data-store/data-streams/tsds-ingest-prometheus-remote-write.md).

Direct ingest bypasses Managed inputs, uses different authentication, and has no buffering or processing before data reaches {{es}}. Use the direct {{es}} endpoint only for self-managed deployments, where Managed inputs aren't available. {{ech}} support for the Managed Prometheus Remote Write Endpoint is planned.
:::

## Prerequisites

- An {{serverless-full}} Observability project.
- A Managed inputs API key with the `event:write` privilege for the `apm` application. Refer to [Authentication](managed-otlp-endpoint.md#authentication) for the required key format and generation steps.

## Send Prometheus metrics through Managed inputs

Follow these steps to configure Prometheus to send metrics to the Managed Prometheus Remote Write Endpoint.

::::::{stepper}

:::::{step} Configure Prometheus

Add a `remote_write` entry to your Prometheus configuration:

```yaml
remote_write:
  - url: https://<managed-inputs-endpoint>/api/v1/write
    authorization:
      type: ApiKey
      credentials: <api-key>
```

To find `<managed-inputs-endpoint>`:

1. Log in to the {{ecloud}} Console.
2. Find your project and select **Manage**.
3. In the **Application endpoints, cluster and component IDs** section, select **Ingest**.
4. Copy the endpoint value and append `/api/v1/write`. For example: `https://<your-endpoint>.apm.elastic.cloud/api/v1/write`

:::::

:::::{step} Route metrics to custom data streams

By default, all PRW metrics land in `metrics-generic.prometheus-default`.

To route to a custom data stream, attach the `data_stream_dataset` and `data_stream_namespace` labels to your time series:

| Label | Sets | Example |
| --- | --- | --- |
| `data_stream_dataset` | Dataset component of the data stream name | `myapp` |
| `data_stream_namespace` | Namespace component of the data stream name | `production` |

A time series with `data_stream_dataset: myapp` and `data_stream_namespace: production` routes to `metrics-myapp.prometheus-production`.

In Prometheus, use `write_relabel_configs` to add these labels to every time series sent to a `remote_write` target:

```yaml
remote_write:
  - url: https://<managed-inputs-endpoint>/api/v1/write
    authorization:
      type: ApiKey
      credentials: <api-key>
    write_relabel_configs:
      - target_label: data_stream_dataset
        replacement: myapp
      - target_label: data_stream_namespace
        replacement: production
```

:::::

::::::

## How Prometheus data appears in {{es}}

Prometheus labels are mapped as TSDS dimensions in {{es}}, and metric types are inferred from naming conventions. For details on the full mapping behavior, refer to the [{{es}} Prometheus remote write endpoint](docs-content://manage-data/data-store/data-streams/tsds-ingest-prometheus-remote-write.md) documentation.

## Limitations

- URL-path routing (for example, `/_prometheus/metrics/{dataset}/api/v1/write`) to custom data streams is not supported through Managed inputs. Use [label-based routing](docs-content://manage-data/data-store/data-streams/tsds-ingest-prometheus-remote-write.md#route-by-labels) instead.
- Available on {{serverless-full}} only.
- Samples with non-finite values (NaN, Infinity) are silently dropped by {{es}}, and staleness markers are not supported.
