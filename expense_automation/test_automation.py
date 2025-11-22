import unittest
from unittest.mock import MagicMock, patch
import os
import pandas as pd
from main import process_expenses
import excel_manager

class TestExpenseAutomation(unittest.TestCase):

    def setUp(self):
        # Clean up excel file before test
        if os.path.exists('monthly_expenses.xlsx'):
            os.remove('monthly_expenses.xlsx')

    def tearDown(self):
        # Clean up excel file after test
        if os.path.exists('monthly_expenses.xlsx'):
            os.remove('monthly_expenses.xlsx')

    @patch('main.get_gmail_service')
    @patch('main.search_messages')
    @patch('main.get_message_body')
    @patch('main.send_email')
    def test_process_expenses(self, mock_send_email, mock_get_body, mock_search, mock_service):
        # Mock Gmail service
        mock_service.return_value = MagicMock()

        # Mock search results (one message for Costco)
        mock_search.return_value = [{'id': '123'}]

        # Mock email body
        mock_get_body.return_value = "Your Costco receipt total is $150.00. Thank you."

        # Run the process
        process_expenses()

        # Verify Excel file was created
        self.assertTrue(os.path.exists('monthly_expenses.xlsx'))
        
        # Verify content
        df = pd.read_excel('monthly_expenses.xlsx')
        self.assertEqual(len(df), 4)
        self.assertEqual(df.iloc[0]['Category'], 'Costco')
        self.assertEqual(df.iloc[0]['Amount'], 150.0)

        # Verify alert was sent (since 150 > 100)
        self.assertEqual(mock_send_email.call_count, 4)
        
        # Check if Costco alert was among the calls
        calls = [args[0][2] for args in mock_send_email.call_args_list]
        self.assertTrue(any('ALERT: Costco Budget Exceeded' in subject for subject in calls))

if __name__ == '__main__':
    unittest.main()
