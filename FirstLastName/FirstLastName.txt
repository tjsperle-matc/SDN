#This while loop will continue to ask for the users full name until 2 entries are found
#If the user enters 0, 1, 3, or more entries, it will prompt an error to try again

while True:
    #This asks for the users full name without the middle initial and stores it in the variable "fullname"
    fullname = input("Enter your full name without the middle initial: ")
    #This splits the inputed string "fullname" into a list and stores it in the variable "firstlast"
    firstlast = fullname.split()
    #If the number of values in the list is equal to two, it will prompt the user with the print statement with their given and surname capitalized
    if len(firstlast) == 2:
        
        print("Welcome to Python,",(firstlast[0]).capitalize() + ".",(firstlast[1]).capitalize(),"is a really interesting surname! Are you related to the famous Victoria",(firstlast[1]).capitalize() + "?") 

        break
    
    else:
        #This is the error given if users don't enter exactly two names
        print("Error: please try again")
