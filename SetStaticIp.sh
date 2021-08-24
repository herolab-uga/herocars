#!/bin/bash
echo "Enter static IP:"
read static_ip
echo "Enter routers IP:"
read router_ip
sudo service dhcpcd start
sudo systemctl enable dhcpcd
echo "interface wlan0" >> /etc/dhcpcd.conf
echo "static ip_address=${static_ip}/24" >> /etc/dhcpcd.conf
echo "static routers=${router_ip}" >> /etc/dhcpcd.conf
echo "static domain_name_servers=${router_ip} 8.8.8.8 4.4.4.4" >> /etc/dhcpcd.conf