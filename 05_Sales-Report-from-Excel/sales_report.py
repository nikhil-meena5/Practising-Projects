"""
sales_report.py  -  Task 3.1: Sales report from Excel
-----------------------------------------------------
Reads  sales_data.xlsx  (Date, Product, Quantity, Price, City) and shows:
    1. Total sales
    2. Best-selling product
    3. Sales per month
    4. Sales per city
Then saves everything to a NEW Excel file with charts.

BONUS: report for only one month.

Usage
    python sales_report.py                       # full report (asks if you want a month)
    python sales_report.py --month 2026-03       # only March 2026
    python sales_report.py --month "March 2026"  # same thing
    python sales_report.py --input my_file.xlsx --output my_summary.xlsx
"""
import argparse
import sys
from pathlib import Path

import pandas as pd
from openpyxl import Workbook
from openpyxl.chart import BarChart, Reference
from openpyxl.chart.label import DataLabelList
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter

REQUIRED_COLUMNS = ["Date", "Product", "Quantity", "Price", "City"]
FONT = "Arial"

# ---------------------------------------------------------------- 1. LOAD
def load_data(path: Path) -> pd.DataFrame:
    """Read the Excel file, validate it and add the Sales + Month columns."""
    if not path.exists():
        sys.exit(f"ERROR: file not found -> {path}")

    df = pd.read_excel(path)
    df.columns = df.columns.str.strip()          # remove accidental spaces in headers

    missing = [c for c in REQUIRED_COLUMNS if c not in df.columns]
    if missing:
        sys.exit(f"ERROR: missing column(s): {missing}. Found: {list(df.columns)}")

    df = df[REQUIRED_COLUMNS].copy()

    # --- clean the data ---
    before = len(df)
    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
    df["Quantity"] = pd.to_numeric(df["Quantity"], errors="coerce")
    df["Price"] = pd.to_numeric(df["Price"], errors="coerce")
    for col in ("Product", "City"):
        df[col] = df[col].astype("string").str.strip().str.title()
    df = df.dropna()                              # drop rows with any blank / bad value
    dropped = before - len(df)
    if dropped:
        print(f"[!] Dropped {dropped} row(s) with missing/invalid values.\n")
    if df.empty:
        sys.exit("ERROR: no valid rows left after cleaning.")

    df["Quantity"] = df["Quantity"].astype(int)
    df["Sales"] = df["Quantity"] * df["Price"]               # the key calculation
    df["Month"] = df["Date"].dt.to_period("M").astype(str)   # e.g. "2026-03"
    return df.sort_values("Date").reset_index(drop=True)


# ---------------------------------------------------------------- 2. ANALYSE
def analyse(df: pd.DataFrame) -> dict:
    """All the numbers the task asks for, using groupby."""
    by_product = (df.groupby("Product")
                    .agg(Units=("Quantity", "sum"), Sales=("Sales", "sum"))
                    .sort_values(["Units", "Sales"], ascending=False)
                    .reset_index())
    by_month = df.groupby("Month")["Sales"].sum().reset_index()      # already in date order
    by_city = (df.groupby("City")["Sales"].sum()
                 .sort_values(ascending=False).reset_index())

    return {
        "total_sales": int(df["Sales"].sum()),
        "total_orders": len(df),
        "total_units": int(df["Quantity"].sum()),
        "best_product": by_product.iloc[0]["Product"],           # most UNITS sold
        "best_product_units": int(by_product.iloc[0]["Units"]),
        "top_revenue_product": by_product.sort_values("Sales", ascending=False).iloc[0]["Product"],
        "by_product": by_product,
        "by_month": by_month,
        "by_city": by_city,
    }


