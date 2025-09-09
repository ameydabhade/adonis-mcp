#!/usr/bin/env python3
"""
Zerodha Kite Connect MCP Server
Provides tools for fetching stock data, analyzing with sequential thinking, 
monitoring orders, and executing buy/sell trades.
"""

import json
import os
import asyncio
import logging
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional, Union
from dataclasses import dataclass
from dotenv import load_dotenv

# MCP imports
from mcp.server.models import InitializationOptions
from mcp.server import NotificationOptions, Server
from mcp.types import (
    Resource,
    Tool,
    TextContent,
    ImageContent,
    EmbeddedResource,
    LoggingLevel
)
import mcp.types as types

# Kite Connect imports
from kiteconnect import KiteConnect

# Load environment variables
load_dotenv('config.env')

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Kite Connect
kite = None

def init_kite():
    """Initialize Kite Connect instance"""
    global kite
    api_key = os.getenv('KITE_API_KEY')
    access_token = os.getenv('KITE_ACCESS_TOKEN')
    
    if not api_key or not access_token:
        raise ValueError("KITE_API_KEY and KITE_ACCESS_TOKEN must be set in config.env")
    
    kite = KiteConnect(api_key=api_key)
    kite.set_access_token(access_token)
    logger.info("Kite Connect initialized successfully")
    return kite

@dataclass
class ThinkingStep:
    """Represents a step in sequential thinking process"""
    step_number: int
    thought: str
    analysis: str
    conclusion: str
    next_action: Optional[str] = None

class SequentialAnalyzer:
    """Handles sequential thinking analysis of market data"""
    
    def __init__(self):
        self.thinking_steps: List[ThinkingStep] = []
        self.current_step = 0
    
    def add_thinking_step(self, thought: str, analysis: str, conclusion: str, next_action: str = None):
        """Add a new thinking step"""
        self.current_step += 1
        step = ThinkingStep(
            step_number=self.current_step,
            thought=thought,
            analysis=analysis,
            conclusion=conclusion,
            next_action=next_action
        )
        self.thinking_steps.append(step)
        return step
    
    def analyze_price_data(self, instrument_data: Dict, historical_data: List[Dict]) -> Dict:
        """Perform sequential thinking analysis on price data"""
        
        # Step 1: Current Price Analysis
        current_price = instrument_data.get('last_price', 0)
        prev_close = instrument_data.get('ohlc', {}).get('close', 0)
        change_percent = ((current_price - prev_close) / prev_close * 100) if prev_close else 0
        
        step1 = self.add_thinking_step(
            thought=f"Analyzing current price movement for {instrument_data.get('tradingsymbol', 'Unknown')}",
            analysis=f"Current Price: ₹{current_price}, Previous Close: ₹{prev_close}, Change: {change_percent:.2f}%",
            conclusion="Current price momentum established",
            next_action="Analyze historical trends"
        )
        
        # Step 2: Historical Trend Analysis
        if historical_data and len(historical_data) >= 5:
            recent_closes = [candle['close'] for candle in historical_data[-5:]]
            trend = "Upward" if recent_closes[-1] > recent_closes[0] else "Downward"
            volatility = max(recent_closes) - min(recent_closes)
            
            step2 = self.add_thinking_step(
                thought="Examining 5-day historical trend pattern",
                analysis=f"5-day trend: {trend}, Recent volatility: ₹{volatility:.2f}",
                conclusion=f"Stock shows {trend.lower()} momentum with {'high' if volatility > current_price * 0.05 else 'moderate'} volatility",
                next_action="Evaluate volume patterns"
            )
        
        # Step 3: Volume Analysis
        volume = instrument_data.get('volume', 0)
        avg_volume = instrument_data.get('average_price', 0)  # Using as proxy
        
        step3 = self.add_thinking_step(
            thought="Assessing trading volume relative to average",
            analysis=f"Current Volume: {volume}, Volume indicates {'high' if volume > avg_volume * 1.5 else 'normal'} trading activity",
            conclusion="Volume analysis provides market sentiment insight",
            next_action="Generate trading recommendation"
        )
        
        # Step 4: Final Recommendation
        recommendation = self._generate_recommendation(change_percent, trend if 'trend' in locals() else 'Neutral', volume)
        
        step4 = self.add_thinking_step(
            thought="Synthesizing all analysis into actionable recommendation",
            analysis=f"Price trend: {change_percent:.2f}%, Historical pattern: {trend if 'trend' in locals() else 'Neutral'}, Volume: {'High' if volume > avg_volume * 1.5 else 'Normal'}",
            conclusion=f"Recommendation: {recommendation['action']} - {recommendation['reasoning']}",
            next_action=recommendation['suggested_action']
        )
        
        return {
            'thinking_steps': [
                {
                    'step': step.step_number,
                    'thought': step.thought,
                    'analysis': step.analysis,
                    'conclusion': step.conclusion,
                    'next_action': step.next_action
                } for step in self.thinking_steps
            ],
            'final_recommendation': recommendation,
            'analysis_summary': {
                'current_price': current_price,
                'change_percent': change_percent,
                'trend': trend if 'trend' in locals() else 'Neutral',
                'volume_status': 'High' if volume > avg_volume * 1.5 else 'Normal',
                'volatility': volatility if 'volatility' in locals() else 0
            }
        }
    
    def _generate_recommendation(self, change_percent: float, trend: str, volume: int) -> Dict:
        """Generate trading recommendation based on analysis"""
        if change_percent > 2 and trend == "Upward":
            return {
                'action': 'BUY',
                'reasoning': 'Strong upward momentum with positive trend',
                'suggested_action': 'Consider buying with stop-loss at recent support'
            }
        elif change_percent < -2 and trend == "Downward":
            return {
                'action': 'SELL',
                'reasoning': 'Negative momentum with downward trend',
                'suggested_action': 'Consider selling or shorting with stop-loss'
            }
        else:
            return {
                'action': 'HOLD',
                'reasoning': 'Neutral momentum, wait for clearer signals',
                'suggested_action': 'Monitor for breakout or breakdown signals'
            }

