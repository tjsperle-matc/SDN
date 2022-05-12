#Jack Havlicek, Tyler Sperle, Sean Green 05/04
#This is the script for part 1 of the final

import json
import re


def showDevices(deviceDict):

    print("\n\nHere are the current devices:\n")
    print("Hostname\tManagement IP\tType")
    print('-'*40)
    
    for k in deviceDict['devices']:
        print(k['hostname'] + '\t' + k['mgmtIP'] + '\t' + k['type'])




def getInput(prompt,validationList):    #defining get input function, prompt and allowable answers defined when function is called

    answer = input(prompt)
    
    while answer not in validationList: #if the input is not what we are looking for, tell them what they can say

        print("The following are valid inputs" + str(validationList) + "\n")
        answer = input(prompt)

    return answer  #returning what they answered 





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

        validHost = True     

    else: 

        validHost = False ## If there are special characters in hostname, validHost = False

                        

    return validHost ##If everything passes, it returns "validHost" as true






def validateIP(ipAdd):  #validating IP address function

    ipAddList = ipAdd.split(".")  #splitting on "."'s to check length

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
        print("\nIP address must be in the form of X.X.X.X where X's are numbers between or equal to 0 and 255")

    return valid    #return boolean valid




def addDevice(deviceDict, newHostname, newIP, newDeviceType):

    deviceDict['devices'].append(
        {"hostname" : newHostname,
        "mgmtIP" : newIP,
        "type" : newDeviceType
        }
        )

    
    with open("devices.json" , "w") as outfile:
        json.dump(deviceDict, outfile)
    
    
    return deviceDict





def modifyDevice(deviceDict, deviceIP, hostname, mgmtIP, deviceType): #This function takes an interface dictionary and changes the IP, mask, and description

    for i in range(len(deviceDict['devices'])): #This iterates through each dictionary in the list

        if deviceIP == deviceDict['devices'][i]['mgmtIP']: #Once the user inputted intName matches an interface name, it will change the info only on that interface

            deviceDict['devices'][i]['mgmtIP'] = mgmtIP #This changes the interface IP address
            deviceDict['devices'][i]['hostname'] = hostname #This changes the device hostname
            deviceDict['devices'][i]['type'] = deviceType #This changes the interface description
    

    with open("devices.json" , "w") as outfile:
        json.dump(deviceDict, outfile)


    return deviceDict #This returns the new interfaces list




def deleteDevice(deviceDict, deviceIP):

    for i in range(len(deviceDict['devices'])): #This iterates through each dictionary in the list

        if deviceIP == deviceDict['devices'][i]['mgmtIP']: #Once the user inputted intName matches an interface name, it will change the info only on that interface
            del deviceDict['devices'][i]


    with open("devices.json" , "w") as outfile:
        json.dump(deviceDict, outfile)


    return deviceDict #This returns the new interfaces list






######### MAIN SCRIPT ##########


def readJSON(filename):
    with open(filename) as json_file:
        jsonDict = json.load(json_file)

    return jsonDict





change = "Yes"
 
while change == "Yes":

    deviceDict = readJSON("devices.json")

    ipList = []
    for k in deviceDict['devices']:
        ipList.append(k['mgmtIP'])

    showDevices(deviceDict)

    change = getInput("\n\nWould you like to Add, Modify, or Delete a Device? (Yes or No) -> ", ['Yes','No'])


    if change == "Yes":
        action = getInput("\nWhat action would you like to perform? -> ", ['Add', 'Modify', 'Delete'])


        if action == "Add":

            hostCheck = False   #Control Variables
            ipCheck = False
            
            while hostCheck == False:
                newHostname = input("\nWhat is the hostname of the device you want to add? -> ")
                hostCheck = validateHost(newHostname)

                if hostCheck == False:
                    print("\nSorry that hostname does not work. The conditions for a good hostname are as follows: \n1. Must begin with a letter \n2. Cannot have any spaces \n3. May only contain alphanumeric characters and dashes \n4. Must be no longer than 64 total characters")


            while ipCheck == False:
                newIP = input("\nWhat is the Management IP Address of the new device? -> ")
                ipCheck = validateIP(newIP)

            newDeviceType = getInput("\nWhat is the type of device you are adding? -> ", ['IOSXE', 'NXOS'])

            deviceDict = addDevice(deviceDict, newHostname, newIP, newDeviceType)





        elif action == "Modify":

            deviceToChange = getInput("\nWhat is the management IP of the device you want to change? -> " , ipList)

            hostCheck = False   #Control Variables
            ipCheck = False
            
            while hostCheck == False:
                modHostname = input("\nWhat is the new hostname? -> ")
                hostCheck = validateHost(modHostname)

                if hostCheck == False:
                    print("\nSorry that hostname does not work. The conditions for a good hostname are as follows: \n1. Must begin with a letter \n2. Cannot have any spaces \n3. May only contain alphanumeric characters and dashes \n4. Must be no longer than 64 total characters")


            while ipCheck == False:
                modIP = input("\nWhat is the new Management IP Address? -> ")
                ipCheck = validateIP(modIP)

            modDeviceType = getInput("\nWhat is the new type of device? -> ", ['IOSXE', 'NXOS'])
            

            modifyDevice(deviceDict, deviceToChange, modHostname, modIP, modDeviceType)
            




        elif action == "Delete":
            deviceToDelete = getInput("\nWhat is the management IP of the device you want to delete? -> " , ipList)

            deleteDevice(deviceDict, deviceToDelete)
            



    else:
        print("\nOK, exiting")




