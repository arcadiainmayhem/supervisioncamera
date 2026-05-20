#!/bin/bash
sudo apt update && sudo apt upgrade -y
sudo apt install -y python3-picamera2 libcap-dev python3-opencv

python3 -m venv venv --system-site-packages
source venv/bin/activate
pip install flask