---
navigation_title: Manual Instrumentation
description: Manually instrumenting Python applications with EDOT Python.
applies_to:
  stack:
  serverless:
    observability:
products:
  - id: cloud-serverless
  - id: observability
  - id: edot-python
---

# Manual instrumentation

This guide shows you how to use the Elastic Distribution of OpenTelemetry Python (EDOT Python) to manually instrument your Python application and send OpenTelemetry data to an Elastic Observability deployment.

This guide requires to have already added auto-instrumentation with OpenTelemetry to your application per [Setup](./index.md).

**New to OpenTelemetry?** If your are new to OpenTelemetry we encourage you to take a look at our [Setup documentation](./index.md) instead, which will introduce you to auto-instrumentation.

### Configure EDOT Python

Refer to our [Setup](./index.md#configure-edot-python) page for more details.

### Manually instrument your auto instrumented Python application

In this section we'll show how to add manual instrumentation to an already automatically instrumented application. A use case for
this setup would be to trace something in particular while keeping the benefits of the simplicity of the automatic instrumentation doing
the hard work for us.

As an example we'll use an application using the Flask framework that implements an endpoint mounted on `/hello` returning a friendly
salute. This application is saved in a file named `app.py` that is the default module for Flask applications.

```
import random

from flask import Flask
from opentelemetry import trace

tracer = trace.get_tracer(__name__)

app = Flask(__name__)

@app.route("/hello")
def hello():
    choices = ["there", "world", "folks", "hello"]
    # create a span for the choice of the name, this may be a costly call in your real world application
    with tracer.start_as_current_span("choice") as span:
        choice = random.choice(choices)
        span.set_attribute("choice.value", choice)
    return f"Hello {choice}!"
```


We need to make sure to have Flask and the Flask OpenTelemetry instrumentation installed:

```bash
pip install flask
edot-bootstrap --action=install
```

And then we can run this application with the following command:

```bash
opentelemetry-instrument flask run
```

We may not only need to add a custom span to our application but also want to use a custom metric, like in the example below where we
are tracking how many times we are getting one of the possible choices for our salutes.

```
import random

from flask import Flask
from opentelemetry import metrics, trace

tracer = trace.get_tracer(__name__)
meter = metrics.get_meter(__name__)

hello_counter = meter.create_counter(
    "hello.choice",
    description="The number of times a salute is chosen",
)

app = Flask(__name__)

@app.route("/hello")
def hello():
    choices = ["there", "world", "folks", "hello"]
    # create a span for the choice of the name, this may be a costly call in your real world application
    with tracer.start_as_current_span("choice") as span:
        choice = random.choice(choices)
        span.set_attribute("choice.value", choice)
    hello_counter.add(1, {"choice.value": choice})
    return f"Hello {choice}!"
```

## Confirm that EDOT Python is working

To confirm that EDOT Python has successfully connected to Elastic:

1. Go to **Observability** → **Applications** → **Service Inventory**
1. You should see the name of the service to which you just added EDOT Python. It can take several minutes after initializing EDOT Python for the service to show up in this list.
1. Click on the name in the list to see trace data.

:::{note}
There may be no trace data to visualize unless you have _used_ your application since initializing EDOT Python.
:::
