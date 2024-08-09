# Collect logs and metrics using the guided onboarding
The guided onboarding in Kibana or in a serverless Observability project walks you through collecting logs and metrics using the Elastic Distribution for OpenTelemetry Collector.
To configure the Elastic OTel Collector manually, refer to the [manual configuration](manual-configuration.md) docs.

## Before you begin
The onboarding has the following requirements:

- The **Admin** role or higher is required to onboard system logs and metrics. To learn more, refer to [Assign user roles and privileges](https://www.elastic.co/docs/current/serverless/general/assign-user-roles).
- Root privileges on the host are required to run the OpenTelemetry collector used in this quickstart.
- The Elastic OTel Collector only works on Kubernetes, Linux, and MacOS systems.
- Refer to [Elastic OpenTelemetry Collector limitations](collector-limitations.md) for known limitations when using the Elastic OTel Collector.

## Collect your logs and metrics

Follow these steps to collect logs and metrics using the Elastic OTel collector:

1. Open an [Elastic Cloud](cloud.elastic.co) deployment or a serverless Observability project.
1. To open the guided onboarding, either:
   1. In an Elastic Cloud deployment, open Kibana, and go to **Observability** → **Add Data**.
   1. In a serverless Observability project, go to **Add Data**.
1. Select **Collect and analyze logs**, and then select **OpenTelemetry**.
1. Select the appropriate platform, and complete the following:
   1. For **MacOS and Linux**, copy the command, open a terminal on your host, and run the command to download and configure the OpenTelemetry collector.
   1. For **Kubernetes**, download the manifest.
1. Copy the command under Step 2:
   1. For **MacOS and Linux**, run the command in your terminal to start the Elastic OTel collector.
   1. For **Kubernetes**, run the command from the directory where you downloaded the manifest to install the Elastic OTel Collector on every node of your cluster.

Logs are collected from setup onward, so you won't see logs that occurred before starting the Elastic OTel Collector.
The default log path is `/var/log/*`. To update the path, modify `otel.yml`.

Under **Visualize your data**, you'll see links to **Logs Explorer** to view your logs and **Hosts** to view your host metrics.

## Limitations

Refer to [Elastic OpenTelemetry Collector limitations](collector-limitations.md) for known limitations when using the Elastic Distribution for the OpenTelemetry collector.