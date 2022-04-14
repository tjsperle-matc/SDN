##Tyler Sperle - 03/23/2022

import requests ## This imports the requests module
requests.packages.urllib3.disable_warnings() ## This disables the unsecure request warning
import json ## This imports the json module

##Functions
def getCookie(addr): #This function is used to get an authentication token

#NX REST API Authen See REST API Reference for format of payload below

    url = "https://"+ addr + "/api/aaaLogin.json"
 
    payload= {"aaaUser" :
              {"attributes" :
                   {"name" : "cisco",
                    "pwd" : "cisco"}
               }
          }

    response = requests.post(url, json=payload, verify = False)

    #print(response.json())
    
    return response.json()["imdata"][0]["aaaLogin"]["attributes"]["token"] #This returns the desired token from the response dictionary

##Main

#Get Session Cookie for NX switch. Change address below as needed
address = '10.10.20.177'

#Use the cookie below to pass in request. Cookie is good for 600 seconds
cookie = getCookie(address)

url = "https://" + address + "/api/mo/sys.json" #This adds the IP address to the switch url 

payload= {
"topSystem": {
"children": [
{
"ipv4Entity": {
  "children": [
{
  "ipv4Inst": {
    "children": [
{
"ipv4Dom": {
  "attributes": {
    "name": "default"
},
"children": [
{
  "ipv4If": {
    "attributes": {
      "id": "vlan101" #This is where you can change the interface
    },
"children": [
{
"ipv4Addr": {
  "attributes": {
    "addr": "172.16.101.20/24" #This is where you can change the IP address
}}}]}}]}}]}}]}}]}}


headers = {
  'Content-Type': 'application/json',
  'Cookie': 'APIC-cookie=' + cookie #This passes the newly generated cookie into the function
}

response = requests.request("POST", url, verify = False, headers=headers, data=json.dumps(payload))
print(response.json()) #This prints our new response
