---
title: Supported Technologies
layout: default
nav_order: 3
parent: EDOT PHP
---

# The Elastic Distribution of OpenTelemetry PHP supports the following technologies

## PHP Versions
- PHP 8.1 - 8.4

> Unlike the upstream OpenTelemetry PHP agent, EDOT PHP supports extension-level instrumentation starting from PHP 8.1 (not just 8.2).
> This allows you to capture **detailed traces** from libraries such as **cURL**, **PDO**, and **MySQLi**, even in PHP 8.1 environments.

## Supported PHP SAPI's
- php-cli
- php-fpm
- php-cgi/fcgi
- mod_php (prefork)

EDOT PHP supports all popular variations of using PHP in combination with a web server, such as Apache + mod_php, Apache + php_fpm or cgi, NGINX + php_fpm or cgi, and others.

## Supported Operating Systems
- **Linux**
  - Architectures: **x86_64** and **ARM64**
  - **glibc-based systems**: Packages available as **DEB** and **RPM**
  - **musl libc-based systems (Alpine Linux)**: Packages available as **APK**

## Instrumented Frameworks
- Laravel (v6.x/v7.x/v8.x/v9.x/v10.x/v11.x)
- Slim (v4.x)

## Instrumented Libraries
- Curl (v8.1 - v8.4)
- HTTP Async (php-http/httplug v2.x)
- MySQLi (v8.1 - v8.4)
- PDO (v8.1 - v8.4)

## Extends the upstream OpenTelemetry PHP with additional features and improvements
- **Truly zero-config auto-instrumentation**
  Unlike the upstream OpenTelemetry PHP agent, **EDOT PHP works fully automatically** — no need to modify your application code, add Composer packages, or adjust deployment scripts.
  Once the system package is installed, EDOT PHP automatically detects your application and injects the instrumentation code at runtime, with **no manual integration required**.

- **Automatic Root/Transaction Span**
  Automatically creates the root span for each incoming request, providing a consistent entry point for trace data without requiring manual instrumentation.

- **Root/Transaction Span URL Grouping**
  Groups transaction spans by URL patterns to reduce cardinality and improve readability in dashboards and trace views.

- **Inferred Spans (preview version)**
  Automatically detects and generates spans for common operations like database queries or HTTP calls, even when no manual instrumentation is present (currently in preview).

- **Asynchronous data sending**
  Sends telemetry data in the background to avoid impacting application performance, ensuring minimal latency and efficient resource usage.

> EDOT PHP supports background data transmission (non-blocking export), but **only when the exporter is set to `http/protobuf` (OTLP over HTTP)** — which is the default configuration.
> If you change the exporter or the transport protocol (e.g., to gRPC or another format), telemetry data will be sent **synchronously**, potentially impacting request latency.