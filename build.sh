#!/bin/bash
sudo podman pull caddy
sudo podman build -t localhost/naive/caddy .
