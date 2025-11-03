FROM gcr.io/datadoghq/agent:latest

USER root

RUN apt-get update && apt-get install -y gettext-base && rm -rf /var/lib/apt/lists/*

# Install the published Datadog Aerospike Enterprise integration into the agent's embedded env
RUN /opt/datadog-agent/bin/agent/agent integration install -t datadog-aerospike_enterprise==1.0.0 --allow-root

# Copy template file
COPY config/datadog/conf.yaml.template /etc/datadog-agent/conf.d/aerospike_enterprise.d/conf.yaml.template

RUN chown dd-agent:root /etc/datadog-agent/conf.d/aerospike_enterprise.d
RUN chown dd-agent:root /etc/datadog-agent/conf.d/aerospike_enterprise.d/*

COPY scripts/datadog/docker-entrypoint.sh /docker-entrypoint.sh

# back to dd-agent user (the base image runs as this)
ENTRYPOINT [ "/docker-entrypoint.sh" ]
