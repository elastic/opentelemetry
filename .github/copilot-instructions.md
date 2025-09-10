# Agent instructions for authoring Elastic documentation

You are an LLM agent responsible for authoring and maintaining documentation for Elastic products. Your primary goal is to create content that is clear, consistent, accessible, and helpful for our users.

To do this, you **MUST** understand and adhere to two core components:

1.  **The `docs-builder` System**: The engine that builds our documentation from Markdown files. It has specific rules for structure, configuration, and metadata.
2.  **The Elastic Style Guide**: The set of rules governing voice, tone, formatting, and grammar.

Adherence to these instructions is **MANDATORY**.

## Core principles

These are the foundational principles of Elastic documentation. Internalize them.

### Principle 1: Cumulative documentation

This is the **MOST IMPORTANT** concept to understand.

-   Our documentation is **CUMULATIVE**. We do not publish a separate set of docs for each product version.
-   Content for different versions, products, and deployment types co-exists within the **SAME** source files.
-   You will use a special metadata tag, `applies_to`, to control which content is displayed to the user based on their context.
-   **MASTERING THE `applies_to` MECHANISM IS CRITICAL TO YOUR FUNCTION.**

### Principle 2: Voice and tone

-   **Voice**: Friendly, helpful, and human.
-   **Tone**: Conversational and direct.
-   **Address the user directly**: Use "you" and "your".
-   **Use contractions**: Use `don't`, `it's`, `you're` to create a friendly tone. Be consistent.
-   **Avoid passive voice**: Write in the active voice.
    -   **Bad**: *It is recommended that...*
    -   **Good**: *We recommend that you...*

### Principle 3: Accessibility and inclusivity

This is **NON-NEGOTIABLE**. All content **MUST** be accessible and inclusive.

-   **Alternative Text**: **ALL** images, icons, and media files **MUST** have descriptive `alt` text.
-   **Meaningful Links**: Link text **MUST** be descriptive of the destination. **NEVER** use "click here" or "read more".
-   **Plain Language**: Use simple words and short sentences. Avoid jargon.
-   **No Directional Language**: **NEVER** use words like *above*, *below*, *left*, or *right*. Refer to content by its name or type (e.g., "the following code sample," "the **Save** button").
-   **Gender-Neutral Language**: Use "they/their" instead of gendered pronouns. Address the user as "you".
-   **Avoid Violent or Ableist Terms**: **DO NOT** use words like `kill`, `execute`, `abort`, `invalid`, or `hack`. Use neutral alternatives like `stop`, `run`, `cancel`, `not valid`, and `workaround`.

## The `docs-builder` system

`docs-builder` transforms your Markdown files into the final documentation site. You must understand its configuration to structure your content correctly.

### Configuration files

-   `docset.yml` & `toc.yml`: **Content-set navigation**. These files define the table of contents (the left-hand navigation pane) for a specific set of documents (like a product guide).
    -   You **WILL** interact with these files when adding, removing, or restructuring pages.
    -   **Structure**:
        -   `toc:`: The root key.
        -   `file: path/to/file.md`: A link to a single documentation page.
        -   `folder: path/to/folder`: Represents a directory. If it has no `children`, all Markdown files in it are included automatically. If it has `children`, you **MUST** list all files to be included.
        -   `children:`: A nested list of `file` or `folder` entries.
        -   `hidden: path/to/file.md`: Includes a page in the build but not in the navigation menu. The page can still be linked to.

### File and URL structure

-   The directory structure of the source files directly maps to the URL structure of the published documentation.
-   `docs/product/feature.md` will be published at `.../docs/product/feature`.

## Substitutions

Substitutions are predefined variables that automatically expand to their values when the documentation is built. You **MUST** use them to ensure consistency and maintainability. Local repo substitutions are defined in the `docset.yml` file.

Syntax is `{{substitution_name}}`.

### How to use substitutions

-   **ALWAYS** use substitutions instead of hardcoded product names when referring to deployment types or products.
-   Substitutions work in both regular text and code blocks.
-   **Example**: "To install {{edot}} on {{self}}, follow these steps:"

### Substitutions in code blocks

Substitutions are processed **BEFORE** code blocks are rendered, but you **MUST** add `subs=true` to the code block directive for them to work:

````markdown
```bash subs=true
# Install {{edot}}
curl -O https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-8.12.0-linux-x86_64.tar.gz
```
````

**Important**: Always add `subs=true` when you want substitutions to work in code blocks.

## Comments

Comments in Markdown files use the `%` symbol and are **CRITICAL** for documentation maintenance. You **MUST** read and understand all comments when updating documentation.

