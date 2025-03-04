## 🇪 EDOT Collector

The **Elastic Distribution of OpenTelemetry (EDOT) Collector** is an open-source distribution of the [OpenTelemetry Collector](https://github.com/open-telemetry/opentelemetry-collector).

Built on OpenTelemetry’s modular [architecture](https://opentelemetry.io/docs/collector/), the EDOT Collector offers a curated and fully supported selection of Receivers, Processors, Exporters, and Extensions. Designed for production-grade reliability. 

### 🚀 Get started
The quickest way to get started with EDOT is to follow our [quick start guide](https://github.com/elastic/opentelemetry/blob/miguel-docs/quickstart-guide.md).

### 🎛️ Collector configuration
The EDOT collector can be configured using the standard OTel collector configuration file or values.yml if you have deployed using Helm.

For full details on each option visit [this page](docs/EDOT-collector/edot-collector-config.md)

### 🧩 EDOT Collector components

The Elastic Distribution of OpenTelemetry (EDOT) Collector is built on OpenTelemetry’s modular architecture, integrating a carefully curated selection of Receivers, Processors, Exporters, and Extensions to ensure stability, scalability, and seamless observability. 

Visit [this page](https://github.com/elastic/elastic-agent/tree/main/internal/pkg/otel#components) for the full list of components

#### Request a component to be added
To request a component to be added to EDOT Collector, please submit a [github issue](https://github.com/elastic/opentelemetry/issues/new/choose).

### Collector Limitations
The EDOT collector has some limitations which are mostly inherited from the upstream components, see the [full list](docs/EDOT-collector/edot-collector-limitations.md) here before troubleshooting.

### 🔧 Troubleshooting Quick Reference

* **Check Logs**: Review the Collector’s logs for error messages.
* **Validate Configuration:** Use the `--dry-run` option to test configurations.
* Enable Debug Logging: Run the Collector with `--log-level=debug` for detailed logs.
* **Check Service Status:** Ensure the Collector is running with `systemctl status <collector-service>` (Linux) or `tasklist` (Windows).
* **Test Connectivity:** Use `telnet <endpoint> <port>` or `curl` to verify backend availability.
* **Check Open Ports:** Run netstat `-tulnp or lsof -i` to confirm the Collector is listening.
* **Monitor Resource Usage:** Use top/htop (Linux) or Task Manager (Windows) to check CPU & memory.
* **Validate Exporters:** Ensure exporters are properly configured and reachable.
* **Verify Pipelines:** Use `otelctl` diagnose (if available) to check pipeline health.
* **Check Permissions:** Ensure the Collector has the right file and network permissions.
* **Review Recent Changes:** Roll back recent config updates if the issue started after changes.

For in-depth details on troubleshooting refer to the [OpenTelemetry Collector troubleshooting documentation](https://opentelemetry.io/docs/collector/troubleshooting/)