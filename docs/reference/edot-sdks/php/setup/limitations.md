---
navigation_title: Limitations
description: Limitations of the Elastic Distribution of OpenTelemetry PHP.
---

# Limitations

This section describes potential limitations of Elastic Distribution of OpenTelemetry PHP (EDOT PHP)
and how you can work around them.

## OpenTelemetry extension and SDK loaded in parallel with EDOT PHP

Currently, the Elastic Distribution of OpenTelemetry PHP (EDOT PHP) does not support scenarios where both EDOT and a vanilla OpenTelemetry PHP setup are installed in the application. This includes the `opentelemetry.so` extension and the OpenTelemetry PHP SDK.

In such cases, a conflict will occur, preventing both solutions from functioning correctly. To resolve this, remove OpenTelemetry components from your application's `composer.json` and update the project accordingly.

We are actively working on an automated solution to address this issue.

## `open_basedir` PHP configuration option

Please be aware that if the `open_basedir` option ([documentation](https://www.php.net/manual/en/ini.core.php#ini.open-basedir)) is configured in your php.ini, the installation directory of EDOT PHP (by default `/opt/elastic/apm-agent-php`) must be located within one of the paths specified in the `open_basedir` option.
Otherwise, EDOT PHP will not be loaded correctly.


## `Xdebug` stability and memory issues

We strongly advise against running the agent alongside the Xdebug extension. Using both extensions simultaneously can lead to stability issues in the instrumented application, such as increased memory usage or memory leaks. It is highly recommended to disable xdebug, preferably by disabling it directly in your `php.ini` configuration.
