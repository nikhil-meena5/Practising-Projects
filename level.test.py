#print only the even numbers from a list ,plus their total.
def even_number(numbers):
    total = 0

    for num in numbers:
        if num % 2 == 0 :
            print (num)
            total +=1

    return total

result = even_number([1,2,3,4,5,6,7,8,9,10])
print (result)

#count how many times  each word appears in a sentence 

text = "each word appear in a sentence each of folloowing question  that does not make logic of it each chahracter and these each word is coming through it ."
count = 0  

for char in text:
    if char in text:
        count += 1

print("number of each:",count)