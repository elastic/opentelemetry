# Contributing to the EDOT docs

This repository contains the EDOT documentation. We welcome pull requests.

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
    ├── edot-collector     # EDOT Collector
    ├── edot-sdks          # EDOT SDKs
    ├── images             # Images
    ├── quickstart         # Quickstarts
    └── use-cases          # Use cases
```

This structure might evolve as we refine the EDOT documentation according to the new V3 information architecture.

## Style guide

Elastic docs strive to keep a consistent voice and tone, with a distinct style throughout all repositories.

Tech writers will help you refine your contributions. Refer to [Technical writing style guide](https://docs.elastic.dev/tech-writing-guidelines/home) to learn more.

Always use US English spellings.

## Terminology

Use the following terms consistently and respect capitalization.

| Term | Description | Alias | Example |
|---|---|---|---|
| **Elastic Distributions of OpenTelemetry** | Use to describe all distributions built by Elastic collectively | EDOTs | Use one of the Elastic Distributions of OpenTelemetry (EDOTs) in your application. EDOTs include... |
| **Elastic Distributions of OpenTelemetry language SDKs** | Use to describe the collection of all the Elastic distributions that extend language SDKs (i.e. the APM-related distros) | EDOT language SDKs | With the Elastic Distributions of OpenTelemetry (EDOT) language SDKs you have access to all the features of the OpenTelemetry SDK that it customizes, plus... |
| **Elastic Distribution of OpenTelemetry {language}** | Use to refer to a specific language distribution | EDOT {language} | The Elastic Distribution of OpenTelemetry (EDOT) Java is a Java package that provides an easy way to instrument your application with OpenTelemetry and configuration defaults for best usage. EDOT Java is a wrapper around... |
| **Elastic Distribution of OpenTelemetry Collector** | Use to describe the customized version of the OpenTelemetry Collector that is built and maintained by Elastic | EDOT Collector | This guide shows you how to use the Elastic Distribution of OpenTelemetry (EDOT) Collector. The EDOT Collector sends logs and host metrics to Elastic Cloud. |
| **Upstream** | Use to describe the upstream OpenTelemetry solutions. Do not use "vanilla" or other terms. |  | The upstream OpenTelemetry Collector is maintained by the OpenTelemetry community. |
| **Collector** | Use it to refer to any Collector instance, either upstream or EDOT. Always capitalize Collector when referring to the technical solution. Use lowercase when referring to multiple collectors. |  | Deploy a Collector to receive and process telemetry data. Multiple collectors can be used for scaling. |

Keep these rules in mind when using EDOT terms:

* Always use the full product name the first time you refer to the product on each page.
* Always establish the acronym for the product name (for example, EDOT) the first time it is mentioned in the body text.
  * Note: Do *not* establish the acronym for the first time in the page title or in a heading. If a heading comes *after* the first time the acronym is established in the body text, then it's ok to use the acronym instead of the full product name in the heading.
* Avoid overusing the full product name. Use the shorter, already-established alias.

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
products: # See https://docs-v3-preview.elastic.dev/elastic/docs-builder/tree/main/syntax/frontmatter#products
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
