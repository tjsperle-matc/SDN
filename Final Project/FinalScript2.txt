#Jack Havlicek, Tyler Sperle, Sean Green 05/05
#This is the script for part 2 of the final


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



#-------------These are DME model requests for NXOS switches--------------#

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




def printInt(intList): ## This function prints the devices interface names, proto-states, link-states, and IP addresses in a table

    print("Name \t Proto \t Link \t Address") ## This prints the header names

    print("---- \t ----- \t ---- \t -------") ## This prints each divider

    for interface in intList:
        print(interface["intf-name"] + "\t", interface["proto-state"] + "\t", interface["link-state"] + "\t", interface["prefix"]) ## This prints the
                                                                                                                            ##specified device information



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



def changeAddrThirty(intName, updatedIP, IP): ## This is a function that sends an ip address command to a network device url, and returns a response

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
          "cmd": "ip address " + updatedIP + " 255.255.255.252", ## This sends the third command to the device
          "version": 1
        },
        "id": 3
      }
    ]

    ## verify=False below is to accept untrusted certificate
    response = requests.post(url,data=json.dumps(payload), verify = False, headers=myheaders,auth=(switchuser,switchpassword)).json() ## This is our
                                                                                                                ##original response converted to json
    return response




        

def getCookie(addr) :   #defining getCookie function, takes input of address

    url = "https://"+ addr + "/api/aaaLogin.json"
 
    payload= {"aaaUser" :
              {"attributes" :
                   {"name" : "cisco",
                    "pwd" : "cisco"}
               }
          }


    response = requests.post(url, json=payload, verify = False)
    return response.json()["imdata"][0]["aaaLogin"]["attributes"]["token"]




def vlanAPI(switchIP, vlanNumber, vlanName):
    cookie = getCookie(switchIP) #Use the cookie below to pass in request. Cookie is good for 600 seconds

    url = "https://" + switchIP + "/api/mo/sys.json" #This adds the IP address to the switch url 

    payload= { #This payload creates and names a vlan
      "topSystem": {
        "children": [
          {
            "bdEntity": {
              "children": [
                {
                  "l2BD": {
                    "attributes": {
                      "fabEncap": "vlan-" + vlanNumber,
                      "name": vlanName
                    }
                  }
                }
              ]
            }
          }
        ]
      }
    }


    headers = {
      'Content-Type': 'application/json',
      'Cookie': 'APIC-cookie=' + cookie #This passes the newly generated cookie into the function
    }

    response = requests.request("POST", url, verify = False, headers=headers, data=json.dumps(payload)) 

    return response #This is our returned response in json




def sviAPI(switchIP, sviInterface, newIP):
    cookie = getCookie(switchIP) #Use the cookie below to pass in request. Cookie is good for 600 seconds

    url = "https://" + switchIP + "/api/mo/sys.json" #This adds the IP address to the switch url 

    payload= { #This payload creates an SVI interface for a vlan and adds an IP address
      "topSystem": {
        "children": [
          {
            "ipv4Entity": {
              "children": [
                {
                  "ipv4Inst": {
                    "children": [
                      {
                        "ipv4Dom": {
                          "attributes": {
                            "name": "default"
                          },
                          "children": [
                            {
                              "ipv4If": {
                                "attributes": {
                                  "id": sviInterface
                                },
                                "children": [
                                  {
                                    "ipv4Addr": {
                                      "attributes": {
                                        "addr": newIP + "/24"
                                      }
                                    }
                                  }
                                ]
                              }
                            }
                          ]
                        }
                      }
                    ]
                  }
                }
              ]
            }
          },
          {
            "interfaceEntity": {
              "children": [
                {
                  "sviIf": {
                    "attributes": {
                      "adminSt": "up",
                      "id": sviInterface
                    }
                  }
                }
              ]
            }
          }
        ]
      }
    }

    headers = {
      'Content-Type': 'application/json',
      'Cookie': 'APIC-cookie=' + cookie #This passes the newly generated cookie into the function
    }

    response = requests.request("POST", url, verify = False, headers=headers, data=json.dumps(payload)) 

    return response #This is our returned response in json



def hsrpAPI(switchIP, sviInterface, hsrpGroup, hsrpAddress):
    cookie = getCookie(switchIP) #Use the cookie below to pass in request. Cookie is good for 600 seconds

    url = "https://" + switchIP + "/api/mo/sys.json" #This adds the IP address to the switch url 

    payload= { #This payload adds our HSRP information to the SVI
      "topSystem": {
        "children": [
          {
            "interfaceEntity": {
              "children": [
                {
                  "sviIf": {
                    "attributes": {
                      "id": sviInterface
                    }
                  }
                }
              ]
            }
          },
          {
            "hsrpEntity": {
              "children": [
                {
                  "hsrpInst": {
                    "children": [
                      {
                        "hsrpIf": {
                          "attributes": {
                            "id": sviInterface
                          },
                          "children": [
                            {
                              "hsrpGroup": {
                                "attributes": {
                                  "af": "ipv4",
                                  "id": hsrpGroup,
                                  "ip": hsrpAddress,
                                  "ipObtainMode": "admin"
                                }
                              }
                            }
                          ]
                        }
                      }
                    ]
                  }
                }
              ]
            }
          }
        ]
      }
    }

    headers = {
      'Content-Type': 'application/json',
      'Cookie': 'APIC-cookie=' + cookie #This passes the newly generated cookie into the function
    }

    response = requests.request("POST", url, verify = False, headers=headers, data=json.dumps(payload)) 

    return response #This is our returned response in json



