# Apache2 Setup

## Install

```bash
sudo apt install apache2 -y
sudo systemctl start apache2
sudo systemctl enable apache2
```

## Verify

```bash
curl http://192.168.56.12
```

Should return the target web page.

## Notes
- Victim IP: 192.168.56.12
- Interface: enp0s8
- Apache serves on port 80
- Web root: /var/www/html/
