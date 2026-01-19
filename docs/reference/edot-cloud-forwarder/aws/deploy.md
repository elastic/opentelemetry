---
navigation_title: Deployment methods
description: Deploy the EDOT Cloud Forwarder for AWS using CloudFormation CLI, AWS Console, or AWS Serverless Application Repository.
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

# Deploy EDOT Cloud Forwarder for AWS

{{edot-cf}} for AWS can be deployed using any of the following methods:

| Deployment method | Description |
| --- | --- |
| CloudFormation (AWS CLI) | Deploy using AWS CLI commands with CloudFormation templates. |
| CloudFormation (AWS Console) | Deploy using the AWS Management Console UI. |
| AWS Serverless Application Repository (SAR) | Deploy directly from the AWS Serverless Application Repository. |

Each method achieves the same result and uses CloudFormation templates. Choose the method that best adapts to your workflow.

## Deploy using CloudFormation (AWS CLI)

Use the AWS CLI to deploy the EDOT Cloud Forwarder with CloudFormation templates. This method is ideal for automation and infrastructure-as-code workflows.

### Deployment examples

The following examples show how to deploy the ECF Cloud Forwarder using AWS CloudFormation CLI. Copy and paste these commands after replacing the placeholder values with your actual configuration.

- Use the `--template-url` flag to reference a template hosted on S3. 
- Use the `--region` flag to specify the AWS region where the CloudFormation stack will be deployed. The CloudFormation stack deployment region must match the region of the S3 bucket where your logs are stored.
- To always use the most recent stable templates, use the `latest` path. For example, `v1/latest`.  
- To pin a specific version, replace `latest` with the desired version tag. For example, `v1/v{{version.edot-cf-aws}}`.  

Alternatively, if you have downloaded the template file, use the `--template-body file://<path>` option with a local template file.

:::::{tab-set}
::::{tab-item} VPC Flow logs

This example deploys a CloudFormation stack to collect VPC Flow logs stored in an S3 bucket.

```sh
aws cloudformation create-stack \
  --stack-name edot-cloud-forwarder-vpc \
  --template-url https://edot-cloud-forwarder.s3.amazonaws.com/v1/latest/cloudformation/s3_logs-cloudformation.yaml \
  --capabilities CAPABILITY_NAMED_IAM \
  --region eu-central-1 \
  --parameters \
    ParameterKey=SourceS3BucketARN,ParameterValue=your-s3-vpc-bucket-arn \
    ParameterKey=OTLPEndpoint,ParameterValue="<placeholder>" \
    ParameterKey=ElasticAPIKey,ParameterValue="<placeholder>" \
    ParameterKey=EdotCloudForwarderS3LogsType,ParameterValue="vpcflow"
```
::::

::::{tab-item} ELB Access logs

This example deploys a CloudFormation stack to collect ALB Access logs stored in an S3 bucket.

```sh
aws cloudformation create-stack \
  --stack-name edot-cloud-forwarder-alb \
  --template-url https://edot-cloud-forwarder.s3.amazonaws.com/v1/latest/cloudformation/s3_logs-cloudformation.yaml \
  --capabilities CAPABILITY_NAMED_IAM \
  --region eu-central-1 \
  --parameters \
    ParameterKey=SourceS3BucketARN,ParameterValue=your-s3-alb-bucket-arn \
    ParameterKey=OTLPEndpoint,ParameterValue="<placeholder>" \
    ParameterKey=ElasticAPIKey,ParameterValue="<placeholder>" \
    ParameterKey=EdotCloudForwarderS3LogsType,ParameterValue="elbaccess"
```
::::

::::{tab-item} CloudTrail logs

This example deploys a CloudFormation stack to collect CloudTrail logs stored in an S3 bucket.

```sh
aws cloudformation create-stack \
  --stack-name edot-cloud-forwarder-cloudtrail \
  --template-url https://edot-cloud-forwarder.s3.amazonaws.com/v1/latest/cloudformation/s3_logs-cloudformation.yaml \
  --capabilities CAPABILITY_NAMED_IAM \
  --region eu-central-1 \
  --parameters \
    ParameterKey=SourceS3BucketARN,ParameterValue=your-cloudtrail-bucket-arn \
    ParameterKey=OTLPEndpoint,ParameterValue="<placeholder>" \
    ParameterKey=ElasticAPIKey,ParameterValue="<placeholder>" \
    ParameterKey=EdotCloudForwarderS3LogsType,ParameterValue="cloudtrail_log"
```
::::

