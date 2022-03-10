##Tyler Sperle - 03/07/2022

import requests ## This imports the requests module
requests.packages.urllib3.disable_warnings() ## This disables the unsecure request warning
import json ## This imports the json module

##Functions
def showIP(cmdCLI, IP): ## This is a function that sends a CLI command to a network device url, and returns a response

    switchuser='cisco' ## This supplies the devices username
    switchpassword='cisco' ## This supplies the devices password

    url='https://' + IP + '/ins' ## This is the device URL where "IP" is the device's management IP address

    myheaders={'content-type':'application/json-rpc'}
    payload=[
      {
        "jsonrpc": "2.0",
        "method": "cli",
        "params": {
          "cmd": cmdCLI, ## This sends the command to the device
          "version": 1
        },
        "id": 1
      }
    ]

    ## verify=False below is to accept untrusted certificate
    response = requests.post(url,data=json.dumps(payload), verify = False, headers=myheaders,auth=(switchuser,switchpassword)).json() ## This is our
                                                                                                                ##original response converted to json
    intList = response["result"]["body"]["TABLE_intf"]["ROW_intf"] ## This strips the "response" dictionary into the list of all interfaces

    return intList ## This returns the new interface list

def changeAddr(intName, updatedIP, IP): ## This is a function that sends an ip address command to a network device url, and returns a response

    switchuser='cisco' ## This supplies the devices username
    switchpassword='cisco' ## This supplies the devices password

    url='https://' + IP + '/ins' ## This is the device URL where "IP" is the device's management IP address

    myheaders={'content-type':'application/json-rpc'}
    payload=[
      {
        "jsonrpc": "2.0",
        "method": "cli",
        "params": {
          "cmd": "configure terminal", ## This sends the first command to the device
          "version": 1
        },
        "id": 1
      },
      {
        "jsonrpc": "2.0",
        "method": "cli",
        "params": {
          "cmd": "interface " + intName.lower(), ## This sends the second command to the device
          "version": 1
        },
        "id": 2
      },
      {
        "jsonrpc": "2.0",
        "method": "cli",
        "params": {
          "cmd": "ip address " + updatedIP + " 255.255.255.0", ## This sends the third command to the device
          "version": 1
        },
        "id": 3
      }
    ]

    ## verify=False below is to accept untrusted certificate
    response = requests.post(url,data=json.dumps(payload), verify = False, headers=myheaders,auth=(switchuser,switchpassword)).json() ## This is our
                                                                                                                ##original response converted to json
    return response

def printInt(intList): ## This function prints the devices interface names, proto-states, link-states, and IP addresses in a table

    print("Name \t Proto \t Link \t Address") ## This prints the header names

    print("---- \t ----- \t ---- \t -------") ## This prints each divider

    for interface in intList:
        print(interface["intf-name"] + "\t", interface["proto-state"] + "\t", interface["link-state"] + "\t", interface["prefix"]) ## This prints the
                                                                                                                            ##specified device information

def changeIP(intIP, octet, delta):
    octetNum = octet - 1 ##This subtracts 1 from the given octet number so it True list value is correct
    
    octets = intIP.split('.') ##This splits the input into four separate strings that can be iterated

    addOctet = int(octets[octetNum]) + delta ##This adds the given delta number to the correct octet number

    changedOctet = str(addOctet) ##This converts the added octet back into a string
    
    octets[octetNum] = changedOctet ##This will assign the desired octet to the "changedOctet"
    
    newIP = octets[0] + "." + octets[1] + "." + octets[2] + "." + octets[3] ##This reiterates through the octets, changing the desired octet

    return newIP ##This returns the new IP address


##Main
devices = { ## This is my devices dictionary, with device/IP - key/value pairs
    "dist-sw01" : "10.10.20.177",
    "dist-sw02" : "10.10.20.178"
    }

for device, IP in devices.items(): ## This iterates through the devices dictionary
    intList = showIP("show ip interface brief", IP) ## This calls the function "showIP" with a cmd of "show ip interface brief" and an IP address
    print(device) ## This prints the device name
    printInt(intList) ## This calls the function "printInt" using the returned intList from the "showIP" function
    print("")

for device, IP in devices.items(): ## This iterates through the devices dictionary
    changingIntList = showIP("show ip interface brief", IP) ## This calls the function "showIP" with a cmd of "show ip interface brief" and an IP address
    
    for interface in changingIntList: ## This iterates through each interface in the returned "changingIntList"
        intName = interface["intf-name"] ## This assigns the interface name to a variable
        intIP = interface["prefix"] ## This assigns the interface IP to a variable
        
        if intName.startswith("V" or "v"): ## If an interface begins with "V" or "v", it will proceed, if not it will pass the interface
            updatedIP = changeIP(intIP, 4, 5) ## This runs the "changeIP" function by taking the interface IP, and adding 5 to the fourth octet
            changeAddr(intName, updatedIP, IP) ## This runs the "changeAddr" function that pushes the changes to each switch

        else: ## This passes any interface that does NOT begin with "V" or "v"
            pass

print("Updated VLAN IP Addresses") ## This prints a divider message showing the VLAN IP addresses have been updated
print("")

for device, IP in devices.items(): ## This iterates through the devices dictionary
    updatedIntList = showIP("show ip interface brief", IP) ## This calls the function "showIP" with a cmd of "show ip interface brief" and an IP address
    print(device) ## This prints the device name
    printInt(updatedIntList) ## This calls the function "printInt" using the returned updatedIntList from the "showIP" function
    print("")

