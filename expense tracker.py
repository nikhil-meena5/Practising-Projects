#Task 4.2:
#  Mini project 1 — Expense tracker (Day 3–5) Add an expense: date, amount, category (Food, Travel, Bills, etc.), note.
#  Show monthly total, total per category, and the biggest expense.
#  Save data to a CSV file.
#  Skills: everything from Weeks 1–3 combined. 
#  How to check:
#  Add 10 expenses, check the totals yourself.
#  Data stays after reopening.
#  Wrong date or negative amount is rejected.
#  Bonus: Pie chart of spending by category.

import pandas as pd
import matplotlib.pyplot as plt
import os
from datetime import datetime

FILE_NAME = "expenses.csv"

CATEGORIES = [
    "Food", "Travel", "Bills",
    "Shopping", "Health", "Other"
]


# Create CSV file
def create_file():
    if not os.path.exists(FILE_NAME):
        df = pd.DataFrame(
            columns=["Date", "Amount", "Category", "Note"]
        )
        df.to_csv(FILE_NAME, index=False)


# Load expenses
def load_data():
    return pd.read_csv(FILE_NAME)


# Add Expense
def add_expense():

    # Date validation
    while True:
        date = input("Enter date (YYYY-MM-DD): ")

        try:
            datetime.strptime(date, "%Y-%m-%d")
            break
        except ValueError:
            print("Invalid date! Please enter YYYY-MM-DD.")

    # Amount validation
    while True:
        try:
            amount = float(input("Enter amount: "))

            if amount <= 0:
                print("Amount must be greater than zero!")
            else:
                break

        except ValueError:
            print("Please enter a valid number.")

    # Category validation
    print("\nAvailable Categories:", CATEGORIES)

    while True:
        category = input("Enter category: ").strip().title()

        if category in CATEGORIES:
            break
        else:
            print("Invalid category! Try again.")

    note = input("Enter note: ")

    new_expense = pd.DataFrame([{
        "Date": date,
        "Amount": amount,
        "Category": category,
        "Note": note
    }])

    new_expense.to_csv(
        FILE_NAME,
        mode="a",
        header=False,
        index=False
    )

    print("\nExpense added successfully!")


# Show all expenses
def show_expenses():

    df = load_data()

    if df.empty:
        print("No expenses found!")
    else:
        print("\nALL EXPENSES")
        print(df.to_string(index=False))


# Monthly total
def monthly_total():

    df = load_data()

    if df.empty:
        print("No expenses found!")
        return

    month = input("Enter month (YYYY-MM): ")

    try:
        datetime.strptime(month, "%Y-%m")
    except ValueError:
        print("Invalid month format!")
        return

    df["Date"] = pd.to_datetime(df["Date"])

    monthly_data = df[
        df["Date"].dt.strftime("%Y-%m") == month
    ]

    print("\nMonthly Total: ₹",
          monthly_data["Amount"].sum())


# Category-wise total
def category_total():

    df = load_data()

    if df.empty:
        print("No expenses found!")
        return

    result = df.groupby("Category")["Amount"].sum()

    print("\nCATEGORY-WISE EXPENSES")
    print(result)


# Biggest expense
def biggest_expense():

    df = load_data()

    if df.empty:
        print("No expenses found!")
        return

    biggest = df.loc[df["Amount"].idxmax()]

    print("\nBIGGEST EXPENSE")
    print(biggest)


# Pie chart
def expense_chart():

    df = load_data()

    if df.empty:
        print("No expenses found!")
        return

    category_data = df.groupby("Category")["Amount"].sum()

    plt.figure(figsize=(8, 8))

    plt.pie(
        category_data,
        labels=category_data.index,
        autopct="%1.1f%%",
        startangle=90
    )

    plt.title("Spending by Category")
    plt.show()


# Main menu
def main():

    create_file()

    while True:

        print("\n===== PERSONAL EXPENSE TRACKER =====")
        print("1. Add Expense")
        print("2. Show All Expenses")
        print("3. Monthly Total")
        print("4. Category-wise Total")
        print("5. Biggest Expense")
        print("6. Pie Chart")
        print("7. Exit")

        choice = input("\nEnter your choice: ")

        if choice == "1":
            add_expense()

        elif choice == "2":
            show_expenses()

        elif choice == "3":
            monthly_total()

        elif choice == "4":
            category_total()

        elif choice == "5":
            biggest_expense()

        elif choice == "6":
            expense_chart()

        elif choice == "7":
            print("Thank you for using Expense Tracker!")
            break

        else:
            print("Invalid choice!")


if __name__ == "__main__":
    main()