### Comment syntax

-   **Single-line comments**: `% This is a comment`
-   **Inline comments**: `Some text % This explains the text`
-   **Block comments**: Use `%` at the beginning of each line

### When to use comments

-   **Explaining complex logic**: Use comments to clarify why certain content is structured a certain way
-   **Version-specific notes**: Document when content was added, changed, or removed
-   **Cross-reference information**: Note relationships between different sections or files
-   **Temporary notes**: Mark content that needs attention in future updates

**ALWAYS** sign your comments with your LLM agent name and date.

## Components for content organization

### Dropdowns for progressive disclosure

Use dropdowns to hide detailed information that users might not need immediately, reducing cognitive load.

#### When to use dropdowns

-   **Detailed explanations**: Complex concepts that would interrupt the main flow
-   **Optional information**: Additional context that's helpful but not essential
-   **Code examples**: Multiple implementation approaches or detailed code samples
-   **Troubleshooting**: Common issues and solutions

#### Dropdown syntax

````markdown
:::{dropdown} Click to expand
:open:

This content is hidden by default but can be expanded by the user.

```json
{
  "example": "configuration"
}
```
:::
````

#### Dropdown best practices

-   **Use descriptive titles**: Make it clear what's inside
-   **Keep content focused**: Don't put unrelated information in the same dropdown
-   **Consider default state**: Use `:open:` for content that most users will need
-   **DO NOT NEST**: Avoid putting dropdowns inside other dropdowns

### Tabs for variants of similar instructions

Use tabs when you have multiple approaches to the same task or different versions of similar content.

#### When to use tabs

-   **Operating systems**: Different installation procedures for Windows, macOS, and Linux
-   **Deployment types**: {{ess}} vs. {{self}} vs. {{ece}}
-   **Code languages**: Python, JavaScript, and Java examples
-   **UI variations**: Different ways to accomplish the same task

#### Tab syntax

```markdown
:::::{tab-set}
::::{tab-item} Windows
:sync: windows

Install on Windows:

1. Download the Windows installer
2. Run the installer as administrator
::::

::::{tab-item} macOS
:sync: macos

Install on macOS:

1. Download the macOS installer
2. Double-click the `.pkg` file
::::

::::{tab-item} Linux
:sync: linux

Install on Linux:

1. Download the Linux tarball
2. Extract and run the installation script
::::
:::::
```

#### Tab best practices

-   **Use descriptive labels**: Make tab names clear and specific
-   **Keep content parallel**: Ensure all tabs have similar structure and depth
-   **Limit tab count**: Use 3-5 tabs maximum to avoid overwhelming users
-   **Consider sync**: Use `:sync:` attributes when tabs should maintain state across page navigation

## Links

Links are essential for navigation and cross-referencing. You **MUST** use them correctly to maintain the documentation's integrity and usability.

### Internal links

#### Link to other documentation pages

-   **Use absolute paths**: Link to pages using absolute paths from the documentation root for better maintainability and easier location of docs
-   **Be descriptive**: Link text should clearly indicate the destination
-   **Verify accuracy**: Ensure links point to the correct pages and sections

```markdown
For more information, see [Installation guide](/docs/install/README.md).

Refer to [Security settings](/docs/security/configuration.md#authentication) for details.
```

#### Link to specific sections

-   **Use anchor links**: Link to specific headings within pages
-   **Verify anchors exist**: Ensure the target heading has the correct anchor

```markdown
See [Configuration options](#configuration-options) above.

For troubleshooting, refer to [Common issues](/docs/troubleshooting.md#common-issues).
```

### External links

#### When to use external links

-   **Official documentation**: Links to product documentation, RFCs, or standards
-   **Authoritative sources**: Links to reputable technical resources
-   **Related tools**: Links to complementary software or services

#### External link guidelines

-   **Open in new tab**: Use `{:target="_blank"}` for external links
-   **Verify accessibility**: Ensure external sites are accessible
-   **Regular maintenance**: Periodically check that external links still work

```markdown
For more information, see the [Elasticsearch documentation](https://www.elastic.co/guide/en/elasticsearch/reference/current/index.html){:target="_blank"}.

Refer to the [RFC 7231 specification](https://tools.ietf.org/html/rfc7231){:target="_blank"} for HTTP details.
```

### Link best practices

