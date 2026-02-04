---
navigation_title: Rate limiting
description: Rate limiting for the Elastic Cloud Managed OTLP Endpoint.
applies_to:
  serverless:
    observability: ga
    security: ga
  deployment:
    ess: ga
products:
  - id: cloud-serverless
  - id: observability
  - id: edot-collector
---

# Rate limiting

Requests to the {{motlp}} are subject to rate limiting and throttling. If you send data at a rate that exceeds the limits, your requests might be rejected.

The following rate limits and burst limits apply:

| Deployment type | Rate limit | Burst limit | Dynamic scaling |
|----------------|------------|-------------|-----------------|
| Serverless | 30 MB/s | 60 MB/s | Not available |
| ECH | 1 MB/s (initial) | 2 MB/s (initial) | Yes |

As long as your data ingestion rate stays at or below the rate limit and burst limit, your requests are accepted.

:::{note}
For the {{serverless-full}} trial, the rate limit is reduced to 15 MB/s and the burst limit is 30 MB/s.
:::

## Dynamic rate scaling for {{ech}}

```{applies_to}
ess:
```

For {{ech}} deployments, rate limits can scale up or down dynamically based on backpressure from {{es}}. Every deployment starts with a 1 MB/s rate limit and 2 MB/s burst limit. The system automatically adjusts these limits based on your {{es}} capacity and load patterns. Scaling requires time, so sudden load spikes might still result in temporary rate limiting.

## Exceeding the rate limit

If you send data that exceeds the available limits, the {{motlp}} responds with an HTTP `429` Too Many Requests status code. A log message similar to this appears in the OpenTelemetry Collector's output:

```json
{
  "code": 8,
  "message": "error exporting items, request to <ingest endpoint> responded with HTTP Status Code 429"
}
```

The causes of rate limiting differ by deployment type:

- **{{serverless-full}}**: You exceed the 15 MB/s rate limit or 30 MB/s burst limit.
- **{{ech}}**: You send load spikes that exceed current limits (temporary `429`s) or your {{es}} cluster can't keep up with the load (consistent `429`s).

After your sending rate goes back to the allowed limit, or after the system scales up the rate limit for {{ech}}, requests are automatically accepted again.

## Solutions to rate limiting

The solutions to rate limiting depend on your deployment type:

### {{ech}} deployments

For {{ech}} deployments, if you're experiencing consistent `429` errors, the primary solution is to increase your {{es}} capacity. Because rate limits are affected by {{es}} backpressure, scaling up your {{es}} cluster reduces backpressure and, over time, increases the ingestion rate for your deployment.

To scale your deployment:

- [Scaling considerations](docs-content://deploy-manage/production-guidance/scaling-considerations.md)
- [Resize deployment](docs-content://deploy-manage/deploy/cloud-enterprise/resize-deployment.md)
- [Autoscaling in ECE and ECH](docs-content://deploy-manage/autoscaling/autoscaling-in-ece-and-ech.md)

Temporary `429`s from load spikes typically resolve on their own as the system scales up, as long as your {{es}} cluster has sufficient capacity.

### {{serverless-full}} deployments

For {{serverless-full}} projects, you can either decrease data volume or request higher limits.

To increase the rate limit, [contact Elastic Support](docs-content://troubleshoot/ingest/opentelemetry/contact-support.md).
