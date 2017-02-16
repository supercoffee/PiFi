# PiFi

Turn your Raspberry Pi into a wireless access point. 

## Setup

###Flash the raspbian minimal image

1. Download image from https://minibianpi.wordpress.com/
2. Follow [instructions](http://elinux.org/RPi_Easy_SD_Card_Setup#Using_the_Linux_command_line) to flash base OS image to the SD card. 
3. Plug in the ethernet cable, WiFi card, SD card, and power to the Raspberry Pi.


####Locating your raspberry Pi on the network

You'll need to determine the Pi's IP address.
This step assumes that your computer is connected to the same network as the Raspberry Pi's ethernet. 
If you have a keyboard and monitor connected to the Pi, type `ifconfig` to see a list of network interfaces. 

Otherwise, you'll need to do a quick nmap scan to find it. Adjust the IP range according to your own network configuration. (The IP subnet should be the same as your machine.)

```

$ sudo nmap -sN 192.168.0.1-254

...

Nmap scan report for 192.168.2.2
Host is up (0.0011s latency).
All 1000 scanned ports on 192.168.2.2 are open|filtered
MAC Address: B8:27:EB:48:25:AD (Raspberry Pi Foundation)

Nmap done: 254 IP addresses (2 hosts up) scanned in 41.21 seconds
```

### Install dependencies
The minimal raspbian image does not include python. We'll need to install that to run the ansible script for the next step.

Ssh into the Pi.
Substitute the IP address you found from the Nmap scan earlier.
```
$ ssh root@192.168.2.2

```
Install python
```
$ sudo apt-get install python

```

### Install ansible on your machine
This project uses ansible to configure the Raspberry Pi into a WiFi router. Ansible is a general purpose system configuration tool for Unix / Linux systems.  
Follow the [installation guide](https://docs.ansible.com/ansible/intro_installation.html) for installing ansible. Ansible is not Windows compatible, so you'll need to do this step from a Linux or Mac machine.


### Run Ansible to configure

1. Place the IP address into the `hosts` file.
2. Run `ansible-playbook -i hosts pifi.yml --tags=wireless --ask-pass -u root`
3. Make coffee.  Step 2 will take a while.

If you don't see any red error messages, your Raspberry Pi has been successfully configured as a WiFi access point.  

#Tweaking configurations 

The ansible playbook contains all the configuration files relevant to the access point functionality. 

#### WiFi settings
__File:__ `roles/ap/defaults/main.yml`
__Update command:__ `ansible-playbook -i hosts pifi.yml --tags=wireless --ask-pass -u root --tags=wireless`.