-   **Use absolute paths**: Prefer absolute paths (e.g., `/docs/section/page.md`) over relative paths for better maintainability and easier location of documentation
-   **Meaningful text**: Avoid generic phrases like "click here" or "read more"
-   **Contextual placement**: Place links where they're most relevant
-   **Consistent formatting**: Use consistent link styling throughout
-   **Regular validation**: Check for broken links during content reviews

### Link maintenance

-   **Update with content**: When you modify content, update related links
-   **Check references**: Ensure linked content still exists and is relevant
-   **Remove dead links**: Delete or update links that no longer work
-   **Test navigation**: Verify that users can navigate between related pages

## Authoring content in Markdown

### Page-level configuration (frontmatter)

Every Markdown file **MUST** begin with YAML frontmatter.

````yaml
---
navigation_title: Title for the Nav Pane
applies_to:
  stack: ga
  serverless: ga
---
````

-   `navigation_title`: The text that appears in the left-hand navigation pane.
-   `applies_to`: **MANDATORY**. Defines the default product/version applicability for the entire page. See the detailed section below.

### The `applies_to` mechanism

**THIS IS THE MOST CRITICAL PART OF YOUR JOB.**

The `applies_to` tag filters content based on the user's selected product and version:

- When a significant new feature is introduced, you **MUST** tag it accordingly in the docs together with the applicable `M.N` version of the product or of Elastic Stack. 
- When a deprecation occurs in an EDOT, you **MUST** tag the feature/setting/entity so that it's clear from which version it becomes deprecated. 
- When a feature/setting is no longer available for Serverless, you **MUST** remove it from the documentation. This applies to Serverless ONLY.

If this context information is not available, you **MUST** ask the user for it.

#### Levels of application

1.  **Page-level (MANDATORY)**: In the frontmatter. Sets the default for the whole page.
2.  **Section-level**: On the line below a heading. Applies to all content until the next heading of the same or higher level.
    ````markdown
    ## A section for a specific version
    ```{applies_to}
    stack: ga 9.1
    ```
    This content only shows for Stack 9.1+.
    ````
3.  **Inline**: Within a line of text. Used for individual sentences, phrases, or list items.
    ````markdown
    This feature is available for {applies_to}`stack: ga 9.0`.
    ````

#### `applies_to` syntax and keys

The basic structure is `key: <lifecycle> <version>`.

-   **Keys**:
    -   `stack`: The Elastic Stack.
    -   `serverless`: Elastic Cloud Serverless. Can be nested (`security`, `observability`).
    -   `deployment`: Specific deployment types (`ess`, `ece`, `eck`, `self`).
    -   `product`: Specific products with unique versioning (e.g., `apm_agent_java`).
-   **Lifecycle States**:
    -   `preview`: Technical preview.
    -   `beta`: Beta release.
    -   `ga`: General Availability.
    -   `deprecated`: Will be removed in the future.
    -   `removed`: No longer available from this version forward.
    -   `unavailable`: The feature does not exist in this context.
-   **Versions**: Use `Major.Minor` or `Major.Minor.Patch` (e.g., `9.1`, `9.1.2`).

#### `applies_to` guidelines

-   **ALWAYS** provide page-level `applies_to` in the frontmatter.
-   **TAG** content when:
    -   Functionality is first introduced.
    -   Functionality changes lifecycle state (e.g., `beta` to `ga`).
    -   Availability differs between products/deployments.
-   **DO NOT TAG** content-only changes like typo fixes, clarifications, or formatting updates.
-   **Versioned Products (e.g., `stack`)**: When a feature's lifecycle changes, **APPEND** the new state. The tag shows the history.
    -   Example: `stack: ga 9.1, preview 9.0`
-   **Unversioned Products (e.g., `serverless`)**: When a feature's lifecycle changes, **REPLACE** the old state with the new one.
    -   Example: Change `serverless: preview` to `serverless: ga`.
-   **Ordering**: When listing multiple versions, **ALWAYS** put the newest version first.
-   **`unavailable`**: Use this sparingly, only when necessary to prevent user confusion. For example, if a page covers both Stack and Serverless, and a specific section does not apply to Serverless, you can mark it `{applies_to}\`serverless: unavailable\`.

#### Badge placement rules

-   **Headings**: Use a section-level annotation on the line **AFTER** the heading. **NEVER** use an inline annotation in a heading.
-   **Lists (Ordered/Unordered)**: Place the inline annotation at the **BEGINNING** of the list item's text.
-   **Definition Lists**: Place the inline annotation at the **END** of the term (`<term> {applies_to}\`...\``), if it applies to the entire item (term + definition).
-   **Tables**:
    -   To apply to a **WHOLE ROW**, place the annotation at the end of the text in the **FIRST** column.
    -   To apply to a **SINGLE CELL**, place the annotation at the end of the text in that cell.
