---
navigation_title: Install the agent
description: Install and initialize the EDOT Browser agent (package or bundle).
applies_to:
  stack: ga
  serverless:
    observability: ga
products:
  - id: cloud-serverless
  - id: observability
  - id: edot-sdk
---

# Install the agent

EDOT Browser is distributed in two ways. The choice affects how you install it, how much control you have over instrumentations and bundle size, and how updates might affect your application.

## Package versus bundle [package-vs-bundle]

| Option | Best for | Trade-offs |
|--------|----------|------------|
| **Bundle** | Applications that don't use a bundler (single JS file loaded using script tag). | Works out of the box with no build step. Updating the bundle can introduce breaking changes when upstream instrumentations or configuration change. You have to absorb those changes when you upgrade. |
| **Package** | Applications that use a bundler (for example: webpack, Vite, Rollup). | You choose which instrumentations to include, so you have more control and can achieve a smaller bundle size by installing only what you need. You control when to upgrade instrumentations and can pin versions to avoid breaking changes until you are ready. |

Before installing, ensure you have [configured a reverse proxy and CORS](proxy-cors.md) so the browser can export telemetry securely.

## Install using the package [install-package]

Install EDOT Browser using your package manager:

```bash
npm install @elastic/opentelemetry-browser
```

When you use the package, your bundler includes only the code you import. You can control which instrumentations are enabled using configuration and, if the SDK supports it in the future, by passing only the instrumentation instances you need. This can reduce the final bundle size compared to the full bundle.

For supported bundlers and browser requirements, refer to [Supported technologies](supported-technologies.md).

## Install using the bundle [install-bundle]

A single JS bundle is available for script-tag usage (for example, from a CDN or your own host). Use it when your application doesn't use a bundler.

The bundle works out of the box: you add a script tag and initialize the SDK. When you update to a newer bundle version, upstream instrumentation or configuration changes might introduce breaking changes. You must test upgrades in a non-production environment.

<!-- TODO: add instructions and URL for the bundle when released -->

## Initialize EDOT Browser [initialize]

Initialize EDOT Browser as early as possible in your application lifecycle so it can capture initial page loads, user interactions, and network requests. Call `startBrowserSdk`:

- At the top of your application entry point
- In a framework-specific bootstrap location (for example, a React root component, Angular `main.ts`, or a Vue plugin)

Minimal example (package):

```js
import { startBrowserSdk } from '@elastic/opentelemetry-browser';

startBrowserSdk({
  serviceName: 'my-web-app',
  otlpEndpoint: 'https://telemetry.example.com', // reverse proxy URL; do not include /v1/traces or other signal paths
});
```

At a minimum, configure:

- `serviceName`: Identifies your frontend application in {{product.observability}}.
- `otlpEndpoint`: Must point to your reverse proxy (not directly to {{product.observability}}).

For all configuration options, refer to [Configure EDOT Browser](configuration.md).

## Verify setup [verify]

You have successfully set up EDOT Browser when the SDK loads without errors in the browser console and telemetry flows to your reverse proxy. To confirm data in {{product.observability}}, open {{kib}} and check for your service and traces. For what you see in the UI, refer to [What to expect in {{kib}}](setup.md#what-to-expect-in-kibana) in the setup guide.

## Next steps [next-steps]

- Refer to [Set up EDOT Browser](setup.md) for an overview and what to expect in {{kib}}.
- Refer to [Configure EDOT Browser](configuration.md) to customize behavior and defaults.
- Review [Supported technologies](supported-technologies.md) for browsers and instrumentations.
