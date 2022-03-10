##Tyler Sperle - 02/23/2022

import requests ## This imports the requests module
requests.packages.urllib3.disable_warnings() ## This disables the unsecure request warning
import json ## This imports the json module


##Functions

def sendCLI(cmdCLI, IP): ## This is a function that sends a CLI command to a network device url, and returns a response

    switchuser='cisco' ## This supplies the devices username
    switchpassword='cisco' ## This supplies the devices password

    url='https://' + IP + '/ins' ## This is the device URL where "IP" is the devices management IP address

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
    response = requests.post(url,data=json.dumps(payload), verify = False, headers=myheaders,auth=(switchuser,switchpassword)).json() ## This is our
                                                                                                                ##original response converted to json
    return response


def printInfo(deviceInfo): ## This function prints the devices hostname, memory, memory type, chassis, and boot file all in one table

    print("Host" + "\t\t", "Memory" + "\t\t", "Mem Type" + "\t", "Chassis" + "\t\t\t", "Boot File") ## This prints the header objects for the table

    print("-" * 110,sep="") ## This prints the divider for the table

    print(deviceInfo["result"]["body"]["host_name"], "\t", deviceInfo["result"]["body"]["memory"], "\t", deviceInfo["result"]["body"]["mem_type"], 
          "\t\t", deviceInfo["result"]["body"]["chassis_id"], "\t", deviceInfo["result"]["body"]["kick_file_name"])
            ## This prints out the requested information from the deviceInfo dictionary

        
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

   
deviceInfo = sendCLI("show version", "10.10.20.177") ## This runs the sendCLI function with the cmd "show version" and mgmt IP "10.10.20.177"

printInfo(deviceInfo) # This runs the printInfo function and displays the requested info in a table



