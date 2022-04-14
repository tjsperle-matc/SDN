##Tyler Sperle - 03/30/2022

import requests ## This imports the requests module
requests.packages.urllib3.disable_warnings() ## This disables the unsecure request warning
import json ## This imports the json module

##Functions
def getCookie(switchIP): #This function is used to get an authentication token

#NX REST API Authen See REST API Reference for format of payload below

    url = "https://"+ switchIP + "/api/aaaLogin.json"
 
    payload= {"aaaUser" :
              {"attributes" :
                   {"name" : "cisco",
                    "pwd" : "cisco"}
               }
          }

    response = requests.post(url, json=payload, verify = False)

    #print(response.json())
    
    return response.json()["imdata"][0]["aaaLogin"]["attributes"]["token"] #This returns the desired token from the response dictionary

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

def changeIP(ipString, octet, delta):
    octetNum = octet - 1 ##This subtracts 1 from the given octet number so it True list value is correct
    
    octets = ipString.split('.') ##This splits the input into four separate strings that can be iterated

    addOctet = int(octets[octetNum]) + delta ##This adds the given delta number to the correct octet number

    changedOctet = str(addOctet) ##This converts the added octet back into a string
    
    octets[octetNum] = changedOctet ##This will assign the desired octet to the "changedOctet"
    
    newIP = octets[0] + "." + octets[1] + "." + octets[2] + "." + octets[3] ##This reiterates through the octets, changing the desired octet

    return newIP ##This returns the new IP address

##Main

devicesDict = { ## This is a nested dictionary housing our two NXOS switches and their respective information
    "dist-sw01" : {
        "hostname" : "dist-sw01",
        "deviceType" : "switch",
        "mgmtIP" : "10.10.20.177"
        },
    
    "dist-sw02" : {
        "hostname" : "dist-sw02",
        "deviceType" : "switch",
        "mgmtIP" : "10.10.20.178"
        }
    }
"""
change the variables below before adding a new vlan interface
"""
vlanNumber = "110" #This is the VLAN number

vlanName = "testNXOS" #This is the VLAN name

sviInterface = "vlan110" #This is the SVI interface name

ipAddress = "172.16.110.1" #This is the SVI interface IP address

hsrpGroup = "10" #This is the HSRP group number

hsrpAddress = "172.16.110.1" #This is the HSRP IP address

ospfProcessID = "1" #This is the OSPF process ID

ospfArea = "0.0.0.0" #This is the OSPF area

for device in devicesDict.values(): ## This iterates the devices in "devicesDict" dictionary

    switchIP = device["mgmtIP"] ## This assigns each device mgmtIP to the variable "switchIP"

    newVlan = vlanAPI(switchIP, vlanNumber, vlanName) #This runs the function vlanAPI and creates the vlan using the given parameters

    ipAddress = changeIP(ipAddress, 4, 1) #This runs the function changeIP and adds 1 to the 4th octet each time the address goes through the loop
    
    newSVI = sviAPI(switchIP, sviInterface, ipAddress) #This runs the function sviAPI and creates the SVI interface with the given parameters

    newHSRP = hsrpAPI(switchIP, sviInterface, hsrpGroup, hsrpAddress) #This runs the function hsrpAPI and adds an HSRP group and address to the interface

    newOSPF = ospfAPI(switchIP, sviInterface, ospfProcessID, ospfArea) #This runs the fucntion ospfAPI and adds an OSPF process and area to the interface
