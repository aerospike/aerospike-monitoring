# Easy Aerospike Monitoring Stack

The easy deploy Aerospike Monitoring Stack is a docker compose configuration
which creates the following containers running on the same host as a single node
Aerospike cluster:
1. aerospike-prometheus-exporter
1. prometheus
1. alertmanager
1. grafana

To start the stack:
```
docker-compose -f easy-compose.yml up
```

To stop the stack:
```
docker-compose -f easy-compose.yml down
```

Note that the alertmanager reports a configuration error because a placeholder mail
service has been referenced in the configuration; if you wish to receive alerts,
modify the `config/prometheus/alertmanager.yml` with the configuration to your SMTP
server.
