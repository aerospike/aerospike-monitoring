# OTel Aerospike Monitoring Stack

The otel deploy Aerospike Monitoring Stack is a docker compose configuration
which creates the following containers running on the same host as a single-node
Aerospike cluster:
1. aerospike-prometheus-exporter latest version
1. otel collector contrib latest version

A prerequisite is that you have a single-node cluster, with the service port
accessible from port 3000 of the host where the monitoring stack is deployed.  If you
do not already have such an Aerospike cluster, you can deploy a single-node cluster
in a container using:

```
$ docker run -tid --name aerospike -p 3000:3000 -p 3001:3001 -p 3002:3002 aerospike/aerospike-server:latest
```

These examples cover integration of aerospike monitoring with 

1. NewRelic
1. Datadog
1. AWS Cloudwatch

> **Note**: You need to update the API Key or Access Key in the respective configuration files.

## NewRelic 
### modify newrelic-otel-collector-config.yml and update below key with respective values 
###### <NEWRELIC-API-KEY> 
### To start the stack pointing to NewRelic
```
$ docker-compose -f newrelic-docker-compose.yml up
```
## To stop the stack
```
$ docker-compose -f newrelic-docker-compose.yml down
```
Now simply point your browser at NewRelic cloud https://one.newrelic.com/data-explorer to see Aerospike metrics.

## Datadog
### modify datadog-otel-collector-config.yml and update below key with respective values 
###### <DATADOG-APP-KEY> 
### To start the stack pointing to Datadog
```
$ docker-compose -f datadog-docker-compose.yml up
```

## To stop the stack
```
$ docker-compose -f datadog-docker-compose.yml down
```
Now simply point your browser at Datadog cloud https://app.datadoghq.com/metric/explorer to see Aerospike metrics.

## Cloudwatch
### modify cloudwatch-docker-compose.yml and update below keys with respective values 
###### AWS_REGION=<AWS_REGION_LOCATION>
###### AWS_ACCESS_KEY_ID=<MENTION-YOUR-AWS-CLOUD-WATCH-KEY>
###### AWS_SECRET_ACCESS_KEY=<MENTION-YOUR-AWS-CW-SECRET-ACCESS-KEY>
### To start the stack pointing to AWS Cloudwatch
```
$ docker-compose -f cloudwatch-docker-compose.yml up
```

Now simply point your browser at AWS Cloudwatch to see Aerospike metrics.

## To stop the stack
```
$ docker-compose -f cloudwatch-docker-compose.yml down
```
