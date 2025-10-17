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
          # To specify a custom endpoint, uncomment the following line 
          # and set the endpoint to the custom endpoint
          # endpoint: "<CUSTOM_OPAMP_ENDPOINT>"
    source:
      elasticsearch:
        endpoint: "<ELASTICSEARCH_ENDPOINT>"
        auth:
          authenticator: bearertokenauth

service:
  extensions: [bearertokenauth, apmconfig]
```

:::{note}
For comprehensive authentication configuration options, refer to [Authentication methods](elastic-agent://reference/edot-collector/config/authentication-methods.md).
:::