import streamlit as st
import pandas as pd
from datetime import datetime, date, timedelta
from google_sheets_manager import get_sheets_manager

def show_fd_rd():
    """FD & RD Management"""
    st.header("🏦 Fixed Deposits & Recurring Deposits")
    
    sheets_manager = get_sheets_manager()
    
    tab1, tab2, tab3 = st.tabs(["📋 View FD/RD", "➕ Add FD/RD", "✏️ Manage FD/RD"])
    
    with tab1:
        fd_rd_data = sheets_manager.read_data('FD_RD')
        if not fd_rd_data.empty:
            st.dataframe(fd_rd_data, use_container_width=True)
        else:
            st.info("No FD/RD added yet.")
    
    with tab2:
        with st.form("add_fd_rd_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                name = st.text_input("FD/RD Name*", placeholder="e.g., SBI FD 2024")
                type_investment = st.selectbox("Type*", ["FD", "RD"])
                bank = st.text_input("Bank*", placeholder="e.g., State Bank of India")
                amount = st.number_input("Amount (₹)*", min_value=1.0)
            
            with col2:
                interest_rate = st.number_input("Interest Rate (%)*", min_value=0.0, max_value=20.0, format="%.2f")
                start_date = st.date_input("Start Date*", value=date.today())
                maturity_date = st.date_input("Maturity Date*", value=date.today() + timedelta(days=365))
                status = st.selectbox("Status*", ["Active", "Matured", "Premature Closure"])
            
            notes = st.text_area("Notes", placeholder="Additional notes")
            
            submitted = st.form_submit_button("Add FD/RD", type="primary")
            
            if submitted:
                if name and type_investment and bank and amount and interest_rate and status:
                    new_fd_rd = {
                        'id': datetime.now().strftime("%Y%m%d%H%M%S"),
                        'name': name,
                        'type': type_investment,
                        'bank': bank,
                        'amount': amount,
                        'interest_rate': interest_rate,
                        'start_date': start_date.strftime("%Y-%m-%d"),
                        'maturity_date': maturity_date.strftime("%Y-%m-%d"),
                        'status': status,
                        'notes': notes,
                        'date_created': datetime.now().strftime("%Y-%m-%d")
                    }
                    
                    if sheets_manager.append_data('FD_RD', new_fd_rd):
                        st.success("✅ FD/RD added successfully!")
                        st.rerun()
                    else:
                        st.error("❌ Failed to add FD/RD.")
                else:
                    st.error("Please fill in all required fields (*).")
    
    with tab3:
        fd_rd_data = sheets_manager.read_data('FD_RD')
        if not fd_rd_data.empty:
            selected_fd_rd = st.selectbox(
                "Select FD/RD to Manage",
                options=fd_rd_data.index,
                format_func=lambda x: f"{fd_rd_data.loc[x, 'name']} - ₹{fd_rd_data.loc[x, 'amount']}"
            )
            
            fd_rd_info = fd_rd_data.loc[selected_fd_rd]
            
            # Calculate maturity value
            start_date = pd.to_datetime(fd_rd_info['start_date'])
            maturity_date = pd.to_datetime(fd_rd_info['maturity_date'])
            years = (maturity_date - start_date).days / 365.25
            principal = float(fd_rd_info['amount'])
            rate = float(fd_rd_info['interest_rate'])
            
            if fd_rd_info['type'] == 'FD':
                maturity_value = principal * (1 + rate/100) ** years
            else:  # RD
                # Simple RD calculation (monthly compounding)
                months = years * 12
                maturity_value = principal * months * (1 + rate/100/12) ** months
            
            st.subheader("FD/RD Details")
            col1, col2 = st.columns(2)
            
            with col1:
                st.write(f"**Name:** {fd_rd_info['name']}")
                st.write(f"**Type:** {fd_rd_info['type']}")
                st.write(f"**Bank:** {fd_rd_info['bank']}")
                st.write(f"**Amount:** ₹{fd_rd_info['amount']:,.2f}")
            
            with col2:
                st.write(f"**Interest Rate:** {fd_rd_info['interest_rate']}%")
                st.write(f"**Start Date:** {fd_rd_info['start_date']}")
                st.write(f"**Maturity Date:** {fd_rd_info['maturity_date']}")
                st.write(f"**Estimated Maturity Value:** ₹{maturity_value:,.2f}")
            
            # Status management
            col1, col2 = st.columns(2)
            with col1:
                if st.button("✅ Mark as Matured", type="secondary"):
                    if sheets_manager.update_row('FD_RD', selected_fd_rd, {'status': 'Matured'}):
                        st.success("✅ Status updated!")
                        st.rerun()
            
            with col2:
                if st.button("🗑️ Delete FD/RD", type="secondary"):
                    if sheets_manager.delete_row('FD_RD', selected_fd_rd):
                        st.success("✅ FD/RD deleted!")
                        st.rerun()
        else:
            st.info("No FD/RD to manage.")
