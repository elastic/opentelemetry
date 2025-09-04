---
navigation_title: Zero-code instrumentation
description: Use the EDOT .NET automatic instrumentation to send traces and metrics from .NET applications and services to observability backends without having to modify source code.
applies_to:
  stack:
  serverless:
    observability:
  product:
    edot_dotnet: ga
products:
  - id: cloud-serverless
  - id: observability
  - id: edot-sdk

---

# Using profiler-based zero-code instrumentation

EDOT .NET includes a redistribution of the zero-code installer scripts so most of the documentation in the [.NET zero-code instrumentation documentation](https://opentelemetry.io/docs/zero-code/dotnet/) applies.

Use the EDOT .NET automatic instrumentation to send traces and metrics from .NET applications and services to observability backends without having to modify source code.

## Compatibility

EDOT .NET automatic instrumentation should work with all officially supported operating systems and versions of .NET. The minimal supported version of .NET Framework is 4.6.2.

Supported processor architectures are:

- x86
- AMD64 (x86-64)
- ARM64 (Experimental)

:::{note}
ARM64 build does not support CentOS based images.
:::

## Setup

To instrument a .NET application automatically, download and run the installer script for your operating system.

### Linux and macOS

Download and run the .sh script:

```bash
# Download the bash script
curl -sSfL https://github.com/elastic/elastic-otel-dotnet/releases/latest/download/elastic-dotnet-auto-install.sh -O

# Install core files
sh ./otel-dotnet-auto-install.sh

# Enable execution for the instrumentation script
chmod +x $HOME/.otel-dotnet-auto/instrument.sh

# Setup the instrumentation for the current shell session
. $HOME/.otel-dotnet-auto/instrument.sh

# Run your application with instrumentation
OTEL_SERVICE_NAME=myapp OTEL_RESOURCE_ATTRIBUTES=deployment.environment=staging,service.version=1.0.0 ./MyNetApp
```

### Windows (PowerShell)

On Windows, use the PowerShell module as an Administrator:

```powershell
# PowerShell 5.1 or higher is required
# Download the module
$module_url = "https://github.com/elastic/elastic-otel-dotnet/releases/latest/download/Elastic.OpenTelemetry.DotNet.psm1"
$download_path = Join-Path $env:temp "Elastic.OpenTelemetry.DotNet.psm1"
Invoke-WebRequest -Uri $module_url -OutFile $download_path -UseBasicParsing

# Import the module to use its functions
Import-Module $download_path

# Install core files (online vs offline method)
Install-OpenTelemetryCore
Install-OpenTelemetryCore -LocalPath "C:\Path\To\OpenTelemetry.zip"

# Set up the instrumentation for the current PowerShell session
Register-OpenTelemetryForCurrentSession -OTelServiceName "MyServiceDisplayName"

# Run your application with instrumentation
.\MyNetApp.exe

# You can get usage information by calling the following commands

# List all available commands
Get-Command -Module OpenTelemetry.DotNet.Auto

# Get command's usage information
Get-Help Install-OpenTelemetryCore -Detailed
```

For more information on instrumenting specific application types visit the [contrib OpenTelemetry documentation](https://opentelemetry.io/docs/zero-code/dotnet/).
