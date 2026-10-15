# Aerospike dashboards for Dynatrace

Twenty Dynatrace dashboards for monitoring Aerospike clusters, from the
metrics of the Aerospike Prometheus exporter: the dashboards of the
Aerospike Monitoring Stack, built for Dynatrace, with a launchpad that says
which one to open when.

This guide covers what has to be in place first, how to install the
dashboards (with the installer or by hand), and what to expect from them.

## What is here

One JSON file per dashboard. Dynatrace names each dashboard after its file:

| Group     | Dashboards                                                                                                                                                                   |
| --------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Core      | Alerts View, Cluster Overview, Latency View, Multi Cluster View, Namespace View, Node Overview, Secondary Index View, Set Dashboard, Unique Data Usage, Users View, XDR View |
| Use cases | All Flash, Batch Transactions View, Datacenter Comparison, LRU Cache View, MRT View, Node & Host view, Rolling Restarts, Secondary Index Summary                             |
| Host      | Host View                                                                                                                                                                    |

**Which one to open, and when:** `WHICH-DASHBOARD.md`, next to this guide,
groups them by the question each answers. The installer (Step 2) puts the
same guidance in Dynatrace as a launchpad.

## Before you start

### 1. A Dynatrace environment with the Dashboards app

The dashboards are for the **Dashboards** app and query metrics with DQL
(Grail). They do not work in Dashboards Classic.

### 2. Permissions

The person uploading needs permission to **create dashboards** and to
**read metrics** in the environment. If either is missing, ask your
Dynatrace administrator before going further.

### 3. Aerospike metrics in Dynatrace, in this shape

The dashboards read the metrics of the **Aerospike Prometheus Exporter**
(on each Aerospike node, port 9145), and the Host View also reads the
**Prometheus Node Exporter** (port 9100), shipped to Dynatrace by an
**OpenTelemetry Collector** (the contrib distribution) over OTLP. Metric
names stay as the exporters publish them (`aerospike_namespace_objects`...),
and the exporters' labels (`cluster_name`, `service`, `ns`, `set`, `dc`...)
become the attributes the dashboards filter on.

A minimal collector configuration. The lines marked `CHANGE` are the ones
to set for your own installation; the rest can stay as they are.

<!-- prettier-ignore -->
```yaml
receivers:
  prometheus:
    config:
      scrape_configs:
        - job_name: aerospike
          scrape_interval: 30s
          static_configs:
            # CHANGE: every Aerospike node's address, with the Aerospike
            # Prometheus Exporter's port (9145 unless you changed it). The
            # collector must be able to reach each one.
            - targets: ["10.0.0.11:9145", "10.0.0.12:9145", "10.0.0.13:9145"]
        - job_name: node # only for the Host View; remove if not needed
          scrape_interval: 30s
          static_configs:
            # CHANGE: the same nodes, with the Node Exporter's port (9100
            # unless you changed it).
            - targets: ["10.0.0.11:9100", "10.0.0.12:9100", "10.0.0.13:9100"]
              # CHANGE: the cluster's name exactly as Aerospike reports it
              # (cluster-name in aerospike.conf). For several clusters, add
              # one static_configs entry per cluster, each with its nodes.
              labels: { cluster_name: "<the Aerospike cluster's name>" }

processors:
  # Values the exporter types as counters but that are states (roster sizes,
  # log levels, client user agents, file sizes): make them gauges, or as
  # deltas they arrive as 0.
  transform/states:
    error_mode: ignore
    metric_statements:
      - context: metric
        statements:
          - convert_sum_to_gauge() where IsMatch(name, "^aerospike_.*_pseudo_.*|^aerospike_node_stats_user_agent_details$|^aerospike_namespace_storage_engine_filesize$")
  # Dynatrace takes counters as deltas; Prometheus counters are cumulative.
  cumulativetodelta: {}
  batch: {}

exporters:
  otlphttp/dynatrace:
    # CHANGE: your environment's id (the first part of its address, for
    # example abc12345). Note live.dynatrace.com, not apps.dynatrace.com.
    endpoint: "https://<environment-id>.live.dynatrace.com/api/v2/otlp"
    headers:
      # CHANGE: the scheme matching your token, and set the DT_API_TOKEN
      # environment variable for the collector (keep the token out of
      # this file):
      #   an access token with metrics.ingest: "Api-Token <token>"
      #   a platform token with openpipeline:metrics:ingest: "Bearer <token>"
      Authorization: "Api-Token ${env:DT_API_TOKEN}"
    compression: gzip

service:
  pipelines:
    metrics:
      receivers: [prometheus]
      processors: [transform/states, cumulativetodelta, batch]
      exporters: [otlphttp/dynatrace]
```

