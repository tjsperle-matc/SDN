##Tyler Sperle - 2/1/2022

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

##This is a for loop that prints out each management IP address from each device and attaches ping before it

for key, value in devices.items():
    print("ping" + " " + value["mgmtIP"])




"""

##This is a dictionary called "router1"
##"interfaces" is a dictionary object that stores more key/value pairs

router1 = {
    "hostname": "R1",
    "brand": "Cisco",
    "mgmtIP": "10.0.0.1",
    "interfaces": {
        "G0/0": "10.1.1.1",
        "G0/1": "10.1.2.1"
        }

    }

print("router1 keys")
print(router1.keys()) ##prints "router1" dictionary keys

print("router1[interfaces] keys")
print(router1["interfaces"].keys()) ##prints "interfaces" dictionary keys

print("router1 values")
print(router1.values()) ##prints "router1" dictionary values

print("router1[interfaces] values")
print(router1["interfaces"].values()) ##prints "interfaces" dictionary values

print("router1 items")
print(router1.items()) ##prints "router1" dictionary key and value tuples

print("router1[interfaces] items")
print(router1["interfaces"].items()) ##prints "interfaces" dictionary key and value tuples

"""



























