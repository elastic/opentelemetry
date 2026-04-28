To retrieve your {{motlp}} endpoint and generate an API key to authenticate your OTLP shipper, follow the steps for your environment.

:::::{applies-switch}
::::{applies-item} serverless:
**Find your endpoint**

1. Log in to the {{ecloud}} Console.
2. Find your project and select **Manage**.
3. In the **Application endpoints** section, select **Ingest**.
4. Copy the endpoint value.

:::{tip}
Alternatively, from within your project, go to **Add data**, select **Applications**, then **OpenTelemetry**, and copy the endpoint value. The Add data wizard also generates a pre-configured API key — copy the authentication headers value to skip the API key creation steps below.
:::

**Create an API key using {{kib}}**

1. Go to **Admin and Settings** → **API keys**.
2. Click **Create API key**, enter a name, and expand **Control security privileges**.
3. In the role descriptors box, enter the following privileges:

    ```json
    {
      "otlp_writer": {
        "cluster": [],
        "indices": [
          {
            "names": ["traces-generic.otel-*", "metrics-generic.otel-*", "logs-generic.otel-*"],
            "privileges": ["auto_configure", "create_doc"]
          }
        ]
      }
    }
    ```

4. Click **Create API key** and copy the encoded value.

**Create an API key using the {{es}} API**

Use the [Create API key](https://www.elastic.co/docs/api/doc/elasticsearch-serverless/operation/operation-security-create-api-key) API:

```console
POST /_security/api_key
{
  "name": "otlp-writer",
  "role_descriptors": {
    "otlp_writer": {
      "cluster": [],
      "indices": [
        {
          "names": ["traces-generic.otel-*", "metrics-generic.otel-*", "logs-generic.otel-*"],
          "privileges": ["auto_configure", "create_doc"]
        }
      ]
    }
  }
}
```

:::{note}
The API key both authenticates the OTLP shipper to the {{motlp}} endpoint and authorizes writes to the destination {{es}} data streams. The `auto_configure` and `create_doc` privileges are required for all target data streams. If you route data to custom datasets, add the corresponding index patterns to the `names` list.
:::
::::

::::{applies-item} ech:
**Find your endpoint**

1. Log in to the {{ecloud}} Console.
2. From the home page, find your deployment in **Hosted deployments**, and select **Manage**. Or, on the **Hosted deployments** page, select your deployment.
3. In the **Application endpoints, cluster and component IDs** section, select **Managed OTLP**.
4. Copy the public endpoint value.

**Create an API key using {{kib}}**

1. Open the **API keys** management page from the navigation menu.
2. Click **Create API key**, enter a name, and enable **Control security privileges**.
3. In the role descriptors box, enter the following privileges:

    ```json
    {
      "otlp_writer": {
        "cluster": [],
        "indices": [
          {
            "names": ["traces-generic.otel-*", "metrics-generic.otel-*", "logs-generic.otel-*"],
            "privileges": ["auto_configure", "create_doc"]
          }
        ]
      }
    }
    ```

4. Click **Create API key** and copy the encoded value.

**Create an API key using the {{es}} API**

Use the [Create API key](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-security-create-api-key) API:

```console
POST /_security/api_key
{
  "name": "otlp-writer",
  "role_descriptors": {
    "otlp_writer": {
      "cluster": [],
      "indices": [
        {
          "names": ["traces-generic.otel-*", "metrics-generic.otel-*", "logs-generic.otel-*"],
          "privileges": ["auto_configure", "create_doc"]
        }
      ]
    }
  }
}
```

:::{note}
The API key both authenticates the OTLP shipper to the {{motlp}} endpoint and authorizes writes to the destination {{es}} data streams. The `auto_configure` and `create_doc` privileges are required for all target data streams. If you route data to custom datasets, add the corresponding index patterns to the `names` list.
:::
::::
:::::
