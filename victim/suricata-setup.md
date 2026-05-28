# Suricata IDS Setup

## Install

```bash
sudo apt install suricata -y
```

Version used: 7.0.3

## Configuration changes in suricata.yaml

**HOME_NET** — tells Suricata what counts as your local network:

```yaml
HOME_NET: "[192.168.56.0/24]"
```

**af-packet** — tells Suricata which interface to monitor:

```yaml
af-packet:
  - interface: enp0s8
```
## Load community rules

```bash
sudo suricata-update
```

Downloads the Emerging Threats Open ruleset.

## Verify

```bash
sudo suricata -T -c /etc/suricata/suricata.yaml
sudo systemctl restart suricata
sudo systemctl status suricata
```

## Log files

| File | Contents |
|---|---|
| /var/log/suricata/fast.log | Quick one-line alert summary |
| /var/log/suricata/eve.json | Full structured alert data in JSON |
