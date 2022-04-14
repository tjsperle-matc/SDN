##Tyler Sperle - 04/13/2022

from collections import OrderedDict #This imports the module required to access and construct an ordered dictionary

#Below is an ordered dictionary for a Cisco router listing some key information and interfaces
router1 = OrderedDict([("brand", "Cisco"), ("model", "1941"), ("mgmtIP", "10.0.0.1"), ("G0/0", "10.0.1.1"), ("G0/1", "10.0.2.1"), ("G0/2", "10.1.0.1")])

for key, value in router1.items(): #This for loop iterates each key and value in the "router1" ordered dictionary
    print("Key = " + key + "\t" + "Value = " + value) #This prints each key and value in the ordered dictionary
