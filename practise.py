#####################################################################################

num1=int(input("enter the number:"))
if num1 % 2 == 0:
    print("even")

else:
    print("odd")



##################-------------------------------------####################



#Write a function largest(a, b, c) that returns the largest of three numbers.
a= 19
b=45
c=1
if a>=b and a>=c:
    print(a)

elif b>=a and b>=c:
    print(b)

elif c>=b and c>=a:
    print(c)

else:
    print("there is no largest ")


#######--------------------------------------------------------------##############

#Write a function that reverses a string without using a loop.


def reverse_stringe(text):
    return text [::-1]

print(reverse_stringe("powershell"))
print(reverse_stringe("text"))

#######################################################################

#Count how many vowels appear in the string 'programming is fun'
text= "programming is fun, ai is the future  "
count = 0 
 
for char in text:
    if char in "a,e,i,o,u":
        count += 1

print("number of vowel:",count)


####################################################################
#Given [1, 2, 2, 3, 1, 4], create a list containing each value only once.
numbers =[1, 2, 2, 3, 1, 4]
result =list(set(numbers))

print(result)


##########################################################################
#Write a function greet(name, message='Welcome') that prints the name and message.
#  Make one call using the default message and another using a custom message

def greet(name,message='Welcome'):
    print(name,message)

greet("NIKHIL")
greet("john","GOOD MORNING")

####################################################################################
#Write a function multiply(a, b) that returns the product. 
# Store the result of multiply(6, 7) and print it.



def multiply(a,b):
    return(a*b)

result = multiply(6,7)
print(result)

###############################################################################
#Predict the output: #x = 5; def test(): x = 10; print(x); test(); print(x).
#Why are the two outputs different?

x = 5

def test():
    x=10
    print(x)

test();
print(x)    

###############################################################################
#Predict the output: items = [1, 2]; def update(x): x.append(3); update(items); print(items).
 
items= [1,2]

def update(x):
    x.append(3)

update(items)
print(items)

################################################################################
#Write a function count_even(numbers) that returns how many even integers are in a list.

def count_even(numbers):
    count=0


    for num in numbers:
        if num % 2 == 0:
            count += 1

    return count

result = count_even([1,2,3,4,5,6,7,8,9,0,33,44,55,66,77,777,88,999,])
print(result)

########################################################################################
#Write a function count_even(numbers) that returns how many even numbers are in a list.
#  For example, count_even([2, 5, 8, 9, 10]) should return 3

def count_even(numbers):
    count=0


    for num in numbers:
        if num % 2 == 0: 
            count +=1
    
    return count

result = count_even([2,5,8,9,10])
print(result)

#####################################################################################
#Create a function using def.
#Start a variable total = 0.
#Use a for loop to visit each number.
#Add each number to total.
#Return total.
#
def sum_list(numbers):
    total =0 

    for num in numbers:
        total += num

    return total


result =   sum_list([2323,33425,455,343])
print(result)

################################################################################
#Find the largest number in a list.

def largest_list(numbers):
    largest = numbers[0]


    for num in numbers :
        if num > largest:
         largest = num

         return largest 

result = largest_list([2332,4,432,45,443,4,24,23342,31])
print (result)

########################################################################
#Exercise 3: Remove duplicates while preserving order.
def remove_duplicate(numbers):
    unique = []

    for num in numbers:
        if num not in unique:
            unique.apeend(num)

    return unique        

result = remove_duplicate([1,2,3,2,3,4,5,6,4,5,6])
print(result)