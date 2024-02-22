#!/bin/bash

aerolab cluster create -n dc1 -c 1 --customconf="./aerospike.conf" --toolsconf="./astools.conf" --instance e2-standard-2 --zone us-central1-a --disk pd-balanced:20 --disk pd-ssd:40 --disk pd-ssd:40
aerolab cluster create -n dc2 -c 3 --customconf="./aerospike.conf" --toolsconf="./astools.conf"  --instance  e2-standard-2 --zone us-central1-a --disk pd-balanced:20 --disk pd-ssd:40 --disk pd-ssd:40



aerolab xdr connect -S dc1 -D dc2 -M test
aerolab conf adjust -n dc1 set "xdr.dc dc2.auth-mode" internal
aerolab conf adjust -n dc1 set "xdr.dc dc2.auth-user" user1
aerolab conf adjust -n dc1 set "xdr.dc dc2.auth-password-file" /etc/password.txt
aerolab files upload -n dc1 password.txt /etc/password.txt


aerolab attach asadm \
--name="dc1" -- \
-e asadm \
-U admin \
-P admin \
-e 'enable; manage acl create user user1 password Wmr4gJgh roles truncate sindex-admin user-admin data-admin read-write read write read-write-udf sys-admin udf-admin'

aerolab attach asadm \
--name="dc1" -- \
-e asadm \
-U admin \
-P admin \
-e 'enable; manage acl create user user2 password Wmr4gJgh roles truncate sindex-admin user-admin data-admin read-write read write read-write-udf sys-admin udf-admin'

aerolab attach asadm \
--name="dc2" -- \
-e asadm \
-U admin \
-P admin \
-e 'enable; manage acl create user user1 password Wmr4gJgh roles truncate sindex-admin user-admin data-admin read-write read write read-write-udf sys-admin udf-admin'

aerolab attach asadm \
--name="dc2" -- \
-e asadm \
-U admin \
-P admin \
-e 'enable; manage acl create user user2 password Wmr4gJgh roles truncate sindex-admin user-admin data-admin read-write read write read-write-udf sys-admin udf-admin'

aerolab attach asadm \
--name="dc1" -- \
-e asadm \
-U admin \
-P admin \
-e 'enable; manage acl delete user admin'

aerolab attach asadm \
--name="dc2" -- \
-e asadm \
-U admin \
-P admin \
-e 'enable; manage acl delete user admin'



aerolab aerospike restart -n dc1



aerolab cluster add exporter -n dc1 -o ape1.toml
aerolab cluster add exporter -n dc2 -o ape2.toml

aerolab client create ams -n ams -s dc1,dc2 --instance e2-medium --zone us-central1-a --disk pd-balanced:20 -e 3000:3000
aerolab client attach  -n ams -- grafana-cli plugins install grafana-polystat-panel
aerolab client attach  -n ams -- grafana-cli plugins install jdbranham-diagram-panel
aerolab client attach  -n ams -- service grafana-server restart
