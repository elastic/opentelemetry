---
title: Elastic Cloud Serverless
layout: default
nav_order: 2
parent: Quickstart
---

# Quickstart on Elastic Cloud Serverless

## Retrieving Connection Details for your Serverless Project

1. **Retrieve the endpoint URL** for your Serverless project

    1. Go to the [Elastic Cloud console](https://cloud.elastic.co/){:target="_blank"}.
    2. Next to your *project*, select `Manage`.
    3. Next to Connection Details, select `View`.
    4. Copy the APM endpoint.
    5. Replace `.apm.` with `.ingest.` in the URL
        <pre><code>
            https://my-prj-a1b2c3<b>.apm.</b>eu-west-1.aws.elastic.cloud
        --> https://my-prj-a1b2c3<b>.ingest.</b>eu-west-1.aws.elastic.cloud
        </code></pre>

2. **Create an API key** 

    Create an API Key following [these instructions](https://www.elastic.co/guide/en/kibana/current/api-keys.html){:target="_blank"}.