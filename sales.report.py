# Sales report from Excel (full week)
# Give the intern a sample sales sheet (Date, Product, Quantity, Price, City). 100+ rows.
# Script must show: total sales, best-selling product, sales per month, sales per city.
# Save the summary to a new Excel file with a chart.
# Skills: pandas, openpyxl or matplotlib.
# How to check:
# Totals match what Excel shows (use SUM / pivot table). 
# The new Excel file opens and the chart is correct. 
# Bonus: Let the user choose a month and see only that month's report.



import pandas as pd
from openpyxl import load_workbook
from openpyxl.chart import BarChart, Reference

# Step 1: Read Excel file
df = pd.read_excel("sales_data.xlsx")

# Step 2: Calculate total sales
df["Sales"] = df["Quantity"] * df["Price"]

# Step 3: Calculate total sales amount
total_sales = df["Sales"].sum()

print("\n----- SALES REPORT -----")
print("Total Sales: Rs.", total_sales)

# Step 4: Find best-selling product
product_sales = df.groupby("Product")["Quantity"].sum()

best_product = product_sales.idxmax()
best_quantity = product_sales.max()

print("\nBest Selling Product:", best_product)
print("Quantity Sold:", best_quantity)

# Step 5: Sales per month
df["Date"] = pd.to_datetime(df["Date"])
df["Month"] = df["Date"].dt.strftime("%Y-%m")

monthly_sales = df.groupby("Month")["Sales"].sum()

print("\nSales Per Month:")
print(monthly_sales)

# Step 6: Sales per city
city_sales = df.groupby("City")["Sales"].sum()

print("\nSales Per City:")
print(city_sales)

# Step 7: Save summary to a new Excel file
with pd.ExcelWriter("sales_summary.xlsx", engine="openpyxl") as writer:

    df.to_excel(writer, sheet_name="Sales Data", index=False)

    monthly_sales.to_excel(writer, sheet_name="Monthly Sales")

    city_sales.to_excel(writer, sheet_name="City Sales")

    product_sales.to_excel(writer, sheet_name="Product Sales")

# Step 8: Add chart to Excel file
workbook = load_workbook("sales_summary.xlsx")

sheet = workbook["Monthly Sales"]

chart = BarChart()

chart.title = "Monthly Sales Report"
chart.x_axis.title = "Month"
chart.y_axis.title = "Sales Amount"

data = Reference(sheet, min_col=2, min_row=1,
                 max_row=sheet.max_row)

categories = Reference(sheet, min_col=1, min_row=2,
                       max_row=sheet.max_row)

chart.add_data(data, titles_from_data=True)
chart.set_categories(categories)

sheet.add_chart(chart, "D2")

# Save final Excel file
workbook.save("sales_summary.xlsx")

print("\nExcel report created successfully!")


# Bonus: Monthly Report

month = input("\nEnter month (example: March): ")

month_data = df[
    df["Date"].dt.strftime("%B").str.lower() == month.lower()
]

if len(month_data) > 0:

    print("\nMonthly Report:", month)

    print("Total Sales:", month_data["Sales"].sum())

    print("\nProduct Sales:")
    print(month_data.groupby("Product")["Quantity"].sum())

    print("\nCity Sales:")
    print(month_data.groupby("City")["Sales"].sum())

    month_data.to_excel(
        "selected_month_report.xlsx",
        index=False
    )

    print("\nMonthly Excel report saved!")

else:
    print("Month not found!")
 