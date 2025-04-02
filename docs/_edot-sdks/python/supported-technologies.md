---
title: Supported Technologies
layout: default
nav_order: 3
parent: EDOT Python
---

# Technologies Supported by the EDOT Python SDK

## Python versions

The following Python versions are supported:

 * 3.8
 * 3.9
 * 3.10
 * 3.11
 * 3.12
 * 3.13

This follows the [OpenTelemetry Python Version Support](https://github.com/open-telemetry/opentelemetry-python/?tab=readme-ov-file#python-version-support).

## Instrumentations

We don't install instrumentations by default and we suggest to use our [edot-bootstrap](./setup/index#install-the-available-instrumentation) command to automatically install the available instrumentations.

| Name | Packages instrumented | Semantic conventions status |
|---|---|---|---|
| [elastic-opentelemetry-instrumentation-openai](https://github.com/elastic/elastic-otel-python-instrumentations/blob/main/instrumentation/elastic-opentelemetry-instrumentation-openai) | openai >= 1.2.0 | development
| [opentelemetry-instrumentation-aio-pika](https://github.com/open-telemetry/opentelemetry-python-contrib/tree/main/instrumentation/opentelemetry-instrumentation-aio-pika) | aio_pika >= 7.2.0, < 10.0.0 | development
| [opentelemetry-instrumentation-aiohttp-client](https://github.com/open-telemetry/opentelemetry-python-contrib/tree/main/instrumentation/opentelemetry-instrumentation-aiohttp-client) | aiohttp ~= 3.0 | migration
| [opentelemetry-instrumentation-aiohttp-server](https://github.com/open-telemetry/opentelemetry-python-contrib/tree/main/instrumentation/opentelemetry-instrumentation-aiohttp-server) | aiohttp ~= 3.0 | development
| [opentelemetry-instrumentation-aiokafka](https://github.com/open-telemetry/opentelemetry-python-contrib/tree/main/instrumentation/opentelemetry-instrumentation-aiokafka) | aiokafka >= 0.8, < 1.0 | development
| [opentelemetry-instrumentation-aiopg](https://github.com/open-telemetry/opentelemetry-python-contrib/tree/main/instrumentation/opentelemetry-instrumentation-aiopg) | aiopg >= 0.13.0, < 2.0.0 | development
| [opentelemetry-instrumentation-asgi](https://github.com/open-telemetry/opentelemetry-python-contrib/tree/main/instrumentation/opentelemetry-instrumentation-asgi) | asgiref ~= 3.0 | migration
| [opentelemetry-instrumentation-asyncio](https://github.com/open-telemetry/opentelemetry-python-contrib/tree/main/instrumentation/opentelemetry-instrumentation-asyncio) | asyncio | development
| [opentelemetry-instrumentation-asyncpg](https://github.com/open-telemetry/opentelemetry-python-contrib/tree/main/instrumentation/opentelemetry-instrumentation-asyncpg) | asyncpg >= 0.12.0 | development
| [opentelemetry-instrumentation-aws-lambda](https://github.com/open-telemetry/opentelemetry-python-contrib/tree/main/instrumentation/opentelemetry-instrumentation-aws-lambda) | | development
| [opentelemetry-instrumentation-boto](https://github.com/open-telemetry/opentelemetry-python-contrib/tree/main/instrumentation/opentelemetry-instrumentation-boto) | boto~=2.0 | development
| [opentelemetry-instrumentation-boto3sqs](https://github.com/open-telemetry/opentelemetry-python-contrib/tree/main/instrumentation/opentelemetry-instrumentation-boto3sqs) | boto3 ~= 1.0 | development
| [opentelemetry-instrumentation-botocore](https://github.com/open-telemetry/opentelemetry-python-contrib/tree/main/instrumentation/opentelemetry-instrumentation-botocore) | botocore ~= 1.0 | development
| [opentelemetry-instrumentation-cassandra](https://github.com/open-telemetry/opentelemetry-python-contrib/tree/main/instrumentation/opentelemetry-instrumentation-cassandra) | cassandra-driver ~= 3.25,scylla-driver ~= 3.25 | development
| [opentelemetry-instrumentation-celery](https://github.com/open-telemetry/opentelemetry-python-contrib/tree/main/instrumentation/opentelemetry-instrumentation-celery) | celery >= 4.0, < 6.0 | development
| [opentelemetry-instrumentation-click](https://github.com/open-telemetry/opentelemetry-python-contrib/tree/main/instrumentation/opentelemetry-instrumentation-click) | click >= 8.1.3, < 9.0.0 | development
| [opentelemetry-instrumentation-confluent-kafka](https://github.com/open-telemetry/opentelemetry-python-contrib/tree/main/instrumentation/opentelemetry-instrumentation-confluent-kafka) | confluent-kafka >= 1.8.2, <= 2.7.0 | development
| [opentelemetry-instrumentation-dbapi](https://github.com/open-telemetry/opentelemetry-python-contrib/tree/main/instrumentation/opentelemetry-instrumentation-dbapi) | dbapi | development
| [opentelemetry-instrumentation-django](https://github.com/open-telemetry/opentelemetry-python-contrib/tree/main/instrumentation/opentelemetry-instrumentation-django) | django >= 1.10 | development
| [opentelemetry-instrumentation-elasticsearch](https://github.com/open-telemetry/opentelemetry-python-contrib/tree/main/instrumentation/opentelemetry-instrumentation-elasticsearch) | elasticsearch >= 6.0 | development
| [opentelemetry-instrumentation-falcon](https://github.com/open-telemetry/opentelemetry-python-contrib/tree/main/instrumentation/opentelemetry-instrumentation-falcon) | falcon >= 1.4.1, < 5.0.0 | migration
| [opentelemetry-instrumentation-fastapi](https://github.com/open-telemetry/opentelemetry-python-contrib/tree/main/instrumentation/opentelemetry-instrumentation-fastapi) | fastapi ~= 0.58 | migration
| [opentelemetry-instrumentation-flask](https://github.com/open-telemetry/opentelemetry-python-contrib/tree/main/instrumentation/opentelemetry-instrumentation-flask) | flask >= 1.0 | migration
| [opentelemetry-instrumentation-grpc](https://github.com/open-telemetry/opentelemetry-python-contrib/tree/main/instrumentation/opentelemetry-instrumentation-grpc) | grpcio >= 1.42.0 | development
| [opentelemetry-instrumentation-httpx](https://github.com/open-telemetry/opentelemetry-python-contrib/tree/main/instrumentation/opentelemetry-instrumentation-httpx) | httpx >= 0.18.0 | migration
| [opentelemetry-instrumentation-jinja2](https://github.com/open-telemetry/opentelemetry-python-contrib/tree/main/instrumentation/opentelemetry-instrumentation-jinja2) | jinja2 >= 2.7, < 4.0 | development
| [opentelemetry-instrumentation-kafka-python](https://github.com/open-telemetry/opentelemetry-python-contrib/tree/main/instrumentation/opentelemetry-instrumentation-kafka-python) | kafka-python >= 2.0, < 3.0,kafka-python-ng >= 2.0, < 3.0 | development
| [opentelemetry-instrumentation-logging](https://github.com/open-telemetry/opentelemetry-python-contrib/tree/main/instrumentation/opentelemetry-instrumentation-logging) | logging | development
| [opentelemetry-instrumentation-mysql](https://github.com/open-telemetry/opentelemetry-python-contrib/tree/main/instrumentation/opentelemetry-instrumentation-mysql) | mysql-connector-python >= 8.0, < 10.0 | development
| [opentelemetry-instrumentation-mysqlclient](https://github.com/open-telemetry/opentelemetry-python-contrib/tree/main/instrumentation/opentelemetry-instrumentation-mysqlclient) | mysqlclient < 3 | development
| [opentelemetry-instrumentation-pika](https://github.com/open-telemetry/opentelemetry-python-contrib/tree/main/instrumentation/opentelemetry-instrumentation-pika) | pika >= 0.12.0 | development
| [opentelemetry-instrumentation-psycopg](https://github.com/open-telemetry/opentelemetry-python-contrib/tree/main/instrumentation/opentelemetry-instrumentation-psycopg) | psycopg >= 3.1.0 | development
| [opentelemetry-instrumentation-psycopg2](https://github.com/open-telemetry/opentelemetry-python-contrib/tree/main/instrumentation/opentelemetry-instrumentation-psycopg2) | psycopg2 >= 2.7.3.1,psycopg2-binary >= 2.7.3.1 | development
| [opentelemetry-instrumentation-pymemcache](https://github.com/open-telemetry/opentelemetry-python-contrib/tree/main/instrumentation/opentelemetry-instrumentation-pymemcache) | pymemcache >= 1.3.5, < 5 | development
| [opentelemetry-instrumentation-pymongo](https://github.com/open-telemetry/opentelemetry-python-contrib/tree/main/instrumentation/opentelemetry-instrumentation-pymongo) | pymongo >= 3.1, < 5.0 | development
| [opentelemetry-instrumentation-pymssql](https://github.com/open-telemetry/opentelemetry-python-contrib/tree/main/instrumentation/opentelemetry-instrumentation-pymssql) | pymssql >= 2.1.5, < 3 | development
| [opentelemetry-instrumentation-pymysql](https://github.com/open-telemetry/opentelemetry-python-contrib/tree/main/instrumentation/opentelemetry-instrumentation-pymysql) | PyMySQL < 2 | development
| [opentelemetry-instrumentation-pyramid](https://github.com/open-telemetry/opentelemetry-python-contrib/tree/main/instrumentation/opentelemetry-instrumentation-pyramid) | pyramid >= 1.7 | development
| [opentelemetry-instrumentation-redis](https://github.com/open-telemetry/opentelemetry-python-contrib/tree/main/instrumentation/opentelemetry-instrumentation-redis) | redis >= 2.6 | development
| [opentelemetry-instrumentation-remoulade](https://github.com/open-telemetry/opentelemetry-python-contrib/tree/main/instrumentation/opentelemetry-instrumentation-remoulade) | remoulade >= 0.50 | development
| [opentelemetry-instrumentation-requests](https://github.com/open-telemetry/opentelemetry-python-contrib/tree/main/instrumentation/opentelemetry-instrumentation-requests) | requests ~= 2.0 | migration
| [opentelemetry-instrumentation-sqlalchemy](https://github.com/open-telemetry/opentelemetry-python-contrib/tree/main/instrumentation/opentelemetry-instrumentation-sqlalchemy) | sqlalchemy >= 1.0.0, < 2.1.0 | development
| [opentelemetry-instrumentation-sqlite3](https://github.com/open-telemetry/opentelemetry-python-contrib/tree/main/instrumentation/opentelemetry-instrumentation-sqlite3) | sqlite3 | development
| [opentelemetry-instrumentation-starlette](https://github.com/open-telemetry/opentelemetry-python-contrib/tree/main/instrumentation/opentelemetry-instrumentation-starlette) | starlette >= 0.13, <0.15 | development
| [opentelemetry-instrumentation-system-metrics](https://github.com/open-telemetry/opentelemetry-python-contrib/tree/main/instrumentation/opentelemetry-instrumentation-system-metrics) | psutil >= 5 | development
| [opentelemetry-instrumentation-threading](https://github.com/open-telemetry/opentelemetry-python-contrib/tree/main/instrumentation/opentelemetry-instrumentation-threading) | threading | development
| [opentelemetry-instrumentation-tornado](https://github.com/open-telemetry/opentelemetry-python-contrib/tree/main/instrumentation/opentelemetry-instrumentation-tornado) | tornado >= 5.1.1 | development
| [opentelemetry-instrumentation-tortoiseorm](https://github.com/open-telemetry/opentelemetry-python-contrib/tree/main/instrumentation/opentelemetry-instrumentation-tortoiseorm) | tortoise-orm >= 0.17.0 | development
| [opentelemetry-instrumentation-urllib](https://github.com/open-telemetry/opentelemetry-python-contrib/tree/main/instrumentation/opentelemetry-instrumentation-urllib) | urllib | migration
| [opentelemetry-instrumentation-urllib3](https://github.com/open-telemetry/opentelemetry-python-contrib/tree/main/instrumentation/opentelemetry-instrumentation-urllib3) | urllib3 >= 1.0.0, < 3.0.0 | migration
| [opentelemetry-instrumentation-vertexai](https://github.com/open-telemetry/opentelemetry-python-contrib/tree/main/instrumentation-genai/opentelemetry-instrumentation-vertexai) | google-cloud-aiplatform >= 1.64 | development
| [opentelemetry-instrumentation-wsgi](https://github.com/open-telemetry/opentelemetry-python-contrib/tree/main/instrumentation/opentelemetry-instrumentation-wsgi) | wsgi | migration

The semantic conventions status tracks the stabilization of the semantic conventions used in the instrumentation:
- stable, means they are stable and are not expected to change
- development, means they are not stable yet and they may change in the future
- migration, means there may be configuration knobs to switch between different semantic conventions

### Native Elasticsearch instrumentation

Some libraries like the [Python Elasticsearch Client](https://www.elastic.co/guide/en/elasticsearch/client/python-api/current/index.html)
natively supports OpenTelemetry instrumentation.

The [elasticsearch](https://elasticsearch-py.readthedocs.io/en/latest/) package got native OpenTelemetry support since version 8.13.

### LLM instrumentations

We can instrument the following LLM (Large Language Model) libraries with instrumentations implementing the [OpenTelemetry GenAI Semantic Conventions](https://opentelemetry.io/docs/specs/semconv/gen-ai/):

| **SDK**                     | **Instrumentation**                          | **Traces** | **Metrics** | **Logs** | **Notes** |
|-----------------------------|----------------------------------------------|------------|-------------|----------|-----------|
| OpenAI                      | [elastic-opentelemetry-instrumentation-openai](https://github.com/elastic/elastic-otel-python-instrumentations/blob/main/instrumentation/elastic-opentelemetry-instrumentation-openai) | ✅         | ✅          | ✅       | 1.        |
| AWS SDK for Python (Boto3)  | [opentelemetry-instrumentation-botocore](https://github.com/open-telemetry/opentelemetry-python-contrib/tree/main/instrumentation/opentelemetry-instrumentation-botocore)              | ✅         | ✅          | ✅       | 2.        |
| Google Cloud AI Platform    | [opentelemetry-instrumentation-vertexai](https://github.com/open-telemetry/opentelemetry-python-contrib/tree/main/instrumentation-genai/opentelemetry-instrumentation-vertexai)        | ✅         | 🚧          | ✅       | 3.        |

1. Support for sync and async [chat completions create](https://platform.openai.com/docs/guides/text?api-mode=chat) API and [embeddings](https://platform.openai.com/docs/guides/embeddings?lang=python) API.
2. Support for [Bedrock Runtime](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-runtime.html) [InvokeModel](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_runtime_InvokeModel.html), [InvokeModelWithResponseStream](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_runtime_InvokeModelWithResponseStream.html), [Converse](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_runtime_Converse.html) and [ConverseStream](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_runtime_ConverseStream.html) APIs. A subset of models are traced in InvokeModel and InvokeModelWithStreaming API, see [botocore instrumentation](https://github.com/open-telemetry/opentelemetry-python-contrib/tree/main/instrumentation/opentelemetry-instrumentation-botocore#bedrock-runtime).
3. Instrumentation supports tracing and sending events for synchronous API calls, and currently doesn't support async APIs and streaming calls yet.

#### Configuration

These instrumentations implement the following configuration options:

| Option                                                | default | description               |
|-------------------------------------------------------|---------|:--------------------------|
| `OTEL_INSTRUMENTATION_GENAI_CAPTURE_MESSAGE_CONTENT`  | `false`| If set to `true`, enables the capturing of request and response content in the log events outputted by the agent.
