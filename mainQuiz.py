#This python quiz coordinates with seperate custom made difficulty modules/libraries which were created specifically for this quiz. 
#The custom modules are attached named as "easy", "medium" and "hard".

#Quiz features:#Initialising permission#Difficulty levels installed#Answer checking#Lives system#Choice to restart or quit#Score tracker
#Python features used:#Variables#Strings#Integers#User Input#Output#If Statements#Elif Statements#Else Statements#For Loops#Dictionaries#Nested Dictionaries#Imports#Modules#Match Case#Comparison Operators#Membership Operator#String Methods (.lower() and .upper())#Boolean Variables#Loop Control (break and continue)#Maybe some more things

#Code
#Importing difficulty modules. Dictionary is named as questions but also include answers and options for MCQs
from easy import easy_questions
from medium import medium_questions
from hard import hard_questions
#Welcome Greeting and global variables assigned
print("Welcome to Python Quiz!")
print("This quiz is designed to test your coding knowledge")
score = 0
lives = 3
restart = "" 
#Ask user to start the quiz, validated
user_start = input("Would you like to start? ").lower()
#running is assigned to create a loop. That loop prevents the program from crashing after the user does not want to restart
running = True
while running == True:
    #Initialising after permission to start granted
    #Taking difficulty choice
        if user_start == "yes":
            print("")
            print("Level 1: Easy")
            print("Level 2: Medium")
            print("Level 3: Hard")
            print("")
            user_difficulty = input("Which difficlty would you like to play on? ").lower()
        #Closing after choice to reject initialising of the quiz program
        elif user_start == "no":
            print("Quiz ended. You can always come back. ")
        #Input validation
        else:
            print("Invalid input. Try again")
            user_start = input("Would you like to start? ").lower()
        #Matching user choice with the difficulty level
        match user_difficulty:
            case "easy" | "level 1" | "level1" | "1":
                questions = easy_questions
            case "medium" | "level 2" | "level2" | "2":
                questions = medium_questions
            case "hard" | "level 3" | "level3" | "3":
                questions = hard_questions
            #Input validation
            case _:
                print("Invalid difficulty")
                continue
        #loop connecting with the user's preffered difficulty
        for questions, data in questions.items():
            #Taking answers, checking and giving result
            print(questions)
            if "options" in data:
                print(data["options"])
            if "options" in data:
                user_answer = input("Please enter your answer ").upper()
            else:
                user_answer = input("Please enter your answer ").lower()
            if user_answer == data["answer"]:
                #Adding score and displaying lives
                score += 1
                print("Correct answer")
                print("Your score is: ", score)
                print("You have ", lives, "lives")
            #Decreasing lives. Game over when all lives gone 
            else:
                print("Incorrect answer")
                lives -= 1
                print("You have ", lives, "lives")
                if lives == 0:
                    print("Game over. You ran out of lives")
                    print("")
                    restart = input("Would you like to restart? ").lower()
                    if restart == "no":
                        print("You can always come back")
                        #Breaking the while loop generated at the start
                        running = False
                    #Restarting if the user chooses to   
                    elif restart == "yes":
                        lives = 3
                        score = 0
                        restart = ""
                        break
                    break
        #Restart comment is different because the code has 2 restart systems
        #it escapes the 1st after the user says no, then enters the 2nd. user inputs no again to finally end the program
        lives = 0
        print("")
        restart = input("Would you really not like to restart? ").lower()
        #data reset when user chooses to restart for new quiz
        if restart == "yes":
            score = 0
            lives = 3
            continue
        elif restart == "no":
            print("You can always come back")
            break