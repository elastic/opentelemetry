# Manually configure the Elastic Distribution of OpenTelemetry Collector
Collecting logs and host metrics with the Elastic Distribution of OpenTelemetry (EDOT) Collector without using the [guided onboarding](guided-onboarding.md) requires completing some manual steps.

<!-- adding a comment to test; will remove. -->
<!-- adding a new comment here to generate a commit; will remove -->

## Before you begin
The EDOT Collector has the following requirements:

- The **Admin** role or higher is required to onboard system logs and metrics. To learn more, refer to [Assign user roles and privileges](https://www.elastic.co/docs/current/serverless/general/assign-user-roles).
- Root privileges on the host are required to run the OpenTelemetry collector used in this quickstart.
- The EDOT Collector only works on Kubernetes, Linux, and MacOS systems.

## Collect your logs and metrics

To manually configure the EDOT Collector, gather the following information:

- **Your Elasticsearch endpoint**: From the help menu in Elastic Cloud or your serverless Observability project, select **Connection details** and copy the **Elasticsearch endpoint**.
- **API key**:
   - **Elasticsearch Service:** From the help menu, select **Connection details** and select **Create and manage API keys**. From the **API keys** page, select **Create API key**. Give your API key a name, select **Create API key**, and copy the new API key.
   - **Serverless:** From the help menu, select **Connection details** and select the **API key** tab. Give your API key a name, select **Create API key**, and copy the new API key.

Then manually configure the EDOT Collector to collect logs and metrics on a MacOS or Linux system:

1. Download and extract the standalone Elastic Agent for your platform. For more on downloading and extracting a standalone Elastic Agent, refer to the first step in [Install standalone Elastic Agents](https://www.elastic.co/guide/en/fleet/current/install-standalone-elastic-agent.html).
1. From the Elastic Agent base directory, go to the `otel_samples` directory. The `platformlogs_hostmetrics.yml` file has the configurations for the receivers, processors, and exporters needed to collect logs and host metrics.
1. Copy the content of the `platformlogs_hostmetrics.yml` file.
1. From the Elastic Agent base directory, open the `otel.yml` file, and replace the content with the copied content from `platformlogs_hostmetrics.yml`.
1. Find and update the following settings in the configuration:
    - `file_storage.directory`: Set to the directory where you want to store you OpenTelemetry data.
    - `elasticsearch.endpoint`: Set to your Elasticsearch endpoint you copied earlier.
    - `elasticsearch.api_key`: Set to the API key you created earlier.
1. Run the EDOT collector with the following command:
   ```console
   ./elastic-agent otel --config otel.yml
   ```

Logs are collected from setup onward, so you won't see logs that occurred before starting the collector.
The default log path is `/var/log/*`. Update the path in the `otel.yml` file.

## Limitations

Refer to [Elastic OpenTelemetry Collector limitations](collector-limitations.md) for known limitations when using the Elastic Distribution of the OpenTelemetry collector.