<!-- To be added post GA

::::{tab-item} S3 Access logs

This example deploys a CloudFormation stack to collect S3 Access logs stored in an S3 bucket.

```sh
aws cloudformation create-stack \
  --stack-name edot-cloud-forwarder-s3-access \
  --template-url https://edot-cloud-forwarder.s3.amazonaws.com/v1/latest/cloudformation/s3_logs-cloudformation.yaml \
  --capabilities CAPABILITY_NAMED_IAM \
  --region eu-central-1 \
  --parameters \
    ParameterKey=SourceS3BucketARN,ParameterValue=your-s3-access-logs-bucket-arn \
    ParameterKey=OTLPEndpoint,ParameterValue="<placeholder>" \
    ParameterKey=ElasticAPIKey,ParameterValue="<placeholder>" \
    ParameterKey=EdotCloudForwarderS3LogsType,ParameterValue="s3_access_log"
```
::::

::::{tab-item} WAF logs

This example deploys a CloudFormation stack to collect AWS WAF logs stored in an S3 bucket.

```sh
aws cloudformation create-stack \
  --stack-name edot-cloud-forwarder-waf \
  --template-url https://edot-cloud-forwarder.s3.amazonaws.com/v1/latest/cloudformation/s3_logs-cloudformation.yaml \
  --capabilities CAPABILITY_NAMED_IAM \
  --region eu-central-1 \
  --parameters \
    ParameterKey=SourceS3BucketARN,ParameterValue=arn:aws:s3:::aws-waf-logs-your-bucket-arn \
    ParameterKey=OTLPEndpoint,ParameterValue="<placeholder>" \
    ParameterKey=ElasticAPIKey,ParameterValue="<placeholder>" \
    ParameterKey=EdotCloudForwarderS3LogsType,ParameterValue="waf_log"
```

:::{note}
Replace `aws-waf-logs-your-bucket-name` with your actual WAF logging bucket ARN. Remember that the bucket name must start with `aws-waf-logs-` as required by AWS WAF.
:::
::::

::::{tab-item} JSON logs

This example deploys a CloudFormation stack to collect JSON-formatted logs stored in an S3 bucket.

```sh
aws cloudformation create-stack \
  --stack-name edot-cloud-forwarder-json \
  --template-url https://edot-cloud-forwarder.s3.amazonaws.com/v1/latest/cloudformation/s3_logs-cloudformation.yaml \
  --capabilities CAPABILITY_NAMED_IAM \
  --region eu-central-1 \
  --parameters \
    ParameterKey=SourceS3BucketARN,ParameterValue=your-json-logs-bucket-arn \
    ParameterKey=OTLPEndpoint,ParameterValue="<placeholder>" \
    ParameterKey=ElasticAPIKey,ParameterValue="<placeholder>" \
    ParameterKey=EdotCloudForwarderS3LogsType,ParameterValue="json" \
    ParameterKey=S3LogsJsonEncodingMode,ParameterValue="body"
```
::::

::::{tab-item} CloudWatch logs

This example deploys a CloudFormation stack to collect CloudWatch logs sent to a Log Group.

```sh
aws cloudformation create-stack \
  --stack-name edot-cloud-forwarder-cw \
  --template-url https://edot-cloud-forwarder.s3.amazonaws.com/v1/latest/cloudformation/cloudwatch_logs-cloudformation.yaml \
  --capabilities CAPABILITY_NAMED_IAM \
  --region eu-central-1 \
  --parameters \
    ParameterKey=OTLPEndpoint,ParameterValue="<placeholder>" \
    ParameterKey=ElasticAPIKey,ParameterValue="<placeholder>" \
    ParameterKey=SourceCloudWatchLogGroupARN,ParameterValue="<your-log-group-arn>"
```

-->

:::{note}
The `--capabilities CAPABILITY_NAMED_IAM` flag is required because this CloudFormation template creates AWS Identity and Access Management (IAM) resources. More specifically, it creates a named IAM role (`LambdaExecutionRole`) for the Lambda function. To acknowledge that AWS CloudFormation might create or modify IAM resources with custom names, you must specify the `CAPABILITY_NAMED_IAM` capability. 
:::

::::
:::::

### Update an existing stack

To update an existing CloudFormation stack while preserving some parameter values, follow these steps:

::::::{stepper}

:::::{step} Identify the stack to update

Determine the name of the CloudFormation stack you want to modify.

