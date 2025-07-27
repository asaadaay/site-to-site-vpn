#!/bin/bash

sudo apt update
sudo apt install -y strongswan

echo "net.ipv4.ip_forward = 1" | sudo tee -a /etc/sysctl.conf
sudo sysctl -p