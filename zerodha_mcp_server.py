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
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional, Union
from dataclasses import dataclass
from dotenv import load_dotenv
import talib

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

class TechnicalIndicatorCalculator:
    """Pure technical indicator calculation without analysis - provides raw data for AI agents"""
    
    def calculate_indicators(self, df: pd.DataFrame) -> Dict:
        """Calculate raw technical indicators - no interpretation, just values"""
        indicators = {}
        
        if len(df) == 0:
            return {"error": "No data provided"}
        
        # Price data
        close = df['close'].values
        high = df['high'].values  
        low = df['low'].values
        volume = df['volume'].values
        
        # Moving Averages
        indicators['ema_9'] = talib.EMA(close, timeperiod=9).tolist() if len(close) >= 9 else []
        indicators['ema_21'] = talib.EMA(close, timeperiod=21).tolist() if len(close) >= 21 else []
        indicators['sma_20'] = talib.SMA(close, timeperiod=20).tolist() if len(close) >= 20 else []
        indicators['sma_50'] = talib.SMA(close, timeperiod=50).tolist() if len(close) >= 50 else []
        
        # Momentum Indicators  
        indicators['rsi_14'] = talib.RSI(close, timeperiod=14).tolist() if len(close) >= 14 else []
        
        # MACD
        if len(close) >= 26:
            macd, macd_signal, macd_hist = talib.MACD(close)
            indicators['macd'] = macd.tolist()
            indicators['macd_signal'] = macd_signal.tolist()
            indicators['macd_histogram'] = macd_hist.tolist()
        else:
            indicators['macd'] = []
            indicators['macd_signal'] = []
            indicators['macd_histogram'] = []
        
        # Bollinger Bands
        if len(close) >= 20:
            bb_upper, bb_middle, bb_lower = talib.BBANDS(close, timeperiod=20, nbdevup=2, nbdevdn=2)
            indicators['bb_upper'] = bb_upper.tolist()
            indicators['bb_middle'] = bb_middle.tolist()
            indicators['bb_lower'] = bb_lower.tolist()
        else:
            indicators['bb_upper'] = []
            indicators['bb_middle'] = []
            indicators['bb_lower'] = []
        
        # Volatility
        indicators['atr_14'] = talib.ATR(high, low, close, timeperiod=14).tolist() if len(close) >= 14 else []
        
        # Volume indicators
        if len(volume) >= 10:
            indicators['volume_sma_10'] = talib.SMA(volume.astype(float), timeperiod=10).tolist()
        else:
            indicators['volume_sma_10'] = []
        
        # Additional indicators
        indicators['stoch_k'], indicators['stoch_d'] = talib.STOCH(high, low, close) if len(close) >= 14 else ([], [])
        indicators['williams_r'] = talib.WILLR(high, low, close, timeperiod=14).tolist() if len(close) >= 14 else []
        
        return indicators

def get_fno_instruments(symbol: str) -> List[Dict]:
    """Get F&O instruments for a symbol"""
    try:
        if not kite:
            init_kite()
            
        # Get all instruments
        nfo_instruments = kite.instruments("NFO")
        
        # Filter by symbol - try different matching strategies
        fno_list = []
        for inst in nfo_instruments:
            # For NIFTY, also check for variations like NIFTY50
            search_terms = [symbol.upper()]
            if symbol.upper() == "NIFTY":
                search_terms.extend(["NIFTY50", "NIFTY 50"])
            elif symbol.upper() == "BANKNIFTY":
                search_terms.extend(["BANKNIFTY", "NIFTYBANK"])
            
            for term in search_terms:
                if (term in inst['name'].upper() or 
                    term in inst['tradingsymbol'].upper() or
                    inst['tradingsymbol'].upper().startswith(term)):
                    fno_list.append({
                        'instrument_token': inst['instrument_token'],
                        'tradingsymbol': inst['tradingsymbol'],
                        'name': inst['name'],
                        'expiry': inst['expiry'],
                        'strike': inst['strike'],
                        'instrument_type': inst['instrument_type'],  # FUT, CE, PE
                        'lot_size': inst['lot_size'],
                        'tick_size': inst['tick_size']
                    })
                    break
        
        return fno_list
    except Exception as e:
        print(f"Error getting F&O instruments: {e}")
        return []

class SequentialAnalyzer:
    """Legacy analyzer for backward compatibility"""
    
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

