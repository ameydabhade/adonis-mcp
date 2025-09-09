#!/usr/bin/env python3
"""
Demo script showing how to use the Zerodha MCP server tools
This demonstrates all 5 tools with sequential thinking integration.
"""

import json
import asyncio
from datetime import datetime

# This is a demo showing the expected tool calls and responses
# In practice, you'd use this through an MCP client

def demo_tool_usage():
    """Demonstrate all MCP tools"""
    
    print("🚀 Zerodha MCP Server - Tool Usage Demo")
    print("=" * 50)
    
    # Tool 1: Fetch Data
    print("\n📈 Tool 1: Fetch Data")
    print("-" * 25)
    fetch_data_example = {
        "tool": "fetch_data",
        "parameters": {
            "symbol": "RELIANCE",
            "exchange": "NSE",
            "interval": "day",
            "days": 10
        },
        "expected_response": "Real-time price, historical data, volume info"
    }
    print(f"Usage: {json.dumps(fetch_data_example, indent=2)}")
    
    # Tool 2: Analyze Data with Sequential Thinking
    print("\n🧠 Tool 2: Analyze Data (Sequential Thinking)")
    print("-" * 45)
    analyze_data_example = {
        "tool": "analyze_data",
        "parameters": {
            "symbol": "RELIANCE",
            "analysis_type": "technical"
        },
        "thinking_process": [
            "Step 1: Current price movement analysis",
            "Step 2: Historical trend evaluation",
            "Step 3: Volume pattern assessment", 
            "Step 4: Final recommendation synthesis"
        ],
        "expected_response": "BUY/SELL/HOLD recommendation with reasoning"
    }
    print(f"Usage: {json.dumps(analyze_data_example, indent=2)}")
    
    # Tool 3: Monitor Orders
    print("\n👁️ Tool 3: Monitor Orders")
    print("-" * 25)
    monitor_orders_example = {
        "tool": "monitor_orders",
        "parameters": {
            "order_id": "optional_specific_order_id"
        },
        "expected_response": "Order status, execution details, timestamps"
    }
    print(f"Usage: {json.dumps(monitor_orders_example, indent=2)}")
    
    # Tool 4: Buy Stock
    print("\n💰 Tool 4: Buy Stock")
    print("-" * 20)
    buy_stock_example = {
        "tool": "buy_stock",
        "parameters": {
            "symbol": "TCS",
            "quantity": 5,
            "order_type": "MARKET",
            "product": "CNC"
        },
        "expected_response": "Order confirmation with order_id"
    }
    print(f"Usage: {json.dumps(buy_stock_example, indent=2)}")
    
    # Tool 5: Sell Stock
    print("\n💸 Tool 5: Sell Stock")
    print("-" * 21)
    sell_stock_example = {
        "tool": "sell_stock",
        "parameters": {
            "symbol": "TCS",
            "quantity": 5,
            "order_type": "LIMIT",
            "price": 3500.00,
            "product": "CNC"
        },
        "expected_response": "Order confirmation with order_id"
    }
    print(f"Usage: {json.dumps(sell_stock_example, indent=2)}")
    
    # Example Trading Workflow
    print("\n🔄 Example Trading Workflow")
    print("-" * 30)
    workflow = [
        "1. fetch_data(symbol='NIFTY 50') → Get market overview",
        "2. analyze_data(symbol='RELIANCE') → Sequential thinking analysis",
        "3. buy_stock(symbol='RELIANCE', quantity=10) → Place order based on analysis", 
        "4. monitor_orders() → Track order execution",
        "5. sell_stock() → Exit position when targets hit"
    ]
    
    for step in workflow:
        print(f"   {step}")
    
    print("\n📊 Sequential Thinking Analysis Process:")
    print("-" * 40)
    thinking_steps = [
        "🔍 Step 1: Current Price Analysis",
        "   - Evaluate price movement vs previous close",
        "   - Calculate percentage change",
        "   - Assess momentum direction",
        "",
        "📈 Step 2: Historical Trend Analysis", 
        "   - Examine 5-day price patterns",
        "   - Measure volatility levels",
        "   - Identify trend direction",
        "",
        "📊 Step 3: Volume Analysis",
        "   - Compare current vs average volume",
        "   - Assess market sentiment",
        "   - Validate price movements",
        "",
        "🎯 Step 4: Final Recommendation",
        "   - Synthesize all analysis",
        "   - Generate BUY/SELL/HOLD decision",
        "   - Provide reasoning and next actions"
    ]
    
    for step in thinking_steps:
        print(f"   {step}")
    
    print(f"\n✨ MCP Server Status: Running at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("🔗 Connect your MCP client to start trading!")

def main():
    """Main demo function"""
    demo_tool_usage()

if __name__ == "__main__":
    main()
