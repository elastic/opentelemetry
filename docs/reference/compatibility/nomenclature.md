---
navigation_title: Nomenclature
description: Explanation of compatibility and support states (Incompatible, Compatible, Supported) for EDOT components.
---

# Compatibility & Support Nomenclature

OpenTelemetry (OTel) is a modular, extensible framework designed to integrate with a wide range of technologies. Its architecture enables interoperability across many components, extensions, and tools—giving users flexibility to shape their observability pipelines.

Elastic Distributions for OpenTelemetry (EDOT) are built from upstream OTel components and are **technically compatible** with a broad set of community components. Users can also send data to Elastic using other upstream OTel components or distributions like the contrib Collector and OTel SDKs, which are *technically compatible* with Elastic’s ingestion APIs.

**"Supported through Elastic”** refers to components and configurations that Elastic has explicitly tested, validated, and committed to maintaining under our [Support Policies](https://www.elastic.co/support). This includes regular updates, issue triaging, and guidance from Elastic’s support and engineering teams. Components outside of this supported set may still work, but Elastic does not provide guaranteed support or troubleshooting assistance for them.

In the following sections we differentiate the following compatibility and support states:

| State            | Description                                                                                                                                                                                                                                                                                                               | Symbol |
| :--------------- | :-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :-----: |
| **Incompatible** | Component, use case or ingestion path is technically not compatible, thus, functionality is likely to be significantly impacted.                                                                                                                                                                                          |   ❌    |
| **Compatible**   | Component, use case or ingestion path is **technically compatible**. The functionality is not expected to be impaired, though, minor deviations may occur. Component, use case or ingestion path is *not officially supported by Elastic*, hence, Elastic does not provide guaranteed support or troubleshooting assistance |   🟡   |
| **Supported**    | Component, use case or ingestion path is **technically compatible** and Elastic provides **official support**. The functionality is explicitly tested. Limitations will be documented.                                                                                                                                    |   ✅    |

## EDOT Collector Components Categorization
The EDOT Collector includes two types of components with different compatibility and support scope:

### Core Components

These are used by default in Elastic’s onboarding flows and are essential for common use cases.
They are **fully supported** (✅) under your Service Level Agreement (SLA).

### Extended Components

A curated set of optional components that enhance functionality and are **technically compatible** (🟡).
These are not part of Elastic’s core product journeys and are not covered by SLAs.
You’re free to use them, but Elastic provides limited support.

:::{note}
**Recommendation**

For the best support experience, we recommend relying on *Core Components*, and using *Extended Components* only when required.
:::

:::{warning}
Since the EDOT Collector is built on upstream OpenTelemetry, breaking upstream changes (e.g., to semantic conventions or configuration options) may impact both, *Extended Components* and *Core Components*. Elastic highlights and manages these through docs and support channels.
:::