def ospfAPI(switchIP, sviInterface, ospfProcessID, ospfArea):
    cookie = getCookie(switchIP) #Use the cookie below to pass in request. Cookie is good for 600 seconds

    url = "https://" + switchIP + "/api/mo/sys.json" #This adds the IP address to the switch url 

    payload= { #This payload adds our OSPF information to the SVI
      "topSystem": {
        "children": [
          {
            "ospfEntity": {
              "children": [
                {
                  "ospfInst": {
                    "attributes": {
                      "name": ospfProcessID
                    },
                    "children": [
                      {
                        "ospfDom": {
                          "attributes": {
                            "name": "default"
                          },
                          "children": [
                            {
                              "ospfIf": {
                                "attributes": {
                                  "advertiseSecondaries": "yes",
                                  "area": ospfArea,
                                  "id": sviInterface
                                }
                              }
                            }
                          ]
                        }
                      }
                    ]
                  }
                }
              ]
            }
          },
          {
            "interfaceEntity": {
              "children": [
                {
                  "sviIf": {
                    "attributes": {
                      "id": sviInterface
                    }
                  }
                }
              ]
            }
          }
        ]
      }
    }

    headers = {
      'Content-Type': 'application/json',
      'Cookie': 'APIC-cookie=' + cookie #This passes the newly generated cookie into the function
    }

    response = requests.request("POST", url, verify = False, headers=headers, data=json.dumps(payload)) 

    return response #This is our returned response in json





def modifyIP(IPaddress, octet, change):    #function to modify the IP address
    
    ipList = IPaddress.split(".")   #splits the IP address into a list
    ipList[octet-1] = str(change)  #adds the change to the specified octet

    newIP = ""

    for octet in ipList: #adding each octet plus a "." to a string
            newIP = newIP + octet + "."
    newIP = newIP.rstrip(".")   #stripping off the last "."

    return newIP    #returning the modified IP address





def changeIP(ipString, octet, delta):
    octetNum = octet - 1 ##This subtracts 1 from the given octet number so it True list value is correct
    
    octets = ipString.split('.') ##This splits the input into four separate strings that can be iterated

    addOctet = int(octets[octetNum]) + delta ##This adds the given delta number to the correct octet number

    changedOctet = str(addOctet) ##This converts the added octet back into a string
    
    octets[octetNum] = changedOctet ##This will assign the desired octet to the "changedOctet"
    
    newIP = octets[0] + "." + octets[1] + "." + octets[2] + "." + octets[3] ##This reiterates through the octets, changing the desired octet

    return newIP ##This returns the new IP address






#============== These are netconf calls for the IOSXE devices ============================#



def callNetconf(hostIP):    #defining the callNetconf function, takes a device ip
    router = {"host": hostIP , "port" : "830",
              "username":"cisco","password":"cisco"}


    netconf_filter = """

    <interfaces xmlns="urn:ietf:params:xml:ns:yang:ietf-interfaces">
        <interface></interface>
    </interfaces>
       
    """

    with manager.connect(host=router['host'],port=router['port'],username=router['username'],password=router['password'],hostkey_verify=False) as m:

        netconf_reply = m.get_config(source = 'running', filter = ("subtree",netconf_filter))
        return netconf_reply




def displayInterface(interfaceList):        #display interfaces function
    print("Name\t\t\tIP Address\tNetmask\t\tDescription")   #headers
    print("-" *78)
    for int in interfaceList:   #printing the information from the list/dictionary
        if int['name'].startswith('G'):
            print(int['name'] +"\t"+ int['ipv4']['address']['ip'] +"\t"+ int['ipv4']['address']['netmask'] +'\t'+ int['type']['#text'])

              







def getInput(prompt,validationList):    #defining get input function, prompt and allowable answers defined when function is called

    answer = input(prompt)
    while answer not in validationList: #if the input is not what we are looking for, tell them what they can say

        print("The following are valid inputs" + str(validationList) + "\n")
        answer = input(prompt)

    return answer  #returning what they answered 







