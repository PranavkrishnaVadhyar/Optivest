import streamlit as st
import pandas as pd
from datetime import datetime, date
from google_sheets_manager import get_sheets_manager

def show_sip_management():
    """SIP Management"""
    st.header("🔄 SIP Management")
    
    sheets_manager = get_sheets_manager()
    
    tab1, tab2, tab3 = st.tabs(["📋 View SIPs", "➕ Add SIP", "✏️ Manage SIPs"])
    
    with tab1:
        sip_data = sheets_manager.read_data('SIPS')
        if not sip_data.empty:
            st.dataframe(sip_data, use_container_width=True)
        else:
            st.info("No SIPs added yet.")
    
    with tab2:
        with st.form("add_sip_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                sip_name = st.text_input("SIP Name*", placeholder="e.g., HDFC Top 100 SIP")
                fund_id = st.text_input("Fund ID*", placeholder="Fund ID from Mutual Funds")
                amount = st.number_input("SIP Amount (₹)*", min_value=1.0)
                frequency = st.selectbox("Frequency*", ["Monthly", "Weekly", "Quarterly"])
            
            with col2:
                start_date = st.date_input("Start Date*", value=date.today())
                end_date = st.date_input("End Date", value=None)
                status = st.selectbox("Status*", ["Active", "Paused", "Completed"])
                auto_debit = st.checkbox("Auto Debit Enabled")
            
            notes = st.text_area("Notes", placeholder="Additional notes about this SIP")
            
            submitted = st.form_submit_button("Add SIP", type="primary")
            
            if submitted:
                if sip_name and fund_id and amount and frequency and status:
                    new_sip = {
                        'id': datetime.now().strftime("%Y%m%d%H%M%S"),
                        'name': sip_name,
                        'fund_id': fund_id,
                        'amount': amount,
                        'frequency': frequency,
                        'start_date': start_date.strftime("%Y-%m-%d"),
                        'end_date': end_date.strftime("%Y-%m-%d") if end_date else '',
                        'status': status,
                        'auto_debit': auto_debit,
                        'notes': notes,
                        'date_created': datetime.now().strftime("%Y-%m-%d")
                    }
                    
                    if sheets_manager.append_data('SIPS', new_sip):
                        st.success("✅ SIP added successfully!")
                        st.rerun()
                    else:
                        st.error("❌ Failed to add SIP.")
                else:
                    st.error("Please fill in all required fields (*).")
    
    with tab3:
        sip_data = sheets_manager.read_data('SIPS')
        if not sip_data.empty:
            selected_sip = st.selectbox(
                "Select SIP to Manage",
                options=sip_data.index,
                format_func=lambda x: f"{sip_data.loc[x, 'name']} - ₹{sip_data.loc[x, 'amount']}"
            )
            
            sip_info = sip_data.loc[selected_sip]
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                if st.button("⏸️ Pause SIP", type="secondary"):
                    if sheets_manager.update_row('SIPS', selected_sip, {'status': 'Paused'}):
                        st.success("✅ SIP paused!")
                        st.rerun()
            
            with col2:
                if st.button("▶️ Resume SIP", type="secondary"):
                    if sheets_manager.update_row('SIPS', selected_sip, {'status': 'Active'}):
                        st.success("✅ SIP resumed!")
                        st.rerun()
            
            with col3:
                if st.button("✅ Complete SIP", type="secondary"):
                    if sheets_manager.update_row('SIPS', selected_sip, {'status': 'Completed'}):
                        st.success("✅ SIP completed!")
                        st.rerun()
            
            # Display SIP details
            st.subheader("SIP Details")
            col1, col2 = st.columns(2)
            
            with col1:
                st.write(f"**Name:** {sip_info['name']}")
                st.write(f"**Amount:** ₹{sip_info['amount']}")
                st.write(f"**Frequency:** {sip_info['frequency']}")
                st.write(f"**Status:** {sip_info['status']}")
            
            with col2:
                st.write(f"**Start Date:** {sip_info['start_date']}")
                st.write(f"**End Date:** {sip_info.get('end_date', 'Not set')}")
                st.write(f"**Auto Debit:** {'Yes' if sip_info.get('auto_debit') else 'No'}")
                st.write(f"**Notes:** {sip_info.get('notes', 'None')}")
        else:
            st.info("No SIPs to manage.")
