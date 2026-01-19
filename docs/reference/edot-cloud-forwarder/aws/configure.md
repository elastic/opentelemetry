---
navigation_title: Configuration settings
description: Configure the EDOT Cloud Forwarder for AWS CloudFormation template parameters.
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

# Configure EDOT Cloud Forwarder for AWS

Before deploying {{edot-cf}} for AWS, configure the CloudFormation template parameters based on your specific requirements. The template uses the following settings to deploy and configure the EDOT Collector Lambda function.

## CloudFormation templates

The CloudFormation templates are hosted in a public Amazon S3 bucket and are accessible through HTTPS URL. You can reference these templates directly during deployment or download them for local use.

| Log type | Log source | CloudFormation template |
| --- | --- | ------------------------------------------------ |
| VPC |  S3 | `https://edot-cloud-forwarder.s3.amazonaws.com/v1/latest/cloudformation/s3_logs-cloudformation.yaml` |
| ELB |  S3 | `https://edot-cloud-forwarder.s3.amazonaws.com/v1/latest/cloudformation/s3_logs-cloudformation.yaml` |
| CloudTrail |  S3 | `https://edot-cloud-forwarder.s3.amazonaws.com/v1/latest/cloudformation/s3_logs-cloudformation.yaml` |
% | CloudWatch logs | `https://edot-cloud-forwarder.s3.amazonaws.com/v1/latest/cloudformation/cloudwatch_logs-cloudformation.yaml` |

For specific versions, edit `latest` in the URL to the required version in the format `vX.Y.Z`.

## Required settings

These are the required settings:

| Setting                                | Description |
| -------------------------------------- | ----------- |
| `stack-name`                           | Name of the CloudFormation stack, for example, `vpc-edot-cf`<br>Do not use the same name for different stacks. |
| `OTLPEndpoint`                         | The OTLP endpoint URL used for data ingestion, obtained from {{serverless-full}}. |
| `ElasticApiKey`                        | API key for authentication with Elastic, obtained from {{serverless-full}}. |

## Log source settings
<!-- TODO: Enable when CloudWatch logs are supported
Set the following settings based on the log source:

:::::{tab-set}

::::{tab-item} S3
-->
For logs sourced from S3, use the following settings:

| Setting            | Description |
| ------------------ | --- |
| `EdotCloudForwarderS3LogsType` | The encoding format for logs in the S3 bucket. Supported options:<br>- `vpcflow`: VPC Flow Logs<br>- `elbaccess`: ELB Access logs<br>- `cloudtrail`: CloudTrail Logs|
| `SourceS3BucketARN` | Amazon Resource Name (ARN) of the S3 bucket where logs are stored. This bucket will trigger the `edot-cloud-forwarder` Lambda function automatically. |
% | `S3LogsJsonEncodingMode` | _(Required if `EdotCloudForwarderS3LogsType` is `json`)_<br>Defines how JSON logs are structured:<br>- `body` _(default)_: Stores logs in the request body<br>- `body_with_inline_attributes`: Logs include inline attributes |
<!-- TODO: Enable when CloudWatch logs are supported

::::

::::{tab-item} CloudWatch

For logs sourced from CloudWatch, use the following settings:

| Setting            | Description |
| ------------------- | --- |
| `SourceCloudWatchLogGroupARN` | Amazon Resource Name (ARN) of the CloudWatch Log Group where the subscription filter will be created. This Log Group serves as the primary storage location for logs. |

:::{note}
The log group must already exist in your AWS account and region. If the ARN points to a non-existent log group, stack deployment or updates might fail.
:::
::::
:::::
-->

## Optional settings

These are optional settings you can set in the CloudFormation template:

