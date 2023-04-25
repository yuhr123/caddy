# caddy
A script for create a Caddy container quickly.

## Requirements

- Linux system using systemd
- Podman
- Python 3.6+
- a domain name
- a public IP address

## Quickstart

1. Bind your domain name to the public IP.
2. Create a workspace

```shell
mkdir caddy && cd caddy
```
3. Download the script

```shell
curl -LO https://raw.githubusercontent.com/yuhr123/caddy/main/run.py
```

4. Running the script

```shell
sudo python3 run.py
```

The scirpt will build a custom caddy image and create a container with it, and then create a systemd serivce for that container.

5. Manage your caddy container

```shell
# Check status
sudo systemctl status container-caddy

# stop caddy
sudo systemctl stop container-caddy

# restart caddy
sudo systemctl restart container-caddy
```


