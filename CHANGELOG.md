# Changelog

This file documents all notable changes to Aerospike Monitoring Stack


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
