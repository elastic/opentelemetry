::::{tab-set}

:::{tab-item} Bearer token

```yaml
extensions:
  bearertokenauth:
    scheme: "APIKey"
    token: "<ENCODED_ELASTICSEARCH_APIKEY>"

  apmconfig:
    opamp:
      protocols:
        http:
          # Default is localhost:4320
          # endpoint: "<CUSTOM_OPAMP_ENDPOINT>"
    source:
      elasticsearch:
        endpoint: "<ELASTICSEARCH_ENDPOINT>"
        auth:
          authenticator: bearertokenauth
```
:::
:::{tab-item} API key

```yaml
extensions:
  apikeyauth:
    endpoint: "<YOUR_ELASTICSEARCH_ENDPOINT>"
    application_privileges:
      - application: "apm"
        privileges:
          - "config_agent:read"
        resources:
          - "-"
  apmconfig:
    opamp:
      protocols:
        http:
          auth:
            authenticator: apikeyauth
          # Optional: Configure TLS for the OpAMP server
          tls:
            cert_file: server.crt
            key_file: server.key
            ca_file: ca.crt
```

To send the API key, use the following header format:

```
Authorization: ApiKey <base64(id:api_key_value)>
```
:::
::::