# DDoS Attack Detection Simulation

A home lab I built to understand how distributed HTTP flood attacks work
and how Suricata IDS detects them.

The setup uses Docker containers as multiple attackers, Apache2 as the
target web server, and Suricata with custom rules to catch the flood.

## Lab Components

| Component | Role |
|---|---|
| Docker containers (x10) | Simulate 10 independent attackers |
| Apache2 | Target web server receiving the flood |
| Suricata IDS | Detects the attack via custom rules |
| Python scripts | Monitor and summarise Suricata alerts |

## Architecture diagram and full setup guide added as the lab is built.