# Global analyzer instance
analyzer = SequentialAnalyzer()

# Create MCP server
app = Server("zerodha-kite-mcp")

@app.list_tools()
async def handle_list_tools() -> list[Tool]:
    """List available tools"""
    return [
        Tool(
            name="fetch_data",
            description="Fetch real-time and historical data for stocks/indices like NIFTY",
            inputSchema={
                "type": "object",
                "properties": {
                    "symbol": {
                        "type": "string",
                        "description": "Trading symbol (e.g., 'NIFTY 50', 'RELIANCE', 'TCS')"
                    },
                    "exchange": {
                        "type": "string",
                        "description": "Exchange (NSE, BSE, MCX, etc.)",
                        "default": "NSE"
                    },
                    "interval": {
                        "type": "string",
                        "description": "Time interval for historical data (minute, day, 3minute, 5minute, 10minute, 15minute, 30minute, 60minute)",
                        "default": "day"
                    },
                    "days": {
                        "type": "integer",
                        "description": "Number of days of historical data to fetch",
                        "default": 30
                    }
                },
                "required": ["symbol"]
            }
        ),
        Tool(
            name="analyze_data",
            description="Analyze fetched data using sequential thinking process",
            inputSchema={
                "type": "object",
                "properties": {
                    "symbol": {
                        "type": "string",
                        "description": "Trading symbol to analyze"
                    },
                    "analysis_type": {
                        "type": "string",
                        "description": "Type of analysis (technical, fundamental, sentiment)",
                        "default": "technical"
                    }
                },
                "required": ["symbol"]
            }
        ),
        Tool(
            name="monitor_orders",
            description="Monitor placed orders and their status",
            inputSchema={
                "type": "object",
                "properties": {
                    "order_id": {
                        "type": "string",
                        "description": "Specific order ID to monitor (optional)"
                    }
                }
            }
        ),
        Tool(
            name="buy_stock",
            description="Place a buy order for a stock",
            inputSchema={
                "type": "object",
                "properties": {
                    "symbol": {
                        "type": "string",
                        "description": "Trading symbol"
                    },
                    "quantity": {
                        "type": "integer",
                        "description": "Number of shares to buy"
                    },
                    "order_type": {
                        "type": "string",
                        "description": "Order type (MARKET, LIMIT, SL, SL-M)",
                        "default": "MARKET"
                    },
                    "price": {
                        "type": "number",
                        "description": "Price for LIMIT orders"
                    },
                    "product": {
                        "type": "string",
                        "description": "Product type (MIS, CNC, NRML)",
                        "default": "CNC"
                    }
                },
                "required": ["symbol", "quantity"]
            }
        ),
        Tool(
            name="sell_stock",
            description="Place a sell order for a stock",
            inputSchema={
                "type": "object",
                "properties": {
                    "symbol": {
                        "type": "string",
                        "description": "Trading symbol"
                    },
                    "quantity": {
                        "type": "integer",
                        "description": "Number of shares to sell"
                    },
                    "order_type": {
                        "type": "string",
                        "description": "Order type (MARKET, LIMIT, SL, SL-M)",
                        "default": "MARKET"
                    },
                    "price": {
                        "type": "number",
                        "description": "Price for LIMIT orders"
                    },
                    "product": {
                        "type": "string",
                        "description": "Product type (MIS, CNC, NRML)",
                        "default": "CNC"
                    }
                },
                "required": ["symbol", "quantity"]
            }
        )
    ]

