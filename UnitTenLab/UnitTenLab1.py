##Tyler Sperle - 04/06/2022

import requests ## This imports the requests module
requests.packages.urllib3.disable_warnings() ## This disables the unsecure request warning
import json ## This imports the json module

def getIntRest(ipAddr): #This function accepts a deviceIP and returns an interface dictionary
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

def getIntRestMAC(ipAddr): #This function accepts a deviceIP and returns an interface dictionary
    url = "https://" + ipAddr + ":443/restconf/data/interfaces-state" #This is the device url we are accessing

    username = 'cisco' #This is the username credential
    password = 'cisco' #This is the password credential
    payload={} #The payload is empty
    headers = {
      'Content-Type': 'application/yang-data+json',
      'Accept': 'application/yang-data+json',
      'Authorization': 'Basic cm9vdDpEX1ZheSFfMTAm'
    }

    response = requests.request("GET", url, auth = (username,password), verify = False, headers=headers, data=payload).json()
    interfaces = response["ietf-interfaces:interfaces-state"]["interface"] #Our response is first converted to json, then it's sliced down to the interfaces

    return interfaces #This is our returned interface dictionary

def combineIntLists(intList, intStateList):
    newList = []
    
    for interface in intList: #This iterates through each interface in "intList"
        if interface["type"] == "iana-if-type:ethernetCsmacd": #If the interface type is an ethernetCsmacd, it will proceed to print the information
            intName = interface["name"] #This declares the interface name
            intIP = interface["ietf-ip:ipv4"]["address"][0]["ip"] #This declares the interface IP address
            
            for value in intStateList: #This iterates through each interface in "intStateList"
                if interface["name"] == value["name"]: #If the interface names match from each list, it will store the MAC address value
                    intMAC = value["phys-address"] #This declares the interface MAC address
            
            newList.append({"intName": intName, "intIP": intIP, "intMAC": intMAC}) #This appends the needed information into the "newList"

    return newList #This is our returned list

def printList(combinedIntList):
    print("Int" + "\t\t\t" + "IP" + "\t\t" + "Physical") #This prints the header objects for the table
    print("-" * 57,sep="") #This prints the divider for the table
    for interface in combinedIntList: #This iterates throught the "combinedIntList" dictionary
        print(interface["intName"] + "\t" + interface["intIP"] + "\t" + interface["intMAC"]) #This prints each interfaces: name, IP, and MAC
                   
#Main
ipAddr = "10.10.20.175" #This is the management IP address of IOSXE device "dist-rtr01"
intList = getIntRest(ipAddr) #This gets the interface information
intStateList = getIntRestMAC(ipAddr) #This gets the interface state information
combinedIntList = combineIntLists(intList, intStateList) #This combines key elements of both lists into one list that can be iterated
printList(combinedIntList) #This prints the desired information from the new "combinedIntList"
