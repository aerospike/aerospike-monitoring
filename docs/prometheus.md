# Configure Prometheus and AlertManager

This document describes how to configure the Prometheus server to scrape metrics from Aerospike Prometheus Exporter, send alerts to an Alertmanager instance, and add an Aerospike alert rules configuration file.

## Configure Prometheus

### Global Parameters

```yaml
global:
  scrape_interval: 15s      # Set the scrape interval to every 15 seconds. Default is every 1 minute.
  evaluation_interval: 15s  # Evaluate rules every 15 seconds. The default is every 1 minute.
  # scrape_timeout is set to the global default (10s).
```

### AlertManager Configuration (Optional)

To enable sending alerts, configure the AlertManager targets:

```yaml
alerting:
  alertmanagers:
  - static_configs:
    - targets:
      - "alertmanager:9093"
```

### Alert Rules Configuration

1. Download the Aerospike rules-configuration file from the `config/prometheus/` folder of the aerospike-monitoring GitHub repository:
   - Link: [aerospike_rules.yml](https://github.com/aerospike/aerospike-monitoring/blob/master/config/prometheus/aerospike_rules.yml)

2. Copy the file to `/etc/prometheus/`

3. Add the rules file path to your Prometheus configuration:

```yaml
rule_files:
  - "/etc/prometheus/aerospike_rules.yaml"
```

### Scrape Configuration

Configure the instances of Aerospike Prometheus Exporter that Prometheus should scrape:

```yaml
scrape_configs:
  - job_name: 'aerospike'
    static_configs:
      - targets: ['172.20.0.2:9145', '172.20.0.3:9145']
```

## Configure AlertManager

The Alertmanager supports various notification configurations. You can configure it to send alerts to different destinations such as:
- Slack
- Email
- PagerDuty
- Webhooks
- And more

For detailed AlertManager configuration options, refer to the [official AlertManager documentation](https://prometheus.io/docs/alerting/latest/alertmanager/).

## Additional Resources

- [Aerospike Monitoring Stack](https://github.com/aerospike/aerospike-monitoring)
- [Prometheus Documentation](https://prometheus.io/docs/introduction/overview/)
- [AlertManager Documentation](https://prometheus.io/docs/alerting/latest/alertmanager/) 