@app.call_tool()
async def handle_call_tool(name: str, arguments: dict) -> list[types.TextContent]:
    """Handle tool calls"""
    
    if not kite:
        init_kite()
    
    try:
        if name == "fetch_data":
            return await fetch_data_tool(arguments)
        elif name == "analyze_data":
            return await analyze_data_tool(arguments)
        elif name == "monitor_orders":
            return await monitor_orders_tool(arguments)
        elif name == "buy_stock":
            return await buy_stock_tool(arguments)
        elif name == "sell_stock":
            return await sell_stock_tool(arguments)
        else:
            return [types.TextContent(type="text", text=f"Unknown tool: {name}")]
    except Exception as e:
        logger.error(f"Error in tool {name}: {str(e)}")
        return [types.TextContent(type="text", text=f"Error: {str(e)}")]

async def fetch_data_tool(arguments: dict) -> list[types.TextContent]:
    """Fetch stock/index data"""
    symbol = arguments.get("symbol")
    exchange = arguments.get("exchange", "NSE")
    interval = arguments.get("interval", "day")
    days = arguments.get("days", 30)
    
    try:
        # Get instrument token
        instruments = kite.instruments(exchange)
        instrument = None
        
        for inst in instruments:
            if symbol.upper() in inst['tradingsymbol'].upper() or symbol.upper() in inst['name'].upper():
                instrument = inst
                break
        
        if not instrument:
            return [types.TextContent(type="text", text=f"Instrument {symbol} not found on {exchange}")]
        
        instrument_token = instrument['instrument_token']
        
        # Get current quote
        quote = kite.quote(f"{exchange}:{instrument['tradingsymbol']}")
        
        # Get historical data
        from_date = datetime.now() - timedelta(days=days)
        to_date = datetime.now()
        
        historical_data = kite.historical_data(
            instrument_token=instrument_token,
            from_date=from_date,
            to_date=to_date,
            interval=interval
        )
        
        result = {
            "instrument_info": instrument,
            "current_quote": quote,
            "historical_data": historical_data[-10:],  # Last 10 records
            "total_records": len(historical_data),
            "timestamp": datetime.now().isoformat()
        }
        
        return [types.TextContent(
            type="text",
            text=f"📈 **Data fetched for {symbol}**\n\n"
                 f"**Current Price:** ₹{quote[f'{exchange}:{instrument['tradingsymbol']}']['last_price']}\n"
                 f"**Change:** {quote[f'{exchange}:{instrument['tradingsymbol']}']['net_change']} "
                 f"({quote[f'{exchange}:{instrument['tradingsymbol']}']['net_change']/quote[f'{exchange}:{instrument['tradingsymbol']}']['ohlc']['close']*100:.2f}%)\n"
                 f"**Volume:** {quote[f'{exchange}:{instrument['tradingsymbol']}']['volume']:,}\n"
                 f"**Historical Records:** {len(historical_data)} days\n\n"
                 f"**Raw Data:**\n```json\n{json.dumps(result, indent=2, default=str)}\n```"
        )]
        
    except Exception as e:
        return [types.TextContent(type="text", text=f"Error fetching data: {str(e)}")]

