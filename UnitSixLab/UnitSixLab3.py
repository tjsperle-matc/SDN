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
                                                                                                                ## original response converted to json
    return response


def printOSPFNeighbor(OSPF_Neighbor): ## This function prints the devices ospf neighbors with each router id, address, and interface all in one table

    print("Router-ID" + "\t\t", "Neighbor IP" + "\t\t", "Int") ## This prints the header objects for the table

    print("-" * 55,sep="") ## This prints the divider for the table

    neighborList = OSPF_Neighbor["result"]["body"]["TABLE_ctx"]["ROW_ctx"]["TABLE_nbr"]["ROW_nbr"] ## This assigns the neighbor list to a variable

    for neighbor in neighborList:
        print(neighbor["rid"] + "\t\t", neighbor["addr"] + "\t\t", neighbor["intf"]) ## This iterates through the nighborList item and prints the
                                                                                            ## desired information
        
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

for device in devicesDict.values(): ## This for loop helps get and print the information needed to see OSPF Neighbors

    mgmtIP = device["mgmtIP"] ## This assigns each device mgmtIP to the variable "mgmtIP"

    print(device["hostname"], "OSPF Neighbors") ## This prints out each device name with OSPF Neighbors after it
    
    OSPF_Neighbor = sendCLI("show ip ospf neighbor", mgmtIP) ## This runs the sendCLI function with the cmd "show ip ospf neighbor"
                                                                      ## for each mgmtIP from the devicesDict dictionary

    printOSPFNeighbor(OSPF_Neighbor) ## This runs the printOSPFNeighbor function and displays the requested info in a table

    print() ## This is for a space between tables


