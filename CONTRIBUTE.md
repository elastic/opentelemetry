# Contributing to the EDOT docs

## Writing the docs

We write the docs in regular markdown.

The site rendering uses the [Just the Docs Jekyll theme](https://just-the-docs.com/).

### Structuring the docs

All docs must be written in the `./docs` directory.

The docs are currently split into three navigation sections:

- default section (no dedicated directory)
- EDOT Collector (`_edot-collector` dir)
- EDOT SDKs (`_edot-sdks` dir)

(The underscore prefix for navigation sections is a requirement.)

Each markdown file results in a separate page.

Docs pages can be structured hierarchically by using the `parent`, `grand_parent` and `nav_order` properties in the front matter sections in the markdown files:

```
---
title: My Page Title
layout: default
nav_order: 2
parent: Use Cases
---
```

- `title`: Is the page title shown in the navigation bar. This title is also being used to build hierarchies using the `parent` (and `grand_parent`) properties.
- `layout`: That property must be set to the value `default` on all markdown files, otherwise the layout might break.
- `nav_order`: That defines the position of the page in the navigation within it's parent context.
- `parent`: Put the title of the parent page here to build a hierarchical structure of your docs pages. You can omit that property if the page should at the top level of the corresponding navigation section.
- `grand_parent`: Use this property to set the grandparent, when the parent title is not unique within a navigation section.

You can find more information in the [Just the Docs theme documentation](https://just-the-docs.com/docs/navigation/main/order/).

### Linking other pages

You can use relative links when linking other pages within the docs. Howewver, please make sure to not use the file suffix `.md` in the links:

**Correct:**

```markdown
[My Link Text](./relativ/path/to/other_page)
```

**Incorrect:**

```markdown
[My Link Text](./relativ/path/to/other_page.md)
```

> [!WARNING]  
> When linking cross navigation sections (e.g. from EDOT Collector pages to EDOT SDKs pages) make sure to **remove** the underscore `_` prefix of the section!
>
> Correct link: `[Link Text](../edot-sdks/java)`
>
> Incorrect link: `[Link Text](../_edot-sdks/java)`

### Adding Callouts

In this theme we have defined two types of callouts: `NOTE` and `WARNING`.
You can use those by putting a `{: .note }` or `{: .warning }` in front of a paragraph:

```markdown
{: .note }
My Note paragraph with some text.
```

For multi-paragraph callouts use the block syntax:

```markdown
{: .warning }
> My first warning paragraph.
>
> My second warning paragraph.
```

### Using Artifact versions

Jekyll allows to do variable replacement in markdown files. We use that feature to specify artifact versions (for download links, etc.) in the docs.
The variables are defined in the `docs/_config.yml` file. Use the corresponding variable (in the form of `{{ site.edot_versions.collector }}`, etc.) in markdown instead of the concrete version numbers

**Correct**:

```markdown 
My markdown [link](https://artifacts.elastic.co/downloads/beats/elastic-agent/elastic-agent-{{ site.edot_versions.collector }}-darwin-arm64.tar.gz)
```

**Incorrect**:

```markdown 
My markdown [link](https://artifacts.elastic.co/downloads/beats/elastic-agent/elastic-agent-8.17.1-darwin-arm64.tar.gz)
```

## Building and previewing the docs site locally

### Prerequisites 

1. Install Ruby. For more information, see [Installing Ruby](https://www.ruby-lang.org/en/documentation/installation/) in the Ruby documentation.
2. Install Bundler. For more information, see [Bundler](https://bundler.io/).

### Preview the docs locally

Initially, from the `docs` directory containing the `Gemfile` install the dependencies:

```bash
bundle install
```

{: .note }
You may need to install ruby development headers to compile some gems

Run the site locally:

```bash
bundle exec jekyll serve
```

Access your local site under http://localhost:4000/opentelemetry/

### Terms

| Term | Description | Alias<sup>1</sup> | Example |
|---|---|---|---|
| **Elastic Distributions of OpenTelemetry** | Use to describe all distributions built by Elastic collectively | EDOTs | Use one of the Elastic Distributions of OpenTelemetry (EDOTs) in your application. EDOTs include... |
| **Elastic Distributions of OpenTelemetry language SDKs** | Use to describe the collection of all the Elastic distributions that extend language SDKs (i.e. the APM-related distros) | EDOT language SDKs | With the Elastic Distributions of OpenTelemetry (EDOT) language SDKs you have access to all the features of the OpenTelemetry SDK that it customizes, plus... |
| **Elastic Distribution of OpenTelemetry {language}** | Use to refer to a specific language distribution | EDOT {language} | The Elastic Distribution of OpenTelemetry (EDOT) Java is a Java package that provides an easy way to instrument your application with OpenTelemetry and configuration defaults for best usage. EDOT Java is a wrapper around... |
| **Elastic Distribution of OpenTelemetry Collector** | Use to describe the customized version of the OpenTelemetry Collector that is built and maintained by Elastic | EDOT Collector | This guide shows you how to use the Elastic Distribution of OpenTelemetry (EDOT) Collector. The EDOT Collector sends logs and host metrics to Elastic Cloud. |

<sup>1</sup> _Only use after establishing that it is a replacement for the product name._

### Guidelines

* Always use the full product name the first time you refer to the product on each page.
* Always establish the acronym for the product name (i.e. EDOT) the first time it is mentioned in the body text.
  * Note: Do *not* establish the acronym for the first time in the page title or in a heading. If a heading comes *after* the first time the acronym is established in the body text, then it's ok to use the acronym instead of the full product name in the heading.
* Avoid overusing the full product name. Use the shorter, already-established alias.

### Relationship between products

* The general **OpenTelemetry SDK** is the *implementation of* the API provided by the OpenTelemetry project.
* The **OpenTelemetry SDK for {language}** is an *implementation of* the general **OpenTelemetry SDK**. It is built and maintained by OpenTelemetry.
* The **Elastic Distribution of OpenTelemetry {language}** is *a customized version of* the **OpenTelemetry SDK/Agent for {language}**. It is built and maintained by Elastic.
* The **Elastic Distribution of OpenTelemetry Collector** is *a customized version of* the **OpenTelemetry Collector**.

We write our docs in Markdown. See our [syntax guide](https://elastic.github.io/docs-builder/syntax/index.html) for examples and additional functionality.