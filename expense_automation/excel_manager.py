import pandas as pd
import os
from datetime import datetime

EXCEL_FILE = 'monthly_expenses.xlsx'

def initialize_excel():
    """
    Creates the Excel file if it doesn't exist.
    """
    if not os.path.exists(EXCEL_FILE):
        df = pd.DataFrame(columns=['Date', 'Category', 'Description', 'Amount'])
        df.to_excel(EXCEL_FILE, index=False)
        print(f"Created {EXCEL_FILE}")
    else:
        print(f"{EXCEL_FILE} already exists")

def add_expense(date, category, description, amount):
    """
    Adds an expense to the Excel sheet.
    """
    if not os.path.exists(EXCEL_FILE):
        initialize_excel()

    df = pd.read_excel(EXCEL_FILE)
    new_row = pd.DataFrame({'Date': [date], 'Category': [category], 'Description': [description], 'Amount': [amount]})
    df = pd.concat([df, new_row], ignore_index=True)
    df.to_excel(EXCEL_FILE, index=False)
    print(f"Added expense: {category} - ${amount}")

def get_monthly_total(category, month, year):
    """
    Calculates the total expense for a category in a given month and year.
    """
    if not os.path.exists(EXCEL_FILE):
        return 0.0

    df = pd.read_excel(EXCEL_FILE)
    # Ensure Date column is datetime
    df['Date'] = pd.to_datetime(df['Date'])
    
    # Filter by category, month, and year
    mask = (df['Category'] == category) & (df['Date'].dt.month == month) & (df['Date'].dt.year == year)
    total = df.loc[mask, 'Amount'].sum()
    return total
