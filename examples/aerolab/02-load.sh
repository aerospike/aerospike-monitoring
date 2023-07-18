#!/bin/bash

# aerolab attach shell -n dc1 -- asinfo -v "set-config:context=namespace;id=test;set=testset;stop-writes-size=2000"

while true; do aerolab attach shell -n dc1 -- asbench -U user1 -P Wmr4gJgh testset; done;

# asinfo -v "set-config:context=namespace;id=test;set=testset;stop-writes-size=20000000000"
# asinfo -v "set-config:context=namespace;id=test;set=people;stop-writes-size=2000"

#asinfo -v “set-config:context=namespace;id=namespaceName;set=setName;stop-writes-count=2000”