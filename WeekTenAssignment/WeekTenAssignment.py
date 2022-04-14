##Tyler Sperle - 03/28/2022

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

def switchAPI(switchIP):
    cookie = getCookie(switchIP) #Use the cookie below to pass in request. Cookie is good for 600 seconds

    url = "https://" + switchIP + "/api/node/mo/sys/ipv4/inst/dom-default.json?query-target=children" #This adds the IP address to the switch url 

    payload= { #Empty payload
        }


    headers = {
      'Content-Type': 'application/json',
      'Cookie': 'APIC-cookie=' + cookie #This passes the newly generated cookie into the function
    }

    response = requests.request("GET", url, verify = False, headers=headers, data=json.dumps(payload)) 

    return response #This is our returned response in json

##Main

switchIP = '10.10.20.177' #This is the switch IP address

interfaceList = switchAPI(switchIP).json() #This defines the variable "interfaceList", and runs the switchAPI function
                                            #with the parameter "switchIP" and converts it to json

newIntList = interfaceList["imdata"] #This defines the variable "newIntList", and shortens the returned interfaceList so it can be iterated

for interface in newIntList: #This iterates through the "newIntList" and prints out each URL and ID for each interface
    print(interface["ipv4If"]["attributes"]["dn"] + "\t" + interface["ipv4If"]["attributes"]["id"])