:::::

:::::{step} Prepare the update command

Use the following structure for your update command:

- Include all required parameters.
- Use `UsePreviousValue=true` for parameters that should remain unchanged.
- Specify `ParameterValue=<new-value>` for parameters that need to be updated.

:::::

:::::{step} Run the `update-stack` command

Run the command with the following parameters:

```sh
aws cloudformation update-stack \
  --template-url https://edot-cloud-forwarder.s3.amazonaws.com/v1/latest/cloudformation/<template-file-name>.yaml \
  --stack-name <stack-name> \
  --capabilities CAPABILITY_NAMED_IAM \
  --region eu-central-1 \
  --parameters \
      ParameterKey=Param1,UsePreviousValue=true \
      ParameterKey=Param2,UsePreviousValue=true \
      ParameterKey=Param3,UsePreviousValue=true \
      ParameterKey=Param4,ParameterValue=<new-value>
```
::::{dropdown} Example using S3 logs template
For example, to modify the S3 bucket ARN for the `edot-cloud-forwarder-vpc` stack while keeping other parameter values unchanged:

```sh
aws cloudformation update-stack \
  --template-url https://edot-cloud-forwarder.s3.amazonaws.com/v1/latest/cloudformation/s3_logs-cloudformation.yaml \
  --stack-name edot-cloud-forwarder-vpc \
  --capabilities CAPABILITY_NAMED_IAM \
  --region eu-central-1 \
  --parameters \
      ParameterKey=OTLPEndpoint,UsePreviousValue=true \
      ParameterKey=ElasticAPIKey,UsePreviousValue=true \
      ParameterKey=EdotCloudForwarderS3LogsType,UsePreviousValue=true \
      ParameterKey=SourceS3BucketARN,ParameterValue=your-new-s3-vpc-bucket-arn
```
::::
:::::

:::::{step} Verify the update

After running the command, check the stack status in the AWS Management Console under **CloudFormation** → **Stacks**. Then, run this command to confirm the updated parameter values:

```sh
aws cloudformation describe-stacks --stack-name <stack-name>
```
:::::
::::::

## Deploy using CloudFormation (AWS Console)

### Quick start

Deploy {{edot-cf}} for AWS with one click using the AWS CloudFormation console:

