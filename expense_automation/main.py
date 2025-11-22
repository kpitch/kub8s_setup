import os
import datetime
from dotenv import load_dotenv
from gmail_client import get_gmail_service, search_messages, get_message_body, send_email
from excel_manager import initialize_excel, add_expense, get_monthly_total

# Load environment variables
load_dotenv()

# Configuration
EXPENSE_LIMIT = 100.0
ALERT_EMAIL = os.getenv('ALERT_EMAIL', 'me@example.com') # Replace with actual email or env var
CATEGORIES = {
    'Costco': 'from:costco.com subject:receipt',
    'PG&E': 'from:pge.com subject:bill',
    'Sanitation': 'from:sanitation.com subject:bill', # Update with actual sender/subject
    'Internet': 'from:isp.com subject:bill' # Update with actual sender/subject
}

def parse_amount(body, category):
    """
    Parses the amount from the email body based on the category.
    This is a placeholder and needs specific logic for each email format.
    """
    # TODO: Implement specific parsing logic for each vendor
    # This is a dummy implementation
    import re
    # Look for dollar signs
    matches = re.findall(r'\$(\d+\.\d{2})', body)
    if matches:
        return float(matches[0])
    return 0.0

def process_expenses():
    service = get_gmail_service()
    initialize_excel()
    
    today = datetime.date.today()
    # Search for emails from the last month? Or just run daily and check for "newer_than:1d"
    # Let's assume we run this daily
    
    for category, query in CATEGORIES.items():
        full_query = f"{query} newer_than:1d"
        messages = search_messages(service, full_query)
        
        for msg in messages:
            body = get_message_body(service, msg['id'])
            amount = parse_amount(body, category)
            
            if amount > 0:
                add_expense(today, category, "Auto-detected", amount)
                
                # Check limit
                total = get_monthly_total(category, today.month, today.year)
                if total > EXPENSE_LIMIT:
                    subject = f"ALERT: {category} Budget Exceeded"
                    alert_body = f"The total expenses for {category} this month are ${total:.2f}, which exceeds the limit of ${EXPENSE_LIMIT}."
                    send_email(service, ALERT_EMAIL, subject, alert_body)
                    print(f"Sent alert for {category}")

if __name__ == '__main__':
    process_expenses()
