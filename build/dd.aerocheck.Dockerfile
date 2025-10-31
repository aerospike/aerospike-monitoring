FROM gcr.io/datadoghq/agent:latest

USER root

RUN apt-get update && apt-get install -y gettext-base && rm -rf /var/lib/apt/lists/*

# install the published Aerospike Enterprise integration into the agent's embedded env
RUN /opt/datadog-agent/bin/agent/agent integration install -t datadog-aerospike_enterprise==1.0.0 --allow-root

# copy template file
COPY config/datadog/aero_check_conf.yaml.template /etc/datadog-agent/conf.d/aerospike_enterprise.d/aero_check_conf.yaml.template

# create default conf.yaml with default values
RUN cp /etc/datadog-agent/conf.d/aerospike_enterprise.d/conf.yaml.example /etc/datadog-agent/conf.d/aerospike_enterprise.d/conf.yaml
RUN chown dd-agent:root /etc/datadog-agent/conf.d/aerospike_enterprise.d
RUN chown dd-agent:root /etc/datadog-agent/conf.d/aerospike_enterprise.d/*

COPY scripts/docker-entrypoint.sh /docker-entrypoint.sh


# back to dd-agent user (the base image runs as this)
ENTRYPOINT [ "/docker-entrypoint.sh" ]

#USER dd-agent



