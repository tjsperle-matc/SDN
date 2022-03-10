##Tyler Sperle - 02/16/2022

import requests ## This imports the requests module

requests.packages.urllib3.disable_warnings() ## This disables the unsecure request warning

import json ## This imports the json module


##Functions

def sendCLI(cmdCLI, IP): ## This is a function that sends a CLI command to a network device url, and returns a response

    switchuser="cisco"  ## This supplies the devices username

    switchpassword="cisco" ## This supplies the devices password


    url="https://" + IP + "/ins" ## This is the device URL where "IP" is the devices management IP address

    myheaders={'content-type':'application/json-rpc'}

    payload=[ ## This is where the API will send the command to the device

      {

        "jsonrpc": "2.0", 

        "method": "cli",

        "params": {

          "cmd": cmdCLI, ## This is the command we are sending to the device, where "cmdCLI" is the exact command we passed to the function

          "version": 1

        },

        "id": 1

      }

    ]

    ## verify=False below is to accept untrusted certificate

    response = requests.post(url,data=json.dumps(payload), verify=False,headers=myheaders,auth=(switchuser,switchpassword)).json() ## This is our original
                                                                                                                            ##response converted to json

    intList = response["result"]["body"]["TABLE_intf"]["ROW_intf"] ## This strips the "response" dictionary into the list of all interfaces

    return intList ## This returns the new interface list


def printInt(intList): ## This function prints the devices interface names, proto-states, link-states, and IP addresses in a table

    print("Name \t Proto \t Link \t Address") ## This prints the header names

    print("---- \t ----- \t ---- \t -------") ## This prints each divider

    for interface in intList:
        print(interface["intf-name"] + "\t", interface["proto-state"] + "\t", interface["link-state"] + "\t", interface["prefix"]) ## This prints the
                                                                                                                            ##specified device information

##Main

intList = sendCLI("show ip interface brief", "10.10.20.177") ## This calls the function "sendCLI" with a cmdCLI of "show ip interface brief" and an
                                                            ##IP address of "10.10.20.177"                                                   

printInt(intList) ## This calls the function "printInt" using the returned intList from the "sendCLI" function


