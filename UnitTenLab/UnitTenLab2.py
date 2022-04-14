##Tyler Sperle - 04/06/2022

import requests ## This imports the requests module
requests.packages.urllib3.disable_warnings() ## This disables the unsecure request warning
import json ## This imports the json module

def getIntRest(ipAddr): #This function returns an interface dictionary using RESTCONF
    url = "https://" + ipAddr + ":443/restconf/data/ietf-interfaces:interfaces" #This is the device url we are accessing

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

def changeAddr(ipAddr, intName, intIP, intMask): #This function updates an IP address on an interface using RESTCONF
    url = "https://" + ipAddr + ":443/restconf/data/ietf-interfaces:interfaces/interface=" + intName #This is the device url we are accessing
    username = 'cisco'
    password = 'cisco'
    payload={"ietf-interfaces:interface": { #This is our payload with the supplied intName, intIP, and intMask information
                        "name": intName,
                        "description": "Configured by RESTCONF",
                        "type": "iana-if-type:ethernetCsmacd",
                        "enabled": "true",
                                         "ietf-ip:ipv4": {
                                                                "address": [{
                                                                    "ip": intIP,
                                                                    "netmask": intMask
                                                                    
                                                                            }   ]
                                                            }
                                            }
             }

    headers = {
      'Authorization': 'Basic cm9vdDpEX1ZheSFfMTAm',
      'Accept': 'application/yang-data+json',
      'Content-Type': 'application/yang-data+json'
    }

    response = requests.request("PUT", url, auth=(username,password),headers=headers, verify = False, data=json.dumps(payload)
    )
    return response #This is our returned response

def validateIP(ipString): ##This function takes the user's IP input and validates it's a real IP address.
    validIP = True

    octets = ipString.split(".") ##This splits the input into four separate strings that can be iterated

    if len(octets) != 4: ##If the length is 4, it passed the first test and it can proceed
        validIP = False
        
        
    else: ##iterate octets and test one at a time to confirm all of the address is numeric and within the correct range
        for octet in octets:
            if octet.isnumeric() == True: ##check if the octet is numeric
                if int(octet) < 0 or int(octet) > 255: ##invalid range
                    validIP = False

            else:
                validIP = False

    return validIP ##If everything passes, "validIP" remains true and returns the valid IP address

def validateMask(maskString): ##This function takes the user's subnet mask input and validates it's a real mask.
    validMask = True

    octets = maskString.split(".") ##This splits the input into four separate strings that can be iterated
    
    if len(octets) != 4: ##If the length is 4, it passed the first test and it can proceed
        validMask = False
            
    else: ##iterate octets and test one at a time to confirm all of the address is numeric and within the correct range
        for octet in octets:
            if octet.isnumeric() == True: ##check if the octet is numeric
                if int(octet) < 0 or int(octet) > 255: ##invalid range
                    validMask = False

            else:
                validMask = False

    return validMask ##If everything passes, "validMask" remains true and returns the valid subnet mask


def validateInt(intName, intList):
    validInt = False #validInt is False until a interface name is matched with the user input

    for interface in intList: #This iterates through each interface in the supplied intList
        
        if intName == interface["name"]: #If the user inputted intName is equal to a interface name in intList, validInt turns True
            validInt = True

    return validInt #validInt returns either true or false depending on the input

def printInts(intDict):
    for interface in intDict: #This iterates throught the "intDict" dictionary
        
        if interface["type"] == "iana-if-type:ethernetCsmacd": #If the interface type is an ethernetCsmacd, it will proceed to print the information
            intIP = interface["ietf-ip:ipv4"]["address"][0]["ip"] #This declares where the IP address resides
            intMask = interface["ietf-ip:ipv4"]["address"][0]["netmask"] #This declares where the subnet mask resides
            print(interface["name"] + "\t" + intIP + "\t" + intMask) #This prints each interfaces: interface name, IP address, and subnet mask
                   
#Main
ipAddr = "10.10.20.175" #This is the management IP address of IOSXE device "dist-rtr01"
intList = getIntRest(ipAddr) #This gets the interface information
printInts(intList) #This prints the desired information from the "intList"
print("")
intName = input("Please enter the interface name you'd like to configure: ") #This asks the user to enter an interface name
print("")
if validateInt(intName, intList) == True: #If the supplied intName is in intList, it will proceed
    intIP = input("Please enter a new IP address for " + intName + ": ") #This asks the user to enter an IP address for the interface
    print("")
    if validateIP(intIP) == True: #If the supplied IP address is valid, it will proceed
        intMask = input("Please enter a new subnet mask for " + intName + ": ") #This asks the user to enter a subnet mask for the interface
        print("")
        if validateMask(intMask) == True: #If the supplied subnet mask is valid, it will proceed
            updateAddr = changeAddr(ipAddr, intName, intIP, intMask) #This runs the function changeAddr and updates the IP address using RESTCONF
            print("The interface has successfully been updated!") #This lets you know the interface has been updated
            print("")
            
        else:
            print("That is not a valid subnet mask") #If the subnet mask isn't valid, it will print this statement
            print("")
    else:
        print("That is not a valid IP Address") #If the IP address isn't valid, it will print this statement
        print("")
else:
    print("That is not a valid interface name") #If the interface name isn't valid, it will print this statement
    print("")

intList = getIntRest(ipAddr) #This gets the interface information
printInts(intList) #This prints the desired information from the "intList"
