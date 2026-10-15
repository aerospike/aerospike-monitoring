# Which dashboard to open

Not sure where to look? Start with **Cluster Overview**, then follow
the section below that matches your question. The same guidance can
be set up as a launchpad in Dynatrace (the Launchpads app), linking
each dashboard once uploaded.

## Is the cluster healthy?

Start here: a first look, then narrow down to a node or a namespace.

- **Cluster Overview** (Aerospike - Cluster Overview.json): The first stop. Nodes, roster, memory, CPU, network, and read/write TPS for the whole cluster.
- **Node Overview** (Aerospike - Node Overview.json): One node looks different from the others: its uptime, connections, resources and errors, side by side.
- **Namespace View** (Aerospike - Namespace View.json): One namespace in detail: throughput by type, objects, storage, defrag, migrations, indexes.

## Why is it slow?

Latency, throughput and the host underneath.

- **Node & Host view** (Aerospike - Node & Host view.json): Aerospike latency, throughput and migrations next to the host's CPU, memory, disk and network, per node.
- **Host View** (Aerospike - Host View.json): The operating system alone: CPU, memory, disk I/O and network per host.
- **Batch Transactions View** (Aerospike - Batch Transactions View.json): Batch reads, writes, deletes and UDFs, direct and proxied: when the application uses batches.
- **Latency View** (Aerospike - Latency View.json): Latency percentiles. Not available in Dynatrace yet: each tile shows the equivalent Prometheus query.

## Replication between sites (XDR)

Is data reaching the other datacenter, and how do the sites compare?

- **XDR View** (Aerospike - XDR View.json): Per destination: lag, throughput, retries, errors. Open it when lag grows or a site falls behind.
- **Datacenter Comparison** (Aerospike - Datacenter Comparison.json): Two clusters side by side -- resources, throughput, objects per namespace -- to spot drift between sites.
- **Multi Cluster View** (Aerospike - Multi Cluster View.json): All clusters on one page: latency and XDR lag (the map and topology panels are notes for now).

## Data, capacity and indexes

How much is stored, where, and what is it costing?

- **Set Dashboard** (Aerospike - Set Dashboard.json): Objects, data used and indexes per set: which sets grow.
- **Unique Data Usage** (Aerospike - Unique Data Usage.json): Unique data size per namespace.
- **Secondary Index Summary** (Aerospike - Secondary Index Summary.json): All secondary indexes of a namespace: entries, memory, garbage collection, queries.
- **Secondary Index View** (Aerospike - Secondary Index View.json): One secondary index in detail: entries, memory, garbage collection, load time.
- **LRU Cache View** (Aerospike - LRU Cache View.json): For namespaces used as a cache: touches, throughput, objects and expirations.
- **All Flash** (Aerospike - All Flash.json): For namespaces with the primary index on flash: index, data and OS resources.

## Changes and operations

During maintenance, and for specific features.

- **Rolling Restarts** (Aerospike - Rolling Restarts.json): Watch this while restarting or upgrading nodes one by one: errors, migrations, resources.
- **MRT View** (Aerospike - MRT View.json): Multi-record transactions: commits, rollbacks, errors and timeouts, the monitor set.
- **Users View** (Aerospike - Users View.json): Per-user connections, TPS and quotas. Empty unless security is enabled with users configured.
- **Alerts View** (Aerospike - Alerts View.json): Alerts by severity. Not available in Dynatrace yet: the alerts are Prometheus rules, not Dynatrace ones.
