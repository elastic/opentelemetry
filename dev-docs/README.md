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

## Building and previewing the docs site locally

### Prerequisites 

1. Install Ruby. For more information, see [Installing Ruby](https://www.ruby-lang.org/en/documentation/installation/) in the Ruby documentation.
2. Install Bundler. For more information, see [Bundler](https://bundler.io/).

### Preview the docs locally

Initially, install the dependencies:

```bash
bundle install
```

Run the site locally:

```bash
bundle exec jekyll serve
```

Access your local site under http://localhost:4000/opentelemetry/