#Read a CSV of student names and marks in 5 subjects
#Show each student's total, percentage and grade (A/B/C/Fail). Show the topper.
#Save the result to a new CSV file.
import csv

students = []  

with open("students.csv", "r") as file:
    reader = csv.DictReader(file)

    for row in reader:
        NAME = row["NAME"]
        
        
        marks = [int(row[sub]) for sub in
                 ["MATHS","SCIENCE","SST","ENGLISH","COMPUTER"]]


        total = sum(marks)
        percentage = total / 5

    
        if percentage >= 80:
            grade = "A"
        elif percentage >= 70:
            grade = "B"
        elif percentage >= 60:
            grade = "C"
        else:
            grade = "FAIL"

        students.append([NAME, total, percentage, grade])

# Display results
for s in students:
    print(s)

# Find topper
topper = max(students, key=lambda x: x[1])


print("\nTopper:", topper[0])
print("Total:", topper[1])
print("Percentage:", topper[2], "%")
print("Grade:", topper[3])



# Save results to new CSV file
with open("results.csv", "w", newline="") as file:
    writer = csv.writer(file)

    writer.writerow(["Name", "Total", "Percentage", "Grade"])
    writer.writerows(students)

print("\nResults saved successfully!")

