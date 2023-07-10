
# Easy Aerospike Monitoring Stack
This will setup a single node cluster, and deploy the monitoring stack
in a simple docker-compose file. 


## To start the stack
```
$ docker-compose up
```

Now simply point your browser at `http://localhost:4000/dashboards` to see the dashboard.

> **Note**: the alertmanager reports a configuration error because a placeholder mail
service has been referenced in the configuration; if you wish to receive alerts,
modify the `config/prometheus/alertmanager.yml` with the configuration to your SMTP
server.

## To stop the stack
```
$ docker-compose down
```
