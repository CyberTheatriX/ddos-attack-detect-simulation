# Custom DDoS Detection Rules

Two rules written for this lab, saved in local.rules.

## Rule 1 — SID 9000001 — Baseline threshold
Fires when one IP sends more than 100 HTTP requests in 10 seconds.
Normal human browsing never reaches this rate. Flags automated traffic.

## Rule 2 — SID 9000002 — Flood threshold
Fires when one IP sends more than 500 HTTP requests in 5 seconds.
This rate indicates a deliberate flood, not just a busy script.

## Why two rules?
The two-tier approach lets us distinguish between suspicious automated
traffic and an active flood. Useful for alert prioritisation in a SOC.

## Key rule option — track by_src
Counts requests per source IP individually. This means in a distributed
attack, each attacker is tracked separately rather than as combined volume.
