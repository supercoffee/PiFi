

### Basic steps

####Locating your raspberry Pi on the network

A quick nmap scan will reveal it. Adjust the IP range according to your own network configuration. 

```

$ sudo nmap -sN 192.168.0.1-254

...

Nmap scan report for 192.168.2.2
Host is up (0.0011s latency).
All 1000 scanned ports on 192.168.2.2 are open|filtered
MAC Address: B8:27:EB:48:25:AD (Raspberry Pi Foundation)

Nmap done: 254 IP addresses (2 hosts up) scanned in 41.21 seconds
```

### Running Ansible to configure

1. Place the IP address into the `hosts` file.
2. Run `ansible-playbook -i hosts pifi.yml --tags=wireless --ask-pass -u root`