| Setting                                  | Description                                                                                                                                                                                                                                                                                                                                                                                                                   |
|------------------------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `EdotCloudForwarderConcurrentExecutions` | Sets the maximum number of reserved concurrent executions for the Lambda function. Default value is `5`. <br> If new log files arrive frequently and you notice Lambda throttling, consider increasing concurrent executions. Increased reserved concurrency allows multiple log files to be processed in parallel, avoiding processing delays. <br>Make sure this value doesn't exceed your AWS account's concurrency limit. |
| `EdotCloudForwarderMemorySize`           | Sets the allocated memory for the Lambda function, measured in megabytes. The default value is `512` MB. Minimum value is `128` MB. Maximum value is `10240` MB. <br> More memory increases Lambda CPU allocation, increasing processing speed of events.                                                                                                                                                                     |
| `EdotCloudForwarderTimeout`              | Maximum execution time for the Lambda function, measured in seconds. The default is set to `900` seconds or 15 minutes. Accepts values from `1` second to `900` seconds.                                                                                                                                                                                                                                                      |
| `EdotCloudForwarderVersion`              | Version of the EDOT Cloud Forwarder. Expected format is semantic versioning, for example `1.0.0`. Defaults to the latest available patch version. Don't change this value unless advised by Elastic Support.                                                                                                                                                                                                                  |
| `EdotCloudForwarderExporterMaxQueueSize` | Sets the internal OTLP exporter queue size, measured in bytes. The default value is `50000000` (50 MB). <br> This parameter should be used only in exceptional edge cases that require manual tuning of the export queue.                                                                                                                                                                                                     |

The default values provided have been determined through extensive load testing across different log types and data volumes. For most use cases, these defaults provide a good balance between cost and performance. 

:::{tip}
Adjust these parameters only if you notice performance issues such as Lambda timeouts, throttling, high memory usage or dropped data. If you need assistance tuning these parameters for your specific workload, refer to [Contact support](docs-content://troubleshoot/ingest/opentelemetry/contact-support.md).
:::

## Sizing and performance tuning

Use the following sizing suggestions to select appropriate reserved concurrency (`EdotCloudForwarderConcurrentExecutions`) and Lambda memory (`EdotCloudForwarderMemorySize`) based on your expected traffic volumes. This helps maximize performance and prevent Lambda throttling at high log volumes.

:::{tip}
These recommendations can vary depending on how the load is distributed across multiple S3 files. Monitor CloudWatch metrics for Lambda throttling and concurrent executions, as well as CloudWatch Logs for execution duration per Lambda invocation.
:::

### VPC Flow Logs sizing

| Throughput      | Log rate                | Recommended concurrency | Recommended memory | Note                                                          |
|-----------------|-------------------------|-------------------------|--------------------|---------------------------------------------------------------|
| **< 5 MB/s**    | < 50,000 logs/s         | 5                       | 512 MB             | Default configuration                                         |
| **5 - 10 MB/s** | 50,000 - 100,000 logs/s | 10                      | 512 MB             | Increase concurrency                                          |
| **> 10 MB/s**   | > 100,000 logs/s        | > 10                    | 512 MB             | First increase concurrency and then increase memory as needed |

### ELB Access Logs sizing

| Throughput       | Log rate                  | Recommended concurrency | Recommended memory | Note                                                          |
|------------------|---------------------------|-------------------------|--------------------|---------------------------------------------------------------|
| **< 10 MB/s**    | < 25,000 events/s         | 5                       | 512 MB             | Default configuration                                         |
| **10 - 40 MB/s** | 25,000 - 100,000 events/s | 20                      | 512 MB             | Increase concurrency                                          |
| **> 40 MB/s**    | > 100,000 events/s        | > 20                    | 512 MB             | First increase concurrency and then increase memory as needed |

:::{tip}
ELB logs might produce files with gigabytes of data. The default configurations are confirmed to work up to 3GB log files, which translates roughly to 23,000 requests per second per ELB. If you expect higher request volumes, increase Lambda memory allocation.
:::

## Next steps

- [Deployment methods](deploy.md): Deploy using AWS CLI, AWS Console, or AWS Serverless Application Repository.
- [Troubleshooting](troubleshooting.md): Diagnose and resolve issues with log forwarding.
