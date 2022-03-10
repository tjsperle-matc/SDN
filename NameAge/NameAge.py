#This asks for the user's first name and stores it in the variable "name"
name = input("Enter your first name: ")

#This asks for the user's age and stores it in the variable "age"
age = input("Enter your age: ")

#This converts the user's age, which is a string, into an integer
add5 = int(age)

#This adds 5 to the users age and stores it back into a string
newage = str(add5 + 5)

#This prints out the user's name and tells them their age in five years
print("Hello", name + ".", "In five years, you will be", newage, "years old!")
