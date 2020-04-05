# Example - Aerospike Cluster With Monitoring Stack On Docker Swarm

## Pre-Requisites

- A swarm cluster.

    This example also describes creation of a swarm cluster using `docker-machine` and `virtualbox` driver.

## Steps

1. Create a swarm cluster.

    For this example, let's create a three node swarm cluster.

    Create three docker hosts -  `swarm0`, `swarm1` and `swarm2`

    ```sh
    $ docker-machine create -d virtualbox swarm0
    $ docker-machine create -d virtualbox swarm1
    $ docker-machine create -d virtualbox swarm2
    ```

    SSH into `swarm0`, and run `docker swarm init` to initialize a swarm with `swarm0` as manager.

    ```sh
    $ docker-machine ssh swarm0
    ```
    ```sh
    $ docker swarm init --advertise-addr 192.168.99.100


    Swarm initialized: current node (le3p93oniquktlhs0nx4iryfk) is now a manager.

    To add a worker to this swarm, run the following command:

        docker swarm join --token SWMTKN-1-2q1xnl53i3xzxxgirxus8j6dpiwq83efnhqpmg1096s1y02f67-8949delsqf5vkwozlt4rusziu 192.168.99.100:2377

    To add a manager to this swarm, run 'docker swarm join-token manager' and follow the instructions.
    ```

    SSH into `swarm1` and `swarm2` and run the above `docker swarm join` command to join them as worker nodes.

    ```sh
    $ docker-machine ssh swarm1
    ```
    ```sh
    $ docker swarm join --token SWMTKN-1-2q1xnl53i3xzxxgirxus8j6dpiwq83efnhqpmg1096s1y02f67-8949delsqf5vkwozlt4rusziu 192.168.99.100:2377
    ```

2. Once the swarm cluster is created, SSH into swarm manager and clone this repository.

    ```sh
    $ git clone https://github.com/aerospike/aerospike-monitoring.git
    cd aerospike-monitoring/examples/swarm/
    ```

3. Set necessary environment variables used in [`docker-stack.yaml`](docker-stack.yaml).

    ```sh
    export MANAGER_NODE_IP=192.168.99.100
    export GRAFANA_DASHBOARDS_DIR=/home/docker/aerospike-monitoring/config/grafana/dashboards/
    export GRAFANA_PROVISIONING_DIR=/home/docker/aerospike-monitoring/config/grafana/provisioning/
    export FEATURE_KEY_FILE=<feature_key_file_path>
    export AEROSPIKE_ALERT_RULES_FILE=/home/docker/aerospike-monitoring/config/prometheus/aerospike_rules.yml
    export ALERTMANAGER_CONFIG_FILE=/home/docker/aerospike-monitoring/config/prometheus/alertmanager.yml
    ```

4. Deploy the stack.

    The stack `docker-stack.yaml` includes the following:
    - Aerospike cluster,
    - Aerospike prometheus exporter,
    - Prometheus server (with pre-configured Aerospike alert rules),
    - Grafana server (with pre-configured dashboards),
    - Alertmanager,
    - A DNS server for aerospike nodes discovery,
    - A discoverer container to dynamically add and remove nodes from aerospike cluster and to add DNS records for individual aerospike containers.

    ```sh
    env \
    MANAGER_NODE_IP=${MANAGER_NODE_IP} \
    GRAFANA_DASHBOARDS_DIR=${GRAFANA_DASHBOARDS_DIR} \
    GRAFANA_PROVISIONING_DIR=${GRAFANA_PROVISIONING_DIR} \
    FEATURE_KEY_FILE=${FEATURE_KEY_FILE} \
    AEROSPIKE_ALERT_RULES_FILE=${AEROSPIKE_ALERT_RULES_FILE} \
    ALERTMANAGER_CONFIG_FILE=${ALERTMANAGER_CONFIG_FILE} \
    docker stack deploy -c docker-stack.yaml aero
    ```

    > When scaling up/down the `aerospike` service, `exporter` service also needs to be scaled up/down respectively. There should be 1-1 mapping between the exporters and aerospike containers.

5. Check status of all services

    ```sh
    $ docker service ls

    ID                  NAME                MODE                REPLICAS            IMAGE                                            PORTS
    b9a607jfi3v9        aero_aerodns        replicated          1/1                 davd/docker-ddns:latest                          *:53->53/tcp, *:8080->8080/tcp, *:53->53/udp
    dy2m6j894hq0        aero_aerospike      replicated          3/3                 aerospike/aerospike-server-enterprise:latest     
    ifmp20e7m2vn        aero_alertmanager   replicated          1/1                 prom/alertmanager:latest                         *:9093->9093/tcp
    ke5bqx6ld30i        aero_discoverer     replicated          1/1                 spkesan/aerospike-tools:latest                   
    3xdxg8im0m83        aero_exporter       replicated          3/3                 aerospike/aerospike-prometheus-exporter:latest   
    792c1plcdby5        aero_grafana        replicated          1/1                 grafana/grafana:6.3.2                            *:3000->3000/tcp
    4lwwn5kf36km        aero_prometheus     replicated          1/1                 prom/prometheus:v2.11.1                          *:9090->9090/tcp
    ```

6. Grafana and Prometheus dashboards can be accessed at `http://<MANAGER_NODE_IP>:3000` and `http://<MANAGER_NODE_IP>:9090` respectively.