---
navigation_title: Supported Technologies
description: Supported technologies for the Elastic Distribution of OpenTelemetry Node.js (EDOT Node.js).
applies_to:
  stack:
  serverless:
    observability:
  product:
    edot_node: ga
products:
  - id: cloud-serverless
  - id: observability
  - id: edot-sdk
---

# Technologies supported by the EDOT Node.js SDK

The EDOT Node.js agent is a [distribution](https://opentelemetry.io/docs/concepts/distributions/) of OpenTelemetry Node.js. It inherits all the [supported](../../compatibility/nomenclature.md) technologies of the OpenTelemetry Node.js.

## EDOT Collector and Elastic Stack versions

The {{edot}} Node.js (EDOT Node.js) sends data through the OpenTelemetry protocol (OTLP). While OTLP ingest works with later 8.16+ versions of the EDOT Collector, for full support use either [EDOT Collector](../../edot-collector/index.md) versions 9.x or [{{serverless-full}}](docs-content://deploy-manage/deploy/elastic-cloud/serverless.md) for OTLP ingest.

:::{note}
Ingesting data from EDOT SDKs through EDOT Collector 9.x into Elastic Stack versions 8.18+ is supported.
:::

Refer to [EDOT SDKs compatibility](../../compatibility/sdks.md) for support details.

## Node.js versions

EDOT Node.js supports Node.js 18.19.0, 20.6.0, or later. This follows from the [OpenTelemetry JS supported runtimes](https://github.com/open-telemetry/opentelemetry-js#supported-runtimes).

## TypeScript versions

Usage of `@elastic/opentelemetry-node` in TypeScript code requires:

- TypeScript 5.0.4 or later
- Using `"module": "node16"` or "nodenext" in "tsconfig.json" to get support for handling the "exports" entry in package.json. This is so the `@elastic/opentelemetry-node/sdk` entry-point can be used.

## Instrumentations [instrumentations]

The following instrumentations are included in EDOT Node.js. All are turned on by default, except those noted _Turned off by default_.

The 🔹 symbol marks instrumentations that differ between EDOT Node.js and upstream OTel JS, or that only exist in EDOT Node.js.

| Name | Packages instrumented | Notes |
|---|---|---|
| `@elastic/opentelemetry-instrumentation-openai` 🔹 | `openai` version range `>=4.19.0 <5` | [README](https://github.com/elastic/elastic-otel-node/tree/main/packages/instrumentation-openai#readme) |
| `@opentelemetry/instrumentation-amqplib` | `amqplib` version range `>=0.5.5 <1` | [README](https://github.com/open-telemetry/opentelemetry-js-contrib/tree/main/plugins/node/instrumentation-amqplib#readme) |
| `@opentelemetry/instrumentation-aws-sdk` | `aws-sdk` v2 and `@aws-sdk/client-*` v3 | [README](https://github.com/open-telemetry/opentelemetry-js-contrib/tree/main/plugins/node/opentelemetry-instrumentation-aws-sdk#readme) |
| `@opentelemetry/instrumentation-bunyan` | `bunyan` version range `^1.0.0` | [README](https://github.com/open-telemetry/opentelemetry-js-contrib/tree/main/plugins/node/opentelemetry-instrumentation-bunyan#readme) |
| `@opentelemetry/instrumentation-cassandra-driver` | `cassandra-driver` version range `>=4.4.0 <5` | [README](https://github.com/open-telemetry/opentelemetry-js-contrib/tree/main/plugins/node/opentelemetry-instrumentation-cassandra#readme) |
| `@opentelemetry/instrumentation-express` | `express` version range `^4.0.0` | [README](https://github.com/open-telemetry/opentelemetry-js-contrib/tree/main/plugins/node/opentelemetry-instrumentation-express#readme) |
| `@opentelemetry/instrumentation-fastify` | `fastify` version range `>=3 <5` | [README](https://github.com/open-telemetry/opentelemetry-js-contrib/tree/main/plugins/node/opentelemetry-instrumentation-fastify#readme), [disabled by default](#disabled-instrumentations) |
| `@opentelemetry/instrumentation-fs` | `fs` module for supported Node.js versions | [README](https://github.com/open-telemetry/opentelemetry-js-contrib/tree/main/plugins/node/instrumentation-fs#readme), [disabled by default](#disabled-instrumentations) |
| `@opentelemetry/instrumentation-generic-pool` | `generic-pool` version range `2 - 2.3, ^2.4, >=3` | [README](https://github.com/open-telemetry/opentelemetry-js-contrib/tree/main/plugins/node/opentelemetry-instrumentation-generic-pool#readme) |
| `@opentelemetry/instrumentation-graphql` | `graphql` version range `>=14.0.0 <17` | [README](https://github.com/open-telemetry/opentelemetry-js-contrib/tree/main/plugins/node/opentelemetry-instrumentation-graphql#readme) |
| `@opentelemetry/instrumentation-grpc` | `@grpc/grpc-js` version range `^1.0.0` | [README](https://github.com/open-telemetry/opentelemetry-js/tree/main/experimental/packages/opentelemetry-instrumentation-grpc#readme) |
| `@opentelemetry/instrumentation-hapi` | `@hapi/hapi >=17.0.0 <21` | [README](https://github.com/open-telemetry/opentelemetry-js-contrib/tree/main/plugins/node/opentelemetry-instrumentation-hapi#readme) |
| `@opentelemetry/instrumentation-http` | `http` module for supported Node.js versions | [README](https://github.com/open-telemetry/opentelemetry-js/tree/main/experimental/packages/opentelemetry-instrumentation-http#readme) |
| `@opentelemetry/instrumentation-ioredis` | `ioredis` version range `>=2 <6` | [README](https://github.com/open-telemetry/opentelemetry-js-contrib/tree/main/plugins/node/opentelemetry-instrumentation-ioredis#readme) |
| `@opentelemetry/instrumentation-kafkajs` | `kafkajs` version range `>=0.1.0 <3` | [README](https://github.com/open-telemetry/opentelemetry-js-contrib/tree/main/plugins/node/instrumentation-kafkajs#readme) |
| `@opentelemetry/instrumentation-knex` | `knex` version range `>=0.10.0` | [README](https://github.com/open-telemetry/opentelemetry-js-contrib/tree/main/plugins/node/opentelemetry-instrumentation-knex#readme) |
| `@opentelemetry/instrumentation-koa` | `koa` version range `^2.0.0` | [README](https://github.com/open-telemetry/opentelemetry-js-contrib/tree/main/plugins/node/opentelemetry-instrumentation-koa#readme) |
| `@opentelemetry/instrumentation-lru-memoizer` | `lru-memoizer` version range `>=1.3 <3` | [README](https://github.com/open-telemetry/opentelemetry-js-contrib/tree/main/plugins/node/instrumentation-lru-memoizer#readme) |
| `@opentelemetry/instrumentation-memcached` | `memcached` version range `>=2.2` | [README](https://github.com/open-telemetry/opentelemetry-js-contrib/tree/main/plugins/node/opentelemetry-instrumentation-memcached#readme) |
| `@opentelemetry/instrumentation-mongodb` | `mongodb` version range `>=3.3 <7` | [README](https://github.com/open-telemetry/opentelemetry-js-contrib/tree/main/plugins/node/opentelemetry-instrumentation-mongodb#readme) |
| `@opentelemetry/instrumentation-mongoose` | `mongoose` version range `>=5.9.7 <9` | [README](https://github.com/open-telemetry/opentelemetry-js-contrib/tree/main/plugins/node/instrumentation-mongoose#readme) |
| `@opentelemetry/instrumentation-mysql` | `mysql` version range `>=2.0.0 <3` | [README](https://github.com/open-telemetry/opentelemetry-js-contrib/blob/main/plugins/node/opentelemetry-instrumentation-mysql#readme) |
| `@opentelemetry/instrumentation-mysql2` | `mysql2` version range `>=1.4.2 <4` | [README](https://github.com/open-telemetry/opentelemetry-js-contrib/blob/main/plugins/node/opentelemetry-instrumentation-mysql2#readme) |
| `@opentelemetry/instrumentation-nestjs-core` | `@nestjs/core` version range `>=4.0.0` | [README](https://github.com/open-telemetry/opentelemetry-js-contrib/tree/main/plugins/node/opentelemetry-instrumentation-nestjs-core#readme) |
| `@opentelemetry/instrumentation-net` | `net` module for supported Node.js versions | [README](https://github.com/open-telemetry/opentelemetry-js-contrib/tree/main/plugins/node/opentelemetry-instrumentation-net#readme) |
| `@opentelemetry/instrumentation-pino` | `pino` version range `>=5.14.0 <10` | [README](https://github.com/open-telemetry/opentelemetry-js-contrib/tree/main/plugins/node/opentelemetry-instrumentation-pino#readme) |
| `@opentelemetry/instrumentation-pg` | `pg` version range `>=8 <9` | [README](https://github.com/open-telemetry/opentelemetry-js-contrib/tree/main/plugins/node/opentelemetry-instrumentation-pg#readme) |
| `@opentelemetry/instrumentation-redis-4` | `redis` version range `^4.0.0` | [README](https://github.com/open-telemetry/opentelemetry-js-contrib/tree/main/plugins/node/opentelemetry-instrumentation-redis-4#readme) |
| `@opentelemetry/instrumentation-restify` | `restify` version range `>=4.0.0 <12` | [README](https://github.com/open-telemetry/opentelemetry-js-contrib/tree/main/plugins/node/opentelemetry-instrumentation-restify#readme) |
| `@opentelemetry/instrumentation-router` | `router` version range `1` | [README](https://github.com/open-telemetry/opentelemetry-js-contrib/tree/main/plugins/node/opentelemetry-instrumentation-router#readme) |
| `@opentelemetry/instrumentation-socket.io` | `socket.io` version range `2, >=3 <5` | [README](https://github.com/open-telemetry/opentelemetry-js-contrib/tree/main/plugins/node/instrumentation-socket.io#readme) |
| `@opentelemetry/instrumentation-tedious` | `tedious` version range `>=1.11.0 <=15` | [README](https://github.com/open-telemetry/opentelemetry-js-contrib/tree/main/plugins/node/instrumentation-tedious#readme) |
| `@opentelemetry/instrumentation-undici` | `undici` version range `>=5.12.0` | [README](https://github.com/open-telemetry/opentelemetry-js-contrib/tree/main/plugins/node/instrumentation-undici#readme) |
| `@opentelemetry/instrumentation-winston` | `winston` version range `>1 <4` | [README](https://github.com/open-telemetry/opentelemetry-js-contrib/tree/main/plugins/node/opentelemetry-instrumentation-winston#readme) |

### LLM instrumentations

EDOT Node.js can instrument the following Large Language Model (LLM) libraries with instrumentations implementing the [OpenTelemetry GenAI Semantic Conventions](https://opentelemetry.io/docs/specs/semconv/gen-ai/):

| SDK    | Instrumentation | Traces | Metrics | Logs | Notes |
|--------|-----------------|--------|---------|------|-------|
| OpenAI | [@elastic/opentelemetry-instrumentation-openai](https://github.com/elastic/elastic-otel-node/tree/main/packages/instrumentation-openai#readme) | ✅         | ✅          | ✅       | (1)       |

1. Support for [chat](https://platform.openai.com/docs/api-reference/chat) and [embeddings](https://platform.openai.com/docs/api-reference/embeddings) API endpoints.

### Deactivated instrumentations [disabled-instrumentations]

The following instrumentations are included in EDOT Node.js, but deactivated by default:

- `@opentelemetry/instrumentation-fs` (Deactivated upstream in [open-telemetry/opentelemetry-js-contrib#2467](https://github.com/open-telemetry/opentelemetry-js-contrib/pull/2467).)
- `@opentelemetry/instrumentation-fastify` (Deprecated upstream and slated for removal. Refer to [open-telemetry/opentelemetry-js-contrib#2652](https://github.com/open-telemetry/opentelemetry-js-contrib/pull/2652))

To turn on these instrumentations, use the [`OTEL_NODE_ENABLED_INSTRUMENTATIONS` environment variable](./configuration.md#otel_node_disabledenabled_instrumentations-details). Make sure you list all the instrumentations you need for your service since only the ones in that list will be activated. For example:

```bash
export OTEL_EXPORTER_OTLP_ENDPOINT="https://my-deployment-abc123.ingest.us-west-2.aws.elastic.cloud"
export OTEL_EXPORTER_OTLP_HEADERS="Authorization=ApiKey Zm9vO...mJhcg=="
export OTEL_SERVICE_NAME=my-app
export OTEL_NODE_ENABLED_INSTRUMENTATIONS="fs,http,fastify" # only the ones in the list would be enabled
node --import @elastic/opentelemetry-node my-service.js
```

EDOT Node.js uses the upstream [`@opentelemetry/auto-instrumentations-node` package set of instrumentations](https://github.com/open-telemetry/opentelemetry-js-contrib/blob/main/metapackages/auto-instrumentations-node/README.md#supported-instrumentations) as a guide for instrumentations to include, exclude, or turn off by default. This is to maximize compatibility between usage of EDOT Node.js and the upstream OpenTelemetry JS SDK.

## Native instrumentations

Native instrumentation refers to OpenTelemetry instrumentation that is built into a library. When a library includes native OTel instrumentation, it provides telemetry data to providers registered by a running OTel SDK. Native instrumentations of note are listed in the following table. To benefit from these instrumentations you only need to use the library and start the EDOT Node.js SDK:

```bash
node --import @elastic/opentelemetry-node my-app.js
```

| Packages instrumented | Reference |
|---|---|
| `@elastic/elasticsearch` version range `>=8.15.0` | {{es}} JavaScript Client docs |

## ECMAScript Modules (ESM)

EDOT Node.js includes limited and experimental support for instrumenting [ECMAScript module (ESM) imports](https://nodejs.org/api/esm.html#modules-ecmascript-modules). For example modules that are loaded through `import ...` statements and `import('...')` (dynamic import). 

To activate ESM instrumentation, use `node --import @elastic/opentelemetry-node ...` to start the SDK. Using `node --require @elastic/opentelemetry-node ...` does not turn on ESM instrumentation. It is intended to signal that only CommonJS module usage should be instrumented.

### Limitations

The following limitations apply to ESM instrumentation:

* ESM instrumentation is only supported for Node.js versions `^18.19.0 || >=20.6.0`. These are the versions that include `module.register()` support. Using the older `node --experimental-loader=...` option is not supported.
* Currently, only a subset of instrumentations support ESM: `express`, `ioredis`, `koa`, `pg`, `pino`. Refer to [this OpenTelemetry JS tracking issue](https://github.com/open-telemetry/opentelemetry-js-contrib/issues/1942) for progress.
