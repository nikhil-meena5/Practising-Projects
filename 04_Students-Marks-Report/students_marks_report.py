#Read a CSV of student names and marks in 5 subjects
#Show each student's total, percentage and grade (A/B/C/Fail). Show the topper.
#Save the result to a new CSV file.

import csv
from pathlib import Path

# Keep files in the same project folder
BASE_DIR = Path(__file__).resolve().parent
INPUT_FILE = BASE_DIR / "students.csv"
OUTPUT_FILE = BASE_DIR / "results.csv"

SUBJECTS = ["MATHS", "SCIENCE", "SST", "ENGLISH", "COMPUTER"]


def calculate_grade(percentage):
    if percentage >= 80:
        return "A"
    elif percentage >= 70:
        return "B"
    elif percentage >= 60:
        return "C"
    else:
        return "FAIL"


def main():
    students = []

    try:
        with open(INPUT_FILE, "r", newline="", encoding="utf-8-sig") as file:
            reader = csv.DictReader(file)

            required_columns = ["NAME"] + SUBJECTS

            if not reader.fieldnames or not all(
                column in reader.fieldnames for column in required_columns
            ):
                print("Error: CSV file has missing or incorrect columns.")
                return

            for row_number, row in enumerate(reader, start=2):
                try:
                    name = row["NAME"].strip()

                    if not name:
                        raise ValueError("Student name is empty")

                    marks = [int(row[sub]) for sub in SUBJECTS]

                    if any(mark < 0 or mark > 100 for mark in marks):
                        raise ValueError("Marks must be between 0 and 100")

                    total = sum(marks)
                    percentage = total / len(SUBJECTS)
                    grade = calculate_grade(percentage)

                    students.append({
                        "Name": name,
                        "Total": total,
                        "Percentage": round(percentage, 2),
                        "Grade": grade
                    })

                except (ValueError, TypeError, KeyError) as error:
                    print(f"Skipping row {row_number}: {error}")

    except FileNotFoundError:
        print("Error: students.csv file not found!")
        return
    except OSError as error:
        print("File error:", error)
        return

    if not students:
        print("No valid student records found!")
        return

    print("\n========== STUDENTS MARKS REPORT ==========")

    for student in students:
        print(
            f"{student['Name']} | "
            f"Total: {student['Total']} | "
            f"Percentage: {student['Percentage']}% | "
            f"Grade: {student['Grade']}"
        )

    topper = max(students, key=lambda student: student["Total"])

    print("\n========== CLASS TOPPER ==========")
    print("Name:", topper["Name"])
    print("Total:", topper["Total"])
    print("Percentage:", topper["Percentage"], "%")
    print("Grade:", topper["Grade"])

    try:
        with open(OUTPUT_FILE, "w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(
                file,
                fieldnames=["Name", "Total", "Percentage", "Grade"]
            )

            writer.writeheader()
            writer.writerows(students)

        print("\nResults saved successfully!")
        print("Output file:", OUTPUT_FILE.name)

    except OSError as error:
        print("Could not save results:", error)


if __name__ == "__main__":
    main()
