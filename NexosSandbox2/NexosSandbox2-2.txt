##Tyler Sperle - 03/01/2022

##Functions
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


def changeIP(ipString, octet, delta):
    octetNum = octet - 1 ##This subtracts 1 from the given octet number so it True list value is correct
    
    octets = ipString.split('.') ##This splits the input into four separate strings that can be iterated

    addOctet = int(octets[octetNum]) + delta ##This adds the given delta number to the correct octet number

    changedOctet = str(addOctet) ##This converts the added octet back into a string
    
    octets[octetNum] = changedOctet ##This will assign the desired octet to the "changedOctet"
    
    newIP = octets[0] + "." + octets[1] + "." + octets[2] + "." + octets[3] ##This reiterates through the octets, changing the desired octet

    return newIP ##This returns the new IP address

    
##Main
ipString = input("Please enter an IP address: ") ## This asks the user to enter a hostname

## If the validateHost function comes back as True, it will update the devices hostname and say Device updated
if validateIP(ipString) == True: 
    updatedIP = changeIP(ipString, 3, 2) ##This runs the changeIP function with the ipString, octet, and delta. Assigning it to updatedIP
    print("Your new IP is " + updatedIP)
    
else: ## If the validateIP function comes back as False, it will say Invalid IP address
    print("Invalid IP address")
