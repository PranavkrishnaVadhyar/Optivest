import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, date, timedelta
import numpy as np
from google_sheets_manager import get_sheets_manager
from sip_management import show_sip_management
from fd_rd_management import show_fd_rd
from financial_plans import show_financial_plans
from returns_calculator import show_returns_calculator
from monthly_investments import show_monthly_investments
import json

# Page configuration
st.set_page_config(
    page_title="Optivest - Monthly Investment Tracker",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
    }
    .success-message {
        background-color: #d4edda;
        color: #155724;
        padding: 0.75rem;
        border-radius: 0.25rem;
        border: 1px solid #c3e6cb;
    }
    .error-message {
        background-color: #f8d7da;
        color: #721c24;
        padding: 0.75rem;
        border-radius: 0.25rem;
        border: 1px solid #f5c6cb;
    }
    .warning-message {
        background-color: #fff3cd;
        color: #856404;
        padding: 0.75rem;
        border-radius: 0.25rem;
        border: 1px solid #ffeaa7;
    }
</style>
""", unsafe_allow_html=True)

# Initialize Google Sheets Manager
sheets_manager = get_sheets_manager()

def main():
    st.markdown('<h1 class="main-header">💰 Optivest - Monthly Investment Tracker</h1>', unsafe_allow_html=True)
    
    # Check Google Sheets connection
    if not sheets_manager.gc:
        st.warning("⚠️ Google Sheets not configured. Please set up credentials.json file.")
        st.info("For now, the app will work with local data storage.")
    
    # Sidebar navigation
    st.sidebar.title("Navigation")
    page = st.sidebar.selectbox(
        "Choose a page",
        [
            "📊 Dashboard",
            "📈 Mutual Funds",
            "🔄 SIP Management", 
            "🏦 FD & RD",
            "📋 Financial Plans",
            "🧮 Returns Calculator",
            "📅 Monthly Investments"
        ]
    )
    
    if page == "📊 Dashboard":
        show_dashboard()
    elif page == "📈 Mutual Funds":
        show_mutual_funds()
    elif page == "🔄 SIP Management":
        show_sip_management()
    elif page == "🏦 FD & RD":
        show_fd_rd()
    elif page == "📋 Financial Plans":
        show_financial_plans()
    elif page == "🧮 Returns Calculator":
        show_returns_calculator()
    elif page == "📅 Monthly Investments":
        show_monthly_investments()

def show_dashboard():
    """Display the main dashboard"""
    st.header("📊 Investment Dashboard")
    
    # Get data from Google Sheets
    mf_data = sheets_manager.read_data('MUTUAL_FUNDS')
    sip_data = sheets_manager.read_data('SIPS')
    fd_rd_data = sheets_manager.read_data('FD_RD')
    monthly_data = sheets_manager.read_data('MONTHLY_INVESTMENTS')
    
    # Calculate key metrics
    total_monthly_investment = monthly_data['amount'].sum() if not monthly_data.empty else 0
    active_sips = len(sip_data[sip_data['status'] == 'Active']) if not sip_data.empty else 0
    total_fd_rd = fd_rd_data['amount'].sum() if not fd_rd_data.empty else 0
    total_mf_count = len(mf_data) if not mf_data.empty else 0
    
    # Display metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="Monthly Investment",
            value=f"₹{total_monthly_investment:,.2f}"
        )
    
    with col2:
        st.metric(
            label="Active SIPs",
            value=active_sips
        )
    
    with col3:
        st.metric(
            label="FD & RD Amount",
            value=f"₹{total_fd_rd:,.2f}"
        )
    
    with col4:
        st.metric(
            label="Mutual Funds",
            value=total_mf_count
        )
    
    # Monthly investment trend
    if not monthly_data.empty:
        st.subheader("📈 Monthly Investment Trend")
        monthly_data['date'] = pd.to_datetime(monthly_data['date'])
        monthly_summary = monthly_data.groupby(monthly_data['date'].dt.to_period('M'))['amount'].sum()
        
        fig = px.line(
            x=monthly_summary.index.astype(str),
            y=monthly_summary.values,
            title="Monthly Investment Amount",
            labels={'x': 'Month', 'y': 'Amount (₹)'}
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # Investment allocation
    if not monthly_data.empty:
        st.subheader("📊 Investment Allocation")
        allocation_data = monthly_data.groupby('type')['amount'].sum()
        
        if not allocation_data.empty:
            fig = px.pie(
                values=allocation_data.values,
                names=allocation_data.index,
                title="Investment Allocation by Type"
            )
            st.plotly_chart(fig, use_container_width=True)

def show_mutual_funds():
    """Mutual Fund Management"""
    st.header("📈 Mutual Fund Management")
    
    # Tabs for different operations
    tab1, tab2, tab3 = st.tabs(["📋 View Funds", "➕ Add Fund", "✏️ Edit/Delete"])
    
    with tab1:
        mf_data = sheets_manager.read_data('MUTUAL_FUNDS')
        if not mf_data.empty:
            st.dataframe(mf_data, use_container_width=True)
        else:
            st.info("No mutual funds added yet.")
    
    with tab2:
        with st.form("add_mf_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                name = st.text_input("Fund Name*", placeholder="e.g., HDFC Top 100 Fund")
                category = st.selectbox(
                    "Category*",
                    ["Large Cap", "Mid Cap", "Small Cap", "Multi Cap", "ELSS", "Debt", "Hybrid", "Index", "Other"]
                )
                fund_house = st.text_input("Fund House*", placeholder="e.g., HDFC Mutual Fund")
            
            with col2:
                current_nav = st.number_input("Current NAV*", min_value=0.01, format="%.4f")
                fund_code = st.text_input("Fund Code", placeholder="e.g., HDFC100")
                risk_level = st.selectbox("Risk Level*", ["Low", "Medium", "High"])
            
            description = st.text_area("Description", placeholder="Brief description of the fund")
            
            submitted = st.form_submit_button("Add Fund", type="primary")
            
            if submitted:
                if name and category and fund_house and current_nav and risk_level:
                    new_fund = {
                        'id': datetime.now().strftime("%Y%m%d%H%M%S"),
                        'name': name,
                        'category': category,
                        'fund_house': fund_house,
                        'current_nav': current_nav,
                        'fund_code': fund_code,
                        'risk_level': risk_level,
                        'description': description,
                        'date_added': datetime.now().strftime("%Y-%m-%d")
                    }
                    
                    if sheets_manager.append_data('MUTUAL_FUNDS', new_fund):
                        st.success("✅ Fund added successfully!")
                        st.rerun()
                    else:
                        st.error("❌ Failed to add fund.")
                else:
                    st.error("Please fill in all required fields (*).")
    
    with tab3:
        mf_data = sheets_manager.read_data('MUTUAL_FUNDS')
        if not mf_data.empty:
            selected_fund = st.selectbox(
                "Select Fund to Edit/Delete",
                options=mf_data.index,
                format_func=lambda x: f"{mf_data.loc[x, 'name']} - {mf_data.loc[x, 'fund_house']}"
            )
            
            col1, col2 = st.columns(2)
            
            with col1:
                if st.button("✏️ Edit Fund", type="secondary"):
                    st.session_state.editing_fund = selected_fund
                    st.rerun()
            
            with col2:
                if st.button("🗑️ Delete Fund", type="secondary"):
                    if sheets_manager.delete_row('MUTUAL_FUNDS', selected_fund):
                        st.success("✅ Fund deleted successfully!")
                        st.rerun()
                    else:
                        st.error("❌ Failed to delete fund.")
            
            # Edit form
            if hasattr(st.session_state, 'editing_fund') and st.session_state.editing_fund is not None:
                st.subheader("Edit Fund Details")
                fund_to_edit = mf_data.loc[st.session_state.editing_fund]
                
                with st.form("edit_mf_form"):
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        edit_name = st.text_input("Fund Name", value=fund_to_edit['name'])
                        edit_category = st.selectbox("Category", 
                            ["Large Cap", "Mid Cap", "Small Cap", "Multi Cap", "ELSS", "Debt", "Hybrid", "Index", "Other"],
                            index=["Large Cap", "Mid Cap", "Small Cap", "Multi Cap", "ELSS", "Debt", "Hybrid", "Index", "Other"].index(fund_to_edit['category'])
                        )
                        edit_fund_house = st.text_input("Fund House", value=fund_to_edit['fund_house'])
                    
                    with col2:
                        edit_nav = st.number_input("Current NAV", value=float(fund_to_edit['current_nav']), format="%.4f")
                        edit_fund_code = st.text_input("Fund Code", value=fund_to_edit.get('fund_code', ''))
                        edit_risk = st.selectbox("Risk Level", 
                            ["Low", "Medium", "High"],
                            index=["Low", "Medium", "High"].index(fund_to_edit['risk_level'])
                        )
                    
                    edit_description = st.text_area("Description", value=fund_to_edit.get('description', ''))
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        if st.form_submit_button("💾 Save Changes", type="primary"):
                            updated_data = {
                                'name': edit_name,
                                'category': edit_category,
                                'fund_house': edit_fund_house,
                                'current_nav': edit_nav,
                                'fund_code': edit_fund_code,
                                'risk_level': edit_risk,
                                'description': edit_description
                            }
                            
                            if sheets_manager.update_row('MUTUAL_FUNDS', st.session_state.editing_fund, updated_data):
                                st.success("✅ Fund updated successfully!")
                                st.session_state.editing_fund = None
                                st.rerun()
                            else:
                                st.error("❌ Failed to update fund.")
                    
                    with col2:
                        if st.form_submit_button("❌ Cancel"):
                            st.session_state.editing_fund = None
                            st.rerun()
        else:
            st.info("No mutual funds to edit or delete.")

if __name__ == "__main__":
    main()
