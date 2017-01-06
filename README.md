# Maplin Robot Arm GUI for Linux
## Introduction
This is a python script that connect to the Maplin (A37JN) \ Velleman KSR10 USB robotic arm and displays a simple GUI to control it.

It also allow you the record your robotic arm actions and play them back. These recording can be save to a file and reopen inside the program at a later date.
## Installing on GNU/Linux Systems
These instructions are for Debian-based systems. Instructions for other flavors of GNU/Linux should be similar.

Install python and libusb:

    $ sudo apt-get install python libusb-1.0-0

Download the pyusb repositories https://github.com/walac/pyusb 

To install, unzip, navigate to the folder and type:

    $ sudo python setup.py install

You now you have everything you need to run the robot arm code. Download this repositories navigate to the folder and make the file executable

    $ sudo chmod +x RoboticArm.py

## Usage 

    $ sudo ./RoboticArm.py

## Troubleshooting
### Cannot find my device
if you get the message "USB arm cannot be found" first thing is check that it is connect, switch on and the batteries have charge
if you still get the message your device may have a different “product id” my USB robotic arm is 0001. Too check this plug in the USB robotic arm and in the terminal type: 

	$ dmesg | grep 1267
    
You should get a message back like below:

	usb 1-1: New USB device found. idVendor=1267, idProduct=0001
    
Open “RoboticArm.py” in a text editor and modify the line to match your settings

	RobotArm = usb.core.find(idVendor=0x1267, idProduct=0x001)

### Linux - permissions

You will either need to run as root (not recommended) or modify your system to allow all users access to the device.

    sudo nano /etc/udev/rules.d/42-usb-arm-permissions.rules

and add:

    SUBSYSTEM=="usb", ATTR{idVendor}=="1267", ATTR{idProduct}=="0000", MODE:="0666"

Plug in the device and you should be able to access it without being root.
