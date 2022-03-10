##Tyler Sperle - 02/23/2022

##Main

devicesDict = { ## This is a nested dictionary housing our two NXOS switches and their respective information
    "dist-sw01" : {
        "hostname" : "dist-sw01",
        "deviceType" : "switch",
        "mgmtIP" : "10.10.20.177"
        },
    
    "dist-sw02" : {
        "hostname" : "dist-sw02",
        "deviceType" : "switch",
        "mgmtIP" : "10.10.20.178"
        }
    }


print("Host" + "\t\t" + "Type" + "\t\t" + "MgmtIP") ## The next three print statements help create the table, the first one is the header objects

print("-" * 44,sep="") ## This prints the divider for the table

for device in devicesDict.values(): ## This iterates through each device in the "devicesDict" dictionary and prints out each hostname, type, and IP
    print(device["hostname"] + "\t" + device["deviceType"] + "\t\t" + device["mgmtIP"])
    