[![Launch Stack](https://s3.amazonaws.com/cloudformation-examples/cloudformation-launch-stack.png)](https://console.aws.amazon.com/cloudformation/home?#/stacks/new?templateURL=https://edot-cloud-forwarder.s3.amazonaws.com/v1/latest/cloudformation/s3_logs-cloudformation.yaml)

After clicking the button:

1. Configure the required parameters:

   | Parameter | Description |
   | --- | --- |
   | `stack-name` | Name of the CloudFormation stack, for example `vpc-edot-cf`. |
   | `OTLPEndpoint` | The OTLP endpoint URL from {{serverless-full}} or {{ech}}. |
   | `ElasticApiKey` | API key for authentication with Elastic. |
   | `SourceS3BucketARN` | ARN of the S3 bucket where your logs are stored. |
   | `EdotCloudForwarderS3LogsType` | The log type: `vpcflow`, `elbaccess`, or `cloudtrail`. |

2. Select **Next** and check **Acknowledge IAM capabilities**.
3. Review your configuration and select **Submit** to deploy the stack.
4. Monitor the progress until the stack reaches the `CREATE_COMPLETE` state.

:::{tip}
The CloudFormation stack deployment region must match the region of the S3 bucket where your logs are stored.
:::

### Manual deployment

To manually specify the template, follow these steps:

1. Navigate to **CloudFormation** in the AWS Console. 
2. Select **Create Stack** and choose **With new resources (standard)** to start a fresh deployment.
3. Select one of the following options under **Specify template**:  
   - **Amazon S3 URL (Recommended)**: Paste the CloudFormation template URL from [CloudFormation templates](configure.md#cloudformation-templates).
   - **Upload a template file**: Download the template from the S3 URL and upload it manually.
4. Select **Next** and configure all required parameters using the settings described in [Configure the template](configure.md).  
5. Select **Next** again and check **Acknowledge IAM capabilities**. This is required because the template creates named IAM roles with permissions to access the required resources.  
6. Review your configuration and select **Submit** to deploy the stack.  
7. Monitor the progress until the stack reaches the `CREATE_COMPLETE` state.


### Update an existing stack

To modify parameters of an existing stack through the AWS Console:

1. Navigate to **CloudFormation** in the AWS Management Console.  
2. Select the stack you want to update.  
3. Click **Update stack** and select either **Make a direct update** or **Create a change set**.
4. Choose **Use existing template**.  
4. Select **Next**.  
5. Modify the parameter values as needed (refer to [Configure the template](configure.md) for parameter descriptions).  
6. Select **Next** and review your changes.  
7. Select **Submit** to apply the updates. In case of a change set, **Execute changeset** .
8. Monitor the stack update progress in the console.

## Deploy using AWS Serverless Application Repository

In addition to deploying through CloudFormation templates, you can deploy the EDOT Cloud Forwarder application directly from the AWS Serverless Application Repository (SAR).

### Deploy from SAR

To deploy from SAR, follow these steps:

1. Navigate to **AWS Serverless Application Repository** in the AWS Management Console.
2. Select **Available applications** and check the box **Show apps that create custom IAM roles or resource policies**.
3. Search for `edot-cloud-forwarder-s3-logs` and select the application.
4. **Configure the application settings**: Under **Application settings**, fill in the parameters described in the [Configure the template](configure.md) section. Refer to that section for details on each parameter.
5. **Acknowledge IAM role creation**: At the bottom of the page, check the box to acknowledge that the application will create custom IAM roles. This is required for the forwarder to access your S3 bucket and send data to Elastic Observability.
6. Select **Deploy**.

The deployment process will start, and a CloudFormation stack will be created with all the necessary resources. You can monitor the progress in the AWS CloudFormation console under **Stacks**.

:::{note}
The same [deployment considerations](index.md#deployment-considerations) apply to SAR deployments, including the requirement to deploy separate serverless applications for each log type and ensure the deployment region matches your S3 bucket region.
:::

## CloudFormation stack resources

The CloudFormation templates create a number of resources to process logs from a specific log source.

### Resources for S3 logs

This is a list of resources created by the stack when processing S3 logs.

| Resource name                       | Type                                  | Description                                                                                                                                                                                                                                           |
|-------------------------------------|---------------------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `CustomNotificationUpdater`         | `AWS::CloudFormation::CustomResource` | Custom resource used to manage S3 event notifications dynamically.                                                                                                                                                                                    |
| `LambdaExecutionRole`               | `AWS::IAM::Role`                      | IAM role granting permissions needed for the Lambda function to interact with S3 and other AWS services.                                                                                                                                              |
| `LambdaFunction`                    | `AWS::Lambda::Function`               | Core Lambda function responsible for processing incoming logs from S3. This is a key resource in the stack.                                                                                                                                           |
| `LambdaInvokeConfig`                | `AWS::Lambda::EventInvokeConfig`      | Configures error handling and invocation settings for the Lambda function.                                                                                                                                                                            |
| `LambdaLogGroup`                    | `AWS::Logs::LogGroup`                 | CloudWatch log group storing logs for the main Lambda function. Useful for debugging and monitoring.                                                                                                                                                  |
| `LambdaPermissionS3Bucket`          | `AWS::Lambda::Permission`             | Grants permission for S3 to invoke the Lambda function when new logs arrive.                                                                                                                                                                          |
| `LambdaS3TriggerPolicy`             | `AWS::IAM::Policy`                    | IAM policy allowing the Lambda function to process events triggered by S3.                                                                                                                                                                            |
| `NotificationUpdaterLambda`         | `AWS::Lambda::Function`               | Utility Lambda function handling S3 event notification updates dynamically.                                                                                                                                                                           |
| `NotificationUpdaterLambdaLogGroup` | `AWS::Logs::LogGroup`                 | CloudWatch log group storing logs for the `NotificationUpdaterLambda` function.                                                                                                                                                                       |
| `S3FailureBucketARN`                | `AWS::S3::Bucket`                     | ARN of the bucket for storing failed invocations from the `edot-cloud-forwarder` Lambda function, preventing data loss, in the format `arn:aws:s3:::your-bucket-name`. If not defined, the template creates a dedicated failure bucket automatically. |

The main Lambda function, `LambdaFunction`, is the core component for processing S3 logs. S3 event notifications are handled dynamically using `CustomNotificationUpdater` and `NotificationUpdaterLambda`. 

CloudWatch logs ensure detailed monitoring of Lambda executions. IAM roles and permissions control access between S3 and Lambda functions, while `S3FailureBucketARN` prevents data loss by capturing unprocessed logs.


<!-- TODO: Enable when CloudWatch logs are supported

### Resources for CloudWatch Logs

This is a list of resources created by the stack when CloudWatch logs are the source.

| Resource name                  | Type                             | Description |
|------------------------------------|--------------------------------------|----------------|
| `CloudWatchLogSubscriptionFilter` | `AWS::Logs::SubscriptionFilter` | Defines a filter that forwards logs from a CloudWatch Log Group to the Lambda function. Critical for log processing. |
| `LambdaExecutionRole`              | `AWS::IAM::Role`                   | IAM role granting necessary permissions for the Lambda function to interact with CloudWatch Logs and other AWS services. |
| `LambdaFunction`                   | `AWS::Lambda::Function`            | Core Lambda function responsible for processing incoming logs from CloudWatch. This is a key resource in the stack. |
| `LambdaInvokeConfig`               | `AWS::Lambda::EventInvokeConfig`   | Configures event invocation settings, including error handling and retry behavior. |
| `LambdaLogGroup`                   | `AWS::Logs::LogGroup`               | CloudWatch log group that stores execution logs for the main Lambda function, aiding monitoring and debugging. |
| `LambdaPermissionCloudWatch`       | `AWS::Lambda::Permission`          | Grants permission for CloudWatch Logs to invoke the Lambda function, enabling real-time log streaming. |
| `S3FailureBucketARN`               | `AWS::S3::Bucket`                   | ARN of the bucket for storing failed log events to prevent data loss, in the format `arn:aws:s3:::your-bucket-name`. |

The CloudWatch Log Subscription Filter, `CloudWatchLogSubscriptionFilter`, ensures logs are correctly forwarded to the Lambda function. The Lambda function, `LambdaFunction`, serves as the core processing unit for CloudWatch logs. 

CloudWatch Log Groups help monitor execution performance and debug issues. IAM permissions (`LambdaExecutionRole`, `LambdaPermissionCloudWatch`) control interactions between CloudWatch and Lambda, while the failure bucket, `S3FailureBucketARN`, helps prevent data loss in case of processing errors.

-->

## Remove a CloudFormation stack

If you no longer need a deployed stack and want to clean up all associated resources, you can remove it using either the AWS CLI or the AWS Console.

### Important considerations

Deleting a stack removes all AWS resources created by that stack. However:

- If you allowed the stack to automatically create a dedicated S3 bucket for failed Lambda invocations, that bucket is not removed if it contains objects, because CloudFormation doesn't force-remove non-empty buckets. To remove the bucket entirely, you must empty it manually before deleting it.
- If you specified an existing bucket through the `S3FailureBucketARN` parameter, that bucket is not removed because it is not managed by the stack.

### Remove using AWS CLI

Use the following command to remove a stack:

```sh
aws cloudformation delete-stack \
  --stack-name <stack-name> \
  --region <stack-region>
```

You can monitor the deletion progress through this command:

```sh
aws cloudformation describe-stacks \
  --stack-name <stack-name> \
  --region <stack-region>
```

If the stack deletion fails and remains in a `DELETE_FAILED` state, you can retry the deletion with force mode:

```sh
aws cloudformation delete-stack \
  --stack-name <stack-name> \
  --region <stack-region> \
  --deletion-mode FORCE_DELETE_STACK
```

This forcibly removes the stack's resources, except any that cannot be removed, like the failure S3 bucket if it still contains objects. For a complete cleanup, empty the bucket manually before retrying deletion.

:::{dropdown} Example: Deleting a stack using AWS CLI

The following command removes the `edot-cloud-forwarder-vpc` stack:

```sh
aws cloudformation delete-stack \
  --stack-name edot-cloud-forwarder-vpc \
  --region eu-central-1
```

Monitor the deletion progress:

```sh
aws cloudformation describe-stacks \
  --stack-name edot-cloud-forwarder-vpc \
  --region eu-central-1
```

:::

### Remove using AWS Console

To remove a stack using the AWS Management Console:

1. Navigate to **CloudFormation** in the AWS Management Console.
2. Select the stack you want to remove from the list.
3. Click **Delete** at the top of the stack details page.
4. Monitor the deletion progress on the **Events** tab or wait until the stack disappears from the stack list (indicating deletion is complete).

## Next steps

- [Configuration settings](configure.md): Learn about all configuration options, including optional settings and sizing recommendations.
- [Troubleshooting](troubleshooting.md): Diagnose and resolve issues with log forwarding.