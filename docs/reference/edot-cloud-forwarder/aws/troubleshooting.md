---
navigation_title: Troubleshooting
description: Resolve failed log forwarding, Lambda errors, and replay failed events in EDOT Cloud Forwarder for AWS.
type: troubleshooting
applies_to:
  serverless:
    observability:
  deployment:
    ess:
    self: unavailable
  product:
    edot_cf_aws: ga 1.0.0, preview =0.2.6
products:
  - id: cloud-serverless
  - id: observability
  - id: edot-cf
---

# Troubleshooting EDOT Cloud Forwarder for AWS

This page helps you diagnose and resolve issues with {{edot-cf}} for AWS when logs are not being forwarded to {{es}} as expected.

## Failed log forwarding

### Symptoms

You might experience one or more of the following symptoms:

- Logs are not appearing in {{es}} or {{kib}} dashboards.
- The S3 failure bucket contains unprocessed event files.
- CloudWatch logs for the Lambda function show errors.
- Lambda function metrics show increased error rates or throttling.
- `StatusCode` errors when invoking the Lambda function.

### Resolution

::::::{stepper}

:::::{step} Check CloudWatch logs for errors

Open the AWS CloudWatch console and navigate to the `LambdaLogGroup` created by the CloudFormation stack. Look for error messages that indicate:

- Network errors when connecting to the OTLP endpoint.
- Authentication failures due to invalid or expired API key.
- Log type mismatches between the S3 bucket content and the `EdotCloudForwarderS3LogsType` setting.

:::::

:::::{step} Verify your configuration

Confirm that your CloudFormation stack parameters are correct:

- `OTLPEndpoint` points to a valid Managed OTLP endpoint.
- `ElasticApiKey` is valid and not expired.
- `EdotCloudForwarderS3LogsType` matches the log format in your S3 bucket (`vpcflow`, `elbaccess`, or `cloudtrail`).
- The deployment region matches your S3 bucket region.

:::::

:::::{step} Check Lambda metrics

In CloudWatch Metrics Explorer, review the Lambda function metrics:

| Metric | What to look for |
| --- | --- |
| `Errors` | Increased error count indicates processing failures. |
| `Throttles` | High throttle count suggests you need to increase `EdotCloudForwarderConcurrentExecutions`. |
| `Duration` | Long durations approaching the timeout may cause incomplete processing. |
| `ConcurrentExecutions` | Compare against your reserved concurrency limit. |

:::::

:::::{step} Replay failed events

If events failed to process, they are stored in the S3 bucket specified by `S3FailureBucketARN`. Replay them by invoking the Lambda function with the `replayFailedEvents` trigger:

```sh
aws lambda invoke \
  --function-name <LAMBDA_NAME> \
  --payload '{ "replayFailedEvents": {"replayFailedEvents":{"dryrun":false,"removeOnSuccess":true}}}' \
  --cli-binary-format raw-in-base64-out /dev/null
```

Replace `<LAMBDA_NAME>` with the name of your Lambda function from the deployment.

The following options are available:

| Option | Description | Default |
| --- | --- | --- |
| `dryrun` | Run without processing events. Useful for understanding what would be replayed. | `false` |
| `removeOnSuccess` | Remove the error event from the S3 failure bucket after successful processing. | `true` |

When successful, you should get `"StatusCode": 200` as the output.

:::{tip}
Use `--timeout` with the AWS CLI to increase the Lambda timeout for custom invocations. If a timeout occurs, run the command multiple times to process all error events.
:::

:::::

:::::{step} Adjust sizing if needed

If you're experiencing throttling or timeouts, consider adjusting the Lambda configuration. Refer to [Sizing and performance tuning](configure.md#sizing-and-performance-tuning) for recommendations based on your log volume.

:::::

::::::

## Monitoring and troubleshooting

To monitor your {{edot-cf}} Lambda function performance and troubleshoot issues:

1. **CloudWatch Metrics Explorer**: View Lambda metrics such as:
   - Duration
   - ConcurrentExecutions
   - Errors
   - Throttles
   - Invocations

2. **CloudWatch Logs**: Check the Lambda function logs for:
   - Processing errors
   - Configuration issues
   - Data export failures

The `LambdaLogGroup` resource created by the CloudFormation stack stores all Lambda execution logs. Look for error messages or warnings that indicate configuration or performance issues.

## Best practices

- Monitor CloudWatch metrics regularly to catch issues early.
- Set up CloudWatch alarms for Lambda errors and throttles.
- Keep your API key up to date and rotate it before expiration.
- Start with default sizing and increase concurrency or memory only when metrics indicate a need.
- Ensure each log type uses a dedicated S3 bucket and CloudFormation stack.

## Resources

- [Configure EDOT Cloud Forwarder for AWS](configure.md)
- [Deploy EDOT Cloud Forwarder for AWS](deploy.md)
- [Contact support](docs-content://troubleshoot/ingest/opentelemetry/contact-support.md)
