---
navigation_title: Supported Technologies
description: Supported technologies for the Elastic Distribution of OpenTelemetry PHP.
applies_to:
  stack:
  serverless:
    observability:
  product:
    edot_php: ga
products:
  - id: cloud-serverless
  - id: observability
  - id: edot-sdk
---

# Technologies supported by EDOT PHP

EDOT PHP is a [distribution](https://opentelemetry.io/docs/concepts/distributions/) of OpenTelemetry PHP. It inherits all the [supported](../../compatibility/nomenclature.md) technologies of the OpenTelemetry PHP.

## EDOT Collector and Elastic Stack versions

EDOT PHP sends data through the OpenTelemetry protocol (OTLP). While OTLP ingest works with later 8.16+ versions of the EDOT Collector, for full support use either [EDOT Collector](../../edot-collector/index.md) versions 9.x or [{{serverless-full}}](docs-content://deploy-manage/deploy/elastic-cloud/serverless.md) for OTLP ingest.

:::{note}
Ingesting data from EDOT SDKs through EDOT Collector 9.x into Elastic Stack versions 8.18+ is supported.
:::

Refer to [EDOT SDKs compatibility](../../compatibility/sdks.md) for support details.

## PHP versions

EDOT PHP supports PHP versions 8.1 to 8.4.

Unlike the upstream OpenTelemetry PHP agent, EDOT PHP supports extension-level instrumentation starting from PHP 8.1. This allows you to capture detailed traces from libraries such as cURL, PDO, and MySQLi even in PHP 8.1 environments.

## Supported PHP SAPIs

The following SAPIs are supported:

- php-cli
- php-fpm
- php-cgi/fcgi
- mod_php (prefork)

EDOT PHP supports all popular variations of using PHP in combination with a web server, such as Apache with mod_php, Apache with php_fpm or cgi, NGINX with php_fpm or cgi, and others.

## Supported operating systems

The following operating systems are supported:
- Linux
   - Architectures: x86_64 and ARM64
   - glibc-based systems: Packages available as DEB and RPM
   - musl libc-based systems (Alpine Linux): Packages available as APK

## Instrumented frameworks

The following frameworks are supported:

- Laravel versions 6.x, 7.x, 8.x, 9.x, 10.x, and v11.x
- Slim version 4.x

## Instrumented libraries

The following libraries are supported:

- Curl versions 8.1 to 8.4
- HTTP Async (php-http/httplug) version 2.x
- MySQLi versions 8.1 to 8.4
- PDO versions 8.1 to 8.4

## Additional features and improvements
### Truly zero-config auto-instrumentation

Unlike the upstream OpenTelemetry PHP agent, EDOT PHP works fully automatically. There is no need to modify your application code, add Composer packages, or adjust deployment scripts. Once the system package is installed, EDOT PHP automatically detects your application and injects the instrumentation code at runtime, without requiring manual integration.

### Automatic Root/Transaction Span

EDOT PHP automatically creates the root span for each incoming request, providing a consistent entry point for trace data without requiring manual instrumentation.

### Root/Transaction Span URL Grouping

Transaction spans are grouped by URL patterns to reduce cardinality and improve readability in dashboards and trace views.

### Inferred Spans

```{applies_to}
product: preview
```

EDOT PHP automatically detects and generates spans for common operations like database queries or HTTP calls, even when no manual instrumentation is present.

### Asynchronous data sending

Telemetry data is sent in the background to avoid impacting application performance. This ensures minimal latency and efficient resource usage.

:::{note}
EDOT PHP supports background data transmission (non-blocking export), but only when the exporter is set to `http/protobuf` (OTLP over HTTP), which is the default configuration.
If you change the exporter or the transport protocol, for example to gRPC or another format, telemetry will be sent synchronously, potentially impacting request latency.
:::