async def analyze_data_tool(arguments: dict) -> list[types.TextContent]:
    """Analyze data with sequential thinking"""
    symbol = arguments.get("symbol")
    analysis_type = arguments.get("analysis_type", "technical")
    
    try:
        # First fetch the data
        fetch_args = {"symbol": symbol, "days": 10}
        data_result = await fetch_data_tool(fetch_args)
        
        # Extract data from the result (this is a simplified approach)
        # In a real implementation, you'd parse the JSON from the previous result
        
        # Get fresh data for analysis
        instruments = kite.instruments("NSE")
        instrument = None
        
        for inst in instruments:
            if symbol.upper() in inst['tradingsymbol'].upper():
                instrument = inst
                break
        
        if not instrument:
            return [types.TextContent(type="text", text=f"Cannot analyze: {symbol} not found")]
        
        # Get current quote and historical data
        quote_data = kite.quote(f"NSE:{instrument['tradingsymbol']}")
        instrument_data = quote_data[f"NSE:{instrument['tradingsymbol']}"]
        
        # Get historical data
        from_date = datetime.now() - timedelta(days=10)
        historical_data = kite.historical_data(
            instrument_token=instrument['instrument_token'],
            from_date=from_date,
            to_date=datetime.now(),
            interval="day"
        )
        
        # Perform sequential thinking analysis
        global analyzer
        analyzer = SequentialAnalyzer()  # Reset for new analysis
        analysis_result = analyzer.analyze_price_data(instrument_data, historical_data)
        
        # Format the thinking steps
        thinking_steps_text = ""
        for step in analysis_result['thinking_steps']:
            thinking_steps_text += f"**Step {step['step']}:** {step['thought']}\n"
            thinking_steps_text += f"*Analysis:* {step['analysis']}\n"
            thinking_steps_text += f"*Conclusion:* {step['conclusion']}\n"
            if step['next_action']:
                thinking_steps_text += f"*Next Action:* {step['next_action']}\n"
            thinking_steps_text += "\n"
        
        recommendation = analysis_result['final_recommendation']
        summary = analysis_result['analysis_summary']
        
        return [types.TextContent(
            type="text",
            text=f"🧠 **Sequential Thinking Analysis for {symbol}**\n\n"
                 f"## Thinking Process:\n{thinking_steps_text}"
                 f"## Final Recommendation:\n"
                 f"**Action:** {recommendation['action']}\n"
                 f"**Reasoning:** {recommendation['reasoning']}\n"
                 f"**Suggested Action:** {recommendation['suggested_action']}\n\n"
                 f"## Summary:\n"
                 f"- Current Price: ₹{summary['current_price']}\n"
                 f"- Change: {summary['change_percent']:.2f}%\n"
                 f"- Trend: {summary['trend']}\n"
                 f"- Volume: {summary['volume_status']}\n"
                 f"- Volatility: ₹{summary['volatility']:.2f}\n\n"
                 f"*Analysis completed at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*"
        )]
        
    except Exception as e:
        return [types.TextContent(type="text", text=f"Analysis error: {str(e)}")]

async def monitor_orders_tool(arguments: dict) -> list[types.TextContent]:
    """Monitor orders"""
    order_id = arguments.get("order_id")
    
    try:
        if order_id:
            # Get specific order
            order_history = kite.order_history(order_id)
            return [types.TextContent(
                type="text",
                text=f"📊 **Order {order_id} Status:**\n\n```json\n{json.dumps(order_history, indent=2, default=str)}\n```"
            )]
        else:
            # Get all orders
            orders = kite.orders()
            
            if not orders:
                return [types.TextContent(type="text", text="📊 **No orders found**")]
            
            orders_text = "📊 **All Orders:**\n\n"
            for order in orders[-10:]:  # Last 10 orders
                orders_text += f"**Order ID:** {order['order_id']}\n"
                orders_text += f"**Symbol:** {order['tradingsymbol']}\n"
                orders_text += f"**Transaction:** {order['transaction_type']}\n"
                orders_text += f"**Quantity:** {order['quantity']}\n"
                orders_text += f"**Status:** {order['status']}\n"
                orders_text += f"**Price:** ₹{order.get('price', 'N/A')}\n"
                orders_text += f"**Time:** {order['order_timestamp']}\n\n"
            
            return [types.TextContent(type="text", text=orders_text)]
            
    except Exception as e:
        return [types.TextContent(type="text", text=f"Monitoring error: {str(e)}")]

