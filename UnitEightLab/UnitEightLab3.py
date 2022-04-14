##Tyler Sperle - 03/23/2022

import requests ## This imports the requests module
requests.packages.urllib3.disable_warnings() ## This disables the unsecure request warning
import json ## This imports the json module
import re ## This imports regex

##Functions
def getCookie(addr): #This function is used to get an authentication token

#NX REST API Authen See REST API Reference for format of payload below

    url = "https://"+ addr + "/api/aaaLogin.json"
 
    payload= {"aaaUser" :
              {"attributes" :
                   {"name" : "cisco",
                    "pwd" : "cisco"}
               }
          }

    response = requests.post(url, json=payload, verify = False)

    #print(response.json())
    
    return response.json()["imdata"][0]["aaaLogin"]["attributes"]["token"] #This returns the desired token from the response dictionary

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

def changeHostname(switchIP, newHostname):
    cookie = getCookie(switchIP) #Use the cookie below to pass in request. Cookie is good for 600 seconds

    url = "https://" + switchIP + "/api/node/mo/sys.json?query-target=self" #This adds the IP address to the switch url 

    payload= {
                "topSystem": {
                    "attributes": {
                        "name": newHostname #This changes the hostname of the switch
                        
                    }
                }
            }


    headers = {
      'Content-Type': 'application/json',
      'Cookie': 'APIC-cookie=' + cookie #This passes the newly generated cookie into the function
    }

    response = requests.request("POST", url, verify = False, headers=headers, data=json.dumps(payload)) 

    return response #This is our returned response in json

##Main

switchName = input("Please enter the switch hostname you'd like to configure: ") #This asks the user to enter a switch hostname

if validateHost(switchName) == True: #This validates the hostname, if it is true, it will proceed
    switchIP = input("Please enter the management IP address of the switch: ") #This asks the user for the management IP address of the switch
    
    if validateIP(switchIP) == True: #This validates the management IP, if it is true, it will proceed
        newHostname = input("Please enter the new hostname: ") #This asks the user for a new hostname for the switch
        
        if validateHost(newHostname) == True: #This validates the new hostname, if it is true, it will proceed
            changeHostname(switchIP, newHostname) #This runs the function "changeHostname" with the newHostname and swichIP
            print("The hostname has successfully been changed") #This prints that the hostname has successfully been changed

        else:
            print("That is an invalid hostname.") #If the new hostname is invalid, it will print this

    else:
        print("That is an invalid IP address.") #If the management IP address is invalid it will print this

else:
    print("That is an invalid hostname.") #If the switch hostname is invalid, it will print this
