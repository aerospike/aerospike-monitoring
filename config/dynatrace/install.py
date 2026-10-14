#!/usr/bin/env python3
"""Install the Aerospike dashboards in a Dynatrace environment: a guided
walkthrough from creating the access token to a launchpad your users start
from. Python 3.9+ only, no packages to install.

    python3 install.py                 # asks for everything it needs
    python3 install.py --dry-run       # checks everything, changes nothing

It walks through:

  1. the environment's address, and a platform token (how to create one);
  2. a check that the Aerospike metrics are arriving;
  3. a check of every dashboard query with Dynatrace;
  4. creating (or, on a re-run, updating) each dashboard, shared read-only
     with everyone in the environment;
  5. the launchpad "Aerospike: start here", which says which dashboard
     answers which question, linking each;
  6. optionally, making that launchpad the home launchpad of user groups.

Re-running it updates the same dashboards and launchpad in place (fixed
ids), so it is also how a newer version is installed. Edits made to them in
Dynatrace are overwritten by the next run.

Without prompts, for automation: --env URL, the token in the environment
variable DT_PLATFORM_TOKEN, --home-group ID (repeatable), --yes.
"""

from __future__ import annotations

import argparse
import getpass
import json
import os
import pathlib
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
import uuid

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import launchpad  # noqa: E402

ID_PREFIX = "aerospike-"
LAUNCHPAD_ID = "aerospike-launchpad"
HOME_SCHEMA = "app:dynatrace.launcher:home.launchpad"
SETTINGS = "/platform/classic/environment-api/v2/settings"

SCOPES = [
    ("document:documents:read", "find the dashboards on a re-run"),
    ("document:documents:write", "create and update the dashboards and launchpad"),
    ("document:environment-shares:read", "find their shares on a re-run"),
    (
        "document:environment-shares:write",
        "share them with everyone in the environment",
    ),
    ("storage:metrics:read", "check the metrics are there, and check the queries"),
    ("storage:buckets:read", "the same"),
    ("settings:objects:read", "only to set a home launchpad (step 6)"),
    ("settings:objects:write", "only to set a home launchpad (step 6)"),
]


# ------------------------------------------------------------ the API


class Client:
    """Dynatrace platform APIs, with a platform token (Bearer)."""

    def __init__(self, base: str, token: str):
        if not base.startswith("https://"):
            sys.exit(f"expected an https:// Dynatrace URL, got {base}")
        self.base = base
        self._token = token

    def call(
        self,
        method: str,
        path: str,
        body: bytes | None = None,
        ctype: str | None = None,
    ):
        req = urllib.request.Request(self.base + path, data=body, method=method)
        req.add_header("Authorization", f"Bearer {self._token}")
        req.add_header("Accept", "application/json")
        if ctype:
            req.add_header("Content-Type", ctype)
        try:
            with urllib.request.urlopen(
                req, timeout=60
            ) as r:  # nosec B310 -- base is https://, checked in __init__
                data = r.read()
                return r.status, json.loads(data) if data else {}
        except urllib.error.HTTPError as e:
            text = e.read().decode(errors="replace")
            try:
                return e.code, json.loads(text)
            except ValueError:
                return e.code, {"raw": text[:500]}

    def multipart(self, method: str, path: str, fields: dict[str, str], content: bytes):
        boundary = uuid.uuid4().hex
        parts = [
            f'--{boundary}\r\nContent-Disposition: form-data; name="{k}"\r\n\r\n{v}\r\n'.encode()
            for k, v in fields.items()
        ]
        parts.append(
            f'--{boundary}\r\nContent-Disposition: form-data; name="content"; filename="content.json"\r\n'
            "Content-Type: application/json\r\n\r\n".encode() + content + b"\r\n"
        )
        parts.append(f"--{boundary}--\r\n".encode())
        return self.call(
            method, path, b"".join(parts), f"multipart/form-data; boundary={boundary}"
        )

    def query(self, dql: str) -> tuple[list, list[str]]:
        """Run a DQL query: (records, Dynatrace's notifications)."""
        status, res = self.call(
            "POST",
            "/platform/storage/query/v1/query:execute",
            json.dumps({"query": dql, "requestTimeoutMilliseconds": 30000}).encode(),
            "application/json",
        )
        while status in (200, 202) and res.get("state") not in (
            "SUCCEEDED",
            "FAILED",
            "CANCELLED",
            None,
        ):
            tok = urllib.parse.quote(res["requestToken"])
            status, res = self.call(
                "GET",
                f"/platform/storage/query/v1/query:poll?request-token={tok}&request-timeout-milliseconds=10000",
            )
        if status not in (200, 202) or res.get("state") != "SUCCEEDED":
            raise RuntimeError(f"query failed ({status}): {json.dumps(res)[:300]}")
        result = res["result"]
        notes = [
            n.get("message", "")
            for n in (
                result.get("metadata", {}).get("grail", {}).get("notifications") or []
            )
        ]
        return result["records"], notes


