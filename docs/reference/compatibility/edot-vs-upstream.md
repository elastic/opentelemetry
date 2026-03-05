---
navigation_title: EDOT compared to upstream
description: How Elastic Distributions of OpenTelemetry (EDOT) compare to upstream OpenTelemetry components, including Collector, SDKs, Kubernetes Operator, and more.
applies_to:
  stack:
  serverless:
    observability:
products:
  - id: cloud-serverless
  - id: observability
  - id: edot-collector
  - id: edot-sdk
---

# EDOT compared to upstream OpenTelemetry

[Elastic Distributions of OpenTelemetry (EDOT)](/reference/index.md) are a set of [OpenTelemetry distributions](https://opentelemetry.io/docs/concepts/distributions/) curated, tested, and supported by Elastic. Each EDOT component builds on its upstream counterpart, adding production-ready defaults, Elastic-specific capabilities, and official support backed by [Elastic's Support Policy](https://www.elastic.co/support_policy) and SLAs. 

Elastic is also an active contributor to the upstream OpenTelemetry project, working to stabilize components, advance semantic conventions, and move capabilities upstream so that the broader community benefits.

EDOT is always optional. Elastic's OTLP ingestion APIs are vendor-agnostic and preserve OpenTelemetry semantic conventions, so any upstream or third-party OpenTelemetry component that speaks OTLP can send data to the {{stack}}. Upstream components are technically [Compatible] but receive community support only. EDOT is for teams that want a supported, production-grade experience that can be a drop-in replacement for upstream OpenTelemetry components.

The following table summarizes the key differences:

| Aspect | EDOT | Upstream |
|--------|------|----------|
| Configuration | Pre-configured defaults for {{product.observability}}. | Requires manual assembly and configuration. |
| Support | Official Elastic support with SLAs. | Community support only. |
| Integration | Seamless integration with {{stack}} components. | Requires additional configuration for Elastic. |
| Components | Curated, production-tested components optimized for Elastic, including preselected instrumentations for zero-code setup. | Broad ecosystem. Component maturity levels vary. Instrumentations must be selected and configured manually. |
| Deployment | Same deployment methods as upstream, with ready-to-use default configurations. | Same deployment methods; configuration is left to the user. |
| Central management | Central configuration of SDKs and Collectors through [OpAMP](/reference/central-configuration.md). | No centralized configuration support. |
| Compatibility | Fully tested with {{stack}} components. | Compatible but not tested for guaranteed support. |
| Updates | EDOT Collector releases align with {{stack}}. EDOT SDKs follow the upstream OpenTelemetry release cycle. | Follows the upstream OpenTelemetry release cycle. |

The following sections describe how this general comparison applies to each EDOT component.

## EDOT Collector

The upstream OpenTelemetry project does not ship a single, recommended Collector distribution for production use. Instead, it offers a core Collector and a contrib Collector whose components have [mixed stability levels](https://opentelemetry.io/docs/collector/). Assembling a production-ready Collector from these building blocks requires careful component selection, configuration, and testing.

EDOT Collector is a curated distribution that eliminates this assembly step. It includes specific components and configurations optimized for {{product.observability}}, and it ships with Elastic-specific components that are not available in contrib, such as the `elasticsearchexporter` for native ingestion into {{es}} and the `elasticapmintakereceiver` for backward-compatible {{product.apm}} intake. These components are developed by Elastic with the intent of contributing them upstream over time.

EDOT Collector ships with [default configurations](elastic-agent://reference/edot-collector/config/default-config-standalone.md) for common deployment scenarios, including [standalone](elastic-agent://reference/edot-collector/config/default-config-standalone.md) and [Kubernetes](elastic-agent://reference/edot-collector/config/default-config-k8s.md). In self-managed {{stack}} deployments, the EDOT Collector running in [gateway mode](elastic-agent://reference/edot-collector/modes.md) replaces {{product.apm-server}} for OTel-native data ingestion, handling metrics aggregation and format conversion before writing to {{es}}.

Users who need a Collector build that differs from the standard EDOT Collector can follow the [custom Collector guide](elastic-agent://reference/edot-collector/custom-collector.md), which describes the required components and preprocessing pipelines for Elastic compatibility. For the full list of components included in EDOT Collector, refer to the [EDOT Collector components](elastic-agent://reference/edot-collector/components.md) page.

## EDOT SDKs

OpenTelemetry language SDKs provide the instrumentation libraries that applications use to generate traces, metrics, and logs. The upstream project publishes reference SDKs for each supported language, and vendors can wrap these into [distributions](https://opentelemetry.io/docs/concepts/distributions/) that add defaults, extensions, or vendor-specific improvements.

EDOT SDKs are such distributions. They maintain full compatibility with the OpenTelemetry specification and come with preselected instrumentations that enable [zero-code instrumentation](https://opentelemetry.io/docs/concepts/instrumentation/zero-code/) by default. Elastic contributes bug fixes and improvements to upstream first, and only ships fixes in EDOT ahead of upstream when there are strong reasons to do so. 

The following EDOT SDKs are available:

- [EDOT .NET](elastic-otel-dotnet://reference/edot-dotnet/index.md)
- [EDOT Java](elastic-otel-java://reference/edot-java/index.md)
- [EDOT Node.js](elastic-otel-node://reference/edot-node/index.md)
- [EDOT PHP](elastic-otel-php://reference/edot-php/index.md)
- [EDOT Python](elastic-otel-python://reference/edot-python/index.md)
- [EDOT Android](apm-agent-android://reference/edot-android/index.md)
- [EDOT iOS](apm-agent-ios://reference/edot-ios/index.md)

Due to current upstream limitations, some capabilities are temporarily available only in EDOT SDKs. Elastic is actively working to contribute these upstream so that they become part of the standard OpenTelemetry SDKs. Refer to the [EDOT SDKs overview](/reference/edot-sdks/index.md) for the full feature matrix across languages.

| Capability | Status |
|------------|--------|
| Inferred spans | Available in EDOT only. Generates spans from profiling data without manual instrumentation, closing visibility gaps that auto-instrumentation does not cover. |
| Central configuration | Available in EDOT only. Manages SDK settings from {{kib}} through the EDOT Collector using [OpAMP](/reference/central-configuration.md). Most SDKs apply configuration changes dynamically, without restarting or redeploying applications. |
| Profiling integration | Available in EDOT only. Correlates traces with continuous profiling data for deeper performance analysis. |
| Crash reporting | Available in EDOT only. Captures native crash data on mobile platforms for post-mortem analysis. |

Upstream OTel SDKs are technically [Compatible] with Elastic and can send data through the same ingestion paths, but Elastic does not provide official support or troubleshooting assistance for them. Refer to the [SDK compatibility table](sdks.md) for version-level details.

:::{important}
EDOT SDKs are designed to export telemetry through the [EDOT Collector](elastic-agent://reference/edot-collector/index.md) or the [{{motlp}}](/reference/motlp.md). Using EDOT SDKs directly with {{product.apm-server}}'s OpenTelemetry intake is not supported — attribute mapping, enrichment, and processing pipelines are not guaranteed on that path.
:::

## Kubernetes Operator

EDOT does not ship its own Kubernetes operator. Instead, EDOT deployments on Kubernetes rely on the upstream [OpenTelemetry Operator](https://opentelemetry.io/docs/platforms/kubernetes/operator/), which manages Collector deployments and auto-instrumentation of workloads through Kubernetes custom resource definitions (CRDs).

In an EDOT-based Kubernetes setup, the operator's `OpenTelemetryCollector` CRD deploys EDOT Collector images as DaemonSets, Deployments, or StatefulSets, and the `Instrumentation` CRD is configured to inject EDOT SDK images (for example, `docker.elastic.co/observability/elastic-otel-javaagent`) instead of the default upstream images. The operator handles the mechanics of admission webhooks and init container injection, while EDOT provides the container images and configurations that the operator deploys.

This creates a dual support model. The operator itself is an upstream community project and receives community support. The EDOT Collector and SDK images that the operator deploys are covered by Elastic support under the same terms as their standalone counterparts. When filing issues, it is important to distinguish between operator behavior (community) and EDOT component behavior (Elastic).

On platforms that provide their own OpenTelemetry distributions, such as [Red Hat OpenShift](https://docs.redhat.com/en/documentation/openshift_container_platform/4.20/html/red_hat_build_of_opentelemetry/index) or [AWS Lambda (ADOT)](https://aws-otel.github.io/docs/getting-started/lambda), those platform-native distributions can be used [at the edge](/reference/architecture/index.md#understanding-edge-deployment) instead. Elastic does not provide support for third-party distributions, but they remain [Compatible] as long as they export data over OTLP. Refer to the [Kubernetes architecture page](/reference/architecture/k8s.md) and the [Kubernetes use case guide](docs-content://solutions/observability/get-started/opentelemetry/use-cases/kubernetes/index.md) for deployment details.

## EDOT Cloud Forwarders

The [EDOT Cloud Forwarders](/reference/edot-cloud-forwarder/index.md) are Elastic-specific components with no upstream equivalent. They package the EDOT Collector as a cloud function — AWS Lambda, Azure Function, or GCP Cloud Run — to collect telemetry from cloud provider services such as S3, CloudWatch, Blob Storage, Event Hub, GCS, and GCP Operations, and forward it to the [{{motlp}}](/reference/motlp.md).

Because there is no upstream counterpart, the EDOT-versus-upstream comparison does not apply to Cloud Forwarders. Refer to the [EDOT Cloud Forwarder documentation](/reference/edot-cloud-forwarder/index.md) for setup guides and supported cloud services.

## OTel Demo

The upstream [OpenTelemetry Demo](https://opentelemetry.io/docs/demo/) is a multi-service reference application instrumented in over a dozen languages. It demonstrates distributed tracing, metrics collection, and log correlation across a realistic microservices architecture, backed by Jaeger and Prometheus.

Elastic maintains a [fork of the demo](https://github.com/elastic/opentelemetry-demo) that replaces these default backends with an {{stack}} deployment. The fork ships EDOT Collector configurations for both Kubernetes and host scenarios, allowing teams to see how EDOT components work together in a near-production environment before rolling them out.

The EDOT demo is a learning and showcase tool, not a production artifact. Elastic does not provide support for the demo application itself, but the EDOT components running within it follow the same support terms as their standalone releases.

[Incompatible]: nomenclature.md
[Compatible]: nomenclature.md
[Not supported]: nomenclature.md
[Supported]: nomenclature.md
