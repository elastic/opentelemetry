---
title: Performance overhead
layout: default
nav_order: 8
parent: EDOT PHP
---

## Performance Comparison of PHP Instrumentation Agents

The following benchmarks compare the performance overhead of various PHP observability agents, including **EDOT PHP**, **Elastic APM**, and the official **OpenTelemetry PHP** agent. All tests were executed in a local Docker-based environment (PHP-FPM 8.2 + NGINX). In configurations that include a collector, it was also running locally, consuming shared CPU resources.

### Benchmark Setup

- **Application**: Laravel/Aimeos running under PHP-FPM 8.2
- **Environment**: Local Docker with NGINX
- **Telemetry Backends**:
  - Elastic Cloud APM endpoint (for ElasticAPM and EDOT)
  - EDOT Collector (locally for EDOT PHP and for vanilla OTEL PHP agents)

### Results Summary

| Variant                                                   | Avg. Time per Request [ms] | Overhead [ms] |
| --------------------------------------------------------- | -------------------------- | ------------- |
| **NO AGENT**                                              | 17.36                      | 0.00          |
| **Elastic APM PHP**                                       | 20.63                      | 3.27          |
| **EDOT PHP**                                              | 23.08                      | 5.71          |
| **EDOT PHP + Collector**                                  | 24.37                      | 7.01          |
| **Vanilla OTEL PHP + Protobuf (C extension) + Collector** | 25.76                      | 8.40          |
| **Vanilla OTEL PHP pure PHP protobuf export + Collector** | 49.02                      | 31.66         |
| **Vanilla OTEL PHP pure PHP protobuf export**             | 2158.58                    | 2141.22       |

### Key Findings

- **EDOT PHP delivers the best balance** of performance and observability, with low overhead and full compatibility with Elastic and OpenTelemetry ecosystems.
- The **Elastic APM agent** provides slightly lower latency but is limited to the Elastic stack.
- **Vanilla OTEL PHP with Protobuf via C extension** improves significantly over pure PHP, but still trails behind EDOT PHP.
- The **pure PHP implementation of Protobuf export in Vanilla OTEL PHP** leads to extreme performance degradation, rendering it impractical for real-world use.
- Running a local collector increases CPU load, especially when colocated with the application container.

### Recommendation

For modern, production-ready PHP observability, **EDOT PHP is the top recommendation**. It offers strong OpenTelemetry support and excellent performance, significantly outperforming the official OpenTelemetry PHP implementation while remaining flexible and standards-compliant.