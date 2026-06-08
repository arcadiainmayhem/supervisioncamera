#!/bin/bash
sudo apt update && sudo apt upgrade -y
sudo apt install -y python3-picamera2 libcap-dev python3-opencv

python3 -m venv venv --system-site-packages
source venv/bin/activate
pip install flask

# Static IP on eth0 for direct connection to main Pi
sudo nmcli con add type ethernet ifname eth0 con-name eth0-static \
  ipv4.addresses 192.168.2.2/24 \
  ipv4.method manual

sudo nmcli con up eth0-static