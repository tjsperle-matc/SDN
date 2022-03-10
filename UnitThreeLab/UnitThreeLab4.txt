##Tyler Sperle - 2/2/2022

##Functions

def pingDevices(devices): ##This function is a for loop that prints out each management IP address from each device and attaches ping before it
    for device in devices.keys():
        print("ping" + " " + devices[device]["mgmtIP"])

def getInput(prompt,validationList): ##This function accepts an answer from an input prompt, and makes sure it is valid against the given validationList
    answer = input(prompt)
    while answer not in validationList:

        print("The following are valid inputs" + str(validationList)) 
        answer = input(prompt) ##If the answer is wrong, it will print the possible correct answers and reprompt the user

    return answer 

def printDevice(devices): ##This function prints each devices hostname, management IP, and hardware type seperated with tabs. Each device has its own line
    for device in devices.keys():

        print(devices[device]["hostname"] + "\t" + devices[device]["mgmtIP"] + "\t" + devices[device]["type"])

def getDeviceInfo(): ##This function asks the user to enter a hostname, and an IP address, then stores it in a dictionary called "returnDict"
    returnDict = {"type": "",
        "hostname": "",
        "mgmtIP": ""
        }
    returnDict["hostname"] = input("Enter hostname: ")
    returnDict["mgmtIP"] = input("Enter IP: ")
    return returnDict

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

def validateHost(hostname): ##This function validates the users hostname input
    validHost = True

    if len(hostname.split()) > 1: ##There must be more than one character in the name
        validHost = False
    if len(hostname) > 64: ##There cannot be more than 64 characters in the name
        validHost = False
    if hostname[0].isalpha() == False:  ##The first character in the hostname must be an alphabetical letter
        validHost = False
        
    return validHost ##If everything passes, it returns "validHost" as true

def updateDictionary(deviceDict, devices): ##This function takes the new valid "deviceDict", and adds it to the existing "devices" dictionary with the
    hostname = deviceDict["hostname"]      ##hostname being the key to the newly added device

    devices[hostname] = deviceDict

##Main

    
##This is a nested dictionary called "devices"
##Inside "devices", there are dictionary objects for each device that holds there respective information

devices = {
    "R1" : {
        "type": "router",
        "hostname": "R1",
        "mgmtIP": "10.0.0.1"
        },
    "R2" : {
        "type": "router",
        "hostname": "R2",
        "mgmtIP": "10.0.0.2"
        },
    "S1" : {
        "type": "switch",
        "hostname": "S1",
        "mgmtIP": "10.0.0.3"
        },
    "S2" : {
        "type": "switch",
        "hostname": "S2",
        "mgmtIP": "10.0.0.4"
        
        }
    }


printDevice(devices) ##This runs the "printDevice" function, and iterates through each device in the "devices" dictionary

addDevice = getInput("Do you want to add a device? (y or n) ", ["y", "n", "Y", "N"]) ##This runs the function "getInput". The prompt is asking the user
                                                                ##if they want to add a new device. The parameters are yes or no. (y,n,Y,N)
if addDevice.lower() == "y":
    validDevice = False 
    while validDevice == False:
                            ##If the answer is yes it will prompt the user if it is a switch or a router
        deviceType = getInput("Is this a switch or a router? (s or r) ", ["s", "r", "S", "R"]) ##Rerun the "getInput" function with new prompt
        deviceDict = getDeviceInfo()                                                            ##and new parameters. (s,r,S,R)

        validIP = validateIP(deviceDict["mgmtIP"]) ##This runs the "validateIP" function to ensure it is a real IP address

        validHost = validateHost(deviceDict["hostname"]) ##This runs the "validateHost" function to ensure it is a valid hostname
        if deviceType.lower() == "s":
            deviceDict["type"] = "switch"
        else:
            deviceDict["type"] = "router"

        if validIP == True and validHost == True: ##If everything passes, it will change "validDevice" to true and break the loop
            validDevice = True
        if validIP == False: ##If the IP is not valid, it will print "Bad IP". Then rerun the loop for a device type
            print("Bad IP")
        if validHost == False: ##If the hostname is not valid, it will print "Bad hostname". Then rerun the loop for a device type
            print("Bad hostname")

    updateDictionary(deviceDict, devices) ##If "validDevice" returns true, it will update the new device into the "devices" dictionary by running
    print("Device Updated!!! \n\n\n")     ##the "updateDictionary" function
    
    ##printDevice(devices) ##This reruns the "printDevice" function, and iterates through each device in the updated "devices" dictionary

    pingDevices(devices) ##This runs the ping function, and iterates through the updated "devices" dictionary

else: ##If the answer is no, it will break the loop and print "Nothing updated!"
    print("Nothing updated! \n\n\n")



        
