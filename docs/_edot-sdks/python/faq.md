---
title: Frequently Asked Questions
layout: default
nav_order: 7
parent: EDOT Python
---

# Frequently Asked Questions on EDOT Python

## Are semantic convention stable yet?

Unfortunately not yet and so you should expect some changes between versions in order to stabilize them. For some semantic conventions
like HTTP there is a migration path but the conversion to stable HTTP semantic conventions is not done yet for all the instrumentations.

## Does EDOT Python requires access to or modification of application code ?

EDOT Python is distributed as a Python package and so must be installed in the same environment as your application. Once it is
available in the path we can auto-instrument your application without changing the application code.
