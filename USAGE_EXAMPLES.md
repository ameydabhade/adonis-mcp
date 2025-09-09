# Usage Examples - Enhanced Zerodha Kite MCP Server

## 🎯 Pure Data MCP for AI Trading

This MCP server provides raw market data and enhanced order execution capabilities without trading signals. Perfect for AI agents that make their own trading decisions.

## Basic Usage Examples

### 1. Get Market Data for Analysis

```python
# Get real-time market data
get_market_data(
    symbol="RELIANCE",
    days=30,
    interval="day"
)

# Get technical indicators (raw values)
calculate_technical_indicators(
    symbol="RELIANCE",
    days=50
)

# Get F&O data
get_fno_data(symbol="NIFTY")
```

### 2. Place Order with Stop Loss & Target

```python
# Enhanced order placement
place_order(
    tradingsymbol="RELIANCE",
    transaction_type="BUY",
    quantity=10,
    order_type="LIMIT",
    price=1380,
    stop_loss_price=1360,    # Automatic stop loss
    target_price=1420,       # Automatic target
    product="MIS"
)
```

### 3. F&O Trading with Bracket Orders

```python
# F&O with bracket order
place_order(
    tradingsymbol="NIFTY25DEC25000CE",
    transaction_type="BUY", 
    quantity=75,             # NIFTY lot size
    order_type="LIMIT",
    price=50,
    stop_loss_price=40,
    target_price=65,
    bracket_order=True       # Try true bracket order
)
```

## Advanced Examples

### AI Trading Workflow

```python
# 1. AI gets raw data
market_data = get_market_data("INFY", days=20)
indicators = calculate_technical_indicators("INFY", days=30)
fno_data = get_fno_data("INFY")

# 2. AI analyzes data (outside MCP)
# - Process RSI, MACD, volume patterns
# - Analyze options chain data
# - Make trading decision

# 3. AI places trade with protection
if ai_decision == "BUY":
    place_order(
        tradingsymbol="INFY25SEP1500CE",
        transaction_type="BUY",
        quantity=400,
        order_type="LIMIT", 
        price=ai_calculated_price,
        stop_loss_price=ai_stop_loss,
        target_price=ai_target
    )

# 4. Monitor execution
monitor_orders()
get_positions()
```

### Options Strategy Example

```python
# Get options chain for analysis
get_options_chain(
    symbol="NIFTY",
    expiry="2025-09-26"
)

# AI analyzes Greeks, IV, OI
# Decides on options strategy

# Place multi-leg options order
place_order(
    tradingsymbol="NIFTY25SEP25000CE",
    transaction_type="BUY",
    quantity=75,
    order_type="LIMIT",
    price=45,
    stop_loss_price=35,
    target_price=60
)

# Simultaneously place hedge
place_order(
    tradingsymbol="NIFTY25SEP25200CE", 
    transaction_type="SELL",
    quantity=75,
    order_type="LIMIT",
    price=30
)
```

## Risk Management Features

### Built-in Risk Controls

```python
# Check account status
get_margins()
get_risk_status()

# Place protected order
place_order(
    tradingsymbol="BANKNIFTY25SEP54000PE",
    transaction_type="SELL",
    quantity=35,
    order_type="LIMIT",
    price=400,
    stop_loss_price=500,    # Loss protection
    target_price=300        # Profit target
)

# Monitor protective orders
monitor_stop_orders()
```

### Position Management

```python
# Check current positions
positions = get_positions()

# Set stop loss for existing position
set_stop_loss(
    tradingsymbol="RELIANCE",
    stop_loss_price=1350,
    target_price=1450
)

# Monitor all orders
monitor_orders()
```

## Key Benefits for AI Agents

### ✅ Pure Data Focus
- No trading signals or recommendations
- Raw technical indicator values
- Complete market data access
- AI makes all trading decisions

### ✅ Enhanced Order Management
- Built-in stop loss and targets
- Automatic bracket order support
- Smart order type selection
- Risk management integration

### ✅ Complete Trading Infrastructure
- Real-time data feeds
- F&O and options support
- Position and margin tracking
- Comprehensive order monitoring

## Error Handling

The MCP server includes robust error handling:

```python
# Orders may fail due to:
# - Insufficient margins
# - Invalid symbols
# - Risk management limits
# - Market hours restrictions

# Always check order status
result = place_order(...)
# Check result for success/failure
monitor_orders(order_id)
```

## Production Ready

- ✅ Risk management controls
- ✅ Production logging
- ✅ Error handling
- ✅ Rate limiting
- ✅ Market hours validation
- ✅ Dry run mode support

Perfect for AI agents that need reliable market data and execution capabilities without trading interference!