# --------------------------------------------------------- the steps

VAR = re.compile(r"\$(\w+)(?::\w+)?")


def queries(doc: dict):
    c = doc["content"]
    for v in c.get("variables", []):
        if v.get("type") == "query":
            yield f"picker ${v['key']}", v["input"]
    for k, t in c["tiles"].items():
        if t.get("type") == "data":
            yield f"tile {k} {t.get('title', '')!r}", t["query"]


def verify(client: Client, docs: list[tuple[pathlib.Path, dict]]) -> int:
    """Dynatrace checks every query (pickers replaced by a stand-in value);
    returns how many are invalid."""
    bad = total = 0
    for path, doc in docs:
        for where, q in queries(doc):
            total += 1
            status, res = client.call(
                "POST",
                "/platform/storage/query/v1/query:verify",
                json.dumps({"query": VAR.sub('"x"', q)}).encode(),
                "application/json",
            )
            if status in (401, 403):
                sys.exit(
                    f"query check refused ({status}): the token needs storage:metrics:read. {res}"
                )
            if status != 200 or not res.get("valid"):
                bad += 1
                notes = (
                    "; ".join(
                        n.get("message", "") for n in res.get("notifications", [])
                    )
                    or json.dumps(res)[:300]
                )
                print(f"  INVALID {path.name} {where}: {notes}")
    print(f"  {total} queries checked: {total - bad} valid, {bad} invalid")
    return bad


def share(client: Client, did: str, name: str) -> str:
    """Share read-only with everyone in the environment -- a new document is
    private to the token's owner -- and return the share link. Others get
    access by opening the share link once (the document's own address says
    "you don't have access" until then)."""
    status, res = client.call(
        "POST",
        "/platform/document/v1/environment-shares",
        json.dumps({"documentId": did, "access": "read"}).encode(),
        "application/json",
    )
    if status == 409:  # shared already: find it
        status, res = client.call(
            "GET",
            "/platform/document/v1/environment-shares?"
            + urllib.parse.urlencode({"filter": f"documentId == '{did}'"}),
        )
        found = res.get("environment-shares", []) if status == 200 else []
        res = found[0] if found else {}
    elif status not in (200, 201):
        print(
            f"  {name}: not shared ({status}): {res} -- needs document:environment-shares:write"
        )
        return ""
    return f"{client.base}/ui/document/v0/#share={res['id']}" if res.get("id") else ""


def upsert(client: Client, did: str, name: str, dtype: str, body: dict) -> str:
    """Create or update document did, share it, and return its share link
    (or its own address, if sharing failed)."""
    content = json.dumps(body).encode()
    status, meta = client.call("GET", f"/platform/document/v1/documents/{did}/metadata")
    if status == 200:
        status, res = client.multipart(
            "PATCH",
            f"/platform/document/v1/documents/{did}?optimistic-locking-version={meta['version']}",
            {},
            content,
        )
        action = "updated"
    elif status in (403, 404):
        status, res = client.multipart(
            "POST",
            "/platform/document/v1/documents",
            {"id": did, "name": name, "type": dtype},
            content,
        )
        action = "created"
        if status == 409:
            print(
                f"  exists  {name} ({did}): updating it needs document:documents:read on the token"
            )
            return ""
    else:
        sys.exit(f"{name}: reading {did} failed ({status}): {meta}")
    if status not in (200, 201):
        sys.exit(
            f"{name}: {'creating' if action == 'created' else 'updating'} failed ({status}): {res}"
        )
    url = (
        share(client, did, name)
        or f"{client.base}/ui/apps/dynatrace.{dtype}s/{dtype}/{did}"
    )
    print(f"  {action} {name}")
    return url


