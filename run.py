#!/usr/bin/env python
import os

# Prompt user for input
email = input("请输入您的电子邮件地址：")
domain_name = input("请输入您的域名：")
username = input("请输入您的用户名：")
password = input("请输入您的密码：")

# Generate Caddyfile
caddyfile = f"""
{{
  servers {{
    protocols
  }}
  email {email}
}}

:443, {domain_name} {{
  file_server
  root * /usr/share/caddy
  route {{
    forward_proxy {{
      basic_auth {username} {password}
      hide_ip
      hide_via
      probe_resistance
    }}
  }}
}}

{domain_name}:80 {{
  file_server
  root * /usr/share/caddy
}}
"""

# Write Caddyfile
with open("Caddyfile", "w") as f:
    f.write(caddyfile)

# Generate Dockerfile
dockerfile = """
FROM caddy:builder AS builder
RUN xcaddy build \\
    --with github.com/caddyserver/forwardproxy@caddy2=github.com/klzgrad/forwardproxy@naive

FROM caddy:latest
COPY --from=builder /usr/bin/caddy /usr/bin/caddy
"""

# Write Dockerfile
with open("Dockerfile", "w") as f:
    f.write(dockerfile)
    
# Generate systemd service file
service_file = f"""
Documentation=man:podman-generate-systemd(1)
Wants=network-online.target
After=network-online.target
RequiresMountsFor=%t/containers

[Service]
Environment=PODMAN_SYSTEMD_UNIT=%n
Restart=on-failure
TimeoutStopSec=70
ExecStartPre=/bin/rm -f %t/%n.ctr-id
ExecStart=/usr/bin/podman run \\
       	--cidfile=%t/%n.ctr-id \\
       	--cgroups=no-conmon \\
       	--rm \\
       	--sdnotify=conmon \\
       	--replace \\
       	-d \\
       	--name caddy \\
       	-v {os.getcwd()}/Caddyfile:/etc/caddy/Caddyfile:Z \\
       	-v caddy_data:/data \\
       	-v caddy_conf:/config \\
       	-p 80:80 \\
       	-p 443:443 naive/caddy
ExecStop=/usr/bin/podman stop --ignore --cidfile=%t/%n.ctr-id
ExecStopPost=/usr/bin/podman rm -f --ignore --cidfile=%t/%n.ctr-id
Type=notify
NotifyAccess=all

[Install]
WantedBy=default.target
"""

with open("/lib/systemd/system/container-caddy.service", "w") as f:
    f.write(service_file)

# Build image and start caddy service
confirm_build = input("是否编译镜像？(y/n)")
if confirm_build.lower() == "y":
    os.system("sudo podman pull caddy")
    os.system("sudo podman build -t localhost/naive/caddy .")
    confirm_start = input("是否启动 caddy 并设置为开机自动启动？(y/n)")
    if confirm_start.lower() == "y":
        os.system("sudo systemctl enable --now container-caddy.service")
