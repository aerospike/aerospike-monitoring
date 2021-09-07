# Aerospike Monitoring Stack
The Aerospike Monitoring Stack is now **generally available** (GA). If you're an enterprise customer feel free to reach out to support with any questions.
We appreciate feedback from community members on the [issues](https://github.com/aerospike/aerospike-monitoring/issues).

## Docs
The [Aerospike Monitoring Stack](https://www.aerospike.com/docs/tools/monitorstack/index.html) documentation has been moved to https://docs.aerospike.com

## Examples

### Easy single node Aerospike monitoring stack

A single command is needed to deploy containers for the entire monitoring stack for a single node cluster.
```
$ cd examples/easy
$ docker-compose -f easy-compose.yml up
```
See [documentation](examples/easy/).

### Swarm

Deploy monitoring stack using swarm.  See [documentation](examples/swarm/).
