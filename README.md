This repo contains Aerospike's monitoring solution with Prometheus + Grafana.

Steps to use:

1. ./aerospike-prometheus-exporter -h <server_node> -p 3000 -b :9145 -tags agent1,very_nice`  runs the agent.
1. for a second agent on the same machine, bind it to a different port: `go build . && ./aerospike-prometheus-exporter -h <server_node> -p 3000 -b :9146 -tags agent1,very_nice`
1. Edit `docker/prometheus/prometheus.yml` and change the target IPs to aerospike-prometheus-exporter installations.
1. Run `docker-compose up` to download, build and run the docker images. To stop the containers, run `docker-compose down`
1. Go to your browser and use the URL: `http://localhost:3000`. User/Pass is `admin/pass`
1. Prometheus dashboard is at: `http://localhost:9090`
    1. To make a dashboard your default, first choose that dashboard, and then star it on the toolbar on top right of the screen. After that, you can go to grafana preferences and choose that starred dashboard as default.

Enjoy!

Please send your feedback via email to khosrow@aerospike.com