# Global instances
analyzer = SequentialAnalyzer()  # For backward compatibility  
indicator_calculator = TechnicalIndicatorCalculator()

# Create MCP server
app = Server("zerodha-kite-mcp")

@app.list_tools()
async def handle_list_tools() -> list[Tool]:
    """List available tools"""
    return [
        Tool(
            name="get_market_data",
            description="Get real-time quotes and historical data for equity instruments - raw data for AI analysis",
            inputSchema={
                "type": "object",
                "properties": {
                    "symbol": {
                        "type": "string",
                        "description": "Trading symbol (e.g., 'NIFTY 50', 'RELIANCE', 'TCS')"
                    },
                    "exchange": {
                        "type": "string",
                        "description": "Exchange (NSE, BSE)",
                        "default": "NSE"
                    },
                    "interval": {
                        "type": "string",
                        "description": "Time interval (minute, day, 3minute, 5minute, 15minute, 30minute, 60minute)",
                        "default": "day"
                    },
                    "days": {
                        "type": "integer",
                        "description": "Number of days of historical data",
                        "default": 30
                    }
                },
                "required": ["symbol"]
            }
        ),
        Tool(
            name="get_fno_data",
            description="Get futures and options data for F&O trading - includes expiry, strike prices, premiums",
            inputSchema={
                "type": "object",
                "properties": {
                    "symbol": {
                        "type": "string",
                        "description": "Underlying symbol (e.g., 'NIFTY', 'BANKNIFTY', 'RELIANCE')"
                    },
                    "instrument_type": {
                        "type": "string",
                        "description": "Instrument type: 'FUT' for futures, 'CE' for call options, 'PE' for put options, 'ALL' for all types",
                        "default": "ALL"
                    },
                    "expiry": {
                        "type": "string",
                        "description": "Expiry date filter (YYYY-MM-DD format, optional)"
                    }
                },
                "required": ["symbol"]
            }
        ),
        Tool(
            name="get_options_chain",
            description="Get complete options chain data with Greeks for options trading analysis",
            inputSchema={
                "type": "object",
                "properties": {
                    "symbol": {
                        "type": "string",
                        "description": "Underlying symbol (e.g., 'NIFTY', 'BANKNIFTY')"
                    },
                    "expiry": {
                        "type": "string",
                        "description": "Expiry date (YYYY-MM-DD format)"
                    }
                },
                "required": ["symbol", "expiry"]
            }
        ),
        Tool(
            name="calculate_technical_indicators",
            description="Calculate raw technical indicators (RSI, MACD, etc.) - provides numerical data for AI analysis",
            inputSchema={
                "type": "object",
                "properties": {
                    "symbol": {
                        "type": "string",
                        "description": "Trading symbol"
                    },
                    "interval": {
                        "type": "string",
                        "description": "Time interval for analysis",
                        "default": "day"
                    },
                    "days": {
                        "type": "integer",
                        "description": "Number of days of data for calculation",
                        "default": 50
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
            name="place_order",
            description="Place orders for equity, futures, or options - unified order placement tool",
            inputSchema={
                "type": "object",
                "properties": {
                    "tradingsymbol": {
                        "type": "string",
                        "description": "Trading symbol (e.g., 'RELIANCE', 'NIFTY24SEP24FUT', 'NIFTY24SEP2424000CE')"
                    },
                    "exchange": {
                        "type": "string",
                        "description": "Exchange (NSE for equity, NFO for F&O)",
                        "default": "NSE"
                    },
                    "transaction_type": {
                        "type": "string",
                        "description": "BUY or SELL"
                    },
                    "quantity": {
                        "type": "integer",
                        "description": "Quantity (consider lot size for F&O)"
                    },
                    "order_type": {
                        "type": "string",
                        "description": "MARKET, LIMIT, SL, SL-M",
                        "default": "MARKET"
                    },
                    "price": {
                        "type": "number",
                        "description": "Price for LIMIT orders"
                    },
                    "trigger_price": {
                        "type": "number",
                        "description": "Trigger price for SL orders"
                    },
                    "product": {
                        "type": "string",
                        "description": "MIS (intraday), CNC (delivery), NRML (normal F&O)",
                        "default": "MIS"
                    }
                },
                "required": ["tradingsymbol", "transaction_type", "quantity"]
            }
        ),
        Tool(
            name="get_positions",
            description="Get current positions (equity and F&O) - raw position data for portfolio analysis",
            inputSchema={
                "type": "object",
                "properties": {
                    "position_type": {
                        "type": "string",
                        "description": "Type of positions: 'day' for intraday, 'net' for overnight, 'all' for both",
                        "default": "all"
                    }
                }
            }
        ),
        Tool(
            name="get_margins",
            description="Get account margin details for position sizing calculations",
            inputSchema={
                "type": "object",
                "properties": {
                    "segment": {
                        "type": "string",
                        "description": "Market segment: 'equity', 'commodity', or 'all'",
                        "default": "all"
                    }
                }
            }
        )
    ]

@app.call_tool()
async def handle_call_tool(name: str, arguments: dict) -> list[types.TextContent]:
    """Handle tool calls"""
    
    if not kite:
        init_kite()
    
    try:
        if name == "get_market_data":
            return await get_market_data_tool(arguments)
        elif name == "get_fno_data":
            return await get_fno_data_tool(arguments)
        elif name == "get_options_chain":
            return await get_options_chain_tool(arguments)
        elif name == "calculate_technical_indicators":
            return await calculate_technical_indicators_tool(arguments)
        elif name == "monitor_orders":
            return await monitor_orders_tool(arguments)
        elif name == "place_order":
            return await place_order_tool(arguments)
        elif name == "get_positions":
            return await get_positions_tool(arguments)
        elif name == "get_margins":
            return await get_margins_tool(arguments)
        # Legacy tools for backward compatibility
        elif name == "fetch_data":
            return await get_market_data_tool(arguments)
        elif name == "analyze_data":
            return await analyze_data_tool(arguments)
        elif name == "buy_stock" or name == "sell_stock":
            # Convert old format to new unified format
            args = arguments.copy()
            args["tradingsymbol"] = args.pop("symbol", "")
            args["transaction_type"] = "BUY" if name == "buy_stock" else "SELL"
            return await place_order_tool(args)
        else:
            return [types.TextContent(type="text", text=f"Unknown tool: {name}")]
    except Exception as e:
        logger.error(f"Error in tool {name}: {str(e)}")
        return [types.TextContent(type="text", text=f"Error: {str(e)}")]

async def get_market_data_tool(arguments: dict) -> list[types.TextContent]:
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

async def get_fno_data_tool(arguments: dict) -> list[types.TextContent]:
    """Get F&O instruments data"""
    symbol = arguments.get("symbol")
    instrument_type = arguments.get("instrument_type", "ALL")
    expiry_filter = arguments.get("expiry")
    
    try:
        fno_instruments = get_fno_instruments(symbol)
        
        if not fno_instruments:
            return [types.TextContent(type="text", text=f"No F&O instruments found for {symbol}")]
        
        # Filter by instrument type
        if instrument_type != "ALL":
            fno_instruments = [inst for inst in fno_instruments if inst['instrument_type'] == instrument_type]
        
        # Filter by expiry if provided
        if expiry_filter:
            fno_instruments = [inst for inst in fno_instruments if inst['expiry'] == expiry_filter]
        
        # Get quotes for current prices
        result_data = []
        for inst in fno_instruments[:20]:  # Limit to 20 instruments
            try:
                quote_key = f"NFO:{inst['tradingsymbol']}"
                quote = kite.quote(quote_key)
                if quote_key in quote:
                    inst_data = inst.copy()
                    inst_data.update({
                        'current_price': quote[quote_key].get('last_price', 0),
                        'ohlc': quote[quote_key].get('ohlc', {}),
                        'volume': quote[quote_key].get('volume', 0),
                        'bid': quote[quote_key].get('depth', {}).get('buy', [{}])[0].get('price', 0),
                        'ask': quote[quote_key].get('depth', {}).get('sell', [{}])[0].get('price', 0),
                        'change': quote[quote_key].get('net_change', 0)
                    })
                    result_data.append(inst_data)
            except Exception:
                result_data.append(inst)  # Add without quote data if quote fails
        
        return [types.TextContent(
            type="text",
            text=f"📊 **F&O Data for {symbol}**\n\n"
                 f"**Found {len(result_data)} instruments**\n\n"
                 f"```json\n{json.dumps(result_data, indent=2, default=str)}\n```"
        )]
        
    except Exception as e:
        return [types.TextContent(type="text", text=f"F&O data error: {str(e)}")]

async def get_options_chain_tool(arguments: dict) -> list[types.TextContent]:
    """Get options chain data"""
    symbol = arguments.get("symbol")
    expiry = arguments.get("expiry")
    
    try:
        # Get options for specific expiry
        fno_instruments = get_fno_instruments(symbol)
        
        # Filter for options with specified expiry
        options = [inst for inst in fno_instruments 
                  if inst['instrument_type'] in ['CE', 'PE'] and inst['expiry'] == expiry]
        
        if not options:
            return [types.TextContent(type="text", text=f"No options found for {symbol} expiry {expiry}")]
        
        # Get current underlying price
        underlying_quote = kite.quote(f"NSE:{symbol}")
        underlying_price = 0
        if f"NSE:{symbol}" in underlying_quote:
            underlying_price = underlying_quote[f"NSE:{symbol}"].get('last_price', 0)
        
        # Build options chain
        chain_data = {
            'underlying': symbol,
            'underlying_price': underlying_price,
            'expiry': expiry,
            'call_options': [],
            'put_options': []
        }
        
        for option in options[:50]:  # Limit to 50 options
            try:
                quote_key = f"NFO:{option['tradingsymbol']}"
                quote = kite.quote(quote_key)
                
                option_data = {
                    'strike': option['strike'],
                    'premium': quote[quote_key].get('last_price', 0) if quote_key in quote else 0,
                    'change': quote[quote_key].get('net_change', 0) if quote_key in quote else 0,
                    'volume': quote[quote_key].get('volume', 0) if quote_key in quote else 0,
                    'oi': quote[quote_key].get('oi', 0) if quote_key in quote else 0,
                    'tradingsymbol': option['tradingsymbol']
                }
                
                if option['instrument_type'] == 'CE':
                    chain_data['call_options'].append(option_data)
                else:
                    chain_data['put_options'].append(option_data)
                    
            except Exception:
                continue
        
        # Sort by strike price
        chain_data['call_options'].sort(key=lambda x: x['strike'])
        chain_data['put_options'].sort(key=lambda x: x['strike'])
        
        return [types.TextContent(
            type="text",
            text=f"🔗 **Options Chain for {symbol} - {expiry}**\n\n"
                 f"**Underlying Price:** ₹{underlying_price}\n"
                 f"**Calls:** {len(chain_data['call_options'])} options\n"
                 f"**Puts:** {len(chain_data['put_options'])} options\n\n"
                 f"```json\n{json.dumps(chain_data, indent=2, default=str)}\n```"
        )]
        
    except Exception as e:
        return [types.TextContent(type="text", text=f"Options chain error: {str(e)}")]

async def calculate_technical_indicators_tool(arguments: dict) -> list[types.TextContent]:
    """Calculate raw technical indicators"""
    symbol = arguments.get("symbol")
    interval = arguments.get("interval", "day")
    days = arguments.get("days", 50)
    
    try:
        # Get instrument details
        instruments = kite.instruments("NSE")
        instrument = None
        
        for inst in instruments:
            if symbol.upper() in inst['tradingsymbol'].upper():
                instrument = inst
                break
        
        if not instrument:
            return [types.TextContent(type="text", text=f"Instrument {symbol} not found")]
        
        # Get historical data
        from_date = datetime.now() - timedelta(days=days)
        historical_data = kite.historical_data(
            instrument_token=instrument['instrument_token'],
            from_date=from_date,
            to_date=datetime.now(),
            interval=interval
        )
        
        if not historical_data:
            return [types.TextContent(type="text", text=f"No historical data for {symbol}")]
        
        # Convert to DataFrame and calculate indicators
        df = pd.DataFrame(historical_data)
        for col in ['open', 'high', 'low', 'close', 'volume']:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce')
        
        global indicator_calculator
        indicators = indicator_calculator.calculate_indicators(df)
        
        if "error" in indicators:
            return [types.TextContent(type="text", text=f"Indicator calculation error: {indicators['error']}")]
        
        # Add current price info
        current_quote = kite.quote(f"NSE:{instrument['tradingsymbol']}")
        current_data = current_quote.get(f"NSE:{instrument['tradingsymbol']}", {})
        
        result = {
            'symbol': symbol,
            'current_price': current_data.get('last_price', 0),
            'current_change': current_data.get('net_change', 0),
            'volume': current_data.get('volume', 0),
            'technical_indicators': indicators,
            'data_points': len(df),
            'calculation_time': datetime.now().isoformat()
        }
        
        return [types.TextContent(
            type="text",
            text=f"📈 **Technical Indicators for {symbol}**\n\n"
                 f"**Current Price:** ₹{current_data.get('last_price', 0)}\n"
                 f"**Change:** {current_data.get('net_change', 0)}\n"
                 f"**Data Points:** {len(df)} periods\n\n"
                 f"**Raw Indicator Values:**\n"
                 f"```json\n{json.dumps(result, indent=2, default=str)}\n```\n\n"
                 f"*Note: These are raw numerical values for AI analysis. No interpretations provided.*"
        )]
        
    except Exception as e:
        return [types.TextContent(type="text", text=f"Technical indicators error: {str(e)}")]

async def place_order_tool(arguments: dict) -> list[types.TextContent]:
    """Unified order placement for equity and F&O"""
    tradingsymbol = arguments.get("tradingsymbol")
    exchange = arguments.get("exchange", "NSE")
    transaction_type = arguments.get("transaction_type")
    quantity = arguments.get("quantity")
    order_type = arguments.get("order_type", "MARKET")
    price = arguments.get("price")
    trigger_price = arguments.get("trigger_price")
    product = arguments.get("product", "MIS")
    
    try:
        # Prepare order parameters
        order_params = {
            "variety": "regular",
            "tradingsymbol": tradingsymbol,
            "exchange": exchange,
            "transaction_type": transaction_type.upper(),
            "quantity": quantity,
            "order_type": order_type.upper(),
            "product": product.upper()
        }
        
        if order_type.upper() == "LIMIT" and price:
            order_params["price"] = price
        
        if order_type.upper() in ["SL", "SL-M"] and trigger_price:
            order_params["trigger_price"] = trigger_price
        
        # Place order
        order_id = kite.place_order(**order_params)
        
        return [types.TextContent(
            type="text",
            text=f"✅ **Order Placed Successfully**\n\n"
                 f"**Order ID:** {order_id}\n"
                 f"**Symbol:** {tradingsymbol}\n"
                 f"**Exchange:** {exchange}\n"
                 f"**Type:** {transaction_type}\n"
                 f"**Quantity:** {quantity}\n"
                 f"**Order Type:** {order_type}\n"
                 f"**Price:** {'₹' + str(price) if price else 'Market Price'}\n"
                 f"**Product:** {product}\n"
                 f"**Time:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
                 f"Use monitor_orders tool to track execution."
        )]
        
    except Exception as e:
        return [types.TextContent(type="text", text=f"Order placement error: {str(e)}")]

async def get_positions_tool(arguments: dict) -> list[types.TextContent]:
    """Get current positions"""
    position_type = arguments.get("position_type", "all")
    
    try:
        if position_type == "all":
            day_positions = kite.positions()['day']
            net_positions = kite.positions()['net']
            
            result = {
                'day_positions': day_positions,
                'net_positions': net_positions,
                'total_day_positions': len(day_positions),
                'total_net_positions': len(net_positions),
                'timestamp': datetime.now().isoformat()
            }
        else:
            positions = kite.positions()[position_type]
            result = {
                f'{position_type}_positions': positions,
                f'total_{position_type}_positions': len(positions),
                'timestamp': datetime.now().isoformat()
            }
        
        return [types.TextContent(
            type="text",
            text=f"📊 **Current Positions**\n\n"
                 f"```json\n{json.dumps(result, indent=2, default=str)}\n```"
        )]
        
    except Exception as e:
        return [types.TextContent(type="text", text=f"Positions error: {str(e)}")]

async def get_margins_tool(arguments: dict) -> list[types.TextContent]:
    """Get account margins"""
    segment = arguments.get("segment", "all")
    
    try:
        margins = kite.margins()
        
        if segment == "all":
            result = margins
        else:
            result = margins.get(segment, {})
        
        return [types.TextContent(
            type="text",
            text=f"💰 **Account Margins**\n\n"
                 f"```json\n{json.dumps(result, indent=2, default=str)}\n```"
        )]
        
    except Exception as e:
        return [types.TextContent(type="text", text=f"Margins error: {str(e)}")]

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
