# Zerodha Kite MCP Server

A Model Context Protocol (MCP) server for Zerodha Kite Connect API that provides tools for stock trading, market data analysis, and portfolio management with sequential thinking capabilities.

## Features

- **Real-time Market Data**: Fetch live stock prices, quotes, and historical data
- **Sequential Thinking Analysis**: AI-powered technical analysis with step-by-step reasoning
- **Order Management**: Place buy/sell orders and monitor execution
- **Portfolio Tracking**: Monitor positions and account status
- **5 MCP Tools**: Complete trading toolkit accessible via MCP clients

## Quick Start

### 1. Setup Environment
```bash
source zerodha_mcp_env/bin/activate
```

### 2. Configure API Credentials
Update `config.env` with your Zerodha Kite Connect credentials:
```bash
KITE_API_KEY=your_api_key_here
KITE_API_SECRET=your_api_secret_here
```

### 3. Generate Access Token
```bash
python3 generate_access_token.py
```

### 4. Test Connection
```bash
python3 test_connection.py
```

### 5. Start MCP Server
```bash
python3 zerodha_mcp_server.py
```

## Available Tools

### 📈 fetch_data
Fetch real-time and historical stock/index data
- **Parameters**: symbol, exchange, interval, days
- **Returns**: Current price, volume, historical OHLC data, market depth

### 🧠 analyze_data  
Analyze stock data using sequential thinking process
- **Parameters**: symbol, analysis_type
- **Returns**: Step-by-step analysis with BUY/SELL/HOLD recommendation

### 👁️ monitor_orders
Monitor placed orders and their execution status
- **Parameters**: order_id (optional)
- **Returns**: Order status, execution details, timestamps

### 💰 buy_stock
Place buy orders for stocks
- **Parameters**: symbol, quantity, order_type, price, product
- **Returns**: Order confirmation with order_id

### 💸 sell_stock
Place sell orders for stocks  
- **Parameters**: symbol, quantity, order_type, price, product
- **Returns**: Order confirmation with order_id

## Example Usage

```python
# Fetch RELIANCE stock data
fetch_data(symbol="RELIANCE", exchange="NSE", days=5)

# Analyze with sequential thinking
analyze_data(symbol="RELIANCE", analysis_type="technical")

# Place buy order
buy_stock(symbol="TCS", quantity=10, order_type="MARKET")

# Monitor orders
monitor_orders()
```

## Sequential Thinking Process

The analyze_data tool uses a 4-step sequential thinking approach:

1. **Current Price Analysis**: Evaluates price movement vs previous close
2. **Historical Trend Analysis**: Examines multi-day patterns and volatility
3. **Volume Analysis**: Compares current vs average volume for sentiment
4. **Final Recommendation**: Synthesizes analysis into actionable BUY/SELL/HOLD decision

## Files Overview

- `zerodha_mcp_server.py` - Main MCP server implementation
- `config.env` - API credentials configuration
- `generate_access_token.py` - Daily access token generator
- `test_connection.py` - Connection verification tool
- `requirements.txt` - Python dependencies
- `TESTING_RESULTS.md` - Comprehensive test results

## Requirements

- Python 3.13+
- Active Zerodha Kite Connect account
- Valid API key and secret from Kite Connect app

## Security

- Keep `config.env` secure and never commit to version control
- Access tokens expire daily and need regeneration
- Use sandbox credentials for testing

## Status

✅ **Production Ready** - Fully tested and operational
✅ **Live Market Data** - Real-time price and volume data
✅ **Sequential Analysis** - AI-powered trading recommendations
✅ **Error Handling** - Robust error management and graceful failures

---

Built with ❤️ for algorithmic trading and market analysis