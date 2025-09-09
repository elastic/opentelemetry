---
navigation_title: Performance overhead
description: This documentation outlines the performance implications of using the Elastic Distribution of OpenTelemetry SDK in PHP applications and provides strategies to minimize overhead.
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

# Performance overhead of the EDOT SDK for PHP

This documentation outlines the performance implications of using the Elastic Distribution of OpenTelemetry SDK in PHP applications, and provides strategies to minimize overhead.

While designed to have minimal performance overhead, the EDOT PHP agent, like any instrumentation agent, executes within the application process and thus has a small influence on the application performance. 

This performance overhead depends on the application's technical architecture, its configuration and environment, and the load. These factors are not easy to reproduce on their own, and all applications are different, so it is not possible to provide a simple answer.

The following benchmarks compare the performance overhead of various PHP observability agents, including EDOT PHP, Elastic APM and the official OpenTelemetry PHP agent. All tests were executed in a local Docker-based environment (PHP-FPM 8.2 + NGINX). In configurations that include a Collector, it was also running locally, consuming shared CPU resources.

## Benchmark

The benchmark uses the following components:

- Application: Laravel/Aimeos running under PHP-FPM 8.2
- Environment: Local Docker with NGINX
- Telemetry backends:
  - Elastic Cloud APM endpoint (for ElasticAPM and EDOT)
  - EDOT Collector (locally for EDOT PHP and for vanilla OTEL PHP agents)

## Results

| Variant                                                   | Avg. Time per Request [ms] | Overhead [ms] |
| --------------------------------------------------------- | -------------------------- | ------------- |
| **NO AGENT**                                              | 17.36                      | 0.00          |
| **Elastic APM PHP**                                       | 20.63                      | 3.27          |
| **EDOT PHP**                                              | 23.08                      | 5.71          |
| **EDOT PHP + Collector**                                  | 24.37                      | 7.01          |
| **Vanilla OTEL PHP + Protobuf (C extension) + Collector** | 25.76                      | 8.40          |
| **Vanilla OTEL PHP pure PHP protobuf export + Collector** | 49.02                      | 31.66         |
| **Vanilla OTEL PHP pure PHP protobuf export**             | 2158.58                    | 2141.22       |

## Key findings

EDOT PHP delivers the best balance of performance and observability, with low overhead and full compatibility with Elastic and OpenTelemetry ecosystems. The Elastic APM agent provides slightly lower latency but is limited to the Elastic stack.

OTEL PHP with Protobuf via C extension improves significantly over pure PHP, but still trails behind EDOT PHP. The pure PHP implementation of Protobuf export in OTEL PHP leads to extreme performance degradation, rendering it impractical for real-world use.

 Running a local Collector increases CPU load, especially when colocated with the application container.

## Recommendations

For modern, production-ready PHP observability, EDOT PHP is the top recommendation. It offers strong OpenTelemetry support and excellent performance, significantly outperforming the official OpenTelemetry PHP implementation while remaining flexible and standards-compliant.