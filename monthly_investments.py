import streamlit as st
import pandas as pd
from datetime import datetime, date
from google_sheets_manager import get_sheets_manager


def show_monthly_investments():
    """Monthly Investments Tracking"""
    st.header("📅 Monthly Investments")
    
    sheets_manager = get_sheets_manager()
    
    tab1, tab2 = st.tabs(["📋 View Investments", "➕ Add Investment"])
    
    with tab1:
        monthly_data = sheets_manager.read_data('MONTHLY_INVESTMENTS')
        if not monthly_data.empty:
            st.dataframe(monthly_data, use_container_width=True)
            st.subheader("Investment Summary by Type")
            summary = monthly_data.groupby('type')['amount'].sum()
            st.bar_chart(summary)
        else:
            st.info("No monthly investments recorded yet.")
    
    with tab2:
        with st.form("add_monthly_investment_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                investment_type = st.selectbox("Investment Type*", 
                    ["Mutual Fund", "SIP", "FD", "RD", "Stocks", "Bonds", "Gold", "Other"])
                amount = st.number_input("Amount (₹)*", min_value=1.0)
                date_invested = st.date_input("Investment Date*", value=date.today())
            
            with col2:
                description = st.text_input("Description", placeholder="e.g., HDFC Top 100 SIP")
                category = st.selectbox("Category", ["Equity", "Debt", "Hybrid", "Commodity", "Other"])
                notes = st.text_area("Notes", placeholder="Additional notes")
            
            submitted = st.form_submit_button("Add Investment", type="primary")
            
            if submitted:
                if investment_type and amount and date_invested:
                    new_investment = {
                        'id': datetime.now().strftime("%Y%m%d%H%M%S"),
                        'type': investment_type,
                        'amount': amount,
                        'date': date_invested.strftime("%Y-%m-%d"),
                        'description': description,
                        'category': category,
                        'notes': notes,
                        'date_created': datetime.now().strftime("%Y-%m-%d")
                    }
                    
                    if sheets_manager.append_data('MONTHLY_INVESTMENTS', new_investment):
                        st.success("✅ Investment added successfully!")
                        st.rerun()
                    else:
                        st.error("❌ Failed to add investment.")
                else:
                    st.error("Please fill in all required fields (*).")
