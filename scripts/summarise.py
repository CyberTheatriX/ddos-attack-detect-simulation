#!/usr/bin/env python3
"""
summarise.py - reads Suricata's eve.json after an attack
and prints a summary of what was detected
"""

import json
import os
import sys
from collections import defaultdict

EVE_LOG = "/var/log/suricata/eve-wazuh.json"
DDOS_SIDS = {9000001, 9000002}

RULE_NAMES = {
    9000001: "HTTP flood baseline threshold exceeded",
    9000002: "HTTP flood high volume detected"
}


def load_alerts(filepath):
    if not os.path.exists(filepath):
        print(f"Error: {filepath} not found. Is Suricata running?")
        sys.exit(1)

    alerts = []
    with open(filepath, "r") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                event = json.loads(line)
            except json.JSONDecodeError:
                continue

            if event.get("event_type") != "alert":
                continue

            sid = event.get("alert", {}).get("signature_id")
            if sid not in DDOS_SIDS:
                continue

            alerts.append(event)

    return alerts


def summarise(alerts):
    by_ip = defaultdict(int)
    by_rule = defaultdict(int)
    timestamps = []

    for event in alerts:
        src = event.get("src_ip", "unknown")
        sid = event.get("alert", {}).get("signature_id", 0)
        ts = event.get("timestamp", "")

        by_ip[src] += 1
        by_rule[sid] += 1
        if ts:
            timestamps.append(ts)

    print("=" * 55)
    print("  DDoS Simulation — Detection Summary")
    print("=" * 55)
    print(f"\n  Total alerts      : {len(alerts)}")
    print(f"  Unique source IPs : {len(by_ip)}")
    print(f"  First alert       : {min(timestamps) if timestamps else 'n/a'}")
    print(f"  Last alert        : {max(timestamps) if timestamps else 'n/a'}")

    print("\n  Alerts by rule:")
    for sid, count in by_rule.items():
        print(f"    {RULE_NAMES.get(sid, sid)}: {count}")

    print("\n  Alerts by source IP:")
    for ip, count in sorted(by_ip.items(), key=lambda x: x[1], reverse=True):
        bar = "█" * min(count, 30)
        print(f"    {ip:<18} {count:>4} alerts  {bar}")

    print("\n" + "=" * 55)


def main():
    alerts = load_alerts(EVE_LOG)
    if not alerts:
        print("No DDoS alerts found. Run the attack first.")
        return
    summarise(alerts)


if __name__ == "__main__":
    main()
