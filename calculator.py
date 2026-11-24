print ("=====MY CALCULATOR=====")

num1= float(input("Enter the number: "))
operator = input("Enter an operator(+,-,*,/): ")
num2 = float (input("Enter the number :"))


if operator == "+":
    Result = num1 + num2
    print("Result:",Result)


elif operator == "-":
    Result = num1 - num2 
    print ("Result:",Result)



elif operator == "*":
    Result = num1 * num2 
    print ("Result:",Result )


elif operator == "/":
    if  num2 != 0:
        Result = num1 / num2
        print ("Result:",Result )
    else:
        print("cannot divided by zero!") 

else:
    print("invalid operator!")
