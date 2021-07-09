# Easy Aerospike Monitoring Stack

The easy deploy Aerospike Monitoring Stack is a docker compose configuration
which creates the following containers running on the same host as a single-node
Aerospike cluster:
1. aerospike-prometheus-exporter
1. prometheus
1. alertmanager
1. grafana

The only prerequisite is that you have a single-node cluster, with the service port
accessible from port 3000 of the host where the monitoring stack is deployed.  If you
do not already have such an Aerospike cluster, you can deploy a single-node cluster
in a container using:
```
docker run -tid --name aerospike -p 3000:3000 -p 3001:3001 -p 3002:3002 aerospike/aerospike-server:latest
```


## To start the stack
```
docker-compose -f easy-compose.yml up
```

Now simply point your browser at `http://<host>:4000` to see the dashboard.

> **Note**: the alertmanager reports a configuration error because a placeholder mail
service has been referenced in the configuration; if you wish to receive alerts,
modify the `config/prometheus/alertmanager.yml` with the configuration to your SMTP
server.

## To stop the stack
```
docker-compose -f easy-compose.yml down
```

