# Google Sheets Configuration
import os
from google.oauth2.service_account import Credentials

# Google Sheets Configuration
SCOPES = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive'
]

# Sheet IDs and worksheet names
SHEET_CONFIG = {
    'MUTUAL_FUNDS': {
        'sheet_id': 'your_mutual_funds_sheet_id',  # Replace with your actual sheet ID
        'worksheet': 'MutualFunds'
    },
    'SIPS': {
        'sheet_id': 'your_sips_sheet_id',  # Replace with your actual sheet ID
        'worksheet': 'SIPs'
    },
    'FD_RD': {
        'sheet_id': 'your_fd_rd_sheet_id',  # Replace with your actual sheet ID
        'worksheet': 'FD_RD'
    },
    'FINANCIAL_PLANS': {
        'sheet_id': 'your_plans_sheet_id',  # Replace with your actual sheet ID
        'worksheet': 'FinancialPlans'
    },
    'MONTHLY_INVESTMENTS': {
        'sheet_id': 'your_monthly_sheet_id',  # Replace with your actual sheet ID
        'worksheet': 'MonthlyInvestments'
    }
}

# Service account credentials file path
CREDENTIALS_FILE = 'credentials.json'  # You'll need to download this from Google Cloud Console

def get_credentials():
    """Get Google Sheets credentials"""
    if os.path.exists(CREDENTIALS_FILE):
        creds = Credentials.from_service_account_file(CREDENTIALS_FILE, scopes=SCOPES)
        return creds
    else:
        return None
