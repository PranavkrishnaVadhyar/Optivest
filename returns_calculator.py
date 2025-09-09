import streamlit as st
import plotly.graph_objects as go
import numpy as np


def show_returns_calculator():
    """Returns Calculator"""
    st.header("🧮 Returns Calculator")
    
    tab1, tab2 = st.tabs(["📈 Mutual Fund Returns", "🔄 SIP Returns"])
    
    with tab1:
        st.subheader("Mutual Fund Returns Calculator")
        
        with st.form("mf_returns_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                initial_investment = st.number_input("Initial Investment (₹)", min_value=1.0, value=100000.0)
                current_value = st.number_input("Current Value (₹)", min_value=1.0, value=120000.0)
                investment_period = st.number_input("Investment Period (Years)", min_value=0.1, value=1.0)
            
            with col2:
                additional_investments = st.number_input("Additional Investments (₹)", min_value=0.0, value=0.0)
                additional_period = st.number_input("Additional Investment Period (Years)", min_value=0.0, value=0.0)
            
            submitted = st.form_submit_button("Calculate Returns", type="primary")
            
            if submitted:
                total_investment = initial_investment + additional_investments
                absolute_return = current_value - total_investment
                absolute_return_pct = (absolute_return / total_investment) * 100
                
                if investment_period > 0:
                    cagr = ((current_value / total_investment) ** (1/investment_period) - 1) * 100
                else:
                    cagr = 0
                
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.metric("Total Investment", f"₹{total_investment:,.2f}")
                with col2:
                    st.metric("Absolute Return", f"₹{absolute_return:,.2f}", f"{absolute_return_pct:.2f}%")
                with col3:
                    st.metric("CAGR", f"{cagr:.2f}%")
    
    with tab2:
        st.subheader("SIP Returns Calculator")
        
        with st.form("sip_returns_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                sip_amount = st.number_input("SIP Amount (₹)", min_value=1.0, value=5000.0)
                sip_duration = st.number_input("SIP Duration (Years)", min_value=1, value=5)
                expected_return = st.number_input("Expected Return (%)", min_value=0.0, max_value=30.0, value=12.0)
            
            with col2:
                frequency = st.selectbox("Frequency", ["Monthly", "Weekly", "Quarterly"], index=0)
                step_up = st.number_input("Annual Step-up (%)", min_value=0.0, max_value=50.0, value=10.0)
            
            submitted = st.form_submit_button("Calculate SIP Returns", type="primary")
            
            if submitted:
                months = sip_duration * 12
                monthly_return = expected_return / 100 / 12
                
                total_investment = 0
                future_value = 0
                
                for year in range(sip_duration):
                    year_amount = sip_amount * (1 + step_up/100) ** year
                    year_investment = year_amount * 12
                    total_investment += year_investment
                    remaining_months = (sip_duration - year) * 12
                    if monthly_return > 0:
                        year_fv = year_investment * ((1 + monthly_return) ** remaining_months - 1) / monthly_return
                    else:
                        year_fv = year_investment
                    future_value += year_fv
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Total Investment", f"₹{total_investment:,.2f}")
                with col2:
                    st.metric("Future Value", f"₹{future_value:,.2f}")
                with col3:
                    profit = future_value - total_investment
                    profit_pct = (profit / total_investment) * 100 if total_investment > 0 else 0
                    st.metric("Profit", f"₹{profit:,.2f}", f"{profit_pct:.2f}%")
                
                years = list(range(1, sip_duration + 1))
                cumulative_investment = []
                projected_value = []
                
                running_investment = 0
                running_value = 0
                
                for year in years:
                    year_amount = sip_amount * (1 + step_up/100) ** (year - 1)
                    year_investment = year_amount * 12
                    running_investment += year_investment
                    cumulative_investment.append(running_investment)
                    remaining_months = (sip_duration - year + 1) * 12
                    if monthly_return > 0:
                        year_fv = year_investment * ((1 + monthly_return) ** remaining_months - 1) / monthly_return
                    else:
                        year_fv = year_investment
                    running_value += year_fv
                    projected_value.append(running_value)
                
                fig = go.Figure()
                fig.add_trace(go.Scatter(x=years, y=cumulative_investment, name='Total Investment', line=dict(color='blue')))
                fig.add_trace(go.Scatter(x=years, y=projected_value, name='Projected Value', line=dict(color='green')))
                fig.update_layout(title="SIP Projection Over Time", xaxis_title="Years", yaxis_title="Amount (₹)", hovermode='x unified')
                st.plotly_chart(fig, use_container_width=True)