# ---------------------------------------------------------------- 3. PRINT
def print_report(r: dict, title: str) -> None:
    line = "=" * 52
    print(f"\n{line}\n  {title}\n{line}")
    print(f"Total sales          : Rs {r['total_sales']:,}")
    print(f"Total orders / units : {r['total_orders']} / {r['total_units']}")
    print(f"Best-selling product : {r['best_product']} ({r['best_product_units']} units)")
    print(f"Highest revenue item : {r['top_revenue_product']}")
    print("\nSales per month")
    for _, row in r["by_month"].iterrows():
        print(f"  {row['Month']}   Rs {int(row['Sales']):>12,}")
    print("\nSales per city")
    for _, row in r["by_city"].iterrows():
        print(f"  {row['City']:<12} Rs {int(row['Sales']):>12,}")
    print("\nSales per product")
    for _, row in r["by_product"].iterrows():
        print(f"  {row['Product']:<12} {int(row['Units']):>4} units   Rs {int(row['Sales']):>12,}")
    print(line)


# ---------------------------------------------------------------- 4. EXCEL
HEADER_FILL = PatternFill("solid", start_color="1F4E78")
HEADER_FONT = Font(name=FONT, bold=True, color="FFFFFF")
BODY_FONT = Font(name=FONT)
BOLD = Font(name=FONT, bold=True)
THIN = Side(style="thin", color="BFBFBF")
BOX = Border(left=THIN, right=THIN, top=THIN, bottom=THIN)
NUM = "#,##0"


def _header(ws, row, labels, col=1):
    for i, text in enumerate(labels):
        c = ws.cell(row=row, column=col + i, value=text)
        c.font, c.fill, c.border = HEADER_FONT, HEADER_FILL, BOX
        c.alignment = Alignment(horizontal="center")


def _table(ws, top_row, title, headers, rows, num_cols):
    """Write a titled table. Returns (first_data_row, last_data_row)."""
    ws.cell(row=top_row, column=1, value=title).font = Font(name=FONT, bold=True, size=12)
    _header(ws, top_row + 1, headers)
    first = top_row + 2
    for i, values in enumerate(rows):
        for j, v in enumerate(values):
            c = ws.cell(row=first + i, column=1 + j, value=v)
            c.font, c.border = BODY_FONT, BOX
            if j in num_cols:
                c.number_format = NUM
    return first, first + len(rows) - 1


def _bar_chart(ws, title, x_title, y_title, cats_ref, data_ref, anchor, horizontal=False):
    ch = BarChart()
    ch.type = "bar" if horizontal else "col"
    ch.title, ch.style = title, 10
    ch.x_axis.title, ch.y_axis.title = x_title, y_title
    ch.x_axis.delete = False          # required in new openpyxl, else axes are hidden
    ch.y_axis.delete = False
    ch.y_axis.numFmt = NUM
    ch.add_data(data_ref, titles_from_data=True)
    ch.set_categories(cats_ref)
    ch.legend = None
    ch.dataLabels = DataLabelList()
    ch.dataLabels.showVal = True          # show only the number on each bar
    ch.dataLabels.showSerName = False
    ch.dataLabels.showCatName = False
    ch.dataLabels.showLegendKey = False
    ch.dataLabels.showPercent = False
    ch.height, ch.width = 8.5, 16
    ws.add_chart(ch, anchor)


