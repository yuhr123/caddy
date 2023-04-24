#!/usr/bin/env python
import os
import subprocess

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

# Prompt user to build Caddy image
if input("是否编译 Caddy 镜像？(y/n)").lower() == "y":
    os.system("sudo podman pull caddy")
    os.system("sudo podman build -t localhost/naive/caddy .")

# Prompt user to run Caddy container
if input("是否运行 Caddy 容器？(y/n) ").lower() == "y":
    os.system("sudo podman rm -f caddy")
    subprocess.run(["sudo", "podman", "run", "-d", "--name", "caddy", 
        "-v", f"{os.getcwd()}/Caddyfile:/etc/caddy/Caddyfile:Z", "-v", 
        "caddy_data:/data", "-v", "caddy_conf:/config", "-p", "80:80", 
        "-p", "443:443", "naive/caddy"])
