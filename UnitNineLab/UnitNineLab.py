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

    payload= {
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

def sviAPI(switchIP, sviInterface, ipAddress):
    cookie = getCookie(switchIP) #Use the cookie below to pass in request. Cookie is good for 600 seconds

    url = "https://" + switchIP + "/api/mo/sys.json" #This adds the IP address to the switch url 

    payload= {
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
                                        "addr": ipAddress + "/24"
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

    payload= {
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

    payload= {
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

##Main

switchIP = "10.10.20.177" #This is the switch IP address

vlanNumber = "115" #This is the VLAN number

vlanName = "sdn" #This is the VLAN name

sviInterface = "vlan115" #This is the SVI interface name

ipAddress = "172.16.115.2" #This is the SVI interface IP address

hsrpGroup = "10"

hsrpAddress = "172.16.115.1"

ospfProcessID = "1"

ospfArea = "0.0.0.0"

newVlan = vlanAPI(switchIP, vlanNumber, vlanName)
print(newVlan)
newSVI = sviAPI(switchIP, sviInterface, ipAddress)
print(newSVI)
newHSRP = hsrpAPI(switchIP, sviInterface, hsrpGroup, hsrpAddress)
print(newHSRP)
newOSPF = ospfAPI(switchIP, sviInterface, ospfProcessID, ospfArea)
print(newOSPF)
