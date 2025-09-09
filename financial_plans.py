import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, date, timedelta
from google_sheets_manager import get_sheets_manager

def show_financial_plans():
    """Financial Plans Management"""
    st.header("📋 Financial Plans")
    
    sheets_manager = get_sheets_manager()
    
    tab1, tab2, tab3 = st.tabs(["📋 View Plans", "➕ Create Plan", "✏️ Manage Plans"])
    
    with tab1:
        plans_data = sheets_manager.read_data('FINANCIAL_PLANS')
        if not plans_data.empty:
            st.dataframe(plans_data, use_container_width=True)
        else:
            st.info("No financial plans created yet.")
    
    with tab2:
        with st.form("create_plan_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                plan_name = st.text_input("Plan Name*", placeholder="e.g., Retirement Plan 2030")
                plan_type = st.selectbox("Plan Type*", ["Retirement", "Education", "House Purchase", "Emergency Fund", "Other"])
                target_amount = st.number_input("Target Amount (₹)*", min_value=1.0)
                target_date = st.date_input("Target Date*", value=date.today() + timedelta(days=365*5))
            
            with col2:
                current_amount = st.number_input("Current Amount (₹)", min_value=0.0, value=0.0)
                monthly_investment = st.number_input("Monthly Investment (₹)", min_value=0.0, value=0.0)
                expected_return = st.number_input("Expected Return (%)", min_value=0.0, max_value=20.0, format="%.2f", value=12.0)
                priority = st.selectbox("Priority", ["High", "Medium", "Low"])
            
            description = st.text_area("Description", placeholder="Detailed description of the plan")
            
            submitted = st.form_submit_button("Create Plan", type="primary")
            
            if submitted:
                if plan_name and plan_type and target_amount and target_date:
                    new_plan = {
                        'id': datetime.now().strftime("%Y%m%d%H%M%S"),
                        'name': plan_name,
                        'type': plan_type,
                        'target_amount': target_amount,
                        'target_date': target_date.strftime("%Y-%m-%d"),
                        'current_amount': current_amount,
                        'monthly_investment': monthly_investment,
                        'expected_return': expected_return,
                        'priority': priority,
                        'description': description,
                        'status': 'Active',
                        'date_created': datetime.now().strftime("%Y-%m-%d")
                    }
                    
                    if sheets_manager.append_data('FINANCIAL_PLANS', new_plan):
                        st.success("✅ Plan created successfully!")
                        st.rerun()
                    else:
                        st.error("❌ Failed to create plan.")
                else:
                    st.error("Please fill in all required fields (*).")
    
    with tab3:
        plans_data = sheets_manager.read_data('FINANCIAL_PLANS')
        if not plans_data.empty:
            selected_plan = st.selectbox(
                "Select Plan to Manage",
                options=plans_data.index,
                format_func=lambda x: f"{plans_data.loc[x, 'name']} - {plans_data.loc[x, 'type']}"
            )
            
            plan_info = plans_data.loc[selected_plan]
            
            # Calculate plan progress
            target_amount = float(plan_info['target_amount'])
            current_amount = float(plan_info['current_amount'])
            monthly_investment = float(plan_info['monthly_investment'])
            expected_return = float(plan_info['expected_return'])
            
            progress_percentage = (current_amount / target_amount * 100) if target_amount > 0 else 0
            
            st.subheader("Plan Progress")
            st.progress(progress_percentage / 100)
            st.write(f"**Progress:** {progress_percentage:.1f}% (₹{current_amount:,.2f} / ₹{target_amount:,.2f})")
            
            # Projected completion
            if monthly_investment > 0 and expected_return > 0:
                months_to_complete = np.log(target_amount / current_amount) / np.log(1 + expected_return/100/12)
                completion_date = date.today() + timedelta(days=months_to_complete * 30)
                st.write(f"**Projected Completion:** {completion_date.strftime('%Y-%m-%d')}")
            
            # Status management
            col1, col2 = st.columns(2)
            with col1:
                if st.button("✅ Mark as Completed", type="secondary"):
                    if sheets_manager.update_row('FINANCIAL_PLANS', selected_plan, {'status': 'Completed'}):
                        st.success("✅ Plan marked as completed!")
                        st.rerun()
            
            with col2:
                if st.button("🗑️ Delete Plan", type="secondary"):
                    if sheets_manager.delete_row('FINANCIAL_PLANS', selected_plan):
                        st.success("✅ Plan deleted!")
                        st.rerun()
        else:
            st.info("No plans to manage.")
