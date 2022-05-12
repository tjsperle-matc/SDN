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
