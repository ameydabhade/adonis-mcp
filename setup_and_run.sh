#!/bin/bash

# Zerodha MCP Server Setup and Run Script
# =======================================

echo "🚀 Zerodha MCP Server - Setup & Run"
echo "===================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️ $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

print_info() {
    echo -e "${BLUE}ℹ️ $1${NC}"
}

# Check if virtual environment exists
if [ ! -d "zerodha_mcp_env" ]; then
    print_warning "Virtual environment not found. Creating..."
    python3 -m venv zerodha_mcp_env
    print_status "Virtual environment created"
fi

# Activate virtual environment
source zerodha_mcp_env/bin/activate
print_status "Virtual environment activated"

# Check if dependencies are installed
if ! python -c "import kiteconnect, mcp" 2>/dev/null; then
    print_warning "Dependencies not found. Installing..."
    pip install -r requirements.txt
    print_status "Dependencies installed"
else
    print_status "Dependencies already installed"
fi

# Check configuration
if [ ! -f "config.env" ]; then
    print_error "config.env file not found!"
    echo "Please create config.env with your Kite Connect credentials:"
    echo "KITE_API_KEY=your_api_key"
    echo "KITE_API_SECRET=your_api_secret"
    echo "KITE_ACCESS_TOKEN=your_access_token"
    exit 1
fi

print_status "Configuration file found"

# Test connection
print_info "Testing Kite Connect API connection..."
if python test_connection.py; then
    print_status "API connection test passed"
else
    print_error "API connection test failed"
    print_warning "You may need to run: python generate_access_token.py"
    exit 1
fi

# Show available commands
echo ""
print_info "Available commands:"
echo "1. 🚀 Start MCP Server:     python zerodha_mcp_server.py"
echo "2. 🔑 Generate Token:       python generate_access_token.py"
echo "3. 🧪 Test Connection:      python test_connection.py"
echo "4. 📖 View Demo:           python demo_usage.py"

echo ""
print_info "MCP Server Tools Available:"
echo "📈 fetch_data      - Get real-time/historical data for NIFTY, stocks"
echo "🧠 analyze_data    - Sequential thinking analysis with recommendations"
echo "👁️ monitor_orders  - Track order status and execution"
echo "💰 buy_stock       - Place buy orders (MARKET/LIMIT/SL)"
echo "💸 sell_stock      - Place sell orders (MARKET/LIMIT/SL)"

echo ""
print_status "Setup complete! Ready to trade with AI-powered analysis."

# Ask user what to do
echo ""
read -p "What would you like to do? (1=Start Server, 2=Generate Token, 3=Test, 4=Demo, q=Quit): " choice

case $choice in
    1)
        print_info "Starting MCP Server..."
        python zerodha_mcp_server.py
        ;;
    2)
        print_info "Generating access token..."
        python generate_access_token.py
        ;;
    3)
        print_info "Testing API connection..."
        python test_connection.py
        ;;
    4)
        print_info "Showing demo usage..."
        python demo_usage.py
        ;;
    q|Q)
        print_info "Goodbye!"
        exit 0
        ;;
    *)
        print_warning "Invalid choice. Run script again to choose an option."
        ;;
esac

