#!/bin/bash

aerolab cluster stop -n dc1
aerolab cluster stop -n dc2
aerolab client stop -n ams
aerolab cluster destroy -n dc1
aerolab cluster destroy -n dc2
aerolab client destroy -n ams

rm aerospike-server-enterprise*
