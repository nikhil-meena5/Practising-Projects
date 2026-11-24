#Ask for two numbers and an operation (+, −, ×, ÷). Show the answer. 
#Page 1 of 7Python Internship: 3-Month Task Plan Keep running until the user types "exit". 
# Skills: input, if/else, while loop, try/except.
# How to check: Divide by 0 shows a message, does not crash. 
#Typing letters instead of numbers shows a message.
#Typing "exit" closes it.
print("my calculator ")

import math

while True:
    try:

        num1= input("enter the first number (or exit): ")

        if num1.lower() =='exit':
            print("Calculator closed!")
            break
        num1= float(num1)

        operator= input ("Enter  operator(+,-,*,,^,sqrt):")

        if operator.lower() =='exit':
            print("Calculator  closed!")
            break

        if operator =='sqrt':
            if num1 <0:
                print ("cannot find the square root of number")
            else:
                print("result:",math.sqrt(num1))
                continue 

        num2= input('Enter the second number (or exit):')

        if num2.lower() =='exit':
            print("Calculator closed!")
            break
        num2= float(num2)

        if operator =="+":
            print("result:",num1+num2)

        elif operator =="-":
            print("result:",num1-num2)

        elif operator =="*":
            print("result:",num1*num2)    

        elif operator =="/":
            if num1 ==0:
                print("cannot divided by zero")
            else:
                print("result:",num1/num2)

        elif operator =="^":
            print("result:",num1**num2)

        else:
            print("invalid operator!")


    except ValueError:
        print("Invalid input! please enter valid number.")


print("GOODBYE !")    




