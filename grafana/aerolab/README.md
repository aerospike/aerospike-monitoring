# Aerolab Monitoring Stack Deploy
This provides a a reference architecture of using aerolab to
deploy 2 Aerospike clusters that are connected by XDR and
share a single Monitoring Instance. This is helpful for 
testing multi cluster dashboards.

## Create Clusters 
To test locally using docker.
```text
./01-create.sh
```

To use aws or gcp
```text
./01-create.sh GCP|AWS
```

## Add continus load to cluster(s) using asbench
```text
./02-load.sh
```

## Destroy Cluster
```
./destroy.sh
```

