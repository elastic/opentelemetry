---
navigation_title: Elastic APM intake receiver
description: The Elastic APM intake receiver is an OpenTelemetry Collector component that receives APM data from Elastic APM Agents.
applies_to:
  stack:
  serverless:
    observability:
  product:
    edot_collector: ga
products:
  - id: cloud-serverless
  - id: observability
  - id: edot-collector
---

# Elastic APM intake receiver

The Elastic APM intake receiver is an OpenTelemetry Collector component that receives APM data from Elastic APM Agents. This allows users of classic APM agents to gradually migrate to OpenTelemetry and adapt their instrumentation to the new OTel-based approach.

The receiver takes the NDJSON data sent by [classic APM Agents](docs-content://reference/apm-agents/index.md) and turns it into OTel native data, which is processed by the Elastic APM processor and then exported to Elasticsearch, where it's stored in classic APM data streams.

:::{important}
The receiver supports the [Elastic Intake v2 protocol](https://github.com/elastic/apm-server/tree/main/docs/spec/v2).

Real user monitoring (RUM) intake and older intake protocols are not supported.
:::

## Get started

To use the Elastic APM intake receiver, include it in the receiver definitions of the [Collector configuration](/reference/edot-collector/config/index.md):

```yaml
receivers:
  elasticapmintake:
    agent_config:
      enabled: false
```

## Configuration

The Elastic APM intake receiver supports standard HTTP server configuration, including TLS/mTLS and authentication.

### TLS and mTLS settings

You can turn on TLS or mutual TLS to encrypt data in transit between Elastic APM agents and the receiver. Refer to [OpenTelemetry TLS server configuration](https://github.com/open-telemetry/opentelemetry-collector/blob/main/config/configtls/README.md#server-configuration) for more details.

For example:

```yaml
receivers:
  elasticapmintake:
    tls:
      cert_file: server.crt
      key_file: server.key
    agent_config:
      enabled: false
```

#### Agent environment variables [agent_config_ssl]

The Elastic APM intake receiver supports the following environment variables:

- `ELASTIC_APM_SERVER_URL`: The URL of the Elastic APM server.
- `ELASTIC_APM_SERVER_CERT`: The path to the server certificate file.

Refer to [OpenTelemetry TLS server configuration](https://github.com/open-telemetry/opentelemetry-collector/blob/main/config/configtls/README.md#server-configuration) for more details.

### Authentication settings

In addition to TLS, you can configure authentication to make sure that only authorized agents can send data to the receiver. The Elastic APM intake receiver supports any `configauth` authenticator. 

Use the recommended`apikeyauth` extension to validate Elastic APM API keys. For example:

```yaml
extensions:
  apikeyauth:
    endpoint: "<YOUR_ELASTICSEARCH_ENDPOINT>"
    application_privileges:
      - application: "apm"
        privileges:
          - "event:write"
        resources:
          - "-"
receivers:
  elasticapmintake:
    auth:
      authenticator: apikeyauth
    tls:
      cert_file: server.crt
      key_file: server.key
    agent_config:
      enabled: false
```

#### Agent environment variables [agent_config_auth]

The Elastic APM intake receiver supports the following environment variables:

- `ELASTIC_APM_API_KEY`: The API key to use for authentication.
- `ELASTIC_APM_SERVER_URL`: The URL of the Elastic APM server.
- `ELASTIC_APM_SERVER_CERT`: The path to the server certificate file.
