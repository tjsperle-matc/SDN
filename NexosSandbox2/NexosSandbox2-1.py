##Tyler Sperle - 03/01/2022

import requests ## This imports the requests module
requests.packages.urllib3.disable_warnings() ## This disables the unsecure request warning
import json ## This imports the json module
import re ## This imports regex

##Functions
def sendCLI(cmdCLI, cmdCLI2, IP): ## This is a function that sends a CLI command to a network device url, and returns a response

    switchuser='cisco' ## This supplies the devices username
    switchpassword='cisco' ## This supplies the devices password

    url='https://' + IP + '/ins' ## This is the device URL where "IP" is the device's management IP address

    myheaders={'content-type':'application/json-rpc'}
    payload=[
      {
        "jsonrpc": "2.0",
        "method": "cli",
        "params": {
          "cmd": cmdCLI, ## This sends the first command to the device
          "version": 1
        },
        "id": 1
      },
      {
        "jsonrpc": "2.0",
        "method": "cli",
        "params": {
          "cmd": "hostname " + cmdCLI2, ## This sends the second command to the device
          "version": 1
        },
        "id": 2
      }
    ]

    ## verify=False below is to accept untrusted certificate
    response = requests.post(url,data=json.dumps(payload), verify = False, headers=myheaders,auth=(switchuser,switchpassword)).json() ## This is our
                                                                                                                ##original response converted to json
    return response

def validateHost(hostname): ##This function validates the users hostname input
    validHost = True

    if len(hostname.split()) > 1: ##There must be more than one character in the name
        validHost = False
    if len(hostname) > 64: ##There cannot be more than 64 characters in the name
        validHost = False
    if hostname[0].isalpha() == False:  ##The first character in the hostname must be an alphabetical letter
        validHost = False
    if hostname.isspace() == True: ##There cannot be anyspaces in the name
        validHost = False
   
    host_check = re.compile('[@_!#$%^&*()<>?/\|}{~:.,]') ## I imported regex to check for these characters

    if(host_check.search(hostname) == None): ## If there are no special characters in hostname, validHost = True
        vaildHost = True     
    else: 
        validHost = False ## If there are special characters in hostname, validHost = False
        
    return validHost ##If everything passes, it returns "validHost" as true

##Main        
hostname = input("Please enter a hostname for the device: ") ## This asks the user to enter a hostname

## If the validateHost function comes back as True, it will update the devices hostname and say Device updated
if validateHost(hostname) == True: 
    updateDevice = sendCLI("configure terminal", hostname, "10.10.20.177")## This runs the sendCLI function with the cmds "configure terminal",
    print("Device updated")                                                 ## hostname, and mgmt IP "10.10.20.177"
    
else: ## If the validateHost function comes back as False, it will say Invalid hostname
    print("Invalid hostname")

