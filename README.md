# Zerodha Kite Connect MCP Server

A comprehensive Model Context Protocol (MCP) server for interacting with Zerodha's Kite Connect API. This server provides intelligent stock market analysis with sequential thinking capabilities, real-time data fetching, and automated trading functions.

## 🚀 Features

### Core Tools
1. **📈 Fetch Data** - Real-time and historical market data for NIFTY, stocks, and indices
2. **🧠 Analyze Data** - Advanced sequential thinking analysis of market trends
3. **👁️ Monitor Orders** - Real-time order tracking and status updates
4. **💰 Buy Stock** - Automated buy order placement
5. **💸 Sell Stock** - Automated sell order placement

### Key Capabilities
- **Sequential Thinking Analysis**: Multi-step reasoning process for market analysis
- **Real-time Data**: Live quotes, historical data, and market indicators
- **Order Management**: Complete order lifecycle management
- **Risk Assessment**: Built-in volatility and trend analysis
- **Smart Recommendations**: AI-driven buy/sell/hold recommendations

## 📋 Prerequisites

1. **Zerodha Kite Connect Account**
   - Sign up at [Kite Connect](https://kite.trade/connect/login)
   - Create an app to get API credentials

2. **Python 3.8+**

3. **Environment Setup**
   - Your `config.env` file with Kite Connect credentials

## 🛠️ Installation

1. **Clone/Download the repository**
   ```bash
   cd /path/to/your/zerodha-mcp
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure credentials** (already done in your `config.env`)
   ```env
   KITE_API_KEY=your_api_key
   KITE_API_SECRET=your_api_secret
   KITE_ACCESS_TOKEN=your_access_token
   ```

## 🏃‍♂️ Usage

### Running the MCP Server

```bash
python zerodha_mcp_server.py
```

### Available Tools

#### 1. Fetch Data
```json
{
  "name": "fetch_data",
  "parameters": {
    "symbol": "NIFTY 50",
    "exchange": "NSE",
    "interval": "day",
    "days": 30
  }
}
```

**Parameters:**
- `symbol`: Trading symbol (e.g., "NIFTY 50", "RELIANCE", "TCS")
- `exchange`: Exchange (NSE, BSE, MCX) - Default: NSE
- `interval`: Time interval (minute, day, 3minute, 5minute, etc.) - Default: day
- `days`: Number of days of historical data - Default: 30

#### 2. Analyze Data with Sequential Thinking
```json
{
  "name": "analyze_data",
  "parameters": {
    "symbol": "RELIANCE",
    "analysis_type": "technical"
  }
}
```

**Features:**
- Step-by-step thinking process
- Price movement analysis
- Historical trend evaluation
- Volume pattern assessment
- Final trading recommendation

#### 3. Monitor Orders
```json
{
  "name": "monitor_orders",
  "parameters": {
    "order_id": "optional_specific_order_id"
  }
}
```

#### 4. Buy Stock
```json
{
  "name": "buy_stock",
  "parameters": {
    "symbol": "TCS",
    "quantity": 10,
    "order_type": "MARKET",
    "product": "CNC"
  }
}
```

#### 5. Sell Stock
```json
{
  "name": "sell_stock",
  "parameters": {
    "symbol": "TCS",
    "quantity": 10,
    "order_type": "LIMIT",
    "price": 3500.00,
    "product": "CNC"
  }
}
```

## 🧠 Sequential Thinking Analysis

The MCP server includes a sophisticated sequential thinking analyzer that processes market data through multiple reasoning steps:

### Analysis Steps:
1. **Current Price Analysis** - Evaluates current price movement and momentum
2. **Historical Trend Analysis** - Examines 5-day price patterns and volatility
3. **Volume Analysis** - Assesses trading volume relative to averages
4. **Final Recommendation** - Synthesizes all data into actionable insights

### Sample Output:
```
🧠 Sequential Thinking Analysis for RELIANCE

## Thinking Process:
Step 1: Analyzing current price movement
Analysis: Current Price: ₹2,456.75, Previous Close: ₹2,445.20, Change: 0.47%
Conclusion: Current price momentum established
Next Action: Analyze historical trends

Step 2: Examining 5-day historical trend pattern
Analysis: 5-day trend: Upward, Recent volatility: ₹45.30
Conclusion: Stock shows upward momentum with moderate volatility
Next Action: Evaluate volume patterns

## Final Recommendation:
Action: HOLD
Reasoning: Neutral momentum, wait for clearer signals
Suggested Action: Monitor for breakout or breakdown signals
```

## 🔒 Security Notes

- **Never commit `config.env`** to version control
- **Regenerate access tokens daily** for security
- **Use paper trading** for testing before live trades
- **Monitor API rate limits** to avoid restrictions

## 📊 Example Workflows

### 1. Daily Market Analysis
```python
# Fetch NIFTY data
fetch_data(symbol="NIFTY 50", days=5)

# Analyze with sequential thinking
analyze_data(symbol="NIFTY 50")

# Check current positions
monitor_orders()
```

### 2. Stock Trading Flow
```python
# Research stock
fetch_data(symbol="RELIANCE", days=10)
analyze_data(symbol="RELIANCE")

# Place order based on analysis
buy_stock(symbol="RELIANCE", quantity=5, order_type="MARKET")

# Monitor the order
monitor_orders(order_id="order_id_returned")
```

## 🐛 Troubleshooting

### Common Issues:

1. **Authentication Error**
   - Check if access token is valid (regenerate daily)
   - Verify API key and secret in config.env

2. **Symbol Not Found**
   - Use exact trading symbols (e.g., "RELIANCE" not "Reliance Industries")
   - Check if symbol is available on the specified exchange

3. **Order Placement Failed**
   - Ensure sufficient margin/balance
   - Check market hours (9:15 AM - 3:30 PM IST)
   - Verify order parameters

4. **Rate Limiting**
   - Kite Connect has API rate limits
   - Add delays between requests if needed

## 📈 Advanced Features

### Custom Analysis Types
- Technical analysis with indicators
- Fundamental analysis integration
- Sentiment analysis capabilities

### Risk Management
- Built-in stop-loss recommendations
- Position sizing suggestions
- Volatility-based risk assessment

## 🔧 Development

### Adding New Tools
1. Define tool in `handle_list_tools()`
2. Implement handler in `handle_call_tool()`
3. Add sequential thinking logic if needed

### Extending Analysis
- Modify `SequentialAnalyzer` class
- Add new thinking steps
- Implement custom indicators

## 📄 License

This project is for educational and personal use. Please comply with Zerodha's API terms of service.

## 🤝 Contributing

Feel free to submit issues and enhancement requests!

---

**⚠️ Disclaimer**: This software is for educational purposes. Trading involves risk. Always do your own research and consider consulting with a financial advisor before making investment decisions.
