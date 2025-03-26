---
title: Troubleshooting
layout: default
nav_order: 4
parent: EDOT PHP
---

# Troubleshooting the EDOT PHP Agent

Is something not working as expected?
Don't worry if you can't figure out what the problem is; we’re here to help!
As a first step, make sure your application is compatible with the [technologies supported by EDOT PHP](./supported-technologies).

If you're an existing Elastic customer with a support contract, please create a ticket in the
[Elastic Support portal](https://support.elastic.co/customers/s/login/).
Other users can post in the [APM discuss forum](https://discuss.elastic.co/c/apm).

## Enable logging

In diagnosing issues with the agent's operation, logs play a key role. A detailed explanation of the logging configuration options can be found in the [configuration documentation](configure#logging-configuration).

In most cases, setting the logging level to `debug` is sufficient. In extreme cases, `trace` can be used, but keep in mind that the amount of generated data may be significant.

Additionally, it is recommended to enable logging for OpenTelemetry components, for example, as shown in the example below using an environment variable. Logs from OpenTelemetry components will be directed to the same output configured for EDOT logs.

```
export OTEL_LOG_LEVEL=DEBUG
```

> **IMPORTANT:** _Please upload your complete debug logs_ to a service like [GitHub Gist](https://gist.github.com) so that we can analyze the problem. Logs should include everything from when the application starts up until the first request executes. It is important to note that logs may contain sensitive data — be sure to review and sanitize them before sharing.


## Disable the Agent

In the unlikely event the agent causes disruptions to a production application,
you can disable the agent while you troubleshoot.

You can disable the agent by setting [`elastic_otel.enabled`](./configuration#general-configuration) to `false`.

> **IMPORTANT:** You'll need to restart your application for the changes to apply.


## Agent is not instrumenting code

### `open_basedir` PHP configuration option

If you see a similar entry in the agent log, this indicates an incorrect open_basedir configuration.
For more details please see [limitations documentation](./setup/limitations#open_basedir-php-configuration-option).


`EDOT PHP bootstrap file (...php/bootstrap_php_part.php) is located outside of paths allowed by open_basedir ini setting.`

## Collection of diagnostic information

For a more detailed analysis of issues, it is necessary to collect diagnostic information. The agent allows for the automatic collection of such information - all data will be saved to the file specified in the configuration.

There are two possible ways to enable this feature:

- By php.ini - To enable this feature, you need to modify the php.ini file (or 99-elastic.ini) and provide the path to the file where the data will be saved, f.ex:
```
elastic_otel.debug_diagnostic_file=/tmp/php_diags_%p_%t.txt
```

- By environment variable. You can also enable information collection using the environment variable `ELASTIC_OTEL_DEBUG_DIAGNOSTIC_FILE`. It must be exported or directly specified when running php process.

Example of calling php-cli script:
```bash
ELASTIC_OTEL_DEBUG_DIAGNOSTIC_FILE=/tmp/php_diags_%p_%t.txt php test.php
```

Remember, the provided file path must be writable by the PHP process.

If there are multiple PHP processes in your system, we allow you to specify directives in the diagnostic file name. This way, the files will remain unique and won't be overwritten.

- `%p` - In this place, the agent will substitute the process identifier.

- `%t` - In this place, the agent will substitute the UNIX timestamp.

>:warning: **IMPORTANT:** After setting the path, remember to _fully restart the process_ for which you are collecting diagnostic information. This may vary depending on the context, such as PHP, PHP-FPM, Apache, or PHP-CGI. Diagnostic information will be recorded after the first HTTP request is made or at the beginning of script execution for PHP-CLI.
>
>Please also be aware that the information contained in the output file may include sensitive data, such as passwords, security tokens or environment variables from your system. Make sure to review the data and mask sensitive information before sharing the file publicly.
>
>After collecting diagnostic information, remember to disable this feature and restore the previous configuration in php.ini or the environment variable.


What information will be collected:

- Process identifier and parent process identifier
- User identifier of the worker process
- List of loaded PHP extensions
- Result from the `phpinfo()` function
- Process memory information and memory maps (`/proc/{id}/maps` and `/proc/{id}/smaps_rollup`)
- Process status information (`/proc/{id}/status`)

## Enabling Debugging for Instrumented Functions

EDOT allows detailed diagnostics of arguments passed to instrumented functions. This makes it possible to verify whether the data used by the instrumented application is correctly analyzed by the instrumentation code.

This feature can be enabled using an environment variable:

```bash
ELASTIC_OTEL_DEBUG_PHP_HOOKS_ENABLED=true
```


## Enabling instrumentation of the entire application code

For diagnostic purposes (*this feature is not suitable for production use*), EDOT allows instrumentation of the entire code. This enables tracking function calls throughout the processing of an entire request or script. It provides better insight into the application's behavior and can help diagnose issues.

This feature can be enabled using an environment variable:

```bash
ELASTIC_OTEL_DEBUG_INSTRUMENT_ALL=true
```