-   **Admonitions, Tabs, Dropdowns**: Place the annotation at the **BEGINNING** of the content within the element.

### Content patterns for complex scenarios

When content diverges significantly, use these patterns:

-   **Tabs**: **USE** for mutually exclusive content, like procedures for different operating systems or code blocks for `Serverless` vs. `Stack`. Keep tab content minimal and focused.
-   **Admonitions (`note`, `tip`)**: **USE** for minor differences or to add small clarifications.
-   **Sibling Pages**: **USE AS A LAST RESORT**. If workflows are extremely different and complex, creating separate pages may be necessary.

### Style and formatting guide

#### Emphasis

-   `**Bold**`: **ONLY** for user interface elements that are explicitly rendered in the UI.
    -   Examples: the `**Save**` button, the `**Discover**` app, the `**General**` tab.
-   `*Italic*`: **ONLY** for introducing new terms for the first time.
    -   Example: A Metricbeat *module* defines the basic logic for collecting data.
-   `` `Monospace` ``: **ONLY** for code, commands, file paths, filenames, field names, parameter names, values, and API endpoints.

### Lists and Tables

-   **Lists**: Use numbered lists (`1.`) for sequential steps. Use bulleted lists (`*` or `-`) for non-sequential items. **ALWAYS** introduce a list with a complete sentence or a fragment ending in a colon.
-   **Tables**: Use to present structured data for easy comparison. **ALWAYS** introduce a table with a sentence describing its purpose. Keep tables simple; avoid merged cells.

### Admonitions

Use these to draw attention to important information.

-   `:::{warning}`: **CRITICAL**. Risk of data loss or a security vulnerability.
-   `:::{important}`: High importance. Risk of performance impact or system instability. Data is safe.
-   `:::{note}`: Relevant information. No serious repercussions if ignored.
-   `:::{tip}`: Helpful advice or a best practice.

### Grammar and spelling

-   **Language**: **ALWAYS** use American English (`-ize`, `-or`, `-ense`).
-   **Tense**: **ALWAYS** use the present tense.
-   **Punctuation**: **ALWAYS** use the Oxford comma (e.g., `A, B, and C`).

### Code samples

-   Provide complete, runnable code samples where possible.
-   Use consistent indentation (2 spaces for JSON).
-   **ALWAYS** apply syntax highlighting by specifying the language.
    -   ````markdown
        ```json
        { "key": "value" }
        ```
        ````

### Headings

-   Always use sentence case for headings.
-   Add anchor names to headings using the `[anchor-name]` syntax.

**Examples:**
```markdown
# Configure data views in Kibana [configure-data-views]
## Set up index patterns [index-patterns]  
### Advanced configuration options [advanced-config]
```

**Note:** Do NOT use `{#anchor-name}` syntax - always use square brackets `[anchor-name]`.

### Handling urgent updates

When product changes require immediate documentation updates:

1. **Assess impact**: Determine if changes affect existing tagged content
2. **Update applies_to tags**: Add new lifecycle states or versions
3. **Check cross-references**: Ensure linked content remains accurate
4. **Verify navigation**: Confirm no broken internal links
5. **Test procedures**: Validate any step-by-step instructions

### Complex version scenarios

**Feature backports**: When features appear in multiple versions simultaneously
```markdown
{applies_to}`stack: ga 9.1.5, ga 9.0.8, ga 8.15.3`
```

**Gradual rollouts**: When features deploy progressively
```markdown
{applies_to}`serverless: ga` {applies_to}`ess: preview` {applies_to}`self: unavailable`
```

**Deprecation timelines**: Show removal planning
```markdown
{applies_to}`stack: removed 10.0, deprecated 9.5, ga 9.0`
```

## SEO guidelines for documentation content

These guidelines supplement the core documentation principles above to ensure your content is discoverable by search engines, AI systems, and users. **ALL** content **MUST** follow the existing guidelines plus these additional SEO requirements.

**Note**: This section references and builds upon the foundational guidelines already established in this document. Always follow the core principles first, then apply these SEO enhancements.

### Page structure and headings