def validateIP(ipAdd):  #validating IP address function

    ipAddList=ipAdd.split(".")  #splitting on "."'s to check length

    valid = True    #control variable, if any condition isn't correct it changes to false

    if len(ipAddList) != 4: #making sure there are 4 octetes
        valid = False

    for octet in ipAddList:
        if octet.isnumeric() == False:  #checking if all octets are numbers
            valid = False


    if valid == True:   #only check range if it passed the isnumeric test, otherwise code will break
        for octet in ipAddList:
            if int(octet) < 0 or int(octet) > 255:
                valid = False

    if valid == False:  #telling them what we need if they enter a bad address
        print("IP address must be in the form of X.X.X.X where X's are numbers between or equal to 0 and 255")

    return valid    #return boolean valid






def updateAddr(routerIP, intIP, intMask, slicedIntName, intNum):
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
    xmlInt = xmlInt.replace("%intName%", slicedIntName)
    xmlInt = xmlInt.replace("%intNum%", intNum)
    xmlInt = xmlInt.replace("%mask%", intMask)

    with manager.connect(host=routerIP,port='830',username='cisco',password='cisco',hostkey_verify=False) as m:

        netconf_reply = m.edit_config(target = 'running', config = xmlInt)
        
    return netconf_reply



######### MAIN SCRIPT ##########


def readJSON(filename):
    with open(filename) as json_file:
        jsonDict = json.load(json_file)

    return jsonDict

deviceDict = readJSON("devices.json")

devices = deviceDict["devices"]

vlanNumber = "120" #This is the VLAN number

vlanName = "testNXOS" #This is the VLAN name

sviInterface = "vlan120" #This is the SVI interface name

ipAddress = "172.31.120.1" #This is the SVI interface IP address

hsrpGroup = "10" #This is the HSRP group number

hsrpAddress = "172.31.120.1" #This is the HSRP IP address

ospfProcessID = "1" #This is the OSPF process ID

ospfArea = "0.0.0.0" #This is the OSPF area

for device in devices:
    
    if device["type"] == "NXOS":
        switchIP = device["mgmtIP"]
        
        intList = showIP("show ip interface brief", switchIP)
        print(device["hostname"] + "\n")
        printInt(intList)
        print("")

        for interface in intList:
            intIP = interface["prefix"]
            intName = interface["intf-name"]
            
            updatedIP = modifyIP(intIP, 2, 31) ## This runs the "changeIP" function by taking the interface IP, and adding 5 to the fourth octet

            if intName.startswith("E" or "e"):
                changeAddrThirty(intName, updatedIP, switchIP) ## This runs the "changeAddrThirty" function that pushes the changes to each switch

            else:    
                changeAddr(intName, updatedIP, switchIP) ## This runs the "changeAddr" function that pushes the changes to each switch

    
        newVlan = vlanAPI(switchIP, vlanNumber, vlanName) #This runs the function vlanAPI and creates the vlan using the given parameters

        ipAddress = changeIP(ipAddress, 4, 1) #This runs the function changeIP and adds 1 to the 4th octet each time the address goes through the loop
    
        newSVI = sviAPI(switchIP, sviInterface, ipAddress) #This runs the function sviAPI and creates the SVI interface with the given parameters

        newHSRP = hsrpAPI(switchIP, sviInterface, hsrpGroup, hsrpAddress) #This runs the function hsrpAPI and adds an HSRP group and address to the interface

        newOSPF = ospfAPI(switchIP, sviInterface, ospfProcessID, ospfArea) #This runs the fucntion ospfAPI and adds an OSPF process and area to the interface
        

        updatedIntList = showIP("show ip interface brief", switchIP)
        print(device["hostname"] + "\n")
        printInt(updatedIntList)
        print("")
    


    if device["type"] == "IOSXE":
        routerIP = device["mgmtIP"]

        reply = callNetconf(routerIP)
        data = xmltodict.parse(reply.xml)["rpc-reply"]["data"]
        interfaces = data["interfaces"]["interface"]
        print(device["hostname"] + "\n")
        displayInterface(interfaces)
        print("")

        for interface in interfaces:
            if interface["name"].startswith('L'):
                pass

            elif interface["name"] == "GigabitEthernet1":
                pass
            
            else:
                intIP = interface["ipv4"]["address"]["ip"]
                intMask = interface["ipv4"]["address"]["netmask"]
                intName = interface["name"]
                slicedIntName = intName[0:15]
                intNum = intName[15:16]
                
                updatedIP = modifyIP(intIP, 2, 31) ## This runs the "changeIP" function by taking the interface IP, and adding 5 to the fourth octet
                updatedInt = updateAddr(routerIP, updatedIP, intMask, slicedIntName, intNum)


        newReply = callNetconf(routerIP)
        newData = xmltodict.parse(newReply.xml)["rpc-reply"]["data"]
        newInterfaces = newData["interfaces"]["interface"]
        print(device["hostname"] + "\n")
        displayInterface(newInterfaces)
        print("")

print("All interfaces on all devices have been updated.")       
                
        
        




















