##Tyler Sperle - 2/2/2022

##Functions

def printServers(ntpServer): ##This function takes the key value pairs from a dictionary and displays it in a table

    print("Server Name" + "\t""\t" + "Address") ##This prints Server Name and Address on top of the table
    print("-" * 38) ##This prints a divider

    for key, value in ntpServer.items(): ##This will print each server key and address value with three tabs inbetween
        print(key + "\t""\t""\t" + value)


##Main

ntpServer = { ##This is a dictionary housing server and address key/value pairs
    "Server1": "221.100.250.75",
    "Server2": "201.0.113.22",
    "Server3": "58.23.191.6"
    }
    
printServers(ntpServer) ##This calls the "printServers" function and iterates through the "ntpServer" dictionary
