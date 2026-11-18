"""The Aerospike launchpad: one page in Dynatrace's Launchpads app that says
which dashboard answers which question, and links to each.

deploy.py builds it from SECTIONS after deploying the dashboards, linking
each through its share link so it opens for anyone in the environment.
Edit the wording here, not in the app: the next deploy overwrites it.
"""

from __future__ import annotations

import uuid

NAME = "Aerospike: start here"

INTRO = """# Aerospike monitoring

Dashboards for your Aerospike clusters, from the metrics of the Aerospike \
Prometheus exporter. **Not sure where to look? Start with Cluster Overview**, \
then follow the section below that matches your question.

Every dashboard has pickers at the top -- the cluster, and where it applies \
node, namespace, set or XDR datacenter. Tiles stay empty for features a \
cluster doesn't use (XDR, secondary indexes, users...).
"""

# (title, description, [(generated file stem, title, why you would open it)])
SECTIONS = [
    (
        "Is the cluster healthy?",
        "Start here: a first look, then narrow down to a node or a namespace.",
        [
            (
                "core-cluster",
                "Cluster Overview",
                "The first stop. Nodes, roster, memory, CPU, network, and read/write TPS for the whole cluster.",
            ),
            (
                "core-node",
                "Node Overview",
                "One node looks different from the others: its uptime, connections, resources and errors, side by side.",
            ),
            (
                "core-namespace",
                "Namespace View",
                "One namespace in detail: throughput by type, objects, storage, defrag, migrations, indexes.",
            ),
        ],
    ),
    (
        "Why is it slow?",
        "Latency, throughput and the host underneath.",
        [
            (
                "usecases-node_and_host",
                "Node & Host view",
                "Aerospike latency, throughput and migrations next to the host's CPU, memory, disk and network, per node.",
            ),
            (
                "host-hostview",
                "Host View",
                "The operating system alone: CPU, memory, disk I/O and network per host.",
            ),
            (
                "usecases-batch_transactions_view",
                "Batch Transactions View",
                "Batch reads, writes, deletes and UDFs, direct and proxied: when the application uses batches.",
            ),
            (
                "core-latency",
                "Latency View",
                "Latency percentiles. Not available in Dynatrace yet: each tile shows the equivalent Prometheus query.",
            ),
        ],
    ),
    (
        "Replication between sites (XDR)",
        "Is data reaching the other datacenter, and how do the sites compare?",
        [
            (
                "core-xdr",
                "XDR View",
                "Per destination: lag, throughput, retries, errors. Open it when lag grows or a site falls behind.",
            ),
            (
                "usecases-datacenter_comparision",
                "Datacenter Comparison",
                "Two clusters side by side -- resources, throughput, objects per namespace -- to spot drift between sites.",
            ),
            (
                "core-geoview",
                "Multi Cluster View",
                "All clusters on one page: latency and XDR lag (the map and topology panels are notes for now).",
            ),
        ],
    ),
    (
        "Data, capacity and indexes",
        "How much is stored, where, and what is it costing?",
        [
            (
                "core-set",
                "Set Dashboard",
                "Objects, data used and indexes per set: which sets grow.",
            ),
            ("core-uniquedata", "Unique Data Usage", "Unique data size per namespace."),
            (
                "usecases-sindex_summary_view",
                "Secondary Index Summary",
                "All secondary indexes of a namespace: entries, memory, garbage collection, queries.",
            ),
            (
                "core-sindex",
                "Secondary Index View",
                "One secondary index in detail: entries, memory, garbage collection, load time.",
            ),
            (
                "usecases-read_lru_cache_view",
                "LRU Cache View",
                "For namespaces used as a cache: touches, throughput, objects and expirations.",
            ),
            (
                "usecases-all_flash",
                "All Flash",
                "For namespaces with the primary index on flash: index, data and OS resources.",
            ),
        ],
    ),
    (
        "Changes and operations",
        "During maintenance, and for specific features.",
        [
            (
                "usecases-rolling_restart",
                "Rolling Restarts",
                "Watch this while restarting or upgrading nodes one by one: errors, migrations, resources.",
            ),
            (
                "usecases-mrt_view",
                "MRT View",
                "Multi-record transactions: commits, rollbacks, errors and timeouts, the monitor set.",
            ),
            (
                "core-users",
                "Users View",
                "Per-user connections, TPS and quotas. Empty unless security is enabled with users configured.",
            ),
            (
                "core-alertsview",
                "Alerts View",
                "Alerts by severity. Not available in Dynatrace yet: the alerts are Prometheus rules, not Dynatrace ones.",
            ),
        ],
    ),
]


def _id() -> str:
    return str(uuid.uuid4())


def build(urls: dict[str, str]) -> dict:
    """The launchpad's content; urls maps a generated file stem to the link
    to open. Dashboards without a link (not deployed) are left out."""
    blocks = [
        {
            "id": _id(),
            "type": "markdown",
            "properties": {"expanded": True},
            "content": INTRO,
        }
    ]
    for title, description, items in SECTIONS:
        links = [
            {
                "id": _id(),
                "type": "link",
                "title": name,
                "action": {"type": "openExternalLink", "url": urls[stem]},
                "icon": "/platform/app-engine/registry/v1/app-icons/dynatrace.dashboards",
                "description": why,
            }
            for stem, name, why in items
            if stem in urls
        ]
        if links:
            blocks.append(
                {
                    "id": _id(),
                    "type": "links",
                    "properties": {"expanded": True},
                    "appearance": "list",
                    "title": title,
                    "description": description,
                    "contentType": "static",
                    "content": links,
                }
            )
    return {
        "schemaVersion": 2,
        "icon": "default",
        "background": "default",
        "containerList": {
            "containers": [{"blocks": blocks, "horizontalLayoutWeight": 1}]
        },
    }


def stems() -> set[str]:
    return {stem for _, _, items in SECTIONS for stem, _, _ in items}


def purpose(stem: str) -> str:
    """What the dashboard with this generated file stem is for."""
    for _, _, items in SECTIONS:
        for s, _, why in items:
            if s == stem:
                return why
    raise KeyError(f"{stem} is not on the launchpad: add it to SECTIONS")