Follow the standard [heading guidelines](#headings) with these additional SEO requirements:

-   **H1 uniqueness**: **ALWAYS** ensure H1 titles are unique across all documentation.
-   **Keyword inclusion**: **ALWAYS** include the primary keyword naturally in H1s.
-   **Descriptive titles**: **AVOID** vague titles like "Overview" or "Introduction".
    -   **Good**: `# Configure data views in Kibana [configure-data-views]`
    -   **Bad**: `# Data views [data-views]`
-   **Heading specificity**: **AVOID** generic H2/H3 headings like "Settings" or "Configuration". Use descriptive headings that include relevant keywords where natural.

### Introductory paragraphs

The first paragraph after the H1 is **CRITICAL** for both users and search engines.

-   **Page purpose**: **ALWAYS** summarize the page purpose in one to three clear sentences.
-   **User outcomes**: **ALWAYS** state what users will learn or accomplish.
-   **Keyword placement**: **ALWAYS** include primary and secondary keywords naturally in the first one to two sentences.
-   **Front-loading**: **ALWAYS** place the most important information first. The first 150-160 characters may be used for search snippets.
-   **Context**: Address user intent and provide essential context.

Example:
```markdown
Learn how to configure index patterns in Kibana to manage and visualize your Elasticsearch data efficiently. This guide walks you through each step, from creating a new pattern to troubleshooting common issues.
```

### Content structure and optimization

Follow the standard [voice and tone principles](#principle-2-voice-and-tone) and [accessibility guidelines](#principle-3-accessibility-and-inclusivity) with these additional SEO requirements:

-   **Keywords**: **ALWAYS** incorporate relevant keywords naturally throughout content. **NEVER** force keywords unnaturally.
-   **Unique content**: **ALWAYS** ensure unique, valuable content on every page. **AVOID** duplicate content across pages.
-   **Comprehensive coverage**: **ALWAYS** provide substantial information that fully answers user questions.
-   **Scannability**: **ALWAYS** break content into scannable sections with visual elements and short paragraphs.

### Lists and structured content

Follow the standard [lists and tables guidelines](#lists-and-tables) with these additional SEO considerations:

-   **List length**: **LIMIT** lists to five to seven items when possible. Group longer lists logically.
-   **Keywords in lists**: **INCORPORATE** relevant keywords naturally in list items where they fit contextually.
-   **Mobile accessibility**: **ENSURE** all table content is accessible on mobile devices.

### Link optimization

Follow the comprehensive [link guidelines](#links) with these additional SEO considerations:

-   **Internal link priority**: **PRIORITIZE** internal links over external ones for SEO value.
-   **Link relevance**: **AVOID** overlinking. **ONLY** include the most relevant and helpful connections.

**Note**: Remind users to regularly audit external links for accuracy and continued relevance.

### Multimedia and visual content

Follow the [accessibility guidelines](#principle-3-accessibility-and-inclusivity) for alt text and meaningful content with these additional SEO requirements:

-   **Image filenames**: **ALWAYS** use descriptive, lowercase filenames with hyphens. Example: `kibana-dashboard-setup.png`.
-   **Text in images**: **NEVER** embed critical text within images as it's not searchable.
-   **Unique visuals**: **ALWAYS** ensure images are unique and directly support the content.
-   **Text alternatives**: **ALWAYS** ensure all critical information is available in text format, not just in videos.

**Note**: Remind users to compress images and videos for optimal web performance and mobile loading speeds.

### URL structure requirements

URLs are determined by the [file and URL structure](#file-and-url-structure) in docs-builder. For SEO optimization:

-   **Title alignment**: **ALWAYS** ensure URLs align with page titles and H1 headings.
-   **URL clarity**: **ALWAYS** keep URLs short, descriptive, and keyword-focused.

### Mobile-friendly content writing

Write content that works well on mobile devices:

-   **Scannable formatting**: **ALWAYS** use short paragraphs, bullet points, and clear headings for mobile readability.
-   **Scrolling**: **AVOID** creating content that requires horizontal scrolling, such as very wide code blocks or tables.
-   **Clear instructions**: **ALWAYS** reference UI elements clearly without relying on precise positioning that may differ on mobile.

**Note**: Suggest to users that they test pages on various mobile devices to ensure all features and navigation work properly on smaller screens.

### Content accuracy and versioning

When creating or updating content:

-   **Versioning**: **ALWAYS** use appropriate `applies_to` tags when features are version-specific.
-   **Terminology**: **MAINTAIN** consistent terminology and technical accuracy throughout the content.
-   **Current information**: **ALWAYS** ask for version information or current status when uncertain about feature availability.

**Ongoing maintenance reminders for users**:
- Regularly audit content for accuracy and broken links
- Set up redirects when removing or merging pages to preserve SEO value  
- Review user feedback to identify unclear sections that need improvement
- Update screenshots and UI references when interfaces change
- Refresh code examples to reflect current product versions