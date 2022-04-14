##Tyler Sperle - 04/13/2022

from collections import OrderedDict #This imports the module required to access and construct an ordered dictionary

#Below is an ordered dictionary of an interface and its ipv4/ipv6 information
interface = OrderedDict([("name", "GigabitEthernet1"),
                         ("description", "to port6.sandbox-backend"),
                         ("type", OrderedDict([
                             ("@xmlns:ianaift", "urn:ietf:params:xml:ns:yang:iana-if-type"),
                             ("#text", "ianaift:ethernetCsmacd")
                             ])
                          ),
                         ("enabled", "True"),
                         ("ipv4", OrderedDict([
                             ("@xmlns", "urn:ietf:params:xml:ns:yang:ietf-ip"),
                             ("address", OrderedDict([
                                 ("ip", "10.10.20.175"),
                                 ("netmask", "255.255.255.0")
                                 ])
                             )]
                                              )
                          ),
                         ("ipv6", OrderedDict([
                             ("@xmlns", "urn:ietf:params:xml:ns:yang:ietf-ip")]
                                              )
                          )
                         ])

#This prints the interface name, #text value of the interface type, IP address, and subnet mask from the "interface" ordered dictionary
print(interface["name"] + "  " + interface["type"]["#text"] + "  " + interface["ipv4"]["address"]["ip"] + "  " + interface["ipv4"]["address"]["netmask"])


