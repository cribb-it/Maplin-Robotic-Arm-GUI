# Maplin Robot Arm GUI for Linux
## Introduction
## Installing on GNU/Linux Systems
These instructions are for Debian-based systems. Instructions for other flavors of GNU/Linux should be similar.

Install python and libusb:

    $ sudo apt-get install python libusb-1.0-0

Download the pyusb repositories https://github.com/walac/pyusb to install unzip navigate to the folder and type:

    $ sudo python setup.py install

You now you have everything you need to run the robot arm code. Download this repositories navigate to the folder and make the file executable

    $ sudo chmod +x RoboticArm.py

## Usage 

    $ sudo ./RoboticArm.py

