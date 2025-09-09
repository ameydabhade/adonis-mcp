# 🚀 Cursor Integration Guide for Zerodha MCP Server

This guide shows you how to integrate your Zerodha MCP server with Cursor so the AI can directly call your trading tools.

## 📋 Step-by-Step Integration

### **Option 1: Via Cursor Settings UI (Recommended)**

1. **Open Cursor Settings**
   - Press `Cmd + ,` (macOS) or `Ctrl + ,` (Windows/Linux)
   - Or go to `Cursor > Preferences`

2. **Find MCP Settings**
   - In the search bar, type "MCP"
   - Look for "MCP Servers" or "Model Context Protocol"

3. **Add Server Configuration**
   - Click "Add Server" or edit the JSON configuration
   - Add this configuration:

```json
{
  "mcpServers": {
    "zerodha-kite-trading": {
      "command": "/Users/amey/Desktop/$$$$$$$$/zerodha_mcp_env/bin/python",
      "args": ["/Users/amey/Desktop/$$$$$$$$/zerodha_mcp_server.py"],
      "env": {
        "PATH": "/Users/amey/Desktop/$$$$$$$$/zerodha_mcp_env/bin:/usr/bin:/bin",
        "VIRTUAL_ENV": "/Users/amey/Desktop/$$$$$$$$/zerodha_mcp_env"
      }
    }
  }
}
```

### **Option 2: Via settings.json File**

1. **Open Cursor Settings File**
   - Press `Cmd + Shift + P` (macOS) or `Ctrl + Shift + P` (Windows/Linux)
   - Type "Preferences: Open Settings (JSON)"
   - Select the option to open settings.json

2. **Add MCP Configuration**
   - Find the existing `"mcpServers"` section or create it
   - Add the zerodha-kite-trading server configuration

```json
{
  // ... other settings ...
  "mcpServers": {
    "zerodha-kite-trading": {
      "command": "/Users/amey/Desktop/$$$$$$$$/zerodha_mcp_env/bin/python",
      "args": ["/Users/amey/Desktop/$$$$$$$$/zerodha_mcp_server.py"],
      "env": {
        "PATH": "/Users/amey/Desktop/$$$$$$$$/zerodha_mcp_env/bin:/usr/bin:/bin",
        "VIRTUAL_ENV": "/Users/amey/Desktop/$$$$$$$$/zerodha_mcp_env"
      }
    }
  }
}
```

## 🔧 **Important Configuration Notes**

### **Path Configuration**
- ✅ Use **absolute paths** for reliability
- ✅ Point to the virtual environment Python: `/Users/amey/Desktop/$$$$$$$$/zerodha_mcp_env/bin/python`
- ✅ Point to your server script: `/Users/amey/Desktop/$$$$$$$$/zerodha_mcp_server.py`

### **Environment Variables**
- ✅ Set `VIRTUAL_ENV` to activate the Python environment
- ✅ Include the venv `bin` directory in `PATH`

## 🎯 **After Integration - Available Tools**

Once configured, I will have access to these tools in our conversation:

### **📈 fetch_data**
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

### **🧠 analyze_data** (Sequential Thinking)
```json
{
  "name": "analyze_data", 
  "parameters": {
    "symbol": "RELIANCE",
    "analysis_type": "technical"
  }
}
```

### **👁️ monitor_orders**
```json
{
  "name": "monitor_orders",
  "parameters": {
    "order_id": "optional_order_id"
  }
}
```

### **💰 buy_stock**
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

### **💸 sell_stock**
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

## ✅ **Verification Steps**

1. **Save Settings**
   - Save your Cursor settings after adding the configuration
   
2. **Restart Cursor**
   - Close and reopen Cursor to load the new MCP server

3. **Test Connection**
   - Start a new chat
   - Ask me to fetch market data or analyze a stock
   - I should be able to call the tools directly!

## 🔧 **Troubleshooting**

### **Common Issues:**

**🚨 "Command not found"**
- Check that the Python path is correct
- Ensure the virtual environment exists
- Verify the server script path

**🚨 "Permission denied"**
- Make sure the Python executable is executable
- Check file permissions

**🚨 "Module not found"**
- Ensure the virtual environment has all dependencies
- Run: `source zerodha_mcp_env/bin/activate && pip install -r requirements.txt`

**🚨 "Access token expired"**
- Run: `python generate_access_token.py` to refresh token

## 🎉 **Example Usage After Integration**

Once integrated, you can ask me things like:

- "Fetch the latest NIFTY 50 data"
- "Analyze RELIANCE stock with sequential thinking"
- "Buy 5 shares of TCS at market price"
- "Monitor my recent orders"
- "Sell my RELIANCE position"

And I'll be able to execute these directly using your MCP server!

## 🔒 **Security Notes**

- ✅ Your API credentials stay in `config.env` (never shared)
- ✅ All trading happens through your authenticated Zerodha account
- ✅ You maintain full control over the MCP server
- ✅ Stop the server anytime by interrupting the process

---

**Ready to trade with AI assistance!** 🚀

