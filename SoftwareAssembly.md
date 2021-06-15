# Software Assembly Guide


## Imaging Micro SD Card

Download the *.img file to your local folder on your laptop

Use an imaging tool such as Balena Etcher https://www.balena.io/etcher/ to write the .img file to your SD card by selecting the image and your micro sd card slot. Then select flash!

Once the image is flashed, take out the micro SD card and insert it back into your computer. 

Open up the notepad and hit space once. Then save this file and name the file ssh and click all files in the file type selector. 

Open up notepad again and type in the text below.
```
country=US
ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
update_config=1

network={
    ssid="herolabcar"
    psk="herolabcar"
}
network={
    ssid="Name of Network"
    psk="Password of Network"
}
```
If your network is not listed, add in your network name and password in the open option. Once you have named this file wpa_supplicant.conf and selected the All Files option, you may save this file. 

Drag and drop these files onto your raspberry pi boot drive.

## Creating Your Own Hotspot from Your Windows Laptop

Select the Start  button, then select Settings  > Network & Internet > Mobile hotspot.

For Share my Internet connection from, choose the Internet connection you want to share.

Select Edit > enter a new network name and password > Save.

Turn on Share my Internet connection with other devices.

To connect on the other device, go to the Wi-Fi settings on that device, find your network name, select it, enter the password, and then connect.

## Set Static IP Address
If you used the image provided, the car will not have a static IP address.  If you would like to set one, that can be done with the command 
```
sudo /home/pi/LTG-RC-Car/SetStaticIP.sh
```
It will prompt you to provide a static IP, use the range 192.168.0.0 – 192.168.255.255, and then type in your routers IP address or the default gateway. This will likely be 192.168.1.1 or 192.168.0.1.

If you are using the installation script, you do not need to independently set the static IP. It will be apart of the installation script.

## Installing the Software Manually

If you would like to install and setup the software manually, you may use the scripts within this repo for manual installation. For instructions on how to connect the raspberry pi to your network and install Stock Raspbian Buster, follow these instructions, [Setup Raspberry PI](https://desertbot.io/blog/headless-pi-zero-w-wifi-setup-windows) Now that you have installed raspbian and have connected to the Raspberry Pi through your ssh client, you need to run two commands before we start our installation scripts.
```
sudo apt-get update && sudo apt-get upgrade -y && sudo apt-get install git -y
```
To use download and run the scripts within this repo, you must first clone the repo with the command
```
git clone https://github.com/andersonmolter1/LTG-RC-Car/
```
The script we will be running below will prompt ask for what you would like the static ip of the raspberry pi to be, enter it and hit enter and allow the installation to proceed. The command to run this script is below.
```
sudo ./LTG-RC-Car/Setup/Install.sh
```
A prompt will open up with different options for the camera setup after a little while, just hit enter and let the installation proceed.

Once it is over, you will be prompted with a decision if you want to Auto-Start the cam stream when the pi is turned on, hit enter at this option selecting Yes.

## How to run? 
Guess what! The script is already running if you flashed the image to your micro sd or used the installation script. All operations that the car requires are now running as a service, which means they run at boot of the pi. If the car cannot be connected to, first check to see if the service named LTG is running with the command below.
```
sudo systemctl status LTG.service
```
If this comes back that is not running, you can re-create the service by running the ServiceMaker.sh script and this will re-create the service. If that fails as well, you can manually run the script for car operations with the command below.
```
python3 LTG-RC-Car\AI_Driver\main.py
```


## Authors

* **Anderson Molter** - (https://github.com/andersonmolter1)
* **Sanjay Sarma** - (https://github.com/sanjayovs)
* PI: Prof. Ramviyas Parasuraman - HeRoLab UGA - (http://hero.uga.edu)

