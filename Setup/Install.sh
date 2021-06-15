#!/bin/bash
echo "Enter static IP:"
read static_ip
echo "Enter routers IP:"
read router_ip
sudo apt-get update && sudo apt-get upgrade -y
sudo apt-get install python3-pip -y
sudo apt-get install python3-rpi.gpio python3-rpi.gpio -y
sudo pip3 install sparkfun-qwiic-scmd
sudo raspi-config nonint do_camera 0
sudo sh -c "echo 'dtparam=i2c_arm=on' >> /boot/config.txt"
sudo service dhcpcd start
sudo systemctl enable dhcpcd
echo "interface wlan0" >> /etc/dhcpcd.conf
echo "static ip_address=${static_ip}/24" >> /etc/dhcpcd.conf
echo "static routers=${router_ip}" >> /etc/dhcpcd.conf
echo "static domain_name_servers=${router_ip} 8.8.8.8 4.4.4.4" >> /etc/dhcpcd.conf
echo "find . -name \".git\" -type d | sed 's/\/.git//' |  xargs -P10 -I{} git -C {} pull" >> /etc/rc.local
sudo /home/pi/LTG-RC-Car/ServiceMaker.sh
cd /home/pi
git clone https://github.com/silvanmelchior/RPi_Cam_Web_Interface.git
cd RPi_Cam_Web_Interface
./install.sh --sk
