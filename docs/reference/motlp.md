---
navigation_title: Managed OTLP Endpoint
description: Reference documentation for the Elastic Cloud Managed OTLP Endpoint.
applies_to:
  serverless:
    observability: preview
products:
  - id: cloud-serverless
  - id: observability
  - id: edot-collector
---

# Sending Data to Elastic Using the Managed OTLP Endpoint

The {{motlp}} endpoint allows you to send OpenTelemetry data directly to Elastic Cloud using the OTLP protocol. This guide explains how to find your {{motlp}} endpoint, create an API key for authentication, and configure different environments.


## 1. Locate Your {{motlp}} Endpoint

### Elastic Cloud Serverless
1. Create or Login to Go to an Observability project
2. Navigate to the project management page.
3. Click edit on **Connection alias** in the overview section.
4. Copy the **Managed OTLP endpoint** url.

<!--
## commented out until mOTLP on ECH is available
### Elastic Cloud on Elasticsearch ({{ech}})
1. Open your deployment in the Elastic Cloud console.
2. Navigate to **Integrations** and find **OpenTelemetry** or **Managed OTLP**.
3. Copy the endpoint URL shown.

### Self-Managed
For self-managed environments, you can deploy and expose an OTLP-compatible endpoint using the {{edot_collector}} as a gateway. Refer to [EDOT deployment docs](https://www.elastic.co/docs/reference/opentelemetry/edot-collector/modes#edot-collector-as-gateway).

-->

## 2. Create an API Key

You must generate an API key with appropriate ingest privileges to authenticate OTLP traffic.

### Steps:
1. In {{kibana}}, go to **Manage project** → **API Keys** → **Manage Project API Keys** 
2. Click **Create API Key**.
3. Name the key (e.g. `otlp-client`).
4. Apply any of the optional security settings
5. Click **Create API Key** and copy the value shown.

Copy this key to your final API key string which will be:

```
Authorization: ApiKey <your-api-key>
```

---

## Examples

### SDK Configuration Example

Set the following environment variables in your application:

```bash
export OTEL_EXPORTER_OTLP_ENDPOINT="https://<motlp-endpoint>"
export OTEL_EXPORTER_OTLP_HEADERS="Authorization=ApiKey <your-api-key>"
```

Avoid extra spaces in the header. For **Python SDKs** replace any spaces with `%20` 
`OTEL_EXPORTER_OTLP_HEADERS=Authorization=ApiKey%20<your-api-key>`

### OTLP Exporter Collector Example

Example configuration for the OpenTelemetry Collector using the OTLP exporter:

```yaml
exporters:
  otlp:
    endpoint: https://<motlp-endpoint>
    headers:
      Authorization: ApiKey <your-api-key>
```

Set the API key as an environment variable or directly in the configuration as shown above.

### Kubernetes Example: OTLP Exporter with Secret Reference
You can store your API key in a Kubernetes secret and reference it in your OTLP exporter configuration. This is more secure than hardcoding credentials.

**1. Encode and Store the API Key in a Secret**
The API key from Kibana does **not** include the `ApiKey` scheme. You must prepend `ApiKey ` before storing it.

For example, if your API key from Kibana is `abc123`, run:
```bash
kubectl create secret generic otlp-api-key \
  --namespace=default \
  --from-literal=api-key="ApiKey abc123"
```

**2. Reference the Secret in Your Collector Deployment**
Mount the secret as an environment variable or file, then reference it in your OTLP exporter configuration:
```yaml
exporters:
  otlp:
    endpoint: https://<motlp-endpoint>
    headers:
      Authorization: ${API_KEY}
```
And in your deployment spec:
```yaml
env:
  - name: API_KEY
    valueFrom:
      secretKeyRef:
        name: otlp-api-key
        key: api-key
```

---

## Troubleshooting
- **Missing ApiKey Scheme:** The API key copied from Kibana does **not** include the `ApiKey` scheme. Always prepend `ApiKey ` before using it in your configuration or encoding it for Kubernetes secrets. Example:
  - Correct: `Authorization: ApiKey abc123`
  - Incorrect: `Authorization: abc123`
- **Base64 Encoding:** When creating a Kubernetes secret, always encode the full string including the scheme (e.g., `ApiKey abc123`).
