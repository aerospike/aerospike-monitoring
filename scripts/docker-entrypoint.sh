#!/bin/sh
set -e

export AS_HOST=${AS_HOST:-"http://127.0.0.1:9145/metrics"}

if [ -f /etc/datadog-agent/conf.d/aerospike_enterprise.d/aero_check_conf.yaml.template ]; then
        env | while IFS= read -r line; do
                name=${line%%=*}
                value=${line#*=}
                if [ -n "$value" ]; then
                        sed -i --regex "s/# (.*\{$name\}.*)/\1/" /etc/datadog-agent/conf.d/aerospike_enterprise.d/aero_check_conf.yaml.template
                fi
        done
        envsubst < /etc/datadog-agent/conf.d/aerospike_enterprise.d/aero_check_conf.yaml.template > /etc/datadog-agent/conf.d/aerospike_enterprise.d/conf.yaml
fi

#if [ "${1:0:1}" = '-' ]; then
set -- /opt/datadog-agent/bin/agent/agent run "$@"
#fi

#exec /opt/datadog-agent/bin/agent/agent run "$@"

exec "$@"
