import imaplib
import smtplib
import email
from email.header import decode_header
from email.mime.text import MIMEText
import os
import datetime
import re
import pandas as pd
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configuration
EMAIL_USER = os.getenv('EMAIL_USER')
EMAIL_PASS = os.getenv('EMAIL_PASS')
ALERT_EMAIL = os.getenv('ALERT_EMAIL', EMAIL_USER)
EXPENSE_LIMIT = 100.0
EXCEL_FILE = 'monthly_expenses.xlsx'

CATEGORIES = {
    'Costco': {'subject': 'receipt', 'sender': 'costco.com'},
    'PG&E': {'subject': 'bill', 'sender': 'pge.com'},
    'Sanitation': {'subject': 'bill', 'sender': 'sanitation.com'},
    'Internet': {'subject': 'bill', 'sender': 'isp.com'}
}

def initialize_excel():
    if not os.path.exists(EXCEL_FILE):
        df = pd.DataFrame(columns=['Date', 'Category', 'Description', 'Amount'])
        df.to_excel(EXCEL_FILE, index=False)
        print(f"Created {EXCEL_FILE}")

def add_expense(date, category, description, amount):
    if not os.path.exists(EXCEL_FILE):
        initialize_excel()
    
    df = pd.read_excel(EXCEL_FILE)
    new_row = pd.DataFrame({'Date': [date], 'Category': [category], 'Description': [description], 'Amount': [amount]})
    df = pd.concat([df, new_row], ignore_index=True)
    df.to_excel(EXCEL_FILE, index=False)
    print(f"Added expense: {category} - ${amount}")

def get_monthly_total(category, month, year):
    if not os.path.exists(EXCEL_FILE):
        return 0.0
    
    df = pd.read_excel(EXCEL_FILE)
    df['Date'] = pd.to_datetime(df['Date'])
    mask = (df['Category'] == category) & (df['Date'].dt.month == month) & (df['Date'].dt.year == year)
    return df.loc[mask, 'Amount'].sum()

def send_alert(subject, body):
    try:
        msg = MIMEText(body)
        msg['Subject'] = subject
        msg['From'] = EMAIL_USER
        msg['To'] = ALERT_EMAIL

        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(EMAIL_USER, EMAIL_PASS)
            smtp.send_message(msg)
        print(f"Sent alert to {ALERT_EMAIL}")
    except Exception as e:
        print(f"Failed to send alert: {e}")

def parse_amount(body):
    # Simple regex to find dollar amounts
    matches = re.findall(r'\$(\d+\.\d{2})', body)
    if matches:
        return float(matches[0])
    return 0.0

def process_emails():
    if not EMAIL_USER or not EMAIL_PASS:
        print("Error: EMAIL_USER and EMAIL_PASS must be set in .env")
        return

    try:
        # Connect to Gmail IMAP
        mail = imaplib.IMAP4_SSL("imap.gmail.com")
        mail.login(EMAIL_USER, EMAIL_PASS)
        mail.select("inbox")

        today = datetime.date.today()
        # Search for emails from the last 24 hours (simplified to ALL for now, filtering in loop)
        # In production, use proper IMAP search date
        date_str = (datetime.date.today() - datetime.timedelta(days=1)).strftime("%d-%b-%Y")
        status, messages = mail.search(None, f'(SINCE "{date_str}")')
        
        if status != 'OK':
            print("No messages found")
            return

        for num in messages[0].split():
            status, msg_data = mail.fetch(num, "(RFC822)")
            for response_part in msg_data:
                if isinstance(response_part, tuple):
                    msg = email.message_from_bytes(response_part[1])
                    subject, encoding = decode_header(msg["Subject"])[0]
                    if isinstance(subject, bytes):
                        subject = subject.decode(encoding if encoding else "utf-8")
                    sender = msg.get("From")
                    
                    # Check categories
                    for category, criteria in CATEGORIES.items():
                        if criteria['sender'] in sender.lower() and criteria['subject'] in subject.lower():
                            # Extract body
                            body = ""
                            if msg.is_multipart():
                                for part in msg.walk():
                                    if part.get_content_type() == "text/plain":
                                        body = part.get_payload(decode=True).decode()
                                        break
                            else:
                                body = msg.get_payload(decode=True).decode()
                            
                            amount = parse_amount(body)
                            if amount > 0:
                                add_expense(today, category, subject, amount)
                                
                                total = get_monthly_total(category, today.month, today.year)
                                if total > EXPENSE_LIMIT:
                                    alert_sub = f"ALERT: {category} Budget Exceeded"
                                    alert_body = f"Total: ${total:.2f} exceeds limit of ${EXPENSE_LIMIT}"
                                    send_alert(alert_sub, alert_body)

        mail.close()
        mail.logout()
        
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    initialize_excel()
    process_emails()
