#Number guessing game (Day 4–5) Computer picks a random number 1–100.
#User guesses; show "too high" or "too low".
#Show the number of attempts at the end. 
#Ask "Play again?". Skills: random module, loops, counters. 
#How to check: Hints are correct. Attempt count is correct. 
#Wrong input does not crash it. 
#Bonus: Easy / Medium / Hard levels with limited attempts.
import random

print("NUMBER GUESSING GAME")
print("I'm thinking of a number between 1 and 100.")

secret_number = random.randint(1,100)
attempts = 0

while True:
    try:
        guess = input("ENTER THE NUMBER (OR TYPE 'exit' TO QUIT):")


        if guess.lower().strip() =='exit':
            print("GAME ENDED.THE NUMBER WAS:",secret_number)
            break

        guess= int(guess)
        attempts +=1
                   
        if guess < 1 or guess >100:
            print ("ENTER THE NUMBER BETWEEN 1 TO 100")

        elif guess < secret_number:
            print ("TOO LOW ! TRY AGAIN.")

        elif guess > secret_number:
            print("TOO HIGH !TRY AGAIN.")

        else:
            print("CORRECT YOU GUSSED THE NUMBER.")
            print("NUMBER OF attempts:",attempts) 
            break

    except ValueError:
        print("INVALID INPUT! PLEASE ENTER WHOLE NUMBER.")

print("THANKS FOR PLAYING ")                   

