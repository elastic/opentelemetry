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

The {{motlp}} uses queue-based rate limiting to manage data ingestion. Rate limiting occurs when data is received faster than the backend can process and index it. If the queue backlog grows beyond capacity, the endpoint responds with HTTP `429` errors until the backlog is consumed.

## How rate limiting works

Rate limiting behavior differs by deployment type:

- **{{ech}}**: Rate limits depend on your {{es}} cluster capacity. If your cluster can't keep up with incoming data, the endpoint starts rejecting requests with `429` errors.
- **{{serverless-full}}**: Elastic manages scaling automatically. Rate limiting is rare and typically indicates a temporary backend scaling event.

## Identifying rate limiting

When rate limiting occurs, the {{motlp}} responds with an HTTP `429` Too Many Requests status code. A log message similar to this appears in the OpenTelemetry Collector's output:

```json
{
  "code": 8,
  "message": "error exporting items, request to <ingest endpoint> responded with HTTP Status Code 429"
}
```

For troubleshooting steps, refer to [Error: too many requests](./troubleshooting.md#error-too-many-requests).

## Resolving rate limiting

### {{ech}} deployments

For {{ech}} deployments, `429` errors typically indicate that your {{es}} cluster is undersized for the current data volume. Use [AutoOps](./troubleshooting.md#use-autoops-to-diagnose-issues) to check CPU utilization, index queue depth, and node load to confirm whether your cluster is under-resourced.

If metrics confirm the cluster needs more capacity, scale your deployment:

- [Scaling considerations](docs-content://deploy-manage/production-guidance/scaling-considerations.md)
- [Resize deployment](docs-content://deploy-manage/deploy/cloud-enterprise/resize-deployment.md)
- [Autoscaling in ECE and ECH](docs-content://deploy-manage/autoscaling/autoscaling-in-ece-and-ech.md)

Once the queue backlog is consumed and {{es}} capacity matches the data volume, requests are automatically accepted again.

### {{serverless-full}} deployments

For {{serverless-full}} projects, Elastic manages backend scaling automatically. If you experience persistent `429` errors, [contact Elastic Support](docs-content://troubleshoot/ingest/opentelemetry/contact-support.md).
