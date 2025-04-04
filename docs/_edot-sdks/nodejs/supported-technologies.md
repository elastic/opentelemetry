---
title: Supported Technologies
layout: default
nav_order: 3
parent: EDOT Node.js
---

# Technologies Supported by the EDOT Node.js SDK

## Elastic Stack versions

The Elastic Distribution of OpenTelemetry Node.js (EDOT Node.js) sends data via the OpenTelemetry protocol (OTLP). While OTLP ingest works with later 8.x versions of the Elastic Stack, it is strongly recommended that you use either [EDOT Collector](../../edot-collector/) version 9.x or [Elastic Cloud Serverless](https://www.elastic.co/guide/en/serverless/current/intro.html) for OTLP ingest. See [EDOT SDKs compatibility](../../compatibility/sdks) for support details.

## Node.js versions

EDOT Node.js supports **Node.js 18.19.0, 20.6.0, or later.**
This follows from the [OpenTelemetry JS supported runtimes](https://github.com/open-telemetry/opentelemetry-js#supported-runtimes).

<!--
Dev Notes on supported Node.js versions:
- `^18.19.0 || >=20.6.0` is required for `module.register()` support for ESM instrumentation.
-->

## TypeScript versions

To use this package, `@elastic/opentelemetry-node`, in TypeScript code requires:

- **TypeScript 5.0.4 or later**, and
- using `"module": "node16"` (or "nodenext") in "tsconfig.json" to get support for handling the "exports" entry in package.json. This is so the `@elastic/opentelemetry-node/sdk` entry-point can be used. (See https://www.typescriptlang.org/docs/handbook/release-notes/typescript-4-7.html#ecmascript-module-support-in-nodejs)


## Instrumentations

The following instrumentations are included in EDOT Node.js. All are enabled by default, except those noted "disabled by default".
🔹 marks instrumentations that differ between EDOT Node.js and upstream OTel JS, or that only exist in EDOT Node.js.

| Name | Packages instrumented | Notes |
|---|---|---|
| `@elastic/opentelemetry-instrumentation-openai` 🔹 | `openai` version range `>=4.19.0 <5` | [README](https://github.com/elastic/elastic-otel-node/tree/main/packages/instrumentation-openai#readme) |
| `@opentelemetry/instrumentation-amqplib` | `amqplib` version range `>=0.5.5 <1` | [README](https://github.com/open-telemetry/opentelemetry-js-contrib/tree/main/plugins/node/instrumentation-amqplib#readme) |
| `@opentelemetry/instrumentation-aws-sdk` | `aws-sdk` v2 and `@aws-sdk/client-*` v3 | [README](https://github.com/open-telemetry/opentelemetry-js-contrib/tree/main/plugins/node/opentelemetry-instrumentation-aws-sdk#readme) |
| `@opentelemetry/instrumentation-bunyan` | `bunyan` version range `^1.0.0` | [README](https://github.com/open-telemetry/opentelemetry-js-contrib/tree/main/plugins/node/opentelemetry-instrumentation-bunyan#readme) |
| `@opentelemetry/instrumentation-cassandra-driver` | `cassandra-driver` version range `>=4.4.0 <5` | [README](https://github.com/open-telemetry/opentelemetry-js-contrib/tree/main/plugins/node/opentelemetry-instrumentation-cassandra#readme) |
| `@opentelemetry/instrumentation-express` | `express` version range `^4.0.0` | [README](https://github.com/open-telemetry/opentelemetry-js-contrib/tree/main/plugins/node/opentelemetry-instrumentation-express#readme) |
| `@opentelemetry/instrumentation-fastify` | `fastify` version range `>=3 <5` | [README](https://github.com/open-telemetry/opentelemetry-js-contrib/tree/main/plugins/node/opentelemetry-instrumentation-fastify#readme), [disabled by default](#disabled-instrumentations) |
| `@opentelemetry/instrumentation-fs` | `fs` module for suppported Node.js versions | [README](https://github.com/open-telemetry/opentelemetry-js-contrib/tree/main/plugins/node/instrumentation-fs#readme), [disabled by default](#disabled-instrumentations) |
| `@opentelemetry/instrumentation-generic-pool` | `generic-pool` version range `2 - 2.3, ^2.4, >=3` | [README](https://github.com/open-telemetry/opentelemetry-js-contrib/tree/main/plugins/node/opentelemetry-instrumentation-generic-pool#readme) |
| `@opentelemetry/instrumentation-graphql` | `graphql` version range `>=14.0.0 <17` | [README](https://github.com/open-telemetry/opentelemetry-js-contrib/tree/main/plugins/node/opentelemetry-instrumentation-graphql#readme) |
| `@opentelemetry/instrumentation-grpc` | `@grpc/grpc-js` version range `^1.0.0` | [README](https://github.com/open-telemetry/opentelemetry-js/tree/main/experimental/packages/opentelemetry-instrumentation-grpc#readme) |
| `@opentelemetry/instrumentation-hapi` | `@hapi/hapi >=17.0.0 <21` | [README](https://github.com/open-telemetry/opentelemetry-js-contrib/tree/main/plugins/node/opentelemetry-instrumentation-hapi#readme) |
| `@opentelemetry/instrumentation-http` | `http` module for suppported Node.js versions | [README](https://github.com/open-telemetry/opentelemetry-js/tree/main/experimental/packages/opentelemetry-instrumentation-http#readme) |
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
| `@opentelemetry/instrumentation-net` | `net` module for suppported Node.js versions | [README](https://github.com/open-telemetry/opentelemetry-js-contrib/tree/main/plugins/node/opentelemetry-instrumentation-net#readme) |
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

We can instrument the following LLM (Large Language Model) libraries with instrumentations implementing the [OpenTelemetry GenAI Semantic Conventions](https://opentelemetry.io/docs/specs/semconv/gen-ai/):

| SDK    | Instrumentation | Traces | Metrics | Logs | Notes |
|--------|-----------------|--------|---------|------|-------|
| OpenAI | [@elastic/opentelemetry-instrumentation-openai](https://github.com/elastic/elastic-otel-node/tree/main/packages/instrumentation-openai#readme) | ✅         | ✅          | ✅       | (1)       |

1. Support for [chat](https://platform.openai.com/docs/api-reference/chat) and [embeddings](https://platform.openai.com/docs/api-reference/embeddings) API endpoints.


### Disabled instrumentations

The following instrumentations are included in EDOT Node.js, but *disabled by default*:

- `@opentelemetry/instrumentation-fs` (Disabled upstream in [open-telemetry/opentelemetry-js-contrib#2467](https://github.com/open-telemetry/opentelemetry-js-contrib/pull/2467).)
- `@opentelemetry/instrumentation-fastify` (Deprecated upstream and slated for removal. See [open-telemetry/opentelemetry-js-contrib#2652](https://github.com/open-telemetry/opentelemetry-js-contrib/pull/2652))

To enable these instrumentations, use the [`OTEL_NODE_ENABLED_INSTRUMENTATIONS` environment variable](./configuration#otel_node_disabledenabled_instrumentations-details). Make sure you list all the instrumentations you need for your service since only the ones in that list will be enabled. For example:

```bash
export OTEL_EXPORTER_OTLP_ENDPOINT="https://my-deployment-abc123.ingest.us-west-2.aws.elastic.cloud"
export OTEL_EXPORTER_OTLP_HEADERS="Authorization=ApiKey Zm9vO...mJhcg=="
export OTEL_SERVICE_NAME=my-app
export OTEL_NODE_ENABLED_INSTRUMENTATIONS="fs,http,fastify" # only the ones in the list would be enabled
node --import @elastic/opentelemetry-node my-service.js
```

EDOT Node.js uses the upstream [`@opentelemetry/auto-instrumentations-node` package's set of instrumentations](https://github.com/open-telemetry/opentelemetry-js-contrib/blob/main/metapackages/auto-instrumentations-node/README.md#supported-instrumentations) as a guide for instrumentations to include, exclude, or disable by default. This is to maximize compatibility between usage of EDOT Node.js and the vanilla OpenTelemetry JS SDK.


## Native Instrumentations

"Native" instrumentation refers to OpenTelemetry instrumentation that is built into a library. When a library includes native OTel instrumentation, it will provide telemetry data to providers registered by a running OTel SDK. Native instrumentations of note are listed in the table below. To benefit from these instrumentations you only need to (a) use the library and (b) start the EDOT Node.js SDK:

```bash
node --import @elastic/opentelemetry-node my-app.js
```

| Packages instrumented | Reference |
|---|---|
| `@elastic/elasticsearch` version range `>=8.15.0` | [Elasticsearch JavaScript Client docs](https://www.elastic.co/guide/en/elasticsearch/client/javascript-api/current/observability.html) |


## ECMAScript Modules (ESM)

This Distro includes **limited and experimental** support for instrumenting [ECMAScript module (ESM) imports](https://nodejs.org/api/esm.html#modules-ecmascript-modules), i.e. modules that are loaded via `import ...` statements and `import('...')` (dynamic import). To enable ESM instrumentation, use `node --import @elastic/opentelemetry-node ...` to start the SDK. (Using `node --require @elastic/opentelemetry-node ...` will not enable ESM instrumentation. It is intended to signal that only CommonJS module usage should be instrumented.)

<!--
TODO: add this to the above paragraph once we have an esm.md doc:
See the [ECMAScript module support](./esm.md) document for details.
-->

Limitations:

* ESM instrumentation is only support for Node.js versions `^18.19.0 || >=20.6.0`. These are the versions that include `module.register()` support. Using the older `node --experimental-loader=...` option is not supported.
* Currently only a subset of instrumentations support ESM: `express`, `ioredis`, `koa`, `pg`, `pino`. See [this OpenTelemetry JS tracking issue](https://github.com/open-telemetry/opentelemetry-js-contrib/issues/1942) for progress.
