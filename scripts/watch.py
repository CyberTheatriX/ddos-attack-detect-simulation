#!/usr/bin/env python3
"""
watch.py - monitors Suricata's eve.json in real time
and prints DDoS alerts as they happen during an attack
"""

import json
import time
import os
import sys

EVE_LOG = "/var/log/suricata/eve-wazuh.json"
DDOS_SIDS = {9000001, 9000002}


def tail(filepath):
    with open(filepath, "r") as f:
        f.seek(0, 2)
        while True:
            line = f.readline()
            if line:
                yield line.strip()
            else:
                time.sleep(0.1)


def print_alert(event, count):
    alert = event.get("alert", {})
    severity = alert.get("severity", 3)
    sid = alert.get("signature_id", "?")
    msg = alert.get("signature", "unknown")
    src = event.get("src_ip", "?")
    dst = event.get("dest_ip", "?")
    ts = event.get("timestamp", "?")

    if severity == 1:
        level = "HIGH"
    elif severity == 2:
        level = "MEDIUM"
    else:
        level = "LOW"

    print(f"[{count}] {ts}")
    print(f"    Level : {level}")
    print(f"    Rule  : {msg} (SID {sid})")
    print(f"    Source: {src} -> {dst}:80")
    print()


def main():
    if not os.path.exists(EVE_LOG):
        print(f"Error: {EVE_LOG} not found. Is Suricata running?")
        sys.exit(1)

    print("=" * 55)
    print("  Suricata DDoS Monitor — waiting for alerts")
    print("=" * 55)
    print()

    count = 0
    for line in tail(EVE_LOG):
        try:
            event = json.loads(line)
        except json.JSONDecodeError:
            continue

        if event.get("event_type") != "alert":
            continue

        sid = event.get("alert", {}).get("signature_id")
        if sid not in DDOS_SIDS:
            continue

        count += 1
        print_alert(event, count)


if __name__ == "__main__":
    main()
