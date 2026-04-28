To retrieve your {{motlp}} endpoint and generate an API key to authenticate your OTLP shipper, follow the steps for your environment.

:::::{applies-switch}
::::{applies-item} serverless:
**Using the Add data wizard (recommended)**

The Add data wizard retrieves the endpoint and generates an API key with the required privileges automatically:

1. In {{ecloud}}, create an Observability project or open an existing one.
2. Go to **Add data**, select **Applications**, and then select **OpenTelemetry**.
3. Copy the endpoint and authentication headers values.

**Creating an API key manually using {{kib}}**

Retrieve the endpoint from the **Manage project** page, then create an API key:

1. Go to **Admin and Settings** → **API keys**.
2. Click **Create API key**, enter a name, and expand **Control security privileges**.
4. In the role descriptors box, enter the following privileges:

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

**Creating an API key via the {{es}} API**

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
2. Click **Create API key**, enter a name, and select **Restrict privileges**.
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

**Create an API key via the {{es}} API**

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
