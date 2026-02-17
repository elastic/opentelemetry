To retrieve your {{motlp}} endpoint address and API key, follow these steps:

:::::{applies-switch}
::::{applies-item} serverless:
1. In {{ecloud}}, create an Observability project or open an existing one.
2. Go to **Add data**, select **Applications** and then select **OpenTelemetry**.
3. Copy the endpoint and authentication headers values.

Alternatively, you can retrieve the endpoint from the **Manage project** page and create an API key manually from the **API keys** page.
::::

::::{applies-item} ess: preview
1. Log in to the {{ecloud}} Console.
2. Find your deployment on the home page or on the **Hosted deployments** page, and then select **Manage**.
3. In the **Application endpoints, cluster and component IDs** section, select **Managed OTLP**.
4. Copy the public endpoint value.
::::
:::::