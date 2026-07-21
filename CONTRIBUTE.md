# Contributing to the Elastic OpenTelemetry docs

This repository contains the Elastic OpenTelemetry documentation. We welcome pull requests.

## Format and syntax

The docs are written in the CommonMark flavor of Markdown. The Elastic V3 docs system also has a number of directives that allow you to create tabbed content, admonitions, stepped instructions, and much more.

Refer to [Syntax guide](https://docs-v3-preview.elastic.dev/elastic/docs-builder/tree/main/syntax/) for a detailed overview.

## Structure

All docs live in the `./docs` directory. The `./olddocs` repository contains redirections for the old docs and should not be touched.

The docs are organized in the following directories:

```
docs
└── reference              # Contains reference docs
    ├── _snippets          # Reusable snippets
    ├── architecture       # Architecture section
    ├── compatibility      # Compatibility and support
    ├── edot-collector     # Elastic Agent (OTel mode)
    ├── edot-sdks          # Elastic OTel SDKs
    ├── images             # Images
    ├── quickstart         # Quickstarts
    └── use-cases          # Use cases
```

This structure might evolve as we refine the Elastic OpenTelemetry documentation according to the new V3 information architecture.

## Style guide

Elastic docs strive to keep a consistent voice and tone, with a distinct style throughout all repositories.

Tech writers will help you refine your contributions. Refer to [Technical writing style guide](https://docs.elastic.dev/tech-writing-guidelines/home) to learn more.

Always use US English spellings.

## Terminology

Use the following terms consistently and respect capitalization.

| Term | Description | Alias | Example |
|---|---|---|---|
| **Elastic OpenTelemetry** | Use to describe Elastic's OpenTelemetry brand collectively | Elastic OTel | Use Elastic OpenTelemetry to instrument your applications and infrastructure and send telemetry to Elastic Observability. |
| **EDOT SDKs** | Use to describe the collection of Elastic language SDKs | EDOT {language} | With the EDOT SDKs you have access to all the features of the OpenTelemetry SDK that it customizes, plus... |
| **EDOT {language}** | Use to refer to a specific language SDK | EDOT {language} | The EDOT Java SDK is a Java package that provides an easy way to instrument your application with OpenTelemetry and configuration defaults for best usage. |
| **Elastic Agent** | Use to describe Elastic Agent running in OpenTelemetry mode (available from 9.5; formerly called the EDOT Collector). | — | Deploy Elastic Agent in OTel mode to collect and forward telemetry data to Elastic Observability. |
| **Elastic Cloud Forwarder** | Use to describe the cloud-native forwarder for AWS, GCP, and Azure. | — | Use the Elastic Cloud Forwarder to send telemetry from your cloud environment to Elastic Observability. |
| **Upstream** | Use to describe the upstream OpenTelemetry solutions. Do not use "vanilla" or other terms. | — | The upstream OpenTelemetry Collector is maintained by the OpenTelemetry community. |
| **Collector** | Use to refer to any Collector instance, either upstream or Elastic. Always capitalize Collector when referring to the technical solution. Use lowercase when referring to multiple collectors. | — | Deploy a Collector to receive and process telemetry data. Multiple collectors can be used for scaling. |

Keep these rules in mind when writing about Elastic OpenTelemetry:

* Always use the full product name the first time you refer to the product on each page.
* EDOT SDK names (EDOT Java, EDOT Python, EDOT .NET, etc.) remain unchanged. Continue using the EDOT brand for SDK references.
* For the Collector and generic brand, use the new Elastic names (Elastic Agent, Elastic OpenTelemetry).
* Avoid overusing the full product name. Use the shorter alias after the first mention.

## Frontmatter

Each document must have the following frontmatter fields defined:

```yaml
---
navigation_title: Title for the sidebar
description: Description for search engines.
applies_to:  # See https://docs-v3-preview.elastic.dev/elastic/docs-builder/tree/main/syntax/applies
  stack:
  serverless:
    observability:
products: # See https://docs-v3-preview.elastic.dev/elastic/docs-builder/tree/main/syntax/frontmatter#products
  - id: cloud-serverless
  - id: observability
---
```

## Linking other documents

To link other Elastic docs, use [Cross-links](https://docs-v3-preview.elastic.dev/elastic/docs-builder/tree/main/syntax/links#cross-repository-links).

You can use relative links when linking other pages within the docs.

## Building and previewing the docs site locally

Pull requests automatically generate a preview environment. To build the docs locally, use the `docs-builder` tool.

Refer to [Contribute locally](https://docs-v3-preview.elastic.dev/elastic/docs-builder/tree/main/contribute/locally) for instructions on how to install and use `docs-builder`.
