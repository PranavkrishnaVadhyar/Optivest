import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, date
import json
import os

# Page configuration
st.set_page_config(
    page_title="Optivest - Mutual Fund Tracker",
    page_icon="📈",
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
</style>
""", unsafe_allow_html=True)

# Data storage functions
def load_data():
    """Load data from JSON files"""
    data = {
        'funds': [],
        'transactions': [],
        'portfolio': {}
    }
    
    if os.path.exists('funds.json'):
        with open('funds.json', 'r') as f:
            data['funds'] = json.load(f)
    
    if os.path.exists('transactions.json'):
        with open('transactions.json', 'r') as f:
            data['transactions'] = json.load(f)
    
    if os.path.exists('portfolio.json'):
        with open('portfolio.json', 'r') as f:
            data['portfolio'] = json.load(f)
    
    return data

def save_data(data):
    """Save data to JSON files"""
    with open('funds.json', 'w') as f:
        json.dump(data['funds'], f, indent=2)
    
    with open('transactions.json', 'w') as f:
        json.dump(data['transactions'], f, indent=2)
    
    with open('portfolio.json', 'w') as f:
        json.dump(data['portfolio'], f, indent=2)

def calculate_portfolio_value(data):
    """Calculate current portfolio value"""
    portfolio_value = 0
    for fund in data['funds']:
        fund_id = fund['id']
        units = fund.get('units', 0)
        current_nav = fund.get('current_nav', fund.get('nav', 0))
        portfolio_value += units * current_nav
    return portfolio_value

def calculate_total_investment(data):
    """Calculate total amount invested"""
    total_investment = 0
    for transaction in data['transactions']:
        if transaction['type'] == 'buy':
            total_investment += transaction['amount']
        elif transaction['type'] == 'sell':
            total_investment -= transaction['amount']
    return total_investment

# Initialize session state
if 'data' not in st.session_state:
    st.session_state.data = load_data()

# Main app
def main():
    st.markdown('<h1 class="main-header">📈 Optivest - Mutual Fund Tracker</h1>', unsafe_allow_html=True)
    
    # Sidebar navigation
    st.sidebar.title("Navigation")
    page = st.sidebar.selectbox(
        "Choose a page",
        ["Dashboard", "Add Fund", "Add Transaction", "View Portfolio", "Analytics"]
    )
    
    if page == "Dashboard":
        show_dashboard()
    elif page == "Add Fund":
        show_add_fund()
    elif page == "Add Transaction":
        show_add_transaction()
    elif page == "View Portfolio":
        show_portfolio()
    elif page == "Analytics":
        show_analytics()

def show_dashboard():
    """Display the main dashboard"""
    st.header("📊 Investment Dashboard")
    
    data = st.session_state.data
    
    # Calculate key metrics
    portfolio_value = calculate_portfolio_value(data)
    total_investment = calculate_total_investment(data)
    profit_loss = portfolio_value - total_investment
    profit_loss_percentage = (profit_loss / total_investment * 100) if total_investment > 0 else 0
    
    # Display metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="Portfolio Value",
            value=f"₹{portfolio_value:,.2f}",
            delta=f"{profit_loss_percentage:.2f}%"
        )
    
    with col2:
        st.metric(
            label="Total Investment",
            value=f"₹{total_investment:,.2f}"
        )
    
    with col3:
        st.metric(
            label="Profit/Loss",
            value=f"₹{profit_loss:,.2f}",
            delta=f"{profit_loss_percentage:.2f}%"
        )
    
    with col4:
        st.metric(
            label="Number of Funds",
            value=len(data['funds'])
        )
    
    # Recent transactions
    st.subheader("📋 Recent Transactions")
    if data['transactions']:
        recent_transactions = sorted(data['transactions'], key=lambda x: x['date'], reverse=True)[:5]
        df_transactions = pd.DataFrame(recent_transactions)
        st.dataframe(df_transactions, use_container_width=True)
    else:
        st.info("No transactions yet. Add your first transaction!")
    
    # Portfolio allocation chart
    if data['funds']:
        st.subheader("📊 Portfolio Allocation")
        
        fund_names = []
        fund_values = []
        
        for fund in data['funds']:
            fund_names.append(fund['name'])
            fund_values.append(fund.get('units', 0) * fund.get('current_nav', fund.get('nav', 0)))
        
        if fund_values:
            fig = px.pie(
                values=fund_values,
                names=fund_names,
                title="Portfolio Allocation by Fund"
            )
            st.plotly_chart(fig, use_container_width=True)

def show_add_fund():
    """Add a new mutual fund"""
    st.header("➕ Add New Mutual Fund")
    
    with st.form("add_fund_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            fund_name = st.text_input("Fund Name", placeholder="e.g., HDFC Top 100 Fund")
            fund_category = st.selectbox(
                "Category",
                ["Large Cap", "Mid Cap", "Small Cap", "Multi Cap", "ELSS", "Debt", "Hybrid", "Index", "Other"]
            )
            fund_house = st.text_input("Fund House", placeholder="e.g., HDFC Mutual Fund")
        
        with col2:
            current_nav = st.number_input("Current NAV", min_value=0.01, format="%.4f")
            fund_code = st.text_input("Fund Code (Optional)", placeholder="e.g., HDFC100")
            risk_level = st.selectbox("Risk Level", ["Low", "Medium", "High"])
        
        description = st.text_area("Description (Optional)", placeholder="Brief description of the fund")
        
        submitted = st.form_submit_button("Add Fund", type="primary")
        
        if submitted:
            if fund_name and current_nav:
                new_fund = {
                    "id": len(st.session_state.data['funds']) + 1,
                    "name": fund_name,
                    "category": fund_category,
                    "fund_house": fund_house,
                    "current_nav": current_nav,
                    "nav": current_nav,
                    "fund_code": fund_code,
                    "risk_level": risk_level,
                    "description": description,
                    "units": 0,
                    "date_added": datetime.now().strftime("%Y-%m-%d")
                }
                
                st.session_state.data['funds'].append(new_fund)
                save_data(st.session_state.data)
                
                st.success("✅ Fund added successfully!")
                st.rerun()
            else:
                st.error("Please fill in the fund name and current NAV.")

def show_add_transaction():
    """Add a new transaction"""
    st.header("💸 Add Transaction")
    
    data = st.session_state.data
    
    if not data['funds']:
        st.warning("Please add a fund first before adding transactions.")
        return
    
    with st.form("add_transaction_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            fund_id = st.selectbox(
                "Select Fund",
                options=[(fund['id'], fund['name']) for fund in data['funds']],
                format_func=lambda x: next(fund['name'] for fund in data['funds'] if fund['id'] == x)
            )
            transaction_type = st.selectbox("Transaction Type", ["buy", "sell"])
            amount = st.number_input("Amount (₹)", min_value=0.01)
        
        with col2:
            transaction_date = st.date_input("Transaction Date", value=date.today())
            nav_at_transaction = st.number_input("NAV at Transaction", min_value=0.01, format="%.4f")
            units = st.number_input("Units", min_value=0.0001, format="%.4f")
        
        notes = st.text_area("Notes (Optional)", placeholder="Additional notes about this transaction")
        
        submitted = st.form_submit_button("Add Transaction", type="primary")
        
        if submitted:
            if fund_id and amount and units:
                new_transaction = {
                    "id": len(data['transactions']) + 1,
                    "fund_id": fund_id,
                    "type": transaction_type,
                    "amount": amount,
                    "units": units,
                    "nav": nav_at_transaction,
                    "date": transaction_date.strftime("%Y-%m-%d"),
                    "notes": notes
                }
                
                # Update fund units
                for fund in data['funds']:
                    if fund['id'] == fund_id:
                        if transaction_type == "buy":
                            fund['units'] = fund.get('units', 0) + units
                        else:  # sell
                            fund['units'] = max(0, fund.get('units', 0) - units)
                        break
                
                data['transactions'].append(new_transaction)
                save_data(data)
                st.session_state.data = data
                
                st.success("✅ Transaction added successfully!")
                st.rerun()
            else:
                st.error("Please fill in all required fields.")

def show_portfolio():
    """Display detailed portfolio view"""
    st.header("📋 Portfolio Details")
    
    data = st.session_state.data
    
    if not data['funds']:
        st.info("No funds in your portfolio yet. Add your first fund!")
        return
    
    # Portfolio summary table
    portfolio_data = []
    total_value = 0
    
    for fund in data['funds']:
        if fund.get('units', 0) > 0:
            current_value = fund.get('units', 0) * fund.get('current_nav', fund.get('nav', 0))
            total_value += current_value
            
            # Calculate average cost
            fund_transactions = [t for t in data['transactions'] if t['fund_id'] == fund['id']]
            total_invested = sum(t['amount'] for t in fund_transactions if t['type'] == 'buy')
            total_sold = sum(t['amount'] for t in fund_transactions if t['type'] == 'sell')
            net_invested = total_invested - total_sold
            
            avg_cost = net_invested / fund.get('units', 1) if fund.get('units', 0) > 0 else 0
            profit_loss = current_value - net_invested
            profit_loss_pct = (profit_loss / net_invested * 100) if net_invested > 0 else 0
            
            portfolio_data.append({
                "Fund Name": fund['name'],
                "Category": fund['category'],
                "Units": f"{fund.get('units', 0):.4f}",
                "Current NAV": f"₹{fund.get('current_nav', fund.get('nav', 0)):.4f}",
                "Current Value": f"₹{current_value:.2f}",
                "Avg Cost": f"₹{avg_cost:.4f}",
                "P&L": f"₹{profit_loss:.2f}",
                "P&L %": f"{profit_loss_pct:.2f}%"
            })
    
    if portfolio_data:
        df_portfolio = pd.DataFrame(portfolio_data)
        st.dataframe(df_portfolio, use_container_width=True)
        
        st.subheader(f"Total Portfolio Value: ₹{total_value:,.2f}")
    else:
        st.info("No active holdings in your portfolio.")

def show_analytics():
    """Display analytics and charts"""
    st.header("📈 Analytics & Performance")
    
    data = st.session_state.data
    
    if not data['transactions']:
        st.info("No transaction data available for analytics.")
        return
    
    # Convert transactions to DataFrame
    df_transactions = pd.DataFrame(data['transactions'])
    df_transactions['date'] = pd.to_datetime(df_transactions['date'])
    
    # Monthly investment chart
    st.subheader("📊 Monthly Investment Trend")
    
    monthly_data = df_transactions.groupby([df_transactions['date'].dt.to_period('M'), 'type'])['amount'].sum().unstack(fill_value=0)
    monthly_data['net'] = monthly_data.get('buy', 0) - monthly_data.get('sell', 0)
    
    fig = go.Figure()
    fig.add_trace(go.Bar(name='Buy', x=monthly_data.index.astype(str), y=monthly_data.get('buy', 0)))
    fig.add_trace(go.Bar(name='Sell', x=monthly_data.index.astype(str), y=monthly_data.get('sell', 0)))
    fig.add_trace(go.Scatter(name='Net', x=monthly_data.index.astype(str), y=monthly_data['net'], mode='lines+markers'))
    
    fig.update_layout(
        title="Monthly Investment Activity",
        xaxis_title="Month",
        yaxis_title="Amount (₹)",
        barmode='group'
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Fund performance comparison
    if len(data['funds']) > 1:
        st.subheader("🏆 Fund Performance Comparison")
        
        fund_performance = []
        for fund in data['funds']:
            if fund.get('units', 0) > 0:
                current_value = fund.get('units', 0) * fund.get('current_nav', fund.get('nav', 0))
                fund_transactions = [t for t in data['transactions'] if t['fund_id'] == fund['id']]
                total_invested = sum(t['amount'] for t in fund_transactions if t['type'] == 'buy')
                total_sold = sum(t['amount'] for t in fund_transactions if t['type'] == 'sell')
                net_invested = total_invested - total_sold
                
                if net_invested > 0:
                    profit_loss_pct = ((current_value - net_invested) / net_invested * 100)
                    fund_performance.append({
                        'Fund': fund['name'],
                        'Return %': profit_loss_pct,
                        'Current Value': current_value
                    })
        
        if fund_performance:
            df_performance = pd.DataFrame(fund_performance)
            fig = px.bar(df_performance, x='Fund', y='Return %', title="Fund Performance Comparison")
            st.plotly_chart(fig, use_container_width=True)

if __name__ == "__main__":
    main()
