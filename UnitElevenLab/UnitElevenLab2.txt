##Tyler Sperle - 04/13/2022

import xml.etree.ElementTree as ET #These are all of our imported modules to help us utilize netconf, xml, and ordered dictionaries
import xmltodict
import xml.dom.minidom
from lxml import etree
from ncclient import manager
from collections import OrderedDict

#Functions
def netCONF(router):
    netconf_filter = """

    <interfaces xmlns="urn:ietf:params:xml:ns:yang:ietf-interfaces">
        <interface></interface>
    </interfaces>
       
    """

    with manager.connect(host=router['host'],port=router['port'],username=router['username'],password=router['password'],hostkey_verify=False) as m:

        netconf_reply = m.get_config(source = 'running', filter = ("subtree",netconf_filter)) #This sends the request and houses the reply
        
    netconf_data = xmltodict.parse(netconf_reply.xml)["rpc-reply"]["data"] #This parses through the reply in XML

    interfaces = netconf_data["interfaces"]["interface"] #This defines are list of interface dictionaries

    return interfaces

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

def validateInt(intName, interfaces):
    validInt = False #validInt is False until an interface name is matched with the user input

    for interface in interfaces: #This iterates through each interface in the supplied interfaces list
        
        if intName == interface["name"]: #If the user inputted intName is equal to a interface name in interfaces, validInt turns True
            validInt = True

    return validInt #validInt returns either true or false depending on the input

def changeInterface(interfaces, intName, intIP, intMask, intDesc): #This function takes an interface dictionary and changes the IP, mask, and description
    for i in range(len(interfaces)): #This iterates through each dictionary in the list
        if intName == interfaces[i]["name"]: #Once the user inputted intName matches an interface name, it will change the info only on that interface
            interfaces[i]["ipv4"]["address"]["ip"] = intIP #This changes the interface IP address
            interfaces[i]["ipv4"]["address"]["netmask"] = intMask #This changes the interface subnet mask
            interfaces[i]["description"] = intDesc #This changes the interface description

    return interfaces #This returns the new interfaces list

def printTable(interfaces):
    print("Interface" + "\t\t" + "IP Address" + "\t" + "Subnet Mask" + "\t\t" + "Description") #This prints the header for the table

    print("-" * 88, sep="") #This prints a separator for the table

    for interface in interfaces: #This for loop iterates through each interface in the interfaces list
        intType = interface["type"] #This defines the interface type

        if intType["#text"] == "ianaift:ethernetCsmacd": #If the interface is an ethernet interface, it will print its name, IP, mask, and description
            intName = interface["name"] #This defines the interface name
            intIP = interface["ipv4"]["address"]["ip"] #This defines the interface IP address
            intMask = interface["ipv4"]["address"]["netmask"] #This defines the interface subnet mask
            intDesc = interface["description"] #This defines the interface description
            
            print(intName + "\t" + intIP + "\t" + intMask + "\t\t" + intDesc) #This prints the interface name, IP, mask, and description into the table

        if intType["#text"] == "ianaift:softwareLoopback": #If the interface is a loopback interface, it will just print its name
            print(interface["name"]) #This prints the loopback interface
     
#Main        
router = {"host": "10.10.20.175", "port" : "830", #This is our router information housing the IP address, port number, username, and password credentials
          "username":"cisco","password":"cisco"}

interfaces = netCONF(router) #This converts are NETCONF reply into the list "interfaces"

printTable(interfaces) #This prints out each interface name, IP, mask, and description from the interfaces list

print("")

intName = input("Please enter the interface name you'd like to configure: ") #This asks the user to enter an interface name
print("")
if validateInt(intName, interfaces) == True: #If the supplied intName is in interfaces, it will proceed
    intIP = input("Please enter a new IP address for " + intName + ": ") #This asks the user to enter an IP address for the interface
    print("")
    if validateIP(intIP) == True: #If the supplied IP address is valid, it will proceed
        intMask = input("Please enter a new subnet mask for " + intName + ": ") #This asks the user to enter a subnet mask for the interface
        print("")
        if validateMask(intMask) == True: #If the supplied subnet mask is valid, it will proceed
            intDesc = input("Please enter a description for " + intName + ": ") #This asks the user to enter an interface description
            updatedInterface = changeInterface(interfaces, intName, intIP, intMask, intDesc) #This runs "changeInterface" using the given parameters
            print("")
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

printTable(updatedInterface) #This prints out each interface name, IP, mask, and description from the updatedInterface list
