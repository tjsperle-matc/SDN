##Tyler Sperle - 04/04/2022

import requests ## This imports the requests module
requests.packages.urllib3.disable_warnings() ## This disables the unsecure request warning
import json ## This imports the json module

url = "https://10.10.20.175:443/restconf/data/ietf-interfaces:interfaces" #This is the device url we are accessing


username = 'cisco' #This is the username credential
password = 'cisco' #This is the password credential
payload={} #The payload is empty
headers = {
  'Content-Type': 'application/yang-data+json',
  'Accept': 'application/yang-data+json',
  'Authorization': 'Basic cm9vdDpEX1ZheSFfMTAm'
}

response = requests.request("GET", url, auth = (username,password), verify = False, headers=headers, data=payload)

print(response.text) #This is our returned response printed in text
