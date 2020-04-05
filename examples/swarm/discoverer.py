#!/usr/bin/env python

# Copyright 2020 Aerospike All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


import argparse
import socket
import subprocess
import sys
import time
from collections import Counter
import logging
import urllib3
import json


ips = []

args = None


def parseArgs():
    global args
    parser = argparse.ArgumentParser()

    parser.add_argument("--fqdn", "--servicename",
                        dest="servicename", help="The FQDN to resolve")
    parser.add_argument("-p", "--port", dest="port",
                        default=3002, help="The heartbeat port")
    parser.add_argument("--dns-api-endpoint-port", "--api-endpoint-port", dest="apiendpoint",
                        default=8080, help="DNS api endpoint port")
    parser.add_argument("--domain", "--dns-domain", dest="dnsdomain", default="aero",
                        help="DNS domain, if set to aero, container can be accessed using aero1.aerospike.com")
    parser.add_argument("--dns-secret", "--dnssecret",
                        dest="dnssecret", help="dns secret")
    parser.add_argument("-i", "--interval", dest="interval", default=10,
                        type=float, help="The DNS polling interval in s. Defaults to 10")
    parser.add_argument("-v", "--verbose", dest="verbose",
                        action="store_true", help="Print status changes")
    parser.add_argument("-o", "--once", dest="once",
                        action="store_true", help="Run only once. Do not poll")
    parser.add_argument("--master", "--master-ip", dest="masterip",
                        help="Swarm Master IP")
    args = parser.parse_args()


def runCMD(cmd):
    # sys_cmd = "/usr/bin/asinfo -h %s -v \"tip=host=%s;port=$s\""%(host,target,port)
    proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    sys.stdout.write("\n")
    result = proc.stdout.read()
    if args.verbose:
        logging.info("%s %s : %s" % (time.strftime(
            "%Y-%m-%d %H:%M:%S", time.gmtime()), "Running command", cmd))
        logging.info(result)
    return result


def addNode(IP, cluster):
    for node in cluster:
        command = "/usr/bin/asinfo -h %s -v \"tip:host=%s;port=%s\"" % (
            node, IP, args.port)
        runCMD(command)


def removeNode(IP, cluster):
    for node in cluster:
        tipclear = "/usr/bin/asinfo -h %s -v \"tip-clear:host-port-list=%s;%s\"" % (
            node, IP, args.port)
        runCMD(tipclear)
        alumniReset = "/usr/bin/asinfo -h %s  -v 'services-alumni-reset'" % node
        runCMD(alumniReset)


# monitor DNS

parseArgs()

http = urllib3.PoolManager()

logger = logging.getLogger()
logger.setLevel(logging.INFO)

handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.INFO)
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)

logger.addHandler(handler)

if args.verbose:
    logger.info("%s %s : %s" % (time.strftime(
        "%Y-%m-%d %H:%M:%S", time.gmtime()), "arguments", args))

lastKnownIPs = []
ips_for_dns_update = []
while True:
    try:
        ips = socket.gethostbyname_ex(args.servicename)[2]
    except socket.gaierror as e:
        logger.info("%s %s" %
                    (time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime()), e[1]))
        if e[0] == -2:
            # EAI_NONAME/resolve error: may mean cluster is destroyed but discovery is kept running
            logger.info("DNS cleared, resetting history")
            lastKnownIPs = []
            continue
        else:
            # any others, retry
            if args.verbose:
                logger.info("%s %s" % (time.strftime(
                    "%Y-%m-%d %H:%M:%S", time.gmtime()), "unable to connect, fast retry"))
            time.sleep(1)
            continue
    except:
        # other connection/resolve error: fast retry
        if args.verbose:
            logger.info("%s %s" % (time.strftime(
                "%Y-%m-%d %H:%M:%S", time.gmtime()), "unable to connect, fast retry"))
        time.sleep(1)
        continue
    # if no DNS change, sleep
    logger.info("%s %s : %s" % (time.strftime(
        "%Y-%m-%d %H:%M:%S", time.gmtime()), "Found IPs:", ips))

    if set(ips_for_dns_update) != set(ips):
        ips_for_dns_update = ips
        ips_for_dns_update.sort()
        for i in range(len(ips_for_dns_update)):
            r = http.request('GET', "http://"+str(args.masterip)+":"+str(args.apiendpoint)+"/update?secret="+str(args.dnssecret)+"&domain="+str(args.dnsdomain)+str(
                i+1)+"&addr="+str(ips_for_dns_update[i]))
            if r.status == 200:
                logger.info("%s %s : %s" % (time.strftime(
                    "%Y-%m-%d %H:%M:%S", time.gmtime()), "Successfully added DNS record for IP: ", ips_for_dns_update[i]))
            else:
                logger.warn("%s %s : %s" % (time.strftime(
                    "%Y-%m-%d %H:%M:%S", time.gmtime()), "Couldn't add DNS record for IP: ", ips_for_dns_update[i]))
                logger.warn("%s %s : %s" % (time.strftime(
                    "%Y-%m-%d %H:%M:%S", time.gmtime()), json.loads(r.data.decode('utf-8'))['json']))

    if Counter(ips) == Counter(lastKnownIPs):
        time.sleep(args.interval)
        continue
    # if complete DNS change, tip everyone
    if len([val for val in ips if val in lastKnownIPs]) == 0:
        addNode(ips[0], ips)
    else:
        # Clear removed nodes
        for oldHost in lastKnownIPs:
            if oldHost not in ips:
                removeNode(oldHost, ips)
        # Add new nodes
        for newHost in ips:
            if newHost not in lastKnownIPs:
                addNode(newHost, lastKnownIPs)
    lastKnownIPs = ips
    if args.verbose:
        logger.info("%s %s : %s" % (time.strftime(
            "%Y-%m-%d %H:%M:%S", time.gmtime()), args.servicename, lastKnownIPs))
    if args.once:
        logger.info("%s Info command(s) sent. `--once` flag set. Exiting sucessfully" %
                    (time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())))
        sys.exit(0)
