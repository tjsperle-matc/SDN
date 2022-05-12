##Tyler Sperle - 04/20/2022

import xml.etree.ElementTree as ET #These are all of our imported modules to help us utilize netconfand xml
import xmltodict
import xml.dom.minidom
from lxml import etree
from ncclient import manager

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

def validateDevice(deviceIP, routers):
    validDevice = False #validDevice is False until a host IP is matched with the user input

    for device, info in routers.items(): #This iterates through each key/value in the "routers" dictionary
        
        if deviceIP == info["host"]: #If the user inputted deviceIP is equal to a host IP in "routers", validDevice turns True
            validInt = True

    return validDevice #validDevice returns either true or false depending on the input


def updateAddr(router, intIP, intMask):
    xmlInt = """<config xmlns:xc="urn:ietf:params:xml:ns:netconf:base:1.0" xmlns = "urn:ietf:params:xml:ns:netconf:base:1.0">  
                    <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
                            <interface>
                                <%intName%>
                                    <name>%intNum%</name>
                                    
                                    <ip>                                    
                                        <address>
                                            <primary>
                                                <address>%addr%</address>
                                                <mask>%mask%</mask>
                                             </primary>
                                        </address>                                   
                                    </ip>				
                                </GigabitEthernet>
                            </interface>
                        
                    </native>
            </config>"""     

    xmlInt = xmlInt.replace("%addr%", intIP)
    xmlInt = xmlInt.replace("%intName%", "GigabitEthernet")
    xmlInt = xmlInt.replace("%intNum%", "2")
    xmlInt = xmlInt.replace("%mask%", intMask)

    with manager.connect(host=router['host'],port=router['port'],username=router['username'],password=router['password'],hostkey_verify=False) as m:

        netconf_reply = m.edit_config(target = 'running', config = xmlInt)
        
    return netconf_reply

def printTable(interfaces):
    print("Interface" + "\t\t" + "IP Address" + "\t" + "Subnet Mask") #This prints the header for the table

    print("-" * 55, sep="") #This prints a separator for the table

    for interface in interfaces: #This for loop iterates through each interface in the interfaces list
        intType = interface["type"] #This defines the interface type

        if intType["#text"] == "ianaift:ethernetCsmacd": #If the interface is an ethernet interface, it will print its name, IP, mask, and description
            intName = interface["name"] #This defines the interface name
            intIP = interface["ipv4"]["address"]["ip"] #This defines the interface IP address
            intMask = interface["ipv4"]["address"]["netmask"] #This defines the interface subnet mask
            
            print(intName + "\t" + intIP + "\t" + intMask ) #This prints the interface name, IP, and mask into the table

#Main
routers = {
    "dist-rtr01" : {
        "host": "10.10.20.175",
        "port" : "830",
        "username":"cisco",
        "password":"cisco"
        },
    
    "dist-rtr02" : {
        "host": "10.10.20.176",
        "port" : "830",
        "username":"cisco",
        "password":"cisco"
        }
    }


for device, rtrInfo in routers.items():
    interfaces = netCONF(rtrInfo) #This converts are NETCONF reply into the list "interfaces"

    print(device)
    print("")

    printTable(interfaces) #This prints out each interface name, IP, mask, and description from the interfaces list
    print("")