async def buy_stock_tool(arguments: dict) -> list[types.TextContent]:
    """Place buy order"""
    symbol = arguments.get("symbol")
    quantity = arguments.get("quantity")
    order_type = arguments.get("order_type", "MARKET")
    price = arguments.get("price")
    product = arguments.get("product", "CNC")
    
    try:
        # Get instrument details
        instruments = kite.instruments("NSE")
        instrument = None
        
        for inst in instruments:
            if symbol.upper() in inst['tradingsymbol'].upper():
                instrument = inst
                break
        
        if not instrument:
            return [types.TextContent(type="text", text=f"Cannot buy: {symbol} not found")]
        
        # Prepare order parameters
        order_params = {
            "variety": "regular",
            "tradingsymbol": instrument['tradingsymbol'],
            "exchange": "NSE",
            "transaction_type": "BUY",
            "quantity": quantity,
            "order_type": order_type,
            "product": product
        }
        
        if order_type == "LIMIT" and price:
            order_params["price"] = price
        
        # Place order
        order_id = kite.place_order(**order_params)
        
        return [types.TextContent(
            type="text",
            text=f"✅ **Buy Order Placed Successfully!**\n\n"
                 f"**Order ID:** {order_id}\n"
                 f"**Symbol:** {instrument['tradingsymbol']}\n"
                 f"**Quantity:** {quantity}\n"
                 f"**Order Type:** {order_type}\n"
                 f"**Product:** {product}\n"
                 f"**Price:** {'₹' + str(price) if price else 'Market Price'}\n"
                 f"**Time:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
                 f"Monitor this order using the monitor_orders tool with order_id: {order_id}"
        )]
        
    except Exception as e:
        return [types.TextContent(type="text", text=f"Buy order error: {str(e)}")]

async def sell_stock_tool(arguments: dict) -> list[types.TextContent]:
    """Place sell order"""
    symbol = arguments.get("symbol")
    quantity = arguments.get("quantity")
    order_type = arguments.get("order_type", "MARKET")
    price = arguments.get("price")
    product = arguments.get("product", "CNC")
    
    try:
        # Get instrument details
        instruments = kite.instruments("NSE")
        instrument = None
        
        for inst in instruments:
            if symbol.upper() in inst['tradingsymbol'].upper():
                instrument = inst
                break
        
        if not instrument:
            return [types.TextContent(type="text", text=f"Cannot sell: {symbol} not found")]
        
        # Prepare order parameters
        order_params = {
            "variety": "regular",
            "tradingsymbol": instrument['tradingsymbol'],
            "exchange": "NSE",
            "transaction_type": "SELL",
            "quantity": quantity,
            "order_type": order_type,
            "product": product
        }
        
        if order_type == "LIMIT" and price:
            order_params["price"] = price
        
        # Place order
        order_id = kite.place_order(**order_params)
        
        return [types.TextContent(
            type="text",
            text=f"✅ **Sell Order Placed Successfully!**\n\n"
                 f"**Order ID:** {order_id}\n"
                 f"**Symbol:** {instrument['tradingsymbol']}\n"
                 f"**Quantity:** {quantity}\n"
                 f"**Order Type:** {order_type}\n"
                 f"**Product:** {product}\n"
                 f"**Price:** {'₹' + str(price) if price else 'Market Price'}\n"
                 f"**Time:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
                 f"Monitor this order using the monitor_orders tool with order_id: {order_id}"
        )]
        
    except Exception as e:
        return [types.TextContent(type="text", text=f"Sell order error: {str(e)}")]

async def main():
    """Main function to run the server"""
    # Initialize Kite Connect
    try:
        init_kite()
    except Exception as e:
        logger.error(f"Failed to initialize Kite Connect: {e}")
        return
    
    # Run the server
    from mcp.server.stdio import stdio_server
    
    async with stdio_server() as (read_stream, write_stream):
        await app.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="zerodha-kite-mcp",
                server_version="1.0.0",
                capabilities=app.get_capabilities(
                    notification_options=NotificationOptions(),
                    experimental_capabilities={},
                ),
            ),
        )

if __name__ == "__main__":
    asyncio.run(main())
