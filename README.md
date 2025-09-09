# 📈 Optivest - Mutual Fund Tracker

A comprehensive Streamlit application to track your mutual fund investments with detailed analytics and portfolio management.

## 🚀 Features

- **Dashboard**: Overview of your portfolio with key metrics
- **Fund Management**: Add and manage mutual funds
- **Transaction Tracking**: Record buy/sell transactions
- **Portfolio View**: Detailed view of your holdings
- **Analytics**: Performance charts and investment trends
- **Data Persistence**: All data saved locally in JSON format

## 📋 Key Metrics Tracked

- Portfolio Value
- Total Investment
- Profit/Loss (Absolute & Percentage)
- Number of Funds
- Monthly Investment Trends
- Fund Performance Comparison

## 🛠️ Installation

1. **Clone or download this repository**

2. **Install required dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application:**
   ```bash
   streamlit run app.py
   ```

4. **Open your browser** and navigate to `http://localhost:8501`

## 📱 How to Use

### 1. Add Your First Fund
- Go to "Add Fund" page
- Fill in fund details (name, category, NAV, etc.)
- Click "Add Fund"

### 2. Record Transactions
- Go to "Add Transaction" page
- Select the fund and transaction type (buy/sell)
- Enter amount, units, and NAV
- Click "Add Transaction"

### 3. Monitor Your Portfolio
- Use the "Dashboard" for a quick overview
- Check "View Portfolio" for detailed holdings
- Analyze performance in "Analytics"

## 📊 Data Storage

The application stores data in three JSON files:
- `funds.json`: Fund information
- `transactions.json`: Transaction history
- `portfolio.json`: Portfolio data

## 🎨 Features Overview

### Dashboard
- Real-time portfolio metrics
- Recent transactions
- Portfolio allocation pie chart

### Fund Management
- Add new mutual funds
- Track fund categories and risk levels
- Monitor current NAV

### Transaction Tracking
- Record buy/sell transactions
- Automatic unit calculation
- Transaction history

### Analytics
- Monthly investment trends
- Fund performance comparison
- Interactive charts using Plotly

## 🔧 Customization

You can easily customize the application by:
- Modifying the CSS styles in the `st.markdown()` section
- Adding new fund categories in the dropdown
- Extending the analytics with additional charts
- Adding new transaction types

## 📈 Sample Data

To get started quickly, you can add sample funds like:
- **HDFC Top 100 Fund** (Large Cap)
- **SBI Small Cap Fund** (Small Cap)
- **Axis Long Term Equity Fund** (ELSS)

## 🚀 Future Enhancements

Potential features to add:
- Import data from CSV/Excel
- Export portfolio reports
- Email notifications
- Integration with real-time NAV APIs
- Goal-based investing tracking
- SIP calculator

## 📝 Notes

- All calculations are done in real-time
- Data is automatically saved after each transaction
- The application works offline (no internet required)
- Compatible with all major browsers

## 🤝 Contributing

Feel free to fork this project and submit pull requests for any improvements!

## 📄 License

This project is open source and available under the MIT License.

---

**Happy Investing! 📈💰**