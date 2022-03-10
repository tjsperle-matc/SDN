##Tyler Sperle - 2/9/2022

import requests ##imports the module that will let us run request functions

##Functions

def shuffleDeck(): ##shuffles a single deck, returns dictionary
    cardURL = "https://deckofcardsapi.com/api/deck/new/shuffle/?deck_count=1" ##defines the URL variable in line 13

    payload={} ##defines the data variable in line 13, null
    headers = {} ##defines the headers variable in line 13, null

    response = requests.request("GET", cardURL, headers=headers, data=payload) ##runs a requests.request function that takes four parameters, an HTTP verb,
                                                                                ##URL, header, and data. The response is stored in the variable "response"

    deck = response.json() ##converts the response variable to json, which in turn makes it a dictionary

    deckID = deck["deck_id"] ##converts the "deck_id" value to the variable "deckID"

    return deckID

    
def gameRules(): ##prints the game rules to the user
    print("In this game, you first select how many cards you would like to play with. \n" +
          "The game then shuffles a deck of cards and draws the selected amount to you. \n" +
          "It will print out your drawn cards and add the total card value. \n" +
          "The process is then repeated for the computers turn. The opponent with the highest total card value wins! \n")


def getInput(prompt,validationList): ##This function accepts an answer from an input prompt, and makes sure it is valid against the given validationList
    answer = input(prompt)
    while answer not in validationList:

        print("The following are valid inputs" + str(validationList)) 
        answer = input(prompt) ##If the answer is wrong, it will print the possible correct answers and reprompt the user

    return answer


def drawCards(deckID, numberofCards): ##draws the selected amount of cards
    drawURL = "https://deckofcardsapi.com/api/deck/" + deckID + "/draw/?count=" + numberofCards ##defines the URL variable in line 46

    payload={} ##defines the data variable in line 46, null
    headers = {} ##defines the headers variable in line 46, null

    response = requests.request("GET", drawURL, headers=headers, data=payload) ##runs a requests.request function that takes four parameters, an HTTP verb,
                                                                            ##URL, header, and data. The response is stored in the variable "response"

    cardsJSON = response.json() ##converts the response variable to json, which in turn makes it a list

    cardsDrawn = cardsJSON["cards"] ##assigns the "cards" list to the variable "cardsDrawn"
    
    return cardsDrawn


def addCardTotal(cardsDrawn): ##add the card totals together
    sum = 0
    for card in cardsDrawn:
        if card["value"] == ("10"): ##if the string value is 10, it will add the value 10 to the sum
            value = 10
            sum = sum + value
        if card["value"] == ("JACK"): ##if the string value is JACK, it will add the value 10 to the sum
            value = 10
            sum = sum + value
        if card["value"] == ("QUEEN"): ##if the string value is QUEEN, it will add the value 10 to the sum
            value = 10
            sum = sum + value
        if card["value"] == ("KING"): ##if the string value is KING, it will add the value 10 to the sum
            value = 10
            sum = sum + value
        if card["value"] == ("ACE"): ##if the string value is ACE, it will add the value 10 to the sum
            value = 10
            sum = sum + value
        if card["value"] == ("1"): ##if the string value is 1, it will add the value 1 to the sum
            value = 1
            sum = sum + value
        if card["value"] == ("2"): ##if the string value is 2, it will add the value 2 to the sum
            value = 2
            sum = sum + value
        if card["value"] == ("3"): ##if the string value is 3, it will add the value 3 to the sum
            value = 3
            sum = sum + value
        if card["value"] == ("4"): ##if the string value is 4, it will add the value 4 to the sum
            value = 4
            sum = sum + value
        if card["value"] == ("5"): ##if the string value is 5, it will add the value 5 to the sum
            value = 5
            sum = sum + value
        if card["value"] == ("6"): ##if the string value is 6, it will add the value 6 to the sum
            value = 6
            sum = sum + value
        if card["value"] == ("7"): ##if the string value is 7, it will add the value 7 to the sum
            value = 7
            sum = sum + value
        if card["value"] == ("8"): ##if the string value is 8, it will add the value 8 to the sum
            value = 8
            sum = sum + value
        if card["value"] == ("9"): ##if the string value is 9, it will add the value 9 to the sum
            value = 9
            sum = sum + value
            
        total = sum ##the sum of all card values is assigned to the variable "total"
        
    return total


def printCardsDrawn(cardsDrawn, total): ##prints the cards given to the user or computer, and the added total
    print("\n")
    for card in cardsDrawn:
        print(card["value"] + " of " + card["suit"]) ##prints the card value and suit

    print("Your total card value is:", total) ##prints the total card value


##Main

gameRules() ##runs the gameRules function that prints the game rules

numberofCards = getInput("How many cards do you want to play with? [0-5]: ", ["0","1","2","3","4","5"]) ##input prompt, and validation list for the
                                                                                                        ##getInput function
if int(numberofCards) == 0: ##if the user enters 0, break the script and print "All done"
    print("All done")

else:
    deckID = shuffleDeck() ##if the user enters one of the accepted values (1-5), draw selected amount of cards, add card total, and display the results

    #Users Turn
    
    cardsDrawnUser = drawCards(deckID, numberofCards) ##runs the drawCards function for the user

    userTotal = addCardTotal(cardsDrawnUser) ##runs the addCardTotal function for the user's total

    printCardsDrawn(cardsDrawnUser, userTotal) ##runs the printCardsDrawn function which prints the results and total
    
    #Computers Turn

    cardsDrawnComputer = drawCards(deckID, numberofCards) ##runs the drawCards function for the computer

    computerTotal = addCardTotal(cardsDrawnComputer) ##runs the addCardTotal function for the computer's total

    printCardsDrawn(cardsDrawnComputer, computerTotal) ##runs the printCardsDrawn function which prints the results and total

    #Declare Winner

    if userTotal > computerTotal: ##if the user's total is higher, the user wins
        print("\n\nUser Wins!!")
        
    elif computerTotal > userTotal: ##if the computer's total is higher, the computer wins
        print("\n\nComputer Wins!!")
        
    else: ##if the totals are the same/equal to each other, it's a tie
        print("\n\nIt's a Tie!!")
        