Three things matter for the dashboards:

- **`cumulativetodelta` must be there.** Without it Dynatrace rejects the
  counters, and every rate on the dashboards stays empty.
- **So must `transform/states`, before it.** Without it the roster, log
  level, client user agent and file size tiles show 0.
- **The Node Exporter targets need the `cluster_name` label**, the same name
  the Aerospike exporter reports, so the Host View can filter by cluster.

Metrics collected another way -- Dynatrace's own Prometheus integration or
OneAgent scraping, for instance -- may arrive under other names, and the
dashboards will not find them.

## Step 1: check that the metrics are there

1. In Dynatrace, open **Notebooks** and add a new notebook (it doesn't need
   saving).
2. Add a DQL section and run:

    ```text
    timeseries v = avg(aerospike_node_stats_uptime), by: { cluster_name, service }
    ```

3. You should get one row per Aerospike node, each named by `service`
   (its address and port), with its cluster in `cluster_name`.

If nothing comes back, stop here: the dashboards will be empty too. Check
the collector's log for export errors, and that its endpoint is the
environment's `live.dynatrace.com` address (not the `apps.dynatrace.com` one
in the browser's address bar). If Dynatrace shows a message about missing
permissions, see "Permissions" above.

## Step 2: install the dashboards

Work from the folder holding these files (unzip them first if they came
as a zip). Then either run the installer (recommended), or upload the
files by hand.

### With the installer

`install.py` walks through everything: it explains how to create the access
token, checks that the metrics are there and that Dynatrace accepts every
query, installs the dashboards shared read-only with everyone in the
environment, creates the launchpad **Aerospike: start here** (which
dashboard to open for which question, linking each), and can make that
launchpad the home page of the user groups you name. It needs Python 3.9
or later and nothing else.

```bash
python3 install.py --dry-run   # checks everything, changes nothing
python3 install.py             # installs
```

It asks for the environment's address and a **platform token** (Account
Management > Identity & access management > Platform tokens), listing the
scopes to give it. The token is used for that run only and not saved.
Re-running it updates the same dashboards and launchpad in place, which is
also how to install a newer version.

At the end it prints the launchpad's link: share that with your users.
Each person who wants it one click away pins it to the Dock (the bar on
the left) from the launchpad's menu; Dynatrace keeps pins per user.

### By hand

For each JSON file:

1. Open the **Dashboards** app.
2. Select **Upload** (on the Dashboards page, at the upper left, or in the
   side panel).
3. Pick the file and open it.

The dashboard opens, named after the file (for example "Aerospike - Cluster
Overview"), and appears under the recently modified dashboards. Repeat for
the other files; upload only the ones you need, if you prefer -- each stands
alone.

Uploading the same file twice makes a second copy rather than replacing the
first.

## Step 3: use them

- **Start from the launchpad** if you used the installer, or from
  `WHICH-DASHBOARD.md`: both say which dashboard answers which question.
- **Pick at the top.** Each dashboard has filters -- cluster, node,
  namespace, and on some set, secondary index, XDR datacenter or user. Node
  and namespace start with everything selected.
- **Set the timeframe** with the time picker, as on any dashboard.
- **Where a tile comes from:** each tile's description shows the equivalent
  Prometheus query, for comparison or troubleshooting.

## What to expect

- **Most panels are charts; some are notes.** About one panel in nine is
  not available in Dynatrace yet and shows a note with the equivalent
  Prometheus query: latency percentiles computed from histograms, panels that join differently grouped series,
  and the whole Alerts View (the alerts are Prometheus rules, not part of
  these dashboards).
- **Some values are computed slightly differently.** "Top 10" tiles rank
  over the whole timeframe rather than at each point in time, and a few
  ratios are computed from sums rather than per node. Rates are averaged
  over each interval, where the Prometheus queries some panels started from
  take the instantaneous rate (`irate`), so low, bursty rates such as disk
  I/O look smoother. Single values show the last complete interval. A tile's
  description shows the equivalent Prometheus query.
- **Units are not set.** Byte, percentage and per-second values show as plain
  numbers for now.
- **Empty tiles are normal** for features a cluster doesn't use -- XDR,
  secondary indexes, sets, users, or storage types it isn't configured with.
  The dashboards also keep panels for metric names older Aerospike versions
  used, which stay empty on current versions.

## Updating to a newer version

With the installer, run the newer version's `install.py`: it updates the
dashboards and the launchpad in place, links unchanged. By hand, delete the
dashboards uploaded before (or keep them under another name), then upload
the new files. Either way, changes made to the dashboards in the Dashboards
app are not carried into a new version.
