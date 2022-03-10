##Tyler Sperle - 2/2/2022

##Functions
def nameCheck(fullname): ##This function splits an input, makes sure there are two entries in the list, and makes sure all characters are alpha
    name = True
    
    firstlast = fullname.split() ##This splits the input into a list called "firstlast"
   
    if len(firstlast) != 2:##This checks that the length of the list is two, otherwise name = false
        name = False
           
    else: ##This checks both the first and last name, and makes sure they are only alpha characters
        if firstlast[0].isalpha() == False:
            name = False
        if firstlast[1].isalpha() == False:
            name = False
##If everything passes, name remains true and the name is valid
    return name

      
##Main
validName = False

while validName == False: ##This while loop is looking for "validName" to become true
    fullname = input("Enter your full name without the middle initial: ")
    testName = nameCheck(fullname) ##This runs the input from "fullname" against the function "nameCheck"

    if testName == True: ##If the entry is valid, it will change "validName" to true and print out a welcome statement
        validName = True
        firstlast = fullname.split()
        print("Welcome to Python,",(firstlast[0]).capitalize() + ".",(firstlast[1]).capitalize(),
            "is a really interesting surname! Are you related to the famous Victoria",(firstlast[1]).capitalize() + "?")

    else: ##If it is not a valid entry, it will print an error
        validName = False
        print("Error: please try again")
    
