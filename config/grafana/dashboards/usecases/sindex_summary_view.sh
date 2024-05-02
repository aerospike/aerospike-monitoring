{
  "__requires": [
    {
      "type": "panel",
      "id": "bargauge",
      "name": "Bar gauge",
      "version": ""
    },
    {
      "type": "grafana",
      "id": "grafana",
      "name": "Grafana",
      "version": "9.3.2"
    },
    {
      "type": "datasource",
      "id": "prometheus",
      "name": "Prometheus",
      "version": "1.0.0"
    },
    {
      "type": "panel",
      "id": "stat",
      "name": "Stat",
      "version": ""
    },
    {
      "type": "panel",
      "id": "timeseries",
      "name": "Time series",
      "version": ""
    }
  ],
  "annotations": {
    "list": [
      {
        "builtIn": 1,
        "datasource": {
          "type": "grafana",
          "uid": "-- Grafana --"
        },
        "enable": true,
        "hide": true,
        "iconColor": "rgba(0, 211, 255, 1)",
        "name": "Annotations & Alerts",
        "target": {
          "limit": 100,
          "matchAny": false,
          "tags": [],
          "type": "dashboard"
        },
        "type": "dashboard"
      }
    ]
  },
  "description": "Secondary Index Summary dashboard provides information about overview of secondary index usage at namespace level.",
  "editable": true,
  "fiscalYearStartMonth": 0,
  "graphTooltip": 0,
  "id": null,
  "links": [],
  "liveNow": false,
  "panels": [
    {
      "collapsed": false,
      "gridPos": {
        "h": 1,
        "w": 24,
        "x": 0,
        "y": 0
      },
      "id": 59,
      "panels": [],
      "title": "Overview",
      "type": "row"
    },
    {
      "datasource": {
        "type": "prometheus",
        "uid": "${DS_AEROSPIKE_PROMETHEUS}"
      },
      "description": "Secondary index name",
      "fieldConfig": {
        "defaults": {
          "color": {
            "mode": "thresholds"
          },
          "mappings": [],
          "thresholds": {
            "mode": "absolute",
            "steps": [
              {
                "color": "green",
                "value": null
              }
            ]
          },
          "unit": "short"
        },
        "overrides": []
      },
      "gridPos": {
        "h": 4,
        "w": 8,
        "x": 0,
        "y": 1
      },
      "id": 104,
      "options": {
        "colorMode": "background",
        "graphMode": "none",
        "justifyMode": "center",
        "orientation": "auto",
        "reduceOptions": {
          "calcs": [
            "lastNotNull"
          ],
          "fields": "",
          "values": false
        },
        "showPercentChange": false,
        "textMode": "value",
        "wideLayout": true
      },
      "pluginVersion": "9.3.2",
      "targets": [
        {
          "datasource": {
            "type": "prometheus",
            "uid": "${DS_AEROSPIKE_PROMETHEUS}"
          },
          "editorMode": "code",
          "expr": "count (aerospike_sindex_entries{job=\"$job_name\", cluster_name=~\"$cluster\"})",
          "instant": false,
          "legendFormat": "{{sindex}}",
          "range": true,
          "refId": "A"
        }
      ],
      "title": "Sindex Count (total)",
      "type": "stat"
    },
    {
      "datasource": {
        "type": "prometheus",
        "uid": "${DS_AEROSPIKE_PROMETHEUS}"
      },
      "description": "Memory usage of secondary indexes",
      "fieldConfig": {
        "defaults": {
          "color": {
            "mode": "thresholds"
          },
          "mappings": [],
          "thresholds": {
            "mode": "absolute",
            "steps": [
              {
                "color": "green",
                "value": null
              }
            ]
          },
          "unit": "bytes"
        },
        "overrides": []
      },
      "gridPos": {
        "h": 4,
        "w": 4,
        "x": 8,
        "y": 1
      },
      "id": 102,
      "options": {
        "colorMode": "background",
        "graphMode": "none",
        "justifyMode": "center",
        "orientation": "auto",
        "reduceOptions": {
          "calcs": [
            "lastNotNull"
          ],
          "fields": "",
          "values": false
        },
        "showPercentChange": false,
        "textMode": "value",
        "wideLayout": true
      },
      "pluginVersion": "9.3.2",
      "targets": [
        {
          "datasource": {
            "type": "prometheus",
            "uid": "${DS_AEROSPIKE_PROMETHEUS}"
          },
          "editorMode": "code",
          "expr": "sum (aerospike_sindex_used_bytes{job=\"$job_name\", cluster_name=~\"$cluster\"})",
          "instant": false,
          "legendFormat": "{{sindex}}",
          "range": true,
          "refId": "A"
        }
      ],
      "title": "Memory Used (total) (bytes)",
      "type": "stat"
    },
    {
      "datasource": {
        "type": "prometheus",
        "uid": "${DS_AEROSPIKE_PROMETHEUS}"
      },
      "description": "Total bytes in-use on the mount(s) for the secondary indexes used by this namespace on this node.",
      "fieldConfig": {
        "defaults": {
          "color": {
            "mode": "thresholds"
          },
          "mappings": [],
          "thresholds": {
            "mode": "absolute",
            "steps": [
              {
                "color": "green",
                "value": null
              }
            ]
          },
          "unit": "bytes"
        },
        "overrides": []
      },
      "gridPos": {
        "h": 4,
        "w": 4,
        "x": 12,
        "y": 1
      },
      "id": 103,
      "options": {
        "colorMode": "background",
        "graphMode": "none",
        "justifyMode": "center",
        "orientation": "auto",
        "reduceOptions": {
          "calcs": [
            "lastNotNull"
          ],
          "fields": "",
          "values": false
        },
        "showPercentChange": false,
        "textMode": "value",
        "wideLayout": true
      },
      "pluginVersion": "9.3.2",
      "targets": [
        {
          "datasource": {
            "type": "prometheus",
            "uid": "${DS_AEROSPIKE_PROMETHEUS}"
          },
          "editorMode": "code",
          "expr": "sum (aerospike_namespace_sindex_used_bytes{job=\"$job_name\", cluster_name=~\"$cluster\"})",
          "instant": false,
          "legendFormat": "__auto",
          "range": true,
          "refId": "A"
        }
      ],
      "title": "Used (total) (bytes)",
      "type": "stat"
    },
    {
      "datasource": {
        "type": "prometheus",
        "uid": "${DS_AEROSPIKE_PROMETHEUS}"
      },
      "description": "Size of the stage for sindex processing within a namespace",
      "fieldConfig": {
        "defaults": {
          "color": {
            "mode": "thresholds"
          },
          "mappings": [],
          "thresholds": {
            "mode": "absolute",
            "steps": [
              {
                "color": "green",
                "value": null
              }
            ]
          },
          "unit": "bytes"
        },
        "overrides": []
      },
      "gridPos": {
        "h": 4,
        "w": 4,
        "x": 16,
        "y": 1
      },
      "id": 90,
      "options": {
        "colorMode": "background",
        "graphMode": "none",
        "justifyMode": "center",
        "orientation": "auto",
        "reduceOptions": {
          "calcs": [
            "lastNotNull"
          ],
          "fields": "",
          "values": false
        },
        "showPercentChange": false,
        "textMode": "value",
        "wideLayout": true
      },
      "pluginVersion": "9.3.2",
      "targets": [
        {
          "datasource": {
            "type": "prometheus",
            "uid": "${DS_AEROSPIKE_PROMETHEUS}"
          },
          "editorMode": "code",
          "expr": "sum (aerospike_namespace_sindex_stage_size{job=\"$job_name\", cluster_name=~\"$cluster\"})",
          "instant": false,
          "legendFormat": "{{service}}",
          "range": true,
          "refId": "A"
        }
      ],
      "title": "Stage Size (total) (bytes)",
      "type": "stat"
    },
    {
      "datasource": {
        "type": "prometheus",
        "uid": "${DS_AEROSPIKE_PROMETHEUS}"
      },
      "description": "Number of secondary index entries cleaned by sindex GC.",
      "fieldConfig": {
        "defaults": {
          "color": {
            "mode": "thresholds"
          },
          "mappings": [],
          "thresholds": {
            "mode": "absolute",
            "steps": [
              {
                "color": "green",
                "value": null
              }
            ]
          },
          "unit": "none"
        },
        "overrides": []
      },
      "gridPos": {
        "h": 4,
        "w": 4,
        "x": 20,
        "y": 1
      },
      "id": 92,
      "options": {
        "colorMode": "background",
        "graphMode": "none",
        "justifyMode": "center",
        "orientation": "auto",
        "reduceOptions": {
          "calcs": [
            "lastNotNull"
          ],
          "fields": "",
          "values": false
        },
        "showPercentChange": false,
        "textMode": "value",
        "wideLayout": true
      },
      "pluginVersion": "9.3.2",
      "targets": [
        {
          "datasource": {
            "type": "prometheus",
            "uid": "${DS_AEROSPIKE_PROMETHEUS}"
          },
          "editorMode": "code",
          "expr": "sum (rate(aerospike_namespace_sindex_gc_cleaned{job=\"$job_name\", cluster_name=~\"$cluster\"}[$__rate_interval]))",
          "instant": false,
          "legendFormat": "{{service}}",
          "range": true,
          "refId": "A"
        }
      ],
      "title": "Entries Cleaned (total)  (rate)",
      "type": "stat"
    },
    {
      "datasource": {
        "type": "prometheus",
        "uid": "${DS_AEROSPIKE_PROMETHEUS}"
      },
      "description": "Number of secondary index query aggregations completed/aborted/errors",
      "fieldConfig": {
        "defaults": {
          "color": {
            "fixedColor": "green",
            "mode": "palette-classic"
          },
          "mappings": [],
          "thresholds": {
            "mode": "absolute",
            "steps": [
              {
                "color": "green",
                "value": null
              }
            ]
          },
          "unit": "none"
        },
        "overrides": []
      },
      "gridPos": {
        "h": 4,
        "w": 8,
        "x": 0,
        "y": 5
      },
      "id": 87,
      "options": {
        "colorMode": "background",
        "graphMode": "none",
        "justifyMode": "center",
        "orientation": "auto",
        "reduceOptions": {
          "calcs": [
            "lastNotNull"
          ],
          "fields": "",
          "values": false
        },
        "showPercentChange": false,
        "textMode": "value_and_name",
        "wideLayout": true
      },
      "pluginVersion": "9.3.2",
      "targets": [
        {
          "datasource": {
            "type": "prometheus",
            "uid": "${DS_AEROSPIKE_PROMETHEUS}"
          },
          "disableTextWrap": false,
          "editorMode": "code",
          "expr": "sum (rate(aerospike_namespace_si_query_aggr_complete{job=\"$job_name\", cluster_name=~\"$cluster\"}[$__rate_interval]))",
          "fullMetaSearch": false,
          "includeNullMetadata": true,
          "instant": false,
          "legendFormat": "Completed",
          "range": true,
          "refId": "Completed",
          "useBackend": false
        },
        {
          "datasource": {
            "type": "prometheus",
            "uid": "${DS_AEROSPIKE_PROMETHEUS}"
          },
          "editorMode": "code",
          "expr": "sum (rate(aerospike_namespace_si_query_aggr_abort{job=\"$job_name\", cluster_name=~\"$cluster\"}[$__rate_interval]))",
          "hide": false,
          "instant": false,
          "legendFormat": "Aborted",
          "range": true,
          "refId": "Aborted"
        },
        {
          "datasource": {
            "type": "prometheus",
            "uid": "${DS_AEROSPIKE_PROMETHEUS}"
          },
          "editorMode": "code",
          "expr": "sum (rate(aerospike_namespace_si_query_aggr_error{job=\"$job_name\", cluster_name=~\"$cluster\"}[$__rate_interval]))",
          "hide": false,
          "instant": false,
          "legendFormat": "Errors",
          "range": true,
          "refId": "Errors"
        }
      ],
      "title": "Query Aggregations (total) (rate)",
      "type": "stat"
    },
    {
      "datasource": {
        "type": "prometheus",
        "uid": "${DS_AEROSPIKE_PROMETHEUS}"
      },
      "description": "Displays minimum, average and maximum of  memory used by sindex across all namespaces",
      "fieldConfig": {
        "defaults": {
          "color": {
            "fixedColor": "yellow",
            "mode": "fixed"
          },
          "mappings": [],
          "noValue": "No Data",
          "thresholds": {
            "mode": "absolute",
            "steps": [
              {
                "color": "green",
                "value": null
              }
            ]
          },
          "unit": "bytes"
        },
        "overrides": []
      },
      "gridPos": {
        "h": 4,
        "w": 4,
        "x": 8,
        "y": 5
      },
      "id": 108,
      "maxDataPoints": 100,
      "options": {
        "displayMode": "basic",
        "maxVizHeight": 300,
        "minVizHeight": 10,
        "minVizWidth": 0,
        "namePlacement": "auto",
        "orientation": "vertical",
        "reduceOptions": {
          "calcs": [
            "lastNotNull"
          ],
          "fields": "",
          "values": false
        },
        "showUnfilled": true,
        "sizing": "auto",
        "valueMode": "color"
      },
      "pluginVersion": "9.3.2",
      "targets": [
        {
          "datasource": {
            "type": "prometheus",
            "uid": "${DS_AEROSPIKE_PROMETHEUS}"
          },
          "editorMode": "code",
          "expr": "min (aerospike_sindex_used_bytes{job=\"$job_name\", cluster_name=~\"$cluster\"})",
          "hide": false,
          "legendFormat": "Min",
          "range": true,
          "refId": "min"
        },
        {
          "datasource": {
            "type": "prometheus",
            "uid": "${DS_AEROSPIKE_PROMETHEUS}"
          },
          "editorMode": "code",
          "expr": "avg (aerospike_sindex_used_bytes{job=\"$job_name\", cluster_name=~\"$cluster\"})",
          "hide": false,
          "legendFormat": "Avg",
          "range": true,
          "refId": "avg"
        },
        {
          "datasource": {
            "type": "prometheus",
            "uid": "${DS_AEROSPIKE_PROMETHEUS}"
          },
          "editorMode": "code",
          "expr": "max (aerospike_sindex_used_bytes{job=\"$job_name\", cluster_name=~\"$cluster\"})",
          "hide": false,
          "legendFormat": "Max",
          "range": true,
          "refId": "max"
        }
      ],
      "title": "Memory Used (bytes)",
      "transparent": true,
      "type": "bargauge"
    },
    {
      "datasource": {
        "type": "prometheus",
        "uid": "${DS_AEROSPIKE_PROMETHEUS}"
      },
      "description": "Displays minimum, average and maximum of  bytes in-use on the mount(s) for the secondary indexes used by this namespace on this node.",
      "fieldConfig": {
        "defaults": {
          "color": {
            "fixedColor": "yellow",
            "mode": "fixed"
          },
          "mappings": [],
          "noValue": "No Data",
          "thresholds": {
            "mode": "absolute",
            "steps": [
              {
                "color": "green",
                "value": null
              }
            ]
          },
          "unit": "bytes"
        },
        "overrides": []
      },
      "gridPos": {
        "h": 4,
        "w": 4,
        "x": 12,
        "y": 5
      },
      "id": 109,
      "maxDataPoints": 100,
      "options": {
        "displayMode": "basic",
        "maxVizHeight": 300,
        "minVizHeight": 10,
        "minVizWidth": 0,
        "namePlacement": "auto",
        "orientation": "vertical",
        "reduceOptions": {
          "calcs": [
            "lastNotNull"
          ],
          "fields": "",
          "values": false
        },
        "showUnfilled": true,
        "sizing": "auto",
        "valueMode": "color"
      },
      "pluginVersion": "9.3.2",
      "targets": [
        {
          "datasource": {
            "type": "prometheus",
            "uid": "${DS_AEROSPIKE_PROMETHEUS}"
          },
          "editorMode": "code",
          "expr": "min (aerospike_namespace_sindex_used_bytes{job=\"$job_name\", cluster_name=~\"$cluster\"})",
          "hide": false,
          "legendFormat": "Min",
          "range": true,
          "refId": "min"
        },
        {
          "datasource": {
            "type": "prometheus",
            "uid": "${DS_AEROSPIKE_PROMETHEUS}"
          },
          "editorMode": "code",
          "expr": "avg (aerospike_namespace_sindex_used_bytes{job=\"$job_name\", cluster_name=~\"$cluster\"})",
          "hide": false,
          "legendFormat": "Avg",
          "range": true,
          "refId": "avg"
        },
        {
          "datasource": {
            "type": "prometheus",
            "uid": "${DS_AEROSPIKE_PROMETHEUS}"
          },
          "editorMode": "code",
          "expr": "max (aerospike_namespace_sindex_used_bytes{job=\"$job_name\", cluster_name=~\"$cluster\"})",
          "hide": false,
          "legendFormat": "Max",
          "range": true,
          "refId": "max"
        }
      ],
      "title": "Used (bytes)",
      "transparent": true,
      "type": "bargauge"
    },
    {
      "datasource": {
        "type": "prometheus",
        "uid": "${DS_AEROSPIKE_PROMETHEUS}"
      },
      "description": "Number of udf background secondary index queries that were completed/sborted/errors",
      "fieldConfig": {
        "defaults": {
          "color": {
            "mode": "palette-classic"
          },
          "mappings": [],
          "thresholds": {
            "mode": "absolute",
            "steps": [
              {
                "color": "green",
                "value": null
              }
            ]
          }
        },
        "overrides": []
      },
      "gridPos": {
        "h": 4,
        "w": 8,
        "x": 16,
        "y": 5
      },
      "id": 95,
      "options": {
        "colorMode": "background",
        "graphMode": "none",
        "justifyMode": "center",
        "orientation": "auto",
        "reduceOptions": {
          "calcs": [
            "lastNotNull"
          ],
          "fields": "",
          "values": false
        },
        "showPercentChange": false,
        "textMode": "value_and_name",
        "wideLayout": true
      },
      "pluginVersion": "9.3.2",
      "targets": [
        {
          "datasource": {
            "type": "prometheus",
            "uid": "${DS_AEROSPIKE_PROMETHEUS}"
          },
          "editorMode": "code",
          "expr": "sum (rate(aerospike_namespace_si_query_udf_bg_complete{job=\"$job_name\", cluster_name=~\"$cluster\"}[$__rate_interval]))",
          "instant": false,
          "legendFormat": "Completed",
          "range": true,
          "refId": "Completed"
        },
        {
          "datasource": {
            "type": "prometheus",
            "uid": "${DS_AEROSPIKE_PROMETHEUS}"
          },
          "editorMode": "code",
          "expr": "sum (rate(aerospike_namespace_si_query_udf_bg_abort{job=\"$job_name\", cluster_name=~\"$cluster\"}[$__rate_interval]))",
          "hide": false,
          "instant": false,
          "legendFormat": "Aborted",
          "range": true,
          "refId": "Aborted"
        },
        {
          "datasource": {
            "type": "prometheus",
            "uid": "${DS_AEROSPIKE_PROMETHEUS}"
          },
          "editorMode": "code",
          "expr": "sum (rate(aerospike_namespace_si_query_udf_bg_error{job=\"$job_name\", cluster_name=~\"$cluster\"}[$__rate_interval]))",
          "hide": false,
          "instant": false,
          "legendFormat": "Errors",
          "range": true,
          "refId": "Errors"
        }
      ],
      "title": "UDF Queries (total) (rate)",
      "type": "stat"
    },
    {
      "datasource": {
        "type": "prometheus",
        "uid": "${DS_AEROSPIKE_PROMETHEUS}"
      },
      "description": "Number of basic queries  that have been completed/aborted/errors after exceeding a predefined timeout duration within a namespace in sindex queries",
      "fieldConfig": {
        "defaults": {
          "color": {
            "mode": "palette-classic"
          },
          "mappings": [],
          "thresholds": {
            "mode": "absolute",
            "steps": [
              {
                "color": "green",
                "value": null
              },
              {
                "color": "red",
                "value": 80
              }
            ]
          }
        },
        "overrides": []
      },
      "gridPos": {
        "h": 4,
        "w": 8,
        "x": 0,
        "y": 9
      },
      "id": 89,
      "options": {
        "colorMode": "background",
        "graphMode": "none",
        "justifyMode": "center",
        "orientation": "auto",
        "reduceOptions": {
          "calcs": [
            "lastNotNull"
          ],
          "fields": "",
          "values": false
        },
        "showPercentChange": false,
        "textMode": "value_and_name",
        "wideLayout": true
      },
      "pluginVersion": "9.3.2",
      "targets": [
        {
          "datasource": {
            "type": "prometheus",
            "uid": "${DS_AEROSPIKE_PROMETHEUS}"
          },
          "editorMode": "code",
          "expr": "sum (rate(aerospike_namespace_si_query_long_basic_complete{job=\"$job_name\", cluster_name=~\"$cluster\"}[$__rate_interval]))",
          "instant": false,
          "legendFormat": "Completed ",
          "range": true,
          "refId": "Completed"
        },
        {
          "datasource": {
            "type": "prometheus",
            "uid": "${DS_AEROSPIKE_PROMETHEUS}"
          },
          "editorMode": "code",
          "expr": "sum (rate(aerospike_namespace_si_query_long_basic_abort{job=\"$job_name\", cluster_name=~\"$cluster\"}[$__rate_interval]))",
          "hide": false,
          "instant": false,
          "legendFormat": "Aborted",
          "range": true,
          "refId": "Aborted"
        },
        {
          "datasource": {
            "type": "prometheus",
            "uid": "${DS_AEROSPIKE_PROMETHEUS}"
          },
          "editorMode": "code",
          "expr": "sum (rate(aerospike_namespace_si_query_long_basic_error{job=\"$job_name\", cluster_name=~\"$cluster\"}[$__rate_interval]))",
          "hide": false,
          "instant": false,
          "legendFormat": "Errors",
          "range": true,
          "refId": "Errors"
        }
      ],
      "title": "Long Queries (total) (rate)",
      "type": "stat"
    },
    {
      "datasource": {
        "type": "prometheus",
        "uid": "${DS_AEROSPIKE_PROMETHEUS}"
      },
      "description": "Number of basic queries completed/timedout/errors in sindex queries within a namespace within a predefined short duration",
      "fieldConfig": {
        "defaults": {
          "color": {
            "mode": "palette-classic"
          },
          "mappings": [],
          "thresholds": {
            "mode": "absolute",
            "steps": [
              {
                "color": "green",
                "value": null
              }
            ]
          },
          "unit": "none"
        },
        "overrides": []
      },
      "gridPos": {
        "h": 4,
        "w": 8,
        "x": 8,
        "y": 9
      },
      "id": 94,
      "options": {
        "colorMode": "background",
        "graphMode": "none",
        "justifyMode": "center",
        "orientation": "auto",
        "reduceOptions": {
          "calcs": [
            "lastNotNull"
          ],
          "fields": "",
          "values": false
        },
        "showPercentChange": false,
        "textMode": "value_and_name",
        "wideLayout": true
      },
      "pluginVersion": "9.3.2",
      "targets": [
        {
          "datasource": {
            "type": "prometheus",
            "uid": "${DS_AEROSPIKE_PROMETHEUS}"
          },
          "editorMode": "code",
          "expr": "sum (rate(aerospike_namespace_si_query_short_basic_complete{job=\"$job_name\", cluster_name=~\"$cluster\"}[$__rate_interval]))",
          "instant": false,
          "legendFormat": "Completed",
          "range": true,
          "refId": "Completed"
        },
        {
          "datasource": {
            "type": "prometheus",
            "uid": "${DS_AEROSPIKE_PROMETHEUS}"
          },
          "editorMode": "code",
          "expr": "sum (rate(aerospike_namespace_si_query_short_basic_timeout{job=\"$job_name\", cluster_name=~\"$cluster\"}[$__rate_interval]))",
          "hide": false,
          "instant": false,
          "legendFormat": "Timeout",
          "range": true,
          "refId": "Timeout"
        },
        {
          "datasource": {
            "type": "prometheus",
            "uid": "${DS_AEROSPIKE_PROMETHEUS}"
          },
          "editorMode": "code",
          "expr": "sum (rate(aerospike_namespace_si_query_short_basic_error{job=\"$job_name\", cluster_name=~\"$cluster\"}[$__rate_interval]))",
          "hide": false,
          "instant": false,
          "legendFormat": "Errors",
          "range": true,
          "refId": "Errors"
        }
      ],
      "title": "Short Queries (total) (rate)",
      "type": "stat"
    },
    {
      "datasource": {
        "type": "prometheus",
        "uid": "${DS_AEROSPIKE_PROMETHEUS}"
      },
      "description": "Number of ops background secondary index queries completed/aborted/errors",
      "fieldConfig": {
        "defaults": {
          "color": {
            "mode": "palette-classic"
          },
          "mappings": [],
          "thresholds": {
            "mode": "absolute",
            "steps": [
              {
                "color": "green",
                "value": null
              }
            ]
          },
          "unit": "none"
        },
        "overrides": []
      },
      "gridPos": {
        "h": 4,
        "w": 8,
        "x": 16,
        "y": 9
      },
      "id": 93,
      "options": {
        "colorMode": "background",
        "graphMode": "none",
        "justifyMode": "center",
        "orientation": "auto",
        "reduceOptions": {
          "calcs": [
            "lastNotNull"
          ],
          "fields": "",
          "values": false
        },
        "showPercentChange": false,
        "textMode": "value_and_name",
        "wideLayout": true
      },
      "pluginVersion": "9.3.2",
      "targets": [
        {
          "datasource": {
            "type": "prometheus",
            "uid": "${DS_AEROSPIKE_PROMETHEUS}"
          },
          "editorMode": "code",
          "expr": "sum  (rate(aerospike_namespace_si_query_ops_bg_complete{job=\"$job_name\", cluster_name=~\"$cluster\"}[$__rate_interval]))",
          "instant": false,
          "legendFormat": "Completed",
          "range": true,
          "refId": "Completed"
        },
        {
          "datasource": {
            "type": "prometheus",
            "uid": "${DS_AEROSPIKE_PROMETHEUS}"
          },
          "editorMode": "code",
          "expr": "sum (rate(aerospike_namespace_si_query_ops_bg_abort{job=\"$job_name\", cluster_name=~\"$cluster\"}[$__rate_interval]))",
          "hide": false,
          "instant": false,
          "legendFormat": "Aborted",
          "range": true,
          "refId": "Aborted"
        },
        {
          "datasource": {
            "type": "prometheus",
            "uid": "${DS_AEROSPIKE_PROMETHEUS}"
          },
          "editorMode": "code",
          "expr": "sum (rate(aerospike_namespace_si_query_ops_bg_error{job=\"$job_name\", cluster_name=~\"$cluster\"}[$__rate_interval]))",
          "hide": false,
          "instant": false,
          "legendFormat": "Errors",
          "range": true,
          "refId": "Errors"
        }
      ],
      "title": "Ops Background Queries (total) (rate)",
      "type": "stat"
    },
    {
      "collapsed": true,
      "gridPos": {
        "h": 1,
        "w": 24,
        "x": 0,
        "y": 13
      },
      "id": 3,
      "panels": [
        {
          "datasource": {
            "type": "prometheus",
            "uid": "${DS_AEROSPIKE_PROMETHEUS}"
          },
          "description": "Total, pmem and flash type secondary indexclount",
          "fieldConfig": {
            "defaults": {
              "color": {
                "mode": "thresholds"
              },
              "mappings": [],
              "thresholds": {
                "mode": "absolute",
                "steps": [
                  {
                    "color": "green",
                    "value": null
                  }
                ]
              },
              "unit": "short"
            },
            "overrides": []
          },
          "gridPos": {
            "h": 4,
            "w": 6,
            "x": 0,
            "y": 2
          },
          "id": 6,
          "options": {
            "colorMode": "background",
            "graphMode": "none",
            "justifyMode": "center",
            "orientation": "auto",
            "reduceOptions": {
              "calcs": [
                "lastNotNull"
              ],
              "fields": "",
              "values": false
            },
            "showPercentChange": false,
            "textMode": "value_and_name",
            "wideLayout": true
          },
          "pluginVersion": "9.3.2",
          "targets": [
            {
              "datasource": {
                "type": "prometheus",
                "uid": "${DS_AEROSPIKE_PROMETHEUS}"
              },
              "editorMode": "code",
              "expr": "count (aerospike_sindex_entries{job=\"$job_name\", cluster_name=~\"$cluster\", ns=~\"$namespace|$^\"})",
              "instant": false,
              "legendFormat": "Total",
              "range": true,
              "refId": "A"
            },
            {
              "datasource": {
                "type": "prometheus",
                "uid": "${DS_AEROSPIKE_PROMETHEUS}"
              },
              "disableTextWrap": false,
              "editorMode": "code",
              "expr": "count(aerospike_namespace_sindex_gc_cleaned{job=\"$job_name\", cluster_name=~\"$cluster\", ns=~\"$namespace|$^\", storage_engine=\"pmem\"})",
              "fullMetaSearch": false,
              "hide": false,
              "includeNullMetadata": false,
              "instant": false,
              "legendFormat": "PMem",
              "range": true,
              "refId": "pmem",
              "useBackend": false
            },
            {
              "datasource": {
                "type": "prometheus",
                "uid": "${DS_AEROSPIKE_PROMETHEUS}"
              },
              "editorMode": "code",
              "expr": "count (aerospike_namespace_sindex_gc_cleaned{job=\"$job_name\", cluster_name=~\"$cluster\", ns=~\"$namespace|$^\", storage_engine=\"flash\"})",
              "hide": false,
              "instant": false,
              "legendFormat": "Flash",
              "range": true,
              "refId": "flash"
            }
          ],
          "title": "Sindex Count",
          "type": "stat"
        },
        {
          "datasource": {
            "type": "prometheus",
            "uid": "${DS_AEROSPIKE_PROMETHEUS}"
          },
          "description": "Size of the stage for sindex processing within a namespace",
          "fieldConfig": {
            "defaults": {
              "color": {
                "mode": "palette-classic"
              },
              "mappings": [],
              "thresholds": {
                "mode": "absolute",
                "steps": [
                  {
                    "color": "green",
                    "value": null
                  }
                ]
              },
              "unit": "bytes"
            },
            "overrides": []
          },
          "gridPos": {
            "h": 4,
            "w": 3,
            "x": 6,
            "y": 2
          },
          "id": 15,
          "options": {
            "colorMode": "background",
            "graphMode": "none",
            "justifyMode": "center",
            "orientation": "auto",
            "reduceOptions": {
              "calcs": [
                "lastNotNull"
              ],
              "fields": "",
              "values": false
            },
            "showPercentChange": false,
            "textMode": "value",
            "wideLayout": true
          },
          "pluginVersion": "9.3.2",
          "targets": [
            {
              "datasource": {
                "type": "prometheus",
                "uid": "${DS_AEROSPIKE_PROMETHEUS}"
              },
              "editorMode": "code",
              "expr": "sum by (ns)(aerospike_namespace_sindex_stage_size{job=\"$job_name\", cluster_name=~\"$cluster\", ns=~\"$namespace|$^\"})",
              "instant": false,
              "legendFormat": "{{ns}}",
              "range": true,
              "refId": "A"
            }
          ],
          "title": "Stage Size (bytes)",
          "type": "stat"
        },
        {
          "datasource": {
            "type": "prometheus",
            "uid": "${DS_AEROSPIKE_PROMETHEUS}"
          },
          "description": "Memory usage of secondary indexes",
          "fieldConfig": {
            "defaults": {
              "color": {
                "mode": "thresholds"
              },
              "mappings": [],
              "thresholds": {
                "mode": "absolute",
                "steps": [
                  {
                    "color": "green",
                    "value": null
                  }
                ]
              },
              "unit": "bytes"
            },
            "overrides": []
          },
          "gridPos": {
            "h": 4,
            "w": 3,
            "x": 9,
            "y": 2
          },
          "id": 105,
          "options": {
            "colorMode": "background",
            "graphMode": "none",
            "justifyMode": "center",
            "orientation": "auto",
            "reduceOptions": {
              "calcs": [
                "lastNotNull"
              ],
              "fields": "",
              "values": false
            },
            "showPercentChange": false,
            "textMode": "value",
            "wideLayout": true
          },
          "pluginVersion": "9.3.2",
          "targets": [
            {
              "datasource": {
                "type": "prometheus",
                "uid": "${DS_AEROSPIKE_PROMETHEUS}"
              },
              "editorMode": "code",
              "expr": "sum by (ns)(aerospike_sindex_used_bytes{job=\"$job_name\", cluster_name=~\"$cluster\", ns=~\"$namespace|$^\"})",
              "instant": false,
              "legendFormat": "{{sindex}}",
              "range": true,
              "refId": "A"
            }
          ],
          "title": "Memory Used (bytes)",
          "type": "stat"
        },
        {
          "datasource": {
            "type": "prometheus",
            "uid": "${DS_AEROSPIKE_PROMETHEUS}"
          },
          "description": "Maximum mount budget allocated",
          "fieldConfig": {
            "defaults": {
              "color": {
                "mode": "thresholds"
              },
              "mappings": [],
              "thresholds": {
                "mode": "absolute",
                "steps": [
                  {
                    "color": "green",
                    "value": null
                  }
                ]
              },
              "unit": "bytes"
            },
            "overrides": []
          },
          "gridPos": {
            "h": 4,
            "w": 3,
            "x": 12,
            "y": 2
          },
          "id": 133,
          "options": {
            "colorMode": "background_solid",
            "graphMode": "none",
            "justifyMode": "center",
            "orientation": "auto",
            "reduceOptions": {
              "calcs": [
                "lastNotNull"
              ],
              "fields": "",
              "values": false
            },
            "showPercentChange": false,
            "textMode": "auto",
            "wideLayout": true
          },
          "pluginVersion": "9.3.2",
          "targets": [
            {
              "datasource": {
                "type": "prometheus",
                "uid": "${DS_AEROSPIKE_PROMETHEUS}"
              },
              "editorMode": "code",
              "expr": "aerospike_namespace_sindex_type_mounts_budget{job=\"$job_name\", cluster_name=~\"$cluster\", ns=~\"$namespace|$^\"} or aerospike_namespace_sindex_type_mounts_size_limit{job=\"$job_name\", cluster_name=~\"$cluster\", ns=~\"$namespace|$^\"}",
              "legendFormat": "__auto",
              "range": true,
              "refId": "A"
            }
          ],
          "title": "Data Limit (bytes)",
          "type": "stat"
        },
        {
          "datasource": {
            "type": "prometheus",
            "uid": "${DS_AEROSPIKE_PROMETHEUS}"
          },
          "description": "Total bytes in-use on the mount(s) for the secondary indexes used by this namespace on this node.",
          "fieldConfig": {
            "defaults": {
              "color": {
                "mode": "thresholds"
              },
              "mappings": [],
              "thresholds": {
                "mode": "absolute",
                "steps": [
                  {
                    "color": "green",
                    "value": null
                  }
                ]
              },
              "unit": "bytes"
            },
            "overrides": []
          },
          "gridPos": {
            "h": 4,
            "w": 3,
            "x": 15,
            "y": 2
          },
          "id": 106,
          "options": {
            "colorMode": "background",
            "graphMode": "none",
            "justifyMode": "center",
            "orientation": "auto",
            "reduceOptions": {
              "calcs": [
                "lastNotNull"
              ],
              "fields": "",
              "values": false
            },
            "showPercentChange": false,
            "textMode": "value",
            "wideLayout": true
          },
          "pluginVersion": "9.3.2",
          "targets": [
            {
              "datasource": {
                "type": "prometheus",
                "uid": "${DS_AEROSPIKE_PROMETHEUS}"
              },
              "editorMode": "code",
              "expr": "sum by (ns)(aerospike_namespace_sindex_used_bytes{job=\"$job_name\", cluster_name=~\"$cluster\", ns=~\"$namespace|$^\"})",
              "instant": false,
              "legendFormat": "{{ns}}",
              "range": true,
              "refId": "A"
            }
          ],
          "title": "Used (bytes)",
          "type": "stat"
        },
        {
          "datasource": {
            "type": "prometheus",
            "uid": "${DS_AEROSPIKE_PROMETHEUS}"
          },
          "description": "Applies only to Enterprise Edition configured with sindex-type pmem or flash",
          "fieldConfig": {
            "defaults": {
              "color": {
                "mode": "thresholds"
              },
              "mappings": [],
              "thresholds": {
                "mode": "absolute",
                "steps": [
                  {
                    "color": "green",
                    "value": null
                  }
                ]
              },
              "unit": "percent"
            },
            "overrides": []
          },
          "gridPos": {
            "h": 4,
            "w": 3,
            "x": 18,
            "y": 2
          },
          "id": 111,
          "options": {
            "colorMode": "background",
            "graphMode": "none",
            "justifyMode": "center",
            "orientation": "auto",
            "reduceOptions": {
              "calcs": [
                "lastNotNull"
              ],
              "fields": "",
              "values": false
            },
            "showPercentChange": false,
            "textMode": "value",
            "wideLayout": true
          },
          "pluginVersion": "9.3.2",
          "targets": [
            {
              "datasource": {
                "type": "prometheus",
                "uid": "${DS_AEROSPIKE_PROMETHEUS}"
              },
              "editorMode": "code",
              "expr": "aerospike_namespace_sindex_mounts_used_pct{job=\"$job_name\", cluster_name=~\"$cluster\"}",
              "instant": false,
              "legendFormat": "__auto",
              "range": true,
              "refId": "A"
            }
          ],
          "title": "Used  (%)",
          "type": "stat"
        },
        {
          "datasource": {
            "type": "prometheus",
            "uid": "${DS_AEROSPIKE_PROMETHEUS}"
          },
          "description": "Number of secondary index entries cleaned by sindex GC.",
          "fieldConfig": {
            "defaults": {
              "color": {
                "mode": "thresholds"
              },
              "mappings": [],
              "thresholds": {
                "mode": "absolute",
                "steps": [
                  {
                    "color": "green",
                    "value": null
                  }
                ]
              },
              "unit": "none"
            },
            "overrides": []
          },
          "gridPos": {
            "h": 4,
            "w": 3,
            "x": 21,
            "y": 2
          },
          "id": 107,
          "options": {
            "colorMode": "background",
            "graphMode": "none",
            "justifyMode": "center",
            "orientation": "auto",
            "reduceOptions": {
              "calcs": [
                "lastNotNull"
              ],
              "fields": "",
              "values": false
            },
            "showPercentChange": false,
            "textMode": "value",
            "wideLayout": true
          },
          "pluginVersion": "9.3.2",
          "targets": [
            {
              "datasource": {
                "type": "prometheus",
                "uid": "${DS_AEROSPIKE_PROMETHEUS}"
              },
              "editorMode": "code",
              "expr": "sum by (ns) (rate(aerospike_namespace_sindex_gc_cleaned{job=\"$job_name\", cluster_name=~\"$cluster\", ns=~\"$namespace|$^\"}[$__rate_interval]))",
              "instant": false,
              "legendFormat": "{{ns}}",
              "range": true,
              "refId": "A"
            }
          ],
          "title": "Entries Cleaned (rate)",
          "type": "stat"
        },
        {
          "datasource": {
            "type": "prometheus",
            "uid": "${DS_AEROSPIKE_PROMETHEUS}"
          },
          "description": "Memory usage of secondary indexes",
          "fieldConfig": {
            "defaults": {
              "color": {
                "mode": "palette-classic"
              },
              "custom": {
                "axisCenteredZero": false,
                "axisColorMode": "text",
                "axisLabel": "",
                "axisPlacement": "auto",
                "barAlignment": 0,
                "drawStyle": "line",
                "fillOpacity": 0,
                "gradientMode": "none",
                "hideFrom": {
                  "legend": false,
                  "tooltip": false,
                  "viz": false
                },
                "lineInterpolation": "linear",
                "lineWidth": 1,
                "pointSize": 5,
                "scaleDistribution": {
                  "type": "linear"
                },
                "showPoints": "auto",
                "spanNulls": false,
                "stacking": {
                  "group": "A",
                  "mode": "none"
                },
                "thresholdsStyle": {
                  "mode": "off"
                }
              },
              "mappings": [],
              "thresholds": {
                "mode": "absolute",
                "steps": [
                  {
                    "color": "green",
                    "value": null
                  },
                  {
                    "color": "red",
                    "value": 80
                  }
                ]
              },
              "unit": "bytes"
            },
            "overrides": []
          },
          "gridPos": {
            "h": 4,
            "w": 12,
            "x": 0,
            "y": 6
          },
          "id": 13,
          "options": {
            "legend": {
              "calcs": [
                "last",
                "min",
                "max",
                "mean"
              ],
              "displayMode": "table",
              "placement": "right",
              "showLegend": true
            },
            "tooltip": {
              "mode": "single",
              "sort": "none"
            }
          },
          "targets": [
            {
              "datasource": {
                "type": "prometheus",
                "uid": "${DS_AEROSPIKE_PROMETHEUS}"
              },
              "editorMode": "code",
              "expr": "aerospike_sindex_used_bytes{job=\"$job_name\", cluster_name=~\"$cluster\", ns=~\"$namespace|$^\"}",
              "instant": false,
              "legendFormat": "{{sindex}}",
              "range": true,
              "refId": "A"
            }
          ],
          "title": "Memory Used (bytes)",
          "type": "timeseries"
        },
        {
          "datasource": {
            "type": "prometheus",
            "uid": "${DS_AEROSPIKE_PROMETHEUS}"
          },
          "description": "Total bytes in-use on the mount(s) for the secondary indexes used by this namespace on this node.",
          "fieldConfig": {
            "defaults": {
              "color": {
                "mode": "palette-classic"
              },
              "custom": {
                "axisCenteredZero": false,
                "axisColorMode": "text",
                "axisLabel": "",
                "axisPlacement": "auto",
                "barAlignment": 0,
                "drawStyle": "line",
                "fillOpacity": 0,
                "gradientMode": "none",
                "hideFrom": {
                  "legend": false,
                  "tooltip": false,
                  "viz": false
                },
                "lineInterpolation": "linear",
                "lineWidth": 1,
                "pointSize": 5,
                "scaleDistribution": {
                  "type": "linear"
                },
                "showPoints": "auto",
                "spanNulls": false,
                "stacking": {
                  "group": "A",
                  "mode": "none"
                },
                "thresholdsStyle": {
                  "mode": "off"
                }
              },
              "mappings": [],
              "thresholds": {
                "mode": "absolute",
                "steps": [
                  {
                    "color": "green",
                    "value": null
                  },
                  {
                    "color": "red",
                    "value": 80
                  }
                ]
              },
              "unit": "bytes"
            },
            "overrides": []
          },
          "gridPos": {
            "h": 4,
            "w": 12,
            "x": 12,
            "y": 6
          },
          "id": 16,
          "options": {
            "legend": {
              "calcs": [
                "last",
                "min",
                "max",
                "mean"
              ],
              "displayMode": "table",
              "placement": "right",
              "showLegend": true
            },
            "tooltip": {
              "mode": "single",
              "sort": "none"
            }
          },
          "targets": [
            {
              "datasource": {
                "type": "prometheus",
                "uid": "${DS_AEROSPIKE_PROMETHEUS}"
              },
              "editorMode": "code",
              "expr": "aerospike_namespace_sindex_used_bytes{job=\"$job_name\", cluster_name=~\"$cluster\", ns=~\"$namespace|$^\"}",
              "instant": false,
              "legendFormat": "{{service}}-Mounts in-use",
              "range": true,
              "refId": "A"
            }
          ],
          "title": "Used (bytes)",
          "type": "timeseries"
        },
        {
          "datasource": {
            "type": "prometheus",
            "uid": "${DS_AEROSPIKE_PROMETHEUS}"
          },
          "description": "Number of secondary index entries for this secondary index. This is the number of records that have been indexed by this secondary index.",
          "fieldConfig": {
            "defaults": {
              "color": {
                "mode": "palette-classic"
              },
              "custom": {
                "axisCenteredZero": false,
                "axisColorMode": "text",
                "axisLabel": "",
                "axisPlacement": "auto",
                "barAlignment": 0,
                "drawStyle": "line",
                "fillOpacity": 0,
                "gradientMode": "none",
                "hideFrom": {
                  "legend": false,
                  "tooltip": false,
                  "viz": false
                },
                "lineInterpolation": "linear",
                "lineWidth": 1,
                "pointSize": 5,
                "scaleDistribution": {
                  "type": "linear"
                },
                "showPoints": "auto",
                "spanNulls": false,
                "stacking": {
                  "group": "A",
                  "mode": "none"
                },
                "thresholdsStyle": {
                  "mode": "off"
                }
              },
              "mappings": [],
              "thresholds": {
                "mode": "absolute",
                "steps": [
                  {
                    "color": "green",
                    "value": null
                  },
                  {
                    "color": "red",
                    "value": 80
                  }
                ]
              },
              "unit": "none"
            },
            "overrides": []
          },
          "gridPos": {
            "h": 4,
            "w": 12,
            "x": 0,
            "y": 10
          },
          "id": 1,
          "options": {
            "legend": {
              "calcs": [
                "last",
                "min",
                "max",
                "mean"
              ],
              "displayMode": "table",
              "placement": "right",
              "showLegend": true,
              "sortBy": "Name",
              "sortDesc": true
            },
            "tooltip": {
              "mode": "single",
              "sort": "none"
            }
          },
          "targets": [
            {
              "datasource": {
                "type": "prometheus",
                "uid": "${DS_AEROSPIKE_PROMETHEUS}"
              },
              "editorMode": "code",
              "expr": "aerospike_sindex_entries{job=\"$job_name\", cluster_name=~\"$cluster\", ns=~\"$namespace|$^\"}",
              "instant": false,
              "legendFormat": "{{sindex}}",
              "range": true,
              "refId": "A"
            }
          ],
          "title": "Entries",
          "type": "timeseries"
        },
        {
          "datasource": {
            "type": "prometheus",
            "uid": "${DS_AEROSPIKE_PROMETHEUS}"
          },
          "description": "Number of entries per secondary index per record",
          "fieldConfig": {
            "defaults": {
              "color": {
                "mode": "palette-classic"
              },
              "custom": {
                "axisCenteredZero": false,
                "axisColorMode": "text",
                "axisLabel": "",
                "axisPlacement": "auto",
                "barAlignment": 0,
                "drawStyle": "line",
                "fillOpacity": 0,
                "gradientMode": "none",
                "hideFrom": {
                  "legend": false,
                  "tooltip": false,
                  "viz": false
                },
                "lineInterpolation": "linear",
                "lineWidth": 1,
                "pointSize": 5,
                "scaleDistribution": {
                  "type": "linear"
                },
                "showPoints": "auto",
                "spanNulls": false,
                "stacking": {
                  "group": "A",
                  "mode": "none"
                },
                "thresholdsStyle": {
                  "mode": "off"
                }
              },
              "mappings": [],
              "thresholds": {
                "mode": "absolute",
                "steps": [
                  {
                    "color": "green",
                    "value": null
                  },
                  {
                    "color": "red",
                    "value": 80
                  }
                ]
              },
              "unit": "none"
            },
            "overrides": []
          },
          "gridPos": {
            "h": 4,
            "w": 12,
            "x": 12,
            "y": 10
          },
          "id": 8,
          "options": {
            "legend": {
              "calcs": [
                "last",
                "min",
                "max",
                "mean"
              ],
              "displayMode": "table",
              "placement": "right",
              "showLegend": true
            },
            "tooltip": {
              "mode": "single",
              "sort": "none"
            }
          },
          "targets": [
            {
              "datasource": {
                "type": "prometheus",
                "uid": "${DS_AEROSPIKE_PROMETHEUS}"
              },
              "editorMode": "code",
              "expr": "aerospike_sindex_entries_per_rec{job=\"$job_name\", cluster_name=~\"$cluster\", ns=~\"$namespace|$^\"}",
              "instant": false,
              "legendFormat": "{{sindex}}",
              "range": true,
              "refId": "A"
            }
          ],
          "title": "Entries Per Record",
          "type": "timeseries"
        },
        {
          "datasource": {
            "type": "prometheus",
            "uid": "${DS_AEROSPIKE_PROMETHEUS}"
          },
          "description": "Size of the stage for sindex processing within a namespace",
          "fieldConfig": {
            "defaults": {
              "color": {
                "mode": "palette-classic"
              },
              "custom": {
                "axisCenteredZero": false,
                "axisColorMode": "text",
                "axisLabel": "",
                "axisPlacement": "auto",
                "barAlignment": 0,
                "drawStyle": "line",
                "fillOpacity": 0,
                "gradientMode": "none",
                "hideFrom": {
                  "legend": false,
                  "tooltip": false,
                  "viz": false
                },
                "lineInterpolation": "linear",
                "lineWidth": 1,
                "pointSize": 5,
                "scaleDistribution": {
                  "type": "linear"
                },
                "showPoints": "auto",
                "spanNulls": false,
                "stacking": {
                  "group": "A",
                  "mode": "none"
                },
                "thresholdsStyle": {
                  "mode": "off"
                }
              },
              "mappings": [],
              "thresholds": {
                "mode": "absolute",
                "steps": [
                  {
                    "color": "green",
                    "value": null
                  }
                ]
              },
              "unit": "bytes"
            },
            "overrides": []
          },
          "gridPos": {
            "h": 4,
            "w": 12,
            "x": 0,
            "y": 14
          },
          "id": 112,
          "options": {
            "legend": {
              "calcs": [
                "last",
                "min",
                "max",
                "mean"
              ],
              "displayMode": "table",
              "placement": "right",
              "showLegend": true
            },
            "tooltip": {
              "mode": "single",
              "sort": "none"
            }
          },
          "pluginVersion": "10.4.2",
          "targets": [
            {
              "datasource": {
                "type": "prometheus",
                "uid": "${DS_AEROSPIKE_PROMETHEUS}"
              },
              "editorMode": "code",
              "expr": "(aerospike_namespace_sindex_stage_size{job=\"$job_name\", cluster_name=~\"$cluster\", ns=~\"$namespace|$^\"})",
              "instant": false,
              "legendFormat": "{{service}}",
              "range": true,
              "refId": "A"
            }
          ],
          "title": "Stage Size (bytes)",
          "type": "timeseries"
        },
        {
          "datasource": {
            "type": "prometheus",
            "uid": "${DS_AEROSPIKE_PROMETHEUS}"
          },
          "description": "Number of entries per secondary index per bin value",
          "fieldConfig": {
            "defaults": {
              "color": {
                "mode": "palette-classic"
              },
              "custom": {
                "axisCenteredZero": false,
                "axisColorMode": "text",
                "axisLabel": "",
                "axisPlacement": "auto",
                "barAlignment": 0,
                "drawStyle": "line",
                "fillOpacity": 0,
                "gradientMode": "none",
                "hideFrom": {
                  "legend": false,
                  "tooltip": false,
                  "viz": false
                },
                "lineInterpolation": "linear",
                "lineWidth": 1,
                "pointSize": 5,
                "scaleDistribution": {
                  "type": "linear"
                },
                "showPoints": "auto",
                "spanNulls": false,
                "stacking": {
                  "group": "A",
                  "mode": "none"
                },
                "thresholdsStyle": {
                  "mode": "off"
                }
              },
              "mappings": [],
              "thresholds": {
                "mode": "absolute",
                "steps": [
                  {
                    "color": "green",
                    "value": null
                  },
                  {
                    "color": "red",
                    "value": 80
                  }
                ]
              },
              "unit": "none"
            },
            "overrides": []
          },
          "gridPos": {
            "h": 4,
            "w": 12,
            "x": 12,
            "y": 14
          },
          "id": 7,
          "options": {
            "legend": {
              "calcs": [
                "last",
                "min",
                "max",
                "mean"
              ],
              "displayMode": "table",
              "placement": "right",
              "showLegend": true
            },
            "tooltip": {
              "mode": "single",
              "sort": "none"
            }
          },
          "targets": [
            {
              "datasource": {
                "type": "prometheus",
                "uid": "${DS_AEROSPIKE_PROMETHEUS}"
              },
              "editorMode": "code",
              "expr": "aerospike_sindex_entries_per_bval{job=\"$job_name\", cluster_name=~\"$cluster\", ns=~\"$namespace|$^\"}",
              "instant": false,
              "legendFormat": "{{sindex}}",
              "range": true,
              "refId": "A"
            }
          ],
          "title": "Entries Per Bin",
          "type": "timeseries"
        },
        {
          "datasource": {
            "type": "prometheus",
            "uid": "${DS_AEROSPIKE_PROMETHEUS}"
          },
          "description": "Number of secondary index entries cleaned by sindex GC.",
          "fieldConfig": {
            "defaults": {
              "color": {
                "mode": "palette-classic"
              },
              "custom": {
                "axisCenteredZero": false,
                "axisColorMode": "text",
                "axisLabel": "",
                "axisPlacement": "auto",
                "barAlignment": 0,
                "drawStyle": "line",
                "fillOpacity": 0,
                "gradientMode": "none",
                "hideFrom": {
                  "legend": false,
                  "tooltip": false,
                  "viz": false
                },
                "lineInterpolation": "linear",
                "lineWidth": 1,
                "pointSize": 5,
                "scaleDistribution": {
                  "type": "linear"
                },
                "showPoints": "auto",
                "spanNulls": false,
                "stacking": {
                  "group": "A",
                  "mode": "none"
                },
                "thresholdsStyle": {
                  "mode": "off"
                }
              },
              "mappings": [],
              "thresholds": {
                "mode": "absolute",
                "steps": [
                  {
                    "color": "green",
                    "value": null
                  },
                  {
                    "color": "red",
                    "value": 80
                  }
                ]
              },
              "unit": "none"
            },
            "overrides": []
          },
          "gridPos": {
            "h": 4,
            "w": 12,
            "x": 0,
            "y": 18
          },
          "id": 14,
          "options": {
            "legend": {
              "calcs": [
                "last",
                "min",
                "max",
                "mean"
              ],
              "displayMode": "table",
              "placement": "right",
              "showLegend": true
            },
            "tooltip": {
              "mode": "single",
              "sort": "none"
            }
          },
          "targets": [
            {
              "datasource": {
                "type": "prometheus",
                "uid": "${DS_AEROSPIKE_PROMETHEUS}"
              },
              "editorMode": "code",
              "expr": "rate(aerospike_namespace_sindex_gc_cleaned{job=\"$job_name\", cluster_name=~\"$cluster\", ns=~\"$namespace|$^\"}[$__rate_interval])",
              "instant": false,
              "legendFormat": "{{service}}-Entries Cleaned",
              "range": true,
              "refId": "A"
            }
          ],
          "title": "Entries Cleaned (rate)",
          "type": "timeseries"
        },
        {
          "datasource": {
            "type": "prometheus",
            "uid": "${DS_AEROSPIKE_PROMETHEUS}"
          },
          "description": "Number of records that have been garbage collected out of the secondary index memory",
          "fieldConfig": {
            "defaults": {
              "color": {
                "mode": "palette-classic"
              },
              "custom": {
                "axisCenteredZero": false,
                "axisColorMode": "text",
                "axisLabel": "",
                "axisPlacement": "auto",
                "barAlignment": 0,
                "drawStyle": "line",
                "fillOpacity": 0,
                "gradientMode": "none",
                "hideFrom": {
                  "legend": false,
                  "tooltip": false,
                  "viz": false
                },
                "lineInterpolation": "linear",
                "lineWidth": 1,
                "pointSize": 5,
                "scaleDistribution": {
                  "type": "linear"
                },
                "showPoints": "auto",
                "spanNulls": false,
                "stacking": {
                  "group": "A",
                  "mode": "none"
                },
                "thresholdsStyle": {
                  "mode": "off"
                }
              },
              "mappings": [],
              "thresholds": {
                "mode": "absolute",
                "steps": [
                  {
                    "color": "green",
                    "value": null
                  },
                  {
                    "color": "red",
                    "value": 80
                  }
                ]
              },
              "unit": "none"
            },
            "overrides": []
          },
          "gridPos": {
            "h": 4,
            "w": 12,
            "x": 12,
            "y": 18
          },
          "id": 12,
          "options": {
            "legend": {
              "calcs": [
                "last",
                "min",
                "max",
                "mean"
              ],
              "displayMode": "table",
              "placement": "right",
              "showLegend": true
            },
            "tooltip": {
              "mode": "single",
              "sort": "none"
            }
          },
          "targets": [
            {
              "datasource": {
                "type": "prometheus",
                "uid": "${DS_AEROSPIKE_PROMETHEUS}"
              },
              "editorMode": "code",
              "expr": "rate(aerospike_sindex_stat_gc_recs{job=\"$job_name\", cluster_name=~\"$cluster\", ns=~\"$namespace|$^\"}[$__rate_interval])",
              "instant": false,
              "legendFormat": "{{sindex}}",
              "range": true,
              "refId": "A"
            }
          ],
          "title": "Stat GC Records (rate)",
          "type": "timeseries"
        },
        {
          "datasource": {
            "type": "prometheus",
            "uid": "${DS_AEROSPIKE_PROMETHEUS}"
          },
          "description": "Number of basic queries  that have been completed/aborted/errors after exceeding a predefined timeout duration within a namespace in sindex queries",
          "fieldConfig": {
            "defaults": {
              "color": {
                "mode": "palette-classic"
              },
              "custom": {
                "axisBorderShow": false,
                "axisCenteredZero": false,
                "axisColorMode": "text",
                "axisLabel": "",
                "axisPlacement": "auto",
                "barAlignment": 0,
                "drawStyle": "line",
                "fillOpacity": 0,
                "gradientMode": "none",
                "hideFrom": {
                  "legend": false,
                  "tooltip": false,
                  "viz": false
                },
                "insertNulls": false,
                "lineInterpolation": "linear",
                "lineWidth": 1,
                "pointSize": 5,
                "scaleDistribution": {
                  "type": "linear"
                },
                "showPoints": "auto",
                "spanNulls": false,
                "stacking": {
                  "group": "A",
                  "mode": "none"
                },
                "thresholdsStyle": {
                  "mode": "off"
                }
              },
              "mappings": [],
              "thresholds": {
                "mode": "absolute",
                "steps": [
                  {
                    "color": "green"
                  },
                  {
                    "color": "red",
                    "value": 80
                  }
                ]
              }
            },
            "overrides": []
          },
          "gridPos": {
            "h": 4,
            "w": 12,
            "x": 0,
            "y": 22
          },
          "id": 98,
          "options": {
            "legend": {
              "calcs": [
                "last",
                "min",
                "max",
                "mean"
              ],
              "displayMode": "table",
              "placement": "right",
              "showLegend": true
            },
            "tooltip": {
              "mode": "single",
              "sort": "none"
            }
          },
          "pluginVersion": "10.4.2",
          "targets": [
            {
              "datasource": {
                "type": "prometheus",
                "uid": "${DS_AEROSPIKE_PROMETHEUS}"
              },
              "editorMode": "code",
              "expr": "rate(aerospike_namespace_si_query_long_basic_complete{job=\"$job_name\", cluster_name=~\"$cluster\", ns=~\"$namespace|$^\"}[$__rate_interval])",
              "instant": false,
              "legendFormat": "{{service}}-Completed ",
              "range": true,
              "refId": "Completed"
            },
            {
              "datasource": {
                "type": "prometheus",
                "uid": "${DS_AEROSPIKE_PROMETHEUS}"
              },
              "editorMode": "code",
              "expr": "rate(aerospike_namespace_si_query_long_basic_abort{job=\"$job_name\", cluster_name=~\"$cluster\", ns=~\"$namespace|$^\"}[$__rate_interval])",
              "hide": false,
              "instant": false,
              "legendFormat": "{{service}}-Aborted",
              "range": true,
              "refId": "Aborted"
            },
            {
              "datasource": {
                "type": "prometheus",
                "uid": "${DS_AEROSPIKE_PROMETHEUS}"
              },
              "editorMode": "code",
              "expr": "rate(aerospike_namespace_si_query_long_basic_error{job=\"$job_name\", cluster_name=~\"$cluster\", ns=~\"$namespace|$^\"}[$__rate_interval])",
              "hide": false,
              "instant": false,
              "legendFormat": "{{service}}-Errors",
              "range": true,
              "refId": "Errors"
            }
          ],
          "title": "Long Queries (rate)",
          "type": "timeseries"
        },
        {
          "datasource": {
            "type": "prometheus",
            "uid": "${DS_AEROSPIKE_PROMETHEUS}"
          },
          "description": "Number of secondary index query aggregations completed/aborted/errors",
          "fieldConfig": {
            "defaults": {
              "color": {
                "mode": "palette-classic"
              },
              "custom": {
                "axisBorderShow": false,
                "axisCenteredZero": false,
                "axisColorMode": "text",
                "axisLabel": "",
                "axisPlacement": "auto",
                "barAlignment": 0,
                "drawStyle": "line",
                "fillOpacity": 0,
                "gradientMode": "none",
                "hideFrom": {
                  "legend": false,
                  "tooltip": false,
                  "viz": false
                },
                "insertNulls": false,
                "lineInterpolation": "linear",
                "lineWidth": 1,
                "pointSize": 5,
                "scaleDistribution": {
                  "type": "linear"
                },
                "showPoints": "auto",
                "spanNulls": false,
                "stacking": {
                  "group": "A",
                  "mode": "none"
                },
                "thresholdsStyle": {
                  "mode": "off"
                }
              },
              "mappings": [],
              "thresholds": {
                "mode": "absolute",
                "steps": [
                  {
                    "color": "green"
                  }
                ]
              },
              "unit": "none"
            },
            "overrides": []
          },
          "gridPos": {
            "h": 4,
            "w": 12,
            "x": 12,
            "y": 22
          },
          "id": 97,
          "options": {
            "legend": {
              "calcs": [
                "last",
                "min",
                "max",
                "mean"
              ],
              "displayMode": "table",
              "placement": "right",
              "showLegend": true
            },
            "tooltip": {
              "mode": "single",
              "sort": "none"
            }
          },
          "pluginVersion": "10.4.2",
          "targets": [
            {
              "datasource": {
                "type": "prometheus",
                "uid": "${DS_AEROSPIKE_PROMETHEUS}"
              },
              "editorMode": "code",
              "expr": "rate(aerospike_namespace_si_query_aggr_complete{job=\"$job_name\", cluster_name=~\"$cluster\", ns=~\"$namespace|$^\"}[$__rate_interval])",
              "instant": false,
              "legendFormat": "{{service}}-Completed",
              "range": true,
              "refId": "Completed"
            },
            {
              "datasource": {
                "type": "prometheus",
                "uid": "${DS_AEROSPIKE_PROMETHEUS}"
              },
              "editorMode": "code",
              "expr": "rate(aerospike_namespace_si_query_aggr_abort{job=\"$job_name\", cluster_name=~\"$cluster\", ns=~\"$namespace|$^\"}[$__rate_interval])",
              "hide": false,
              "instant": false,
              "legendFormat": "{{service}}-Aborted",
              "range": true,
              "refId": "Aborted"
            },
            {
              "datasource": {
                "type": "prometheus",
                "uid": "${DS_AEROSPIKE_PROMETHEUS}"
              },
              "editorMode": "code",
              "expr": "rate(aerospike_namespace_si_query_aggr_error{job=\"$job_name\", cluster_name=~\"$cluster\", ns=~\"$namespace|$^\"}[$__rate_interval])",
              "hide": false,
              "instant": false,
              "legendFormat": "{{service}}-Errors",
              "range": true,
              "refId": "Errors"
            }
          ],
          "title": "Query Aggregations (rate)",
          "type": "timeseries"
        },
        {
          "datasource": {
            "type": "prometheus",
            "uid": "${DS_AEROSPIKE_PROMETHEUS}"
          },
          "description": "Number of ops background secondary index queries completed/aborted/errors",
          "fieldConfig": {
            "defaults": {
              "color": {
                "mode": "palette-classic"
              },
              "custom": {
                "axisBorderShow": false,
                "axisCenteredZero": false,
                "axisColorMode": "text",
                "axisLabel": "",
                "axisPlacement": "auto",
                "barAlignment": 0,
                "drawStyle": "line",
                "fillOpacity": 0,
                "gradientMode": "none",
                "hideFrom": {
                  "legend": false,
                  "tooltip": false,
                  "viz": false
                },
                "insertNulls": false,
                "lineInterpolation": "linear",
                "lineWidth": 1,
                "pointSize": 5,
                "scaleDistribution": {
                  "type": "linear"
                },
                "showPoints": "auto",
                "spanNulls": false,
                "stacking": {
                  "group": "A",
                  "mode": "none"
                },
                "thresholdsStyle": {
                  "mode": "off"
                }
              },
              "mappings": [],
              "thresholds": {
                "mode": "absolute",
                "steps": [
                  {
                    "color": "green"
                  }
                ]
              },
              "unit": "none"
            },
            "overrides": []
          },
          "gridPos": {
            "h": 4,
            "w": 12,
            "x": 0,
            "y": 26
          },
          "id": 99,
          "options": {
            "legend": {
              "calcs": [
                "last",
                "min",
                "max",
                "mean"
              ],
              "displayMode": "table",
              "placement": "right",
              "showLegend": true
            },
            "tooltip": {
              "mode": "single",
              "sort": "none"
            }
          },
          "pluginVersion": "10.4.2",
          "targets": [
            {
              "datasource": {
                "type": "prometheus",
                "uid": "${DS_AEROSPIKE_PROMETHEUS}"
              },
              "editorMode": "code",
              "expr": "rate(aerospike_namespace_si_query_ops_bg_complete{job=\"$job_name\", cluster_name=~\"$cluster\", ns=~\"$namespace|$^\"}[$__rate_interval])",
              "instant": false,
              "legendFormat": "{{service}}-Completed",
              "range": true,
              "refId": "Completed"
            },
            {
              "datasource": {
                "type": "prometheus",
                "uid": "${DS_AEROSPIKE_PROMETHEUS}"
              },
              "editorMode": "code",
              "expr": "rate(aerospike_namespace_si_query_ops_bg_abort{job=\"$job_name\", cluster_name=~\"$cluster\", ns=~\"$namespace|$^\"}[$__rate_interval])",
              "hide": false,
              "instant": false,
              "legendFormat": "{{service}}-Aborted",
              "range": true,
              "refId": "Aborted"
            },
            {
              "datasource": {
                "type": "prometheus",
                "uid": "${DS_AEROSPIKE_PROMETHEUS}"
              },
              "editorMode": "code",
              "expr": "rate(aerospike_namespace_si_query_ops_bg_error{job=\"$job_name\", cluster_name=~\"$cluster\", ns=~\"$namespace|$^\"}[$__rate_interval])",
              "hide": false,
              "instant": false,
              "legendFormat": "{{service}}-Errors",
              "range": true,
              "refId": "Errors"
            }
          ],
          "title": "Ops Background Queries (rate)",
          "type": "timeseries"
        },
        {
          "datasource": {
            "type": "prometheus",
            "uid": "${DS_AEROSPIKE_PROMETHEUS}"
          },
          "description": "Number of basic queries completed/timedout/errors in sindex queries within a namespace within a predefined short duration",
          "fieldConfig": {
            "defaults": {
              "color": {
                "mode": "palette-classic"
              },
              "custom": {
                "axisBorderShow": false,
                "axisCenteredZero": false,
                "axisColorMode": "text",
                "axisLabel": "",
                "axisPlacement": "auto",
                "barAlignment": 0,
                "drawStyle": "line",
                "fillOpacity": 0,
                "gradientMode": "none",
                "hideFrom": {
                  "legend": false,
                  "tooltip": false,
                  "viz": false
                },
                "insertNulls": false,
                "lineInterpolation": "linear",
                "lineWidth": 1,
                "pointSize": 5,
                "scaleDistribution": {
                  "type": "linear"
                },
                "showPoints": "auto",
                "spanNulls": false,
                "stacking": {
                  "group": "A",
                  "mode": "none"
                },
                "thresholdsStyle": {
                  "mode": "off"
                }
              },
              "mappings": [],
              "thresholds": {
                "mode": "absolute",
                "steps": [
                  {
                    "color": "green"
                  }
                ]
              },
              "unit": "none"
            },
            "overrides": []
          },
          "gridPos": {
            "h": 4,
            "w": 12,
            "x": 12,
            "y": 26
          },
          "id": 100,
          "options": {
            "legend": {
              "calcs": [
                "last",
                "min",
                "max",
                "mean"
              ],
              "displayMode": "table",
              "placement": "right",
              "showLegend": true
            },
            "tooltip": {
              "mode": "single",
              "sort": "none"
            }
          },
          "pluginVersion": "10.4.2",
          "targets": [
            {
              "datasource": {
                "type": "prometheus",
                "uid": "${DS_AEROSPIKE_PROMETHEUS}"
              },
              "editorMode": "code",
              "expr": "rate(aerospike_namespace_si_query_short_basic_complete{job=\"$job_name\", cluster_name=~\"$cluster\", ns=~\"$namespace|$^\"}[$__rate_interval])",
              "instant": false,
              "legendFormat": "{{service}}-Completed",
              "range": true,
              "refId": "Completed"
            },
            {
              "datasource": {
                "type": "prometheus",
                "uid": "${DS_AEROSPIKE_PROMETHEUS}"
              },
              "editorMode": "code",
              "expr": "rate(aerospike_namespace_si_query_short_basic_timeout{job=\"$job_name\", cluster_name=~\"$cluster\", ns=~\"$namespace|$^\"}[$__rate_interval])",
              "hide": false,
              "instant": false,
              "legendFormat": "{{service}}-Timeout",
              "range": true,
              "refId": "Timeout"
            },
            {
              "datasource": {
                "type": "prometheus",
                "uid": "${DS_AEROSPIKE_PROMETHEUS}"
              },
              "editorMode": "code",
              "expr": "rate(aerospike_namespace_si_query_short_basic_error{job=\"$job_name\", cluster_name=~\"$cluster\", ns=~\"$namespace|$^\"}[$__rate_interval])",
              "hide": false,
              "instant": false,
              "legendFormat": "{{service}}-Errors",
              "range": true,
              "refId": "Errors"
            }
          ],
          "title": "Short Queries (rate)",
          "type": "timeseries"
        },
        {
          "datasource": {
            "type": "prometheus",
            "uid": "${DS_AEROSPIKE_PROMETHEUS}"
          },
          "description": "Number of udf background secondary index queries that were completed/sborted/errors",
          "fieldConfig": {
            "defaults": {
              "color": {
                "mode": "palette-classic"
              },
              "custom": {
                "axisBorderShow": false,
                "axisCenteredZero": false,
                "axisColorMode": "text",
                "axisLabel": "",
                "axisPlacement": "auto",
                "barAlignment": 0,
                "drawStyle": "line",
                "fillOpacity": 0,
                "gradientMode": "none",
                "hideFrom": {
                  "legend": false,
                  "tooltip": false,
                  "viz": false
                },
                "insertNulls": false,
                "lineInterpolation": "linear",
                "lineWidth": 1,
                "pointSize": 5,
                "scaleDistribution": {
                  "type": "linear"
                },
                "showPoints": "auto",
                "spanNulls": false,
                "stacking": {
                  "group": "A",
                  "mode": "none"
                },
                "thresholdsStyle": {
                  "mode": "off"
                }
              },
              "mappings": [],
              "thresholds": {
                "mode": "absolute",
                "steps": [
                  {
                    "color": "green"
                  }
                ]
              },
              "unit": "none"
            },
            "overrides": []
          },
          "gridPos": {
            "h": 4,
            "w": 12,
            "x": 12,
            "y": 30
          },
          "id": 101,
          "options": {
            "legend": {
              "calcs": [
                "last",
                "min",
                "max",
                "mean"
              ],
              "displayMode": "table",
              "placement": "right",
              "showLegend": true
            },
            "tooltip": {
              "mode": "single",
              "sort": "none"
            }
          },
          "pluginVersion": "10.4.2",
          "targets": [
            {
              "datasource": {
                "type": "prometheus",
                "uid": "${DS_AEROSPIKE_PROMETHEUS}"
              },
              "editorMode": "code",
              "expr": "rate(aerospike_namespace_si_query_udf_bg_complete{job=\"$job_name\", cluster_name=~\"$cluster\", ns=~\"$namespace|$^\"}[$__rate_interval])",
              "instant": false,
              "legendFormat": "{{service}}-Completed",
              "range": true,
              "refId": "Completed"
            },
            {
              "datasource": {
                "type": "prometheus",
                "uid": "${DS_AEROSPIKE_PROMETHEUS}"
              },
              "editorMode": "code",
              "expr": "rate(aerospike_namespace_si_query_udf_bg_abort{job=\"$job_name\", cluster_name=~\"$cluster\", ns=~\"$namespace|$^\"}[$__rate_interval])",
              "hide": false,
              "instant": false,
              "legendFormat": "{{service}}-Aborted",
              "range": true,
              "refId": "Aborted"
            },
            {
              "datasource": {
                "type": "prometheus",
                "uid": "${DS_AEROSPIKE_PROMETHEUS}"
              },
              "editorMode": "code",
              "expr": "rate(aerospike_namespace_si_query_udf_bg_error{job=\"$job_name\", cluster_name=~\"$cluster\", ns=~\"$namespace|$^\"}[$__rate_interval])",
              "hide": false,
              "instant": false,
              "legendFormat": "{{service}}-Errors",
              "range": true,
              "refId": "Errors"
            }
          ],
          "title": "UDF Queries (rate)",
          "type": "timeseries"
        }
      ],
      "repeat": "namespace",
      "repeatDirection": "h",
      "title": "Namespace - $namespace",
      "type": "row"
    }
  ],
  "refresh": "",
  "schemaVersion": 37,
  "style": "dark",
  "tags": [
    "usecase",
    "monitoring",
    "sindex"
  ],
  "templating": {
    "list": [
      {
        "current": {
          "selected": false,
          "text": "Aerospike Prometheus",
          "value": "Aerospike Prometheus"
        },
        "hide": 0,
        "includeAll": false,
        "label": "Datasource",
        "multi": false,
        "name": "DS_AEROSPIKE_PROMETHEUS",
        "options": [],
        "query": "prometheus",
        "queryValue": "",
        "refresh": 1,
        "regex": "",
        "skipUrlSync": false,
        "type": "datasource"
      },
      {
        "current": {},
        "datasource": {
          "type": "prometheus",
          "uid": "${DS_AEROSPIKE_PROMETHEUS}"
        },
        "definition": "label_values(aerospike_node_stats_uptime,job)",
        "hide": 0,
        "includeAll": false,
        "label": "job_name",
        "multi": false,
        "name": "job_name",
        "options": [],
        "query": {
          "qryType": 1,
          "query": "label_values(aerospike_node_stats_uptime,job)",
          "refId": "PrometheusVariableQueryEditor-VariableQuery"
        },
        "refresh": 1,
        "regex": "",
        "skipUrlSync": false,
        "sort": 0,
        "type": "query"
      },
      {
        "current": {},
        "datasource": {
          "type": "prometheus",
          "uid": "${DS_AEROSPIKE_PROMETHEUS}"
        },
        "definition": "label_values(aerospike_node_stats_uptime{job=\"$job_name\"},cluster_name)",
        "hide": 0,
        "includeAll": false,
        "label": "Cluster",
        "multi": false,
        "name": "cluster",
        "options": [],
        "query": {
          "qryType": 1,
          "query": "label_values(aerospike_node_stats_uptime{job=\"$job_name\"},cluster_name)",
          "refId": "PrometheusVariableQueryEditor-VariableQuery"
        },
        "refresh": 2,
        "regex": "",
        "skipUrlSync": false,
        "sort": 0,
        "type": "query"
      },
      {
        "current": {},
        "datasource": {
          "type": "prometheus",
          "uid": "${DS_AEROSPIKE_PROMETHEUS}"
        },
        "definition": "label_values(aerospike_sindex_entries{job=\"$job_name\", cluster_name=~\"$cluster|$^\"},ns)",
        "hide": 0,
        "includeAll": true,
        "label": "Namespace",
        "multi": true,
        "name": "namespace",
        "options": [],
        "query": {
          "query": "label_values(aerospike_sindex_entries{job=\"$job_name\", cluster_name=~\"$cluster|$^\"},ns)",
          "refId": "StandardVariableQuery"
        },
        "refresh": 1,
        "regex": "",
        "skipUrlSync": false,
        "sort": 0,
        "type": "query"
      }
    ]
  },
  "time": {
    "from": "now-3h",
    "to": "now"
  },
  "timepicker": {},
  "timezone": "browser",
  "title": "Secondary Index Summary View",
  "uid": "adiyrnyfszv28d",
  "version": 5,
  "weekStart": ""
}