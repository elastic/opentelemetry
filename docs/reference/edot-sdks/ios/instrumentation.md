---
navigation_title: Instrumentations
description: Learn about the various instrumentation provided by the Elastic Distribution of OpenTelemetry iOS (EDOT iOS).
applies_to:
  stack:
  serverless:
    observability:
  product:
    edot_ios: ga
products:
  - id: cloud-serverless
  - id: observability
  - id: edot-sdk
mapped_pages:
  - https://www.elastic.co/guide/en/apm/agent/swift/current/Instrumentation.html
---

# EDOT iOS instrumentations [Instrumentation]

The following list describes the various instrumentation provided with the Elastic Distribution of OpenTelemetry iOS (EDOT iOS). These instrumentations can be configured as described in [instrumentation configuration](configuration.md#instrumentationConfiguration).

## Crash reporting [crash-reporting]

The SDK will automatically capture and upload crashes to the APM server. These crashes are stored in the format as described in the [mobile SDK event spec](https://github.com/elastic/apm/blob/main/specs/agents/mobile/events.md#crashes).

## URLSession instrumentation [urlsession-instrumentation]

URLSession instrumentation is provided by the OpenTelemetry Swift SDK, and automatically generates traces for all network requests generated with URLSessions. Refer to [URL Session instrumentation Open Telemetry documentation](https://github.com/open-telemetry/opentelemetry-swift/tree/main/Sources/Instrumentation/URLSession).

## View instrumentation [view-instrumentation]

The SDK provides `SwiftUI.View` and `UIViewController` instrumentation, where the load time of a View is measured using spans. All Views simultaneously loaded will be grouped under the same starting span. The spans' names will be dictated by the following rules, from least to highest precedence:

1. `<view's class name> - view appearing`
2. `<navigation title> - view appearing`
3. The `name` passed to View extension method  `reportName(_ name: String) -> View`

The View’s class name will be a swift name-mangled string, and is the least desirable naming method. If it’s possible, set a navigation title on your views:

`AllProductsList.swift`

```swift
struct AllProductsList: View {
    @EnvironmentObject var modelData : ModelData

    var body: some View {
        VStack {
            List(modelData.products, id: \.id) { product in
                AdminProductRow(product: product)

            }
        }.onAppear  {
            modelData.loadProducts()
        }.navigationTitle("All Products")
    }
}
```

The `All Products - view appearing` will show up in Kibana.

If it isn’t possible to set a navigation title, use `reportName(_ name: String) -> View` to set the name that will show in Kibana:

`AllProductsList.swift`

```swift
struct AllProductsList: View {
    @EnvironmentObject var modelData : ModelData

    var body: some View {
        VStack {
            List(modelData.products, id: \.id) { product in
                AdminProductRow(product: product)

            }
        }.onAppear  {
            modelData.loadProducts()
        }.reportName("All Products - view appearing")
    }
}
```

::::{note}
You must insert the entire string `All Products - view appearing` to match the default formatting used for the other two naming options.
::::

## System metrics [system-metrics]

System-metric instrumentation records CPU and memory usage minutely as metrics. CPU metrics are recorded as `system.cpu.usage` and memory usage is recorded as `system.memory.usage`.

## MetricKit instrumentation [metrickit-instrumentation]

Available for iOS 13 and higher, the SDK provides instrumentation of key MetricKit data points:

* Application Launch times
* Application responsiveness
* Application exit counts

Find technical details on the metric generated in the [Mobile spec](https://github.com/elastic/apm/blob/main/specs/agents/mobile/metrics.md#application-metrics)

### `application.launch.time` [app-launch-time]

This histogram metric provides launch duration broken down by `first draw`, `first draw (optimized)`, and `resumed`. Find more details about the MetricKit data point in the [Apple documentation](https://developer.apple.com/documentation/metrickit/mxapplaunchmetric).


### `application.responsiveness.hangtime` [hangtime]

A histogram of the different durations of time in which the app is too busy to handle user interaction responsively. Find more details about the MetricKit data point in the [Apple documentation](https://developer.apple.com/documentation/metrickit/mxappresponsivenessmetric).


### `application.exits` [exits]

A count of application exits categorized by various attributes: `foreground` or `background`, and `normal` or abnormal, where abnormal exits are further subdivided. Find more details about the MetricKit data point in the [Apple documentation](https://developer.apple.com/documentation/metrickit/mxappexitmetric).


## Application lifecycle events [app-lifecycle-events]

In v0.5.0 the application lifecycle events are automatically instrumented. Find the technical details in the [Mobile spec](https://github.com/elastic/apm/blob/main/specs/agents/mobile/events.md#application-lifecycle-events).

