# Regular Expressions for Aerospike log parsing

This document outlines how Aerospike server logs can be ingested and parsed as fields into 3rd party log management tools, 
around 150 unique regular expression are created to parse various logs.

In this document we are providing details and steps for 2 popular log ingestion tools
* Fluent-bit, and
* Splunk 

> **Note**: These regular expression can parse logs from Aerospike server 6.x and above

> **Note**: Currently Multi-line log parsing is not supported

# fluent-bit ( https://docs.fluentbit.io/manual )

If you are using fluent-bit as your log ingestion agent, then follow below provided guidelines.

Below are the two fluent-bit configurations relatated to Aerospike logs

1. fluent-bit-aerospike-parsers.conf
2. fluent-bit-aerospike.conf

Follow below steps to use and configure fluent-bit to process Aerospike logs

1. copy fluent-bit-aerospike-parsers.conf to folder /etc/fluent-bit/
2. open /etc/fluent-bit/fluent-bit.conf
3. search and update the value of the "parsers_file" key under "SERVICE" section  to /etc/fluent-bit/fluent-bit-aerospike-parsers.conf
4. restart fluent-bit agent

```
[SERVICE]
    .....
    # Parsers File
    # ============
    # specify an optional 'Parsers' configuration file
    # parsers_file /root/fluentbit/parsers.conf
    parsers_file /etc/fluent-bit/fluent-bit-aerospike-parsers.conf
    ....
```

> **NOTE**: multiple parsers can be mentioned or provided in fluent-bit config, please refer https://docs.fluentbit.io/manual/administration/configuring-fluent-bit/classic-mode/configuration-file

We strongly recommend to use a differnt index in Elasticsearch when ingesting Aerospike server logs.

# splunk (https://www.splunk.com)

If you are using splunk, then follow below provided steps to parse logs as individual fields during log ingestion into splunk

Below are the two Splunk configurations relatated to Aerospike logs

1. splunk-aerospike-local_props.conf
2. splunk-aerospike-local_transforms.conf

In your splunk indexer machine 
1. goto $SPLUNK_HOME (like /etc/splunk)
2. cd system/local
3. copy splunk-aerospike-local_props.conf and rename as props.conf
4. copy splunk-aerospike-local_transforms.conf and rename as transforms.conf

If you already have a props.conf and transform.conf in your $SPLUNK_HOME/system/local folder, then,
- append splunk-aerospike-local_props.conf contents to your existing $SPLUNK_HOME/system/local/props.conf
- append  splunk-aerospike-local_transforms.conf to your $SPLUNK_HOME/system/local/transforms.conf

We strongly recommend to import Aerospike logs under a separate "sourcetype".
