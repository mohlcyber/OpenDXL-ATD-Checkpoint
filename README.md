# OpenDXL-ATD-Checkpoint
This integration is focusing on the automated threat response with McAfee ATD, OpenDXL and Check Point Firewalls.
McAfee Advanced Threat Defense (ATD) will produce local threat intelligence that will be pushed via DXL. An OpenDXL wrapper will 
subscribe and parse IP indicators ATD produced and will automatically update Firewall rules and push new configuration to selected Firewalls.

![61_atd_check_point](https://cloud.githubusercontent.com/assets/25227268/25074725/8f6e1b9c-2302-11e7-84d4-2315f8683e79.PNG)

## Component Description

**McAfee Advanced Threat Defense (ATD)** is a malware analytics solution combining signatures and behavioral analysis techniques to rapidly 
identify malicious content and provides local threat intelligence. ATD exports IOC data in STIX format in several ways including the DXL.
https://www.mcafee.com/in/products/advanced-threat-defense.aspx

**Check Point Firewalls** industry leading Next Generation Firewalls that offer network security protection in an integrated 
next generation firewall platform. https://www.checkpoint.com/products-solutions/next-generation-firewalls/

## Prerequisites
McAfee ATD solution (tested with ATD 3.8)

OpenDXL Python installation
1. Python SDK Installation ([Link](https://opendxl.github.io/opendxl-client-python/pydoc/installation.html))
2. Certificate Files Creation ([Link](https://opendxl.github.io/opendxl-client-python/pydoc/certcreation.html))
3. ePO Certificate Authority (CA) Import ([Link](https://opendxl.github.io/opendxl-client-python/pydoc/epocaimport.html))
4. ePO Broker Certificates Export ([Link](https://opendxl.github.io/opendxl-client-python/pydoc/epobrokercertsexport.html))

Check Point Management R80

## Configuration
McAfee ATD receives files from multiple sensors like Endpoints, Web Gateways, Network IPS or via Rest API. 
ATD will perform malware analytics and produce local threat intelligence. After an analysis every indicator of comprise will be published 
via the Data Exchange Layer (topic: /mcafee/event/atd/file/report). 

### atd_subscriber.py
The atd_subscriber.py receives DXL messages from ATD, filters out discovered IP's and loads cp_push.py.

Change the CONFIG_FILE path in the atd_subscriber.py file.

`CONFIG_FILE = "/path/to/config/file"`

### Check Point Management R80
[Check Point API Reference](https://sc1.checkpoint.com/documents/R80/APIs/#introduction)

Before Firewall Rules can be updated via API it is neccessary to enable the API.

![62_atd_check_point](https://cloud.githubusercontent.com/assets/25227268/25074760/b58a7572-2303-11e7-973b-25e1dddbf93c.PNG)

### cp_push.py
The cp_push.py receives only the discovered malicious IP's and will use API's to update Firewall rules / groups.

Change the username and password as well as the IP addresses. The IP address should point to the Check Point Management Server.

The script will:

1. create a new api session 
2. login
3. check if group exist already and create it if it doesn't
4. check if the host exist already and create it if it doesn't
5. assign the new created host to the group
6. publish the configuration
7. logout

Don't forget to create a new Firewall rule related to the IP list.

![63_atd_check_point](https://cloud.githubusercontent.com/assets/25227268/25074798/102db6f0-2305-11e7-838b-674c8babcdad.PNG)

## Run the OpenDXL wrapper
> python atd_subscriber.py

or

> nohup python atd_subscriber.py &

## Summary
With this use case, ATD produces local intelligence that is immediatly updating cyber defense countermeassures like the 
Check Point Next Generation Firewalls with malicious IP's.
