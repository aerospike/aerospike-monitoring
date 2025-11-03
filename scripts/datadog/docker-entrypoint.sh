#!/bin/sh
set -e

# Set the default AS_HOST to http://127.0.0.1:9145/metrics
export AS_HOST=${AS_HOST:-"http://127.0.0.1:9145/metrics"}

env | while IFS= read -r line; do
        # Get the name and value of the environment variable and do uncomment only if value is not empty
        name=${line%%=*}
        value=${line#*=}
        if [ -n "$value" ]; then
                # Uncomment the line in the template file, if the config-key name is in 'env' variable list
                sed -i --regex "s/# (.*\{$name\}.*)/\1/" /etc/datadog-agent/conf.d/aerospike_enterprise.d/aero_check_conf.yaml.template
        fi
done

# Substitute the environment variables in the template file and save the result to the conf.yaml file
envsubst < /etc/datadog-agent/conf.d/aerospike_enterprise.d/aero_check_conf.yaml.template > /etc/datadog-agent/conf.d/aerospike_enterprise.d/conf.yaml

set -- /opt/datadog-agent/bin/agent/agent run "$@"

exec "$@"

