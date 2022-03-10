##Tyler Sperle - 02/22/2022

import requests ## This imports the requests module

import json ## This imports the json module

## This sends a CLI command to a network device url, and returns a response

switchuser='cisco' ## This supplies the devices username

switchpassword='cisco' ## This supplies the devices password

url='https://10.10.20.177/ins' ## This is the device URL where "IP" is the devices management IP address

myheaders={'content-type':'application/json-rpc'}
payload=[ ## This is where the API will send the command to the device
  {
    "jsonrpc": "2.0",
    "method": "cli",
    "params": {
      "cmd": "show version", ## This is the command we are sending to the device
      "version": 1
    },
    "id": 1
  }
]

## verify=False below is to accept untrusted certificate

response = requests.post(url,data=json.dumps(payload), verify = False, headers=myheaders,auth=(switchuser,switchpassword)).json() ## This is our original
                                                                                                                ##response converted to json

print("Hostname =", response["result"]["body"]["host_name"] + "\t", "Memory =",
      response["result"]["body"]["memory"], response["result"]["body"]["mem_type"]) ## This prints the desired information from the response dictionary



