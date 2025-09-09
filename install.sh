echo "🚀 Installing Adonis - Trading MCP Server"
echo "========================================"

if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is required but not found"
    echo "   Please install Python 3.8+ from https://python.org"
    exit 1
fi

echo "✅ Python 3 found: $(python3 --version)"

if [ ! -d "zerodha_mcp_env" ]; then
    echo "🔧 Creating virtual environment..."
    python3 -m venv zerodha_mcp_env
    echo "✅ Virtual environment created"
else
    echo "✅ Virtual environment already exists"
fi

echo "🔄 Activating virtual environment..."
source zerodha_mcp_env/bin/activate

echo "⬆️  Upgrading pip..."
pip install --upgrade pip

echo "📦 Installing Python dependencies..."
pip install -r requirements.txt

if [ ! -f "config.env" ]; then
    echo "📋 Creating configuration file..."
    cp config.env.example config.env
    echo "✅ Created config.env from example"
else
    echo "✅ Configuration file already exists"
fi

echo ""
echo "🎉 Installation completed successfully!"
echo ""
echo "🎯 Next Steps:"
echo "1. Edit config.env with your Zerodha Kite Connect credentials"
echo "2. Run: python3 generate_access_token.py"
echo "3. Start server: python3 zerodha_mcp_server.py"
echo ""
echo "💡 Need help? Check README.md for detailed instructions"
echo ""
echo "⚠️  Remember to:"
echo "   - Keep config.env secure"
echo "   - Never commit credentials to version control"
echo "   - Regenerate access token daily"
