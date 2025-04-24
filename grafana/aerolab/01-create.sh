#!/bin/bash

aerolab cluster create -n dc1 -c 3 --instance e2-standard-2 --zone us-central1-a --disk pd-balanced:20 --disk pd-ssd:40 --disk pd-ssd:40
aerolab cluster create -n dc2 -c 1 --instance  e2-standard-2 --zone us-central1-a --disk pd-balanced:20 --disk pd-ssd:40 --disk pd-ssd:40

aerolab xdr connect -S dc1 -D dc2 -M test,bar

aerolab cluster add exporter -n dc1 -o ape1.toml
aerolab cluster add exporter -n dc2 -o ape2.toml

aerolab client create ams -n ams -s dc1,dc2 --instance e2-medium --zone us-central1-a --disk pd-balanced:20 -e 3000:3000
aerolab client attach  -n ams -- grafana-cli plugins install grafana-polystat-panel
aerolab client attach  -n ams -- grafana-cli plugins install jdbranham-diagram-panel
aerolab client attach  -n ams -- service grafana-server restart


if [ "$1" == "GCP" ]
then
    aerolab config gcp lock-firewall-rules 
fi