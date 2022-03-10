##Tyler Sperle - 1/27/2022

##This is a dictionary labeled "router1", it is filled with key/value pairs that pertain to the router

router1 = {
    "brand": "Cisco",
    "model": "1941",
    "mgmtIP": "10.0.0.1",
    "G0/0": "10.0.1.1 /24",
    "G0/1": "10.0.2.1 /24",
    "G0/2": "10.0.3.1 /24",
    "hostname": "r1"
    }

##The commands below reference keys from the router1 dictionary, and changes there values

router1["G0/2"] = "10.1.3.1 /24"
router1["model"] = "2901"

##The def statement below collects all the print statements used for the table into a function called "routerTable"

def routerTable():
    
##The code below prints each key from the router1 dictionary, horizontally, and with two tab's between each key
    
    for key in router1.keys():
        print(key,"\t"+"\t",end=" ")

##This statement is used to print the hyphen seperator between the keys and the values

    print("\n","-" * 120,sep="")

##The code below prints each value from the router1 dictionary, with the appropriate amount of spaces, and it removes the CIDR notation from the IP's

    print(router1["brand"], "\t"+"\t", router1["model"], "\t"+"\t", router1["mgmtIP"], "\t"+"\t", router1["G0/0"].replace("/24",""), "\t",
          router1["G0/1"].replace("/24",""), "\t", router1["G0/2"].replace("/24",""), "\t", router1["hostname"])

##The statement below runs the "routerTable" function and prints the table

routerTable()

##The code below asks the user if the want to change the management IP address
##Normalize input and check
##If the user answers "y", it will set the flag to ask fro validIP
##If the user answer "n", it will break out of the loop and respond nothing changed

validContinue = False
while validContinue == False:

    changeIP = input("Do you want to change the Management IP address (y or n)?: ")

    if changeIP.upper() == "Y":
        validContinue = True ##Exit While loop
        EnterIP = True ##set flag for validIP. will loop until a valid IP is entered.

    elif changeIP.upper() == "N":
        validContinue = True ##Exit While loop
        EnterIP = False ##skip getting an IP and break loop
        print("Nothing changed!")

    else:
        print("Please choose (y or n).")
        

validIP = False

while EnterIP == True:

##Input IP
##Validate IP
    #1. Are there only 4 octets
    #2. Are all octets numeric
    #3. Are all octets within the correct range

    EnterIP = False
    validIP = True

    ##Get IP address

    IP = input("Enter an IP address for the Management Interface: ")

    octets = IP.split(".")

    if len(octets) == 4: ##If the length is 4, it passed the first test and it can proceed

        ##iterate octets and test one at a time to confirm all of the address is numeric and within the correct range

        for octet in octets:
            if octet.isnumeric() == True: ##check if the octet is numeric
                if int(octet) < 0 or int(octet) > 255: ##invalid range

                    validIP = False
                    EnterIP = True

            else:

                validIP = False
                EnterIP = True

        ##print statement if EnterIP flag is raised to True. meaning it is not a valid IP address

        if EnterIP == True:

            print("IP address not valid. Try x.x.x.x where x is a number from 0-255.")

    ##print statement if the IP address entered is not 4 octets in length
    
    else:

        print("IP address not valid. Try x.x.x.x where x is a number from 0-255.")
        validIP = False
        EnterIP = True

##If validIP == True, it will change the value of mgmtIP to the new address, print that the address was updated, and print the updated routerTable function

if validIP == True:
    
    router1["mgmtIP"] = IP

    print("Address updated!")

    routerTable()

    

        
            
       


    
