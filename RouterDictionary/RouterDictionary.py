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

changeIP = None
IP = None

##The code below asks the user if the want to change the management IP. If no, it will display nothing changed and break
##If yes, it will break and enter another while loop asking for a new IP
##If the answer is not y, n, yes, or no, it will ask the user again for the correct input

while changeIP not in ("y","n","yes","no"):

    changeIP = input("Do you want to change the Management IP address (y or n)?: ")
    
    if changeIP == "y" or changeIP == "yes":
        
        break

    if changeIP == "n" or changeIP == "no":

        print("Nothing changed!")
        break
    
    else:
        
        print("Please choose (y or n).")

##If the answer from the last input "changeIP" is y or yes, it will ask to enter an ip address for the management interface
##This loop will prompt for a new IP until exactly four numbers are entered, seperated by periods, and between 0 and 255
##If the answer is not a valid IP, it will prompt the user it is invalid and to try again

if changeIP == "y" or changeIP == "yes":

    while True:
        
        IP = input("Enter an IP address for the Management Interface: ")

        newIP = IP.split(".")
        
        if len(newIP) != 4:

            print("IP address not valid. Try x.x.x.x where x is a number from 0-255.")

        if len(newIP) == 4:

            for x in newIP:

                if int(x) < 0 or int(x) > 255:

                    print("IP address not valid. Try x.x.x.x where x is a number from 0-255.")

                    break
                
                if int(x) >= 0 and int(x) <= 255:

                    continue

##If all criteria are met, the script will assign the input value "IP" to the mgmtIP dictionary value, print that the address is updated,
##reprint the routerTable function from before, and break the while loop

            else:

                router1["mgmtIP"] = IP

                print("Address updated!")

                routerTable()

                break

        
            
       


    
