import gspread
import pandas as pd
from datetime import datetime
from config import get_credentials, SHEET_CONFIG
import streamlit as st

class GoogleSheetsManager:
    def __init__(self):
        self.credentials = get_credentials()
        self.gc = None
        if self.credentials:
            try:
                self.gc = gspread.authorize(self.credentials)
            except Exception as e:
                st.error(f"Failed to authenticate with Google Sheets: {str(e)}")
    
    def get_worksheet(self, sheet_type):
        """Get a specific worksheet"""
        if not self.gc:
            return None
        
        try:
            config = SHEET_CONFIG[sheet_type]
            sheet = self.gc.open_by_key(config['sheet_id'])
            worksheet = sheet.worksheet(config['worksheet'])
            return worksheet
        except Exception as e:
            st.error(f"Failed to access worksheet {sheet_type}: {str(e)}")
            return None
    
    def read_data(self, sheet_type):
        """Read data from a worksheet"""
        worksheet = self.get_worksheet(sheet_type)
        if not worksheet:
            return pd.DataFrame()
        
        try:
            records = worksheet.get_all_records()
            return pd.DataFrame(records)
        except Exception as e:
            st.error(f"Failed to read data from {sheet_type}: {str(e)}")
            return pd.DataFrame()
    
    def write_data(self, sheet_type, data):
        """Write data to a worksheet"""
        worksheet = self.get_worksheet(sheet_type)
        if not worksheet:
            return False
        
        try:
            if isinstance(data, pd.DataFrame):
                # Clear existing data and write new data
                worksheet.clear()
                if not data.empty:
                    # Add headers
                    worksheet.append_row(data.columns.tolist())
                    # Add data rows
                    for _, row in data.iterrows():
                        worksheet.append_row(row.tolist())
            return True
        except Exception as e:
            st.error(f"Failed to write data to {sheet_type}: {str(e)}")
            return False
    
    def append_data(self, sheet_type, data):
        """Append data to a worksheet"""
        worksheet = self.get_worksheet(sheet_type)
        if not worksheet:
            return False
        
        try:
            if isinstance(data, dict):
                # Convert dict to list in the correct order
                headers = worksheet.row_values(1)
                row_data = [data.get(header, '') for header in headers]
                worksheet.append_row(row_data)
            elif isinstance(data, list):
                worksheet.append_row(data)
            return True
        except Exception as e:
            st.error(f"Failed to append data to {sheet_type}: {str(e)}")
            return False
    
    def update_row(self, sheet_type, row_index, data):
        """Update a specific row"""
        worksheet = self.get_worksheet(sheet_type)
        if not worksheet:
            return False
        
        try:
            if isinstance(data, dict):
                headers = worksheet.row_values(1)
                for col, value in data.items():
                    if col in headers:
                        col_index = headers.index(col) + 1
                        worksheet.update_cell(row_index + 1, col_index, value)
            return True
        except Exception as e:
            st.error(f"Failed to update row in {sheet_type}: {str(e)}")
            return False
    
    def delete_row(self, sheet_type, row_index):
        """Delete a specific row"""
        worksheet = self.get_worksheet(sheet_type)
        if not worksheet:
            return False
        
        try:
            worksheet.delete_rows(row_index + 1)
            return True
        except Exception as e:
            st.error(f"Failed to delete row in {sheet_type}: {str(e)}")
            return False

# Initialize the manager
@st.cache_resource
def get_sheets_manager():
    return GoogleSheetsManager()