def write_excel(df: pd.DataFrame, r: dict, out_path: Path, title: str, month_mode: bool) -> None:
    wb = Workbook()

    # ---------- Sheet 1: Summary ----------
    ws = wb.active
    ws.title = "Summary"
    ws["A1"] = title
    ws["A1"].font = Font(name=FONT, bold=True, size=16, color="1F4E78")

    kpis = [
        ("Total sales (Rs)", r["total_sales"]),
        ("Total orders", r["total_orders"]),
        ("Total units sold", r["total_units"]),
        ("Best-selling product (by units)", f"{r['best_product']} ({r['best_product_units']} units)"),
        ("Highest-revenue product", r["top_revenue_product"]),
    ]
    for i, (label, value) in enumerate(kpis):
        a = ws.cell(row=3 + i, column=1, value=label)
        b = ws.cell(row=3 + i, column=2, value=value)
        a.font, b.font = BOLD, BODY_FONT
        a.border = b.border = BOX
        b.alignment = Alignment(horizontal="right")
        if isinstance(value, int):
            b.number_format = NUM

    row = 10
    charts = []   # (title, x_title, y_title, header_row, first, last, anchor_row, horizontal)

    if not month_mode:
        m_first, m_last = _table(ws, row, "Sales per month", ["Month", "Sales (Rs)"],
                                 r["by_month"].values.tolist(), {1})
        charts.append(("Sales per month", "Month", "Sales (Rs)", 1, row + 1, m_first, m_last, 3, False))
        row = m_last + 3

    c_first, c_last = _table(ws, row, "Sales per city", ["City", "Sales (Rs)"],
                             r["by_city"].values.tolist(), {1})
    charts.append(("Sales per city", "City", "Sales (Rs)", 1, row + 1, c_first, c_last,
                   3 if month_mode else 21, False))
    row = c_last + 3

    p_first, p_last = _table(ws, row, "Sales per product", ["Product", "Units sold", "Sales (Rs)"],
                             r["by_product"].values.tolist(), {1, 2})
    charts.append(("Sales per product", "Product", "Sales (Rs)", 2, row + 1, p_first, p_last,
                   21 if month_mode else 39, False))

    for (t, xt, yt, data_col, hdr, first, last, anchor_row, horiz) in charts:
        cats = Reference(ws, min_col=1, min_row=first, max_row=last)
        data = Reference(ws, min_col=1 + data_col, min_row=hdr, max_row=last)
        _bar_chart(ws, t, xt, yt, cats, data, f"E{anchor_row}", horiz)

    ws.column_dimensions["A"].width = 34
    ws.column_dimensions["B"].width = 26
    ws.column_dimensions["C"].width = 16

    # ---------- Sheet 2: Data (raw rows + Sales formula) ----------
    wd = wb.create_sheet("Data")
    _header(wd, 1, ["Date", "Product", "Quantity", "Price", "City", "Sales", "Month"])
    for i, rec in enumerate(df.itertuples(index=False), start=2):
        wd.cell(row=i, column=1, value=rec.Date.to_pydatetime()).number_format = "dd-mmm-yyyy"
        wd.cell(row=i, column=2, value=rec.Product)
        wd.cell(row=i, column=3, value=int(rec.Quantity))
        wd.cell(row=i, column=4, value=int(rec.Price)).number_format = NUM
        wd.cell(row=i, column=5, value=rec.City)
        wd.cell(row=i, column=6, value=f"=C{i}*D{i}").number_format = NUM   # live Excel formula
        wd.cell(row=i, column=7, value=rec.Month)
        for col in range(1, 8):
            wd.cell(row=i, column=col).font = BODY_FONT
    for col, w in zip("ABCDEFG", (14, 14, 10, 10, 14, 12, 10)):
        wd.column_dimensions[col].width = w
    wd.freeze_panes = "A2"
    last_row = len(df) + 1
    S = f"Data!$F$2:$F${last_row}"     # Sales column
    Q = f"Data!$C$2:$C${last_row}"     # Quantity column

    # ---------- Sheet 3: Verification (Excel formulas vs Python numbers) ----------
    wv = wb.create_sheet("Verification")
    wv["A1"] = "Cross-check: Python (pandas) result vs Excel formula on the Data sheet"
    wv["A1"].font = Font(name=FONT, bold=True, size=12)
    _header(wv, 3, ["Check", "Python result", "Excel formula result", "Difference", "Status"])
    checks = [("TOTAL SALES", f"=Summary!B3", f"=SUM({S})"),
              ("TOTAL UNITS", f"=Summary!B5", f"=SUM({Q})")]
    if not month_mode:
        for i in range(len(r["by_month"])):
            rr = m_first + i
            checks.append((f"Month {r['by_month'].iloc[i]['Month']}", f"=Summary!B{rr}",
                           f'=SUMIFS({S},Data!$G$2:$G${last_row},Summary!A{rr})'))
    for i in range(len(r["by_city"])):
        rr = c_first + i
        checks.append((f"City {r['by_city'].iloc[i]['City']}", f"=Summary!B{rr}",
                       f'=SUMIFS({S},Data!$E$2:$E${last_row},Summary!A{rr})'))
    for i in range(len(r["by_product"])):
        rr = p_first + i
        checks.append((f"Product {r['by_product'].iloc[i]['Product']} (sales)", f"=Summary!C{rr}",
                       f'=SUMIFS({S},Data!$B$2:$B${last_row},Summary!A{rr})'))
        checks.append((f"Product {r['by_product'].iloc[i]['Product']} (units)", f"=Summary!B{rr}",
                       f'=SUMIFS({Q},Data!$B$2:$B${last_row},Summary!A{rr})'))
    for i, (label, py, xl) in enumerate(checks, start=4):
        wv.cell(row=i, column=1, value=label)
        wv.cell(row=i, column=2, value=py)
        wv.cell(row=i, column=3, value=xl)
        wv.cell(row=i, column=4, value=f"=B{i}-C{i}")
        wv.cell(row=i, column=5, value=f'=IF(ABS(D{i})<0.01,"OK","MISMATCH")')
        for col in range(1, 6):
            c = wv.cell(row=i, column=col)
            c.font, c.border = BODY_FONT, BOX
            if col in (2, 3, 4):
                c.number_format = NUM
    end = 3 + len(checks)
    wv.cell(row=end + 2, column=1, value="Overall result").font = BOLD
    wv.cell(row=end + 2, column=2,
            value=f'=IF(COUNTIF(E4:E{end},"MISMATCH")=0,"ALL MATCH","CHECK ERRORS")').font = BOLD
    wv.cell(row=end + 4, column=1,
            value="Note: 'Python result' comes from pandas (via the Summary sheet). "
                  "'Excel formula result' is recalculated live from the Data sheet.").font = Font(name=FONT, italic=True)
    for col, w in zip("ABCDE", (34, 18, 22, 14, 12)):
        wv.column_dimensions[col].width = w

    wb.save(out_path)


