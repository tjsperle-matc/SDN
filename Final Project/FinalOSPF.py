#Jack Havlicek, Tyler Sperle, Sean Greene 05/11
#This is the script where we fuck about


import json
import requests
requests.packages.urllib3.disable_warnings() ## This disables the unsecure request warning
import xml.etree.ElementTree as ET
import xmltodict
import xml.dom.minidom
from lxml import etree
from ncclient import manager
from collections import OrderedDict



#feature nxapi on NXOS switches, and netconf-yang for IOSXE
def changeOSPF(deviceIP, routerID, ospfIP, ospfMask):
    
    router = {"host": deviceIP, "port" : "830",
              "username":"cisco","password":"cisco"}

    ### xmlns:xc added for ios xe 17.x and greater

    xmlInt = """<config xmlns:xc="urn:ietf:params:xml:ns:netconf:base:1.0" xmlns = "urn:ietf:params:xml:ns:netconf:base:1.0">  
                    <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
                        <router>
                            <ospf xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-ospf">
                                <id>1</id>
                                <router-id>%routerID%</router-id>
                                <redistribute>
                                    <connected>
                                      <redist-options>
                                        <subnets/>
                                      </redist-options>
                                    </connected>
                                </redistribute>
                                <network>
                                    <ip>%ospfIP%</ip>
                                    <mask>%ospfMask%</mask>
                                    <area>0</area>
                                </network>
                            </ospf>
                        </router>
                    </native>
                </config>"""     
            
    print(xmlInt)
    
    xmlInt = xmlInt.replace("%routerID%", routerID)
    xmlInt = xmlInt.replace("%ospfIP%", ospfIP)
    xmlInt = xmlInt.replace("%ospfMask%", ospfMask)

    print(xmlInt)

    with manager.connect(host=router['host'],port=router['port'],username=router['username'],password=router['password'],hostkey_verify=False) as m:

        netconf_reply = m.edit_config(target = 'running', config = xmlInt)
        print(netconf_reply)

#Main

router1OSPF = changeOSPF("10.10.20.175", "172.31.252.25", "172.31.252.0", "0.0.3.255")

router2OSPF = changeOSPF("10.10.20.176", "172.31.252.33", "172.31.252.0", "0.0.3.255")





                       
