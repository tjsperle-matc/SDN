##Tyler Sperle - 2/2/2022

##Functions

def pingPrep(ipList): ##This function takes the address values from the dictionary and prepends ping to them

    for value in ipList.values(): ##This will print each address value with ping before it
        print("Ping", value)


##Main

ntpServer = { ##This is a dictionary housing server and address key/value pairs
    "Server1": "221.100.250.75",
    "Server2": "201.0.113.22",
    "Server3": "58.23.161.6"
    }
    
pingPrep(ntpServer) ##This calls the "pingPrep" function and iterates through the "ntpServer" dictionary