# ---------------------------------------------------------------- 5. BONUS: MONTH CHOICE
def resolve_month(text: str, available: list) -> str:
    """Turn user text ('2026-03', 'March 2026', 'March', '3') into '2026-03'."""
    text = text.strip()
    if text in available:
        return text
    years = sorted({m[:4] for m in available})
    try:
        if text.isdigit() and 1 <= int(text) <= 12 and len(years) == 1:
            return f"{years[0]}-{int(text):02d}"
        parsed = pd.to_datetime(text, errors="raise")
        if text.replace(" ", "").isalpha() and len(text.split()) == 1 and len(years) == 1:
            return f"{years[0]}-{parsed.month:02d}"       # just a month name
        return parsed.strftime("%Y-%m")
    except (ValueError, TypeError):
        return ""


def ask_month(available: list) -> str:
    """Interactive prompt. Empty answer = full report."""
    print("Months available:", ", ".join(available))
    ans = input("Type a month (e.g. 2026-03 or 'March') for a single-month report, "
                "or press Enter for the full report: ")
    return ans.strip()


# ---------------------------------------------------------------- MAIN
def main():
    ap = argparse.ArgumentParser(description="Sales report from an Excel file")
    ap.add_argument("--input", default="sales_data.xlsx", help="input Excel file")
    ap.add_argument("--output", default=None, help="output Excel file name")
    ap.add_argument("--month", default=None, help="only this month, e.g. 2026-03 or 'March 2026'")
    args = ap.parse_args()

    df = load_data(Path(args.input))
    available = sorted(df["Month"].unique())
    print(f"Loaded {len(df)} rows  ({df['Date'].min():%d-%b-%Y} to {df['Date'].max():%d-%b-%Y})")

    month_text = args.month if args.month is not None else ask_month(available)

    if month_text:
        month = resolve_month(month_text, available)
        if month not in available:
            sys.exit(f"ERROR: no data for '{month_text}'. Available: {', '.join(available)}")
        df = df[df["Month"] == month].reset_index(drop=True)
        label = pd.Period(month).strftime("%B %Y")
        title, month_mode = f"Sales Report - {label}", True
        out = Path(args.output or f"sales_summary_{month}.xlsx")
    else:
        title, month_mode = "Sales Report - Full Period", False
        out = Path(args.output or "sales_summary.xlsx")

    result = analyse(df)
    print_report(result, title)
    write_excel(df, result, out, title, month_mode)
    print(f"\nSaved -> {out.resolve()}")


if __name__ == "__main__":
    main()
