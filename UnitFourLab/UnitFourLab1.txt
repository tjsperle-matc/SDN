##Tyler Sperle - 2/9/2022

import requests ##imports the module that will let us run request functions

##Functions

def getInput(prompt,validationList): ##This function accepts an answer from an input prompt, and makes sure it is valid against the given validationList
    answer = input(prompt)
    while answer not in validationList:

        print("The following are valid inputs" + str(validationList)) 
        answer = input(prompt) ##If the answer is wrong, it will print the possible correct answers and reprompt the user

    return answer

##Main

numberofCards = getInput("How many cards do you want to play with? [0-5]: ", ["0","1","2","3","4","5"])

if int(numberofCards) == 0:
    print("All done")

else:
    cardURL = "https://deckofcardsapi.com/api/deck/new/shuffle/?deck_count=1" ##defines the URL variable in line 29

    payload={} ##defines the data variable in line 29, null
    headers = {} ##defines the headers variable in line 29, null

    response = requests.request("GET", cardURL, headers=headers, data=payload) ##runs a requests.request function that takes four parameters, an HTTP verb,
                                                                                ##URL, header, and data. The response is stored in the variable "response"

    deck = response.json() ##converts the response variable to json, which in turn makes it a dictionary

    deckID = deck["deck_id"]

    ##print("Your deck is shuffled and ready. Your deck id =", deckID + ".") ##this statement prints the deck is ready and the "deck_id"


    url = "https://deckofcardsapi.com/api/deck/" + deckID + "/draw/?count=" + numberofCards ##defines the URL variable in line 44

    payload={} ##defines the data variable in line 44, null
    headers = {} ##defines the headers variable in line 44, null

    response = requests.request("GET", url, headers=headers, data=payload) ##runs a requests.request function that takes four parameters, an HTTP verb,
                                                                            ##URL, header, and data. The response is stored in the variable "response"

    ##print(response.text) #this statement prints the results from the draw request

    cardsDrawn = response.json()

    print(cardsDrawn)





        
