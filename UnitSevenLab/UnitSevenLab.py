##Tyler Sperle - 03/02/2022

import requests ## This imports the requests module
requests.packages.urllib3.disable_warnings() ## This disables the unsecure request warning
import json ## This imports the json module

##Functions
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

def changeAddr(intName, ipString, maskString, IP): ## This is a function that sends a CLI command to a network device url, and returns a response

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
          "cmd": "ip address " + ipString + " " + maskString, ## This sends the third command to the device
          "version": 1
        },
        "id": 3
      }
    ]

    ## verify=False below is to accept untrusted certificate
    response = requests.post(url,data=json.dumps(payload), verify = False, headers=myheaders,auth=(switchuser,switchpassword)).json() ## This is our
                                                                                                                ##original response converted to json
    return response

def printInt(intList): ## This function prints the devices interface names, proto-states, link-states, and IP addresses in a table

    print("Name \t Proto \t Link \t Address") ## This prints the header names

    print("---- \t ----- \t ---- \t -------") ## This prints each divider

    for interface in intList:
        print(interface["intf-name"] + "\t", interface["proto-state"] + "\t", interface["link-state"] + "\t", interface["prefix"]) ## This prints the
                                                                                                                            ##specified device information
def checkInt(intName, intList): ## This function checks if the users input matches an interface on the device
    validInt = False

    for interface in intList: ## This iterates the interface List for the users input, if it's there, validInt becomes True
        if interface["intf-name"] == intName.capitalize():
            validInt = True

    return validInt

def validateIP(ipString): ##This function takes the user's IP input and validates it's a real IP address.
    validIP = True

    octets = ipString.split(".") ##This splits the input into four separate strings that can be iterated

    if len(octets) != 4: ##If the length is 4, it passed the first test and it can proceed
        validIP = False
        
        
    else: ##iterate octets and test one at a time to confirm all of the address is numeric and within the correct range
        for octet in octets:
            if octet.isnumeric() == True: ##check if the octet is numeric
                if int(octet) < 0 or int(octet) > 255: ##invalid range
                    validIP = False

            else:
                validIP = False

    return validIP ##If everything passes, "validIP" remains true and returns the valid IP address

def validateMask(maskString): ##This function takes the user's subnet mask input and validates it's a real mask.
    validMask = True

    octets = maskString.split(".") ##This splits the input into four separate strings that can be iterated
    
    if len(octets) != 4: ##If the length is 4, it passed the first test and it can proceed
        validMask = False
            
    else: ##iterate octets and test one at a time to confirm all of the address is numeric and within the correct range
        for octet in octets:
            if octet.isnumeric() == True: ##check if the octet is numeric
                if int(octet) < 0 or int(octet) > 255: ##invalid range
                    validMask = False

            else:
                validMask = False

    return validMask ##If everything passes, "validMask" remains true and returns the valid subnet mask


##Main
intList = showIP("show ip interface brief", "10.10.20.177") ## This calls the function "showIP" with a cmdCLI of "show ip interface brief" and an
                                                            ##IP address of "10.10.20.177"

printInt(intList) ## This calls the function "printInt" using the returned intList from the "sendCLI" function

intName = input("Which interface would you like to change the address on?: ") ## This asks the user which interface they would like to change

if checkInt(intName, intList) == True: ## If the interface is valid, it will proceed
    ipString = input("Please enter a valid IP address for the interface: ") ## This asks the user for a valid IP address
    if validateIP(ipString) == True: ## If the IP is valid, it will proceed
        maskString = input("Please enter a valid subnet mask for the interface: ") ## This asks the user for a valid subnet mask
        if validateMask(maskString) == True: ## If the mask is valid, it will proceed
            changeAddr(intName, ipString, maskString, "10.10.20.177") ## This calls the changeAddr function with the intName, ipString, maskString, and IP
            newIntList = showIP("show ip interface brief", "10.10.20.177") ## This calls the function "showIP" with a cmdCLI of "show ip interface brief"
            printInt(newIntList) ## This reprints the show ip int br cmd    ##and an IP address of "10.10.20.177"

        else:
            print("That is not a valid subnet mask") ## If the subnet mask is not valid, it will print this response
            
    else:
        print("That is not a valid IP address") ## If the IP address is not valid, it will print this response
        
else:
    print("That is not a valid interface") ## If the interface is not valid, it will print this response
