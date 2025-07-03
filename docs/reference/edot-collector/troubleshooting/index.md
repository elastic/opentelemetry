---
navigation_title: Troubleshooting
description: Troubleshooting common issues with the EDOT Collector.
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

# Troubleshoot the EDOT Collector

Perform these checks when troubleshooting Collector issues:

* Check Logs: Review the Collector’s logs for error messages.
* Validate Configuration: Use the `--dry-run` option to test configurations.
* Enable Debug Logging: Run the Collector with `--log-level=debug` for detailed logs.
* Check Service Status: Ensure the Collector is running with `systemctl status <collector-service>` (Linux) or `tasklist` (Windows).
* Test Connectivity: Use `telnet <endpoint> <port>` or `curl` to verify backend availability.
* Check Open Ports: Run netstat `-tulnp or lsof -i` to confirm the Collector is listening.
* Monitor Resource Usage: Use top/htop (Linux) or Task Manager (Windows) to check CPU & memory.
* Validate Exporters: Ensure exporters are properly configured and reachable.
* Verify Pipelines: Use `otelctl` diagnose (if available) to check pipeline health.
* Check Permissions: Ensure the Collector has the right file and network permissions.
* Review Recent Changes: Roll back recent config updates if the issue started after changes.

For in-depth details on troubleshooting refer to the [OpenTelemetry Collector troubleshooting documentation](https://opentelemetry.io/docs/collector/troubleshooting/).