def set_home(client: Client, launchpad_id: str, groups: list[str]) -> None:
    """Make the launchpad the home launchpad of each group, keeping the
    environment's other home launchpads (one settings object holds all)."""
    status, res = client.call(
        "GET", f"{SETTINGS}/objects?schemaIds={HOME_SCHEMA}&fields=objectId,value,scope"
    )
    if status != 200:
        print(
            f"  could not read the home launchpads ({status}): {res} -- needs settings:objects:read"
        )
        return
    items = res.get("items", [])
    current = items[0]["value"].get("groupLaunchpads", []) if items else []
    kept = [g for g in current if g.get("userGroupId") not in groups]
    # first, so it ranks highest for these groups
    value = {
        "groupLaunchpads": [
            {"launchpadId": launchpad_id, "userGroupId": g, "isEnabled": True}
            for g in groups
        ]
        + kept
    }
    if items:
        status, res = client.call(
            "PUT",
            f"{SETTINGS}/objects/{items[0]['objectId']}",
            json.dumps({"value": value}).encode(),
            "application/json",
        )
    else:
        body = [{"schemaId": HOME_SCHEMA, "scope": "environment", "value": value}]
        status, res = client.call(
            "POST", f"{SETTINGS}/objects", json.dumps(body).encode(), "application/json"
        )
    if status in (200, 201):
        print(f"  home launchpad set for {len(groups)} group(s)")
    else:
        print(
            f"  could not set the home launchpad ({status}): {json.dumps(res)[:300]} -- needs settings:objects:write"
        )


# ------------------------------------------------------------- helpers


def apps_url(text: str) -> str:
    """https://<id>.apps.dynatrace.com from whatever address was pasted."""
    text = text.strip().rstrip("/")
    m = re.match(
        r"(?:https://)?([a-z0-9-]+)\.(?:live|apps)\.(dynatrace\.com|dynatracelabs\.com)",
        text,
    )
    if m:
        return f"https://{m.group(1)}.apps.{m.group(2)}"
    return text if text.startswith("https://") else f"https://{text}"


def ask(prompt: str, default: str = "") -> str:
    answer = input(f"{prompt}{f' [{default}]' if default else ''}: ").strip()
    return answer or default


def yes(prompt: str, assume: bool) -> bool:
    return True if assume else ask(f"{prompt} (y/n)", "y").lower().startswith("y")


def heading(n: int, text: str) -> None:
    print(f"\n== {n}. {text}")


def dashboards() -> list[tuple[pathlib.Path, dict]]:
    files = sorted(HERE.glob("Aerospike - *.json"))
    if not files:
        sys.exit(
            f"no dashboard files (Aerospike - *.json) next to {pathlib.Path(__file__).name}"
        )
    return [(f, {"name": f.stem, "content": json.loads(f.read_text())}) for f in files]


def doc_id(path: pathlib.Path) -> str:
    """aerospike-cluster-overview, from "Aerospike - Cluster Overview.json"."""
    slug = re.sub(
        r"[^a-z0-9]+", "-", path.stem.lower().removeprefix("aerospike - ")
    ).strip("-")
    return ID_PREFIX + slug


# ---------------------------------------------------------------- main


