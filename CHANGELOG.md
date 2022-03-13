# Changelog

This file documents all notable changes to Aerospike Monitoring Stack


## [v1.4.0](https://github.com/aerospike/aerospike-monitoring/releases/tag/v1.4.0)

### Features
- [TOOLS-1956] - Add `Jobs View` and `Secondary Index View` dashboards
  - [TOOLS-1946] - Add support for per-job scan and query statistics
  - [TOOLS-1947] - Add support for secondary index statistics


## [v1.3.2](https://github.com/aerospike/aerospike-monitoring/releases/tag/v1.3.2)

### Improvements
- [TOOLS-1785] - Added new metrics introduced in Aerospike 5.7


## [v1.3.1](https://github.com/aerospike/aerospike-monitoring/releases/tag/v1.3.1)

### Improvements
- Add `Exporters View` dashboard to track status of all Aerospike Prometheus Exporter targets

### Fixes
- [TOOLS-1721] - Fix incorrect status of the exporters and Aerospike nodes in `Node View` dashboard


## [v1.3.0](https://github.com/aerospike/aerospike-monitoring/releases/tag/v1.3.0)

### Features
- [PROD-1742] - Added support for user statistics (Users View dashboard)
  - Per-user statistics are available in Aerospike 5.6+.

### Improvements
- [PROD-1774] - Add new connections opened/closed statistics introduced in 5.6
    - `client_connections_opened`
    - `client_connections_closed`
    - `heartbeat_connections_opened`
    - `heartbeat_connections_closed`
    - `fabric_connections_opened`
    - `fabric_connections_closed`
- [PROD-1775] - Add new all flash statistics introduced in 5.6
    - `index_flash_alloc_bytes`
    - `index_flash_alloc_pct`
- Add other new metrics introduced in 5.6,
    - `memory_used_set_index_bytes`
    - `fail_client_lost_conflict`
    - `fail_xdr_lost_conflict`
    - `threads_joinable`
    - `threads_detached`
    - `threads_pool_total`
    - `threads_pool_active`

### Fixes
- Fixed 90th percentile latency computation in Latency View dashboard to not use `rate()`


## [v1.2.1](https://github.com/aerospike/aerospike-monitoring/releases/tag/v1.2.1)

### Improvements
- Added DC `nodes` metric to XDR dashboard


## [v1.2.0](https://github.com/aerospike/aerospike-monitoring/releases/tag/v1.2.0)

### Features
- [TOOLS-1589] - Migrate dashboards to Grafana 7.

### Improvements
- [TOOLS-1591] - Make datasource configurable through a dashboard variable (Thanks to @realmgic for the contribution).
- [TOOLS-1588] - Alert when 'close to' stop writes, when node is proxying and when XDR lag is above a threshold.
- [TOOLS-1590] - Add Prometheus' docker swarm service discovery config to the example.

### Fixes
- [TOOLS-1592] - Fix units for "Failure rate" panel in Namespace view.


## [v1.1.1](https://github.com/aerospike/aerospike-monitoring/releases/tag/v1.1.1)

### Improvements
- Use latency time unit in queries to support Aerospike's microsecond histograms.

  Add variable for latency time unit to `Latency View` and `Node Overview` dashboards.

### Fixes
- Refresh variables on time range change.


## [v1.1.0](https://github.com/aerospike/aerospike-monitoring/releases/tag/v1.1.0)

### Features
- Add description info to each dashboard panel.
- Add `clock_skew_stop_writes` to `Namespace View` and `Cluster View` dashboards.
- Add dashboard support for the new latency metrics change in [Aerospike Prometheus Exporter v1.1.0](https://github.com/aerospike/aerospike-prometheus-exporter/releases/tag/v1.1.0).
- Show Primary index usage for namespaces using `index-type` `flash` or `pmem`.

### Improvements
- Remove `aerospike_node_info` metric as per [Aerospike Prometheus Exporter v1.1.0](https://github.com/aerospike/aerospike-prometheus-exporter/releases/tag/v1.1.0).
- Increase default Grafana refresh rate to `1m`.

### Fixes
- Fix primary index usage panel to show values in `MiB`/`GiB`.


## [v1.0.0](https://github.com/aerospike/aerospike-monitoring/releases/tag/v1.0.0)

- Initial Release
