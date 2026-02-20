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

Rate limiting occurs when the {{motlp}} receives data faster than it can process and index into {{es}}. The endpoint responds with HTTP `429` errors until the data volume is reduced.

## How rate limiting works

Rate limiting behavior differs by deployment type:

- **{{ech}}**: Rate limits depend on your {{es}} cluster capacity. If your cluster can't keep up with incoming data, the endpoint starts rejecting requests with `429` errors.
- **{{serverless-full}}**: Elastic manages scaling automatically. Rate limiting is rare and typically indicates a temporary event to protect our system. 

## Identifying rate limiting

When rate limiting occurs, the {{motlp}} responds with an HTTP `429` Too Many Requests status code. A log message similar to this appears in the OpenTelemetry Collector's output:

```
"error": "rpc error: code = ResourceExhausted desc = request exceeded available capacity"
```

For troubleshooting steps, refer to [Error: too many requests](./troubleshooting.md#error-too-many-requests).

## Resolving rate limiting

### {{ech}} deployments

For {{ech}} deployments, `429` errors typically indicate that your {{es}} cluster is undersized for the current data volume. If [AutoOps](./troubleshooting.md#use-autoops-to-diagnose-issues) is available in your region, use it to check CPU utilization, index queue depth, and node load to confirm whether your cluster is under-resourced. If AutoOps is not available in your region, [contact Elastic Support](docs-content://troubleshoot/ingest/opentelemetry/contact-support.md).

If metrics confirm the cluster needs more capacity, scale your deployment:

- [Scaling considerations](docs-content://deploy-manage/production-guidance/scaling-considerations.md)
- [Resize deployment](docs-content://deploy-manage/deploy/cloud-enterprise/resize-deployment.md)
- [Autoscaling in ECE and ECH](docs-content://deploy-manage/autoscaling/autoscaling-in-ece-and-ech.md)

Once your {{es}} capacity is scaled up or is able to accept the incoming data volume, requests to {{motlp}} will be accepted again.

### {{serverless-full}} deployments

For {{serverless-full}} projects, Elastic manages backend scaling automatically. If you experience persistent `429` errors, [contact Elastic Support](docs-content://troubleshoot/ingest/opentelemetry/contact-support.md).