def main() -> int:
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    ap.add_argument(
        "--env",
        help="the environment's address, e.g. https://abc12345.apps.dynatrace.com",
    )
    ap.add_argument(
        "--home-group",
        action="append",
        default=[],
        help="a user group's ID to give the launchpad as home (repeatable)",
    )
    ap.add_argument(
        "--skip",
        action="append",
        default=[],
        help='a dashboard to leave out, e.g. "All Flash" (repeatable)',
    )
    ap.add_argument(
        "--dry-run", action="store_true", help="check everything, change nothing"
    )
    ap.add_argument(
        "--yes", action="store_true", help="no questions: go ahead where it would ask"
    )
    args = ap.parse_args()

    docs = [
        (p, d)
        for p, d in dashboards()
        if p.stem.removeprefix("Aerospike - ") not in args.skip
    ]
    print(
        f"Aerospike dashboards for Dynatrace: {len(docs)} dashboards and a launchpad to install."
    )

    heading(1, "Your Dynatrace environment and an access token")
    env = apps_url(
        args.env
        or ask(
            "The environment's address (as in your browser, e.g. https://abc12345.apps.dynatrace.com)"
        )
    )
    token = os.environ.get("DT_PLATFORM_TOKEN", "")
    if not token:
        print(
            "\nThis needs a platform token. To create one, in Dynatrace open\n"
            "  Account Management > Identity & access management > Platform tokens > Generate token\n"
            "and give it these scopes:"
        )
        for scope, why in SCOPES:
            print(f"  {scope:36} {why}")
        print(
            "A platform token can do no more than the person who creates it, so that\n"
            "person needs the same permissions. The token is only used for this run:\n"
            "it is not saved anywhere, and you can delete it in Dynatrace afterwards."
        )
        token = getpass.getpass("\nPaste the token (input hidden): ").strip()
    if not token:
        sys.exit("no token given")
    client = Client(env, token)
    print(f"  environment: {env}")

    heading(2, "Are the Aerospike metrics arriving?")
    try:
        records, notes = client.query(
            "timeseries v = avg(aerospike_node_stats_uptime), by: { cluster_name, service }, from: now() - 2h"
        )
    except RuntimeError as e:
        sys.exit(
            f"  {e}\n  Check the address and the token's scopes (storage:metrics:read)."
        )
    for n in notes:
        print(f"  Dynatrace says: {n}")
    clusters = sorted({r.get("cluster_name") or "?" for r in records})
    if records:
        print(
            f"  {len(records)} Aerospike nodes in the last 2 hours, cluster(s): {', '.join(clusters)}"
        )
    else:
        print(
            "  No Aerospike metrics in the last 2 hours. The dashboards will install but stay\n"
            "  empty until the OpenTelemetry Collector ships them (see UPLOAD.md, 'Before you start')."
        )
        if not yes("  Install anyway?", args.yes):
            return 1

    heading(3, "Checking every dashboard query with Dynatrace")
    if verify(client, docs) and not yes(
        "  Some queries are invalid. Install anyway?", args.yes
    ):
        return 1

    if args.dry_run:
        print("\nDry run: everything checked, nothing changed.")
        return 0

    heading(
        4,
        "Installing the dashboards (shared read-only with everyone in the environment)",
    )
    urls = {}
    for path, doc in docs:
        urls[doc["name"].removeprefix("Aerospike - ")] = upsert(
            client, doc_id(path), doc["name"], "dashboard", doc["content"]
        )

    heading(5, "Creating the launchpad")
    stem_of = {
        name: stem for _, _, items in launchpad.SECTIONS for stem, name, _ in items
    }
    links = {
        stem_of[n]: u.removeprefix(client.base)
        for n, u in urls.items()
        if u and n in stem_of
    }
    lp_url = upsert(
        client, LAUNCHPAD_ID, launchpad.NAME, "launchpad", launchpad.build(links)
    )

    heading(6, "A home launchpad for your teams (optional)")
    groups = list(args.home_group)
    if not groups and not args.yes:
        print(
            "  The launchpad can be the first page your teams see in Dynatrace. Enter the IDs of\n"
            "  the user groups to give it to: in Account Management > Identity & access management >\n"
            "  Group management, open a group; its ID is the last part of the page's address.\n"
            "  Leave it empty to skip."
        )
        groups = [
            g.strip()
            for g in ask("  Group IDs, separated by commas").split(",")
            if g.strip()
        ]
    if groups:
        set_home(client, LAUNCHPAD_ID, groups)
    else:
        print("  skipped")

    print(
        f"\nDone. Share this link with your users -- the launchpad, which links every dashboard:\n\n  {lp_url}\n\n"
        "Each person opening it once gets access to it and the dashboards. To keep it one click\n"
        "away, open it and pin it to the Dock (the bar on the left) from the launchpad's menu:\n"
        "Dynatrace keeps pins per user, so each person pins it for themselves.\n\n"
        "The dashboards' own share links:"
    )
    for name, url in sorted(urls.items()):
        print(f"  {name:28} {url}")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        sys.exit("\ncancelled")
