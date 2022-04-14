##Tyler Sperle - 04/04/2022

import requests ## This imports the requests module
requests.packages.urllib3.disable_warnings() ## This disables the unsecure request warning
import json ## This imports the json module

def getInts(deviceIP): #This function accepts a deviceIP and returns an interface dictionary
    url = "https://" + deviceIP + ":443/restconf/data/ietf-interfaces:interfaces" #This is the device url we are accessing

    username = 'cisco' #This is the username credential
    password = 'cisco' #This is the password credential
    payload={} #The payload is empty
    headers = {
      'Content-Type': 'application/yang-data+json',
      'Accept': 'application/yang-data+json',
      'Authorization': 'Basic cm9vdDpEX1ZheSFfMTAm'
    }

    response = requests.request("GET", url, auth = (username,password), verify = False, headers=headers, data=payload).json()
    interfaces = response["ietf-interfaces:interfaces"]["interface"] #Our response is first converted to json, then it's sliced down to the interfaces

    return interfaces #This is our returned interface dictionary

def printInt(intDict):
    for interface in intDict: #This iterates throught the "intDict" dictionary
        
        if interface["type"] == "iana-if-type:ethernetCsmacd": #If the interface type is an ethernetCsmacd, it will proceed to print the information
            intIP = interface["ietf-ip:ipv4"]["address"][0]["ip"] #This declares where the IP address resides
            intMask = interface["ietf-ip:ipv4"]["address"][0]["netmask"] #This declares where the subnet mask resides
            print(interface["name"] + "\t" + intIP + "\t" + intMask) #This prints each interfaces: interface name, IP address, and subnet mask
                   
#Main
deviceIP = "10.10.20.175" #This is the management IP address of IOSXE device "dist-rtr01"
intDict = getInts(deviceIP) #This gets the interfaces model
printInt(intDict) #This iterates the dictionary that is returned
