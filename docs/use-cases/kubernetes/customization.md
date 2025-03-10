---
title: Customization
layout: default
nav_order: 6
parent: Monitoring on Kubernetes
grand_parent: Use Cases
---

# Customizing configuration

To customize the installation parameters, change the configuration values provided in `values.yaml` file, or override them using `--set parameter=value` during the installation.

To update an installed release, run a `helm upgrade` with the updated `values.yaml` file. Depending on the changes, some Pods may need to be restarted for the updates to take effect. Refer to [upgrades](./upgrade) for a command example.

## Configurable parameters

The following table lists common parameters that might be relevant for your use case:

| `values.yaml` parameter          |     Description      |
|----------------------------------|----------------------|
| `clusterName`                    | Sets the `k8s.cluster.name` field in all collected data. The cluster name is automatically detected for `EKS/GKE/AKS` clusters, but it might be useful for other environments. When monitoring multiple Kubernetes clusters, ensure that the cluster name is properly set in all your environments.<br><br>Refer to the [resourcedetection processor](https://github.com/open-telemetry/opentelemetry-collector-contrib/blob/main/processor/resourcedetectionprocessor/README.md#cluster-name) for more details about cluster name detection. |
| `collectors.cluster.resources`   | Configures `CPU` and `memory` `requests` and `limits` applied to the `Deployment` EDOT Collector responsible for cluster-level metrics.<br>This setting follows the standard [Kubernetes resources syntax](https://kubernetes.io/docs/concepts/configuration/manage-resources-containers/#requests-and-limits) for specifying requests and limits. |
| `collectors.daemon.resources`    | Configures `CPU` and `memory` `requests` and `limits` applied to the `DaemonSet` EDOT Collector responsible for node-level metrics and application traces.<br>This setting follows the standard [Kubernetes resources syntax](https://kubernetes.io/docs/concepts/configuration/manage-resources-containers/#requests-and-limits) for specifying requests and limits. |
| `certManager.enabled`    | Defaults to `false`.<br>Refer to [cert-manager integrated installation](#cert-manager-integrated-installation) for more details. |

For more information on all available parameters and their meaning, refer to:
* The provided `values.yaml`, which includes the default settings for the EDOT installation.
* The official OpenTelemetry `kube-stack` Helm chart [values file](https://raw.githubusercontent.com/elastic/opentelemetry/refs/heads/{{ site.edot_versions.collector }}/resources/kubernetes/operator/helm/values.yaml), with explanations of all parameters.

## Cert-manager integrated installation

In Kubernetes, for the API server to communicate with the webhook component (created by the operator), the webhook requires a TLS certificate that the API server is configured to trust. The default provided configuration sets the Helm chart to auto generate the required certificate as a self-signed certificate with an expiration policy of 365 days. These certificates **won't be renewed** if the Helm chart's release is not manually updated. For production environments, we highly recommend using a certificate manager like [cert-manager](https://cert-manager.io/docs/installation/).

Integrating the operator with [cert-manager](https://cert-manager.io/) enables automatic generation and renewal of the TLS certificate. This section assumes that cert-manager and its CRDs are already installed in your Kubernetes environment. If that's not the case, refer to the [cert-manager installation guide](https://cert-manager.io/docs/installation/) before continuing.

Follow any of the following options to install the `opentelemetry-kube-stack` Helm chart integrated with `cert-manager`:

* Add `--set opentelemetry-operator.admissionWebhooks.certManager.enabled=true --set opentelemetry-operator.admissionWebhooks.autoGenerateCert=null` to the installation command. For example:

```bash
helm upgrade --install --namespace opentelemetry-operator-system opentelemetry-kube-stack open-telemetry/opentelemetry-kube-stack \
--values https://raw.githubusercontent.com/elastic/opentelemetry/refs/heads/{{ site.edot_versions.collector }}/resources/kubernetes/operator/helm/values.yaml --version 0.3.3 \
--set opentelemetry-operator.admissionWebhooks.certManager.enabled=true --set opentelemetry-operator.admissionWebhooks.autoGenerateCert=null
```

* Keep an updated copy of the `values.yaml` file by following these steps:

  1. **Update** the `values.yaml` file with the following changes:

      - **Enable cert-manager integration for admission webhooks.**

        ```yaml
        opentelemetry-operator:
          admissionWebhooks:
            certManager:
              enabled: true  # Change from `false` to `true`
        ```

      - **Remove the generation of a self-signed certificate.**

        ```yaml
        # Remove the following lines:
            autoGenerateCert:
              enabled: true
              recreate: true
        ```

  2. Run the installation (or upgrade) command pointing to the updated file. For example, assuming that the updated file has been saved as `values_cert-manager.yaml`:

    ```bash
    helm upgrade --install --namespace opentelemetry-operator-system opentelemetry-kube-stack open-telemetry/opentelemetry-kube-stack \
    --values ./resources/kubernetes/operator/helm/values_cert-manager.yaml --version 0.3.3
```
