# Collect logs and metrics using the guided onboarding
The guided onboarding in Kibana or a serverless Observability project walks you through collecting logs and metrics using the Elastic OpenTelemetry Collector.
If you prefer manually configuring the Elastic OpenTelemetry collector, refer to [Manually configure the collector](docs/manual-configuration.md).

## Before you begin
The onboarding has the following requirements and limitations:

- The **Admin** role or higher is required to onboard system logs and metrics. To learn more, refer to <DocLink slug="/serverless/general/assign-user-roles" />.
- Root privileges on the host are required to run the OpenTelemetry collector used in this quickstart.
- The collector only work on Kubernetes, Linux, and MacOS systems.
- Refer to [Elastic OpenTelemetry Collector limitations](collector-limitations.md) for known limitations when using Elastic Distribution for the OpenTelemetry collector.

## Collect your logs and metrics

Follow these steps to collect logs and metrics using the Elastic OpenTelemetry collector

1. Open an [Elastic Cloud](cloud.elastic.co) deployment or a serverless Observability project.
1. To open the guided onboarding, either:
   1. In a Elastic Cloud deployment, open Kibana, and go to **Observability** → **Add Data**.
   1. In a serverless Observability project, go to **Add Data**.
1. Select **Collect and analyze logs**, and then select **OpenTelemetry**.
1. Select the appropriate platform:
   1. For **MacOS and Linux**, copy the command, open a terminal on your host, and run the command to download and configure the OpenTelemetry collector.
   1. For **Kubernetes**, download the manifest.
1. Copy the command under Step 2:
   1. For **MacOS and Linux**, run the command in your terminal to start the OpenTelemetry collector.
   1. For **Kubernetes**, run the command from the directory where you downloaded the manifest to install the collector on every node of your cluster.

Logs are collected from setup onward, so you won't see logs that occurred before starting the collector.
The default log path is `/var/log/*`. To update the path, modify the `otel.yml`.

Under **Visualize your data**, you'll see links to **Logs Explorer** to view your logs and **Hosts** to view your host metrics.