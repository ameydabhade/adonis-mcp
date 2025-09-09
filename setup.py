import os
import shutil
import sys
from pathlib import Path

def main():
    print("🚀 Zerodha Kite MCP Server Setup")
    print("=" * 40)
    
    if not os.path.exists("config.env"):
        print("\n📋 Setting up configuration file...")
        if os.path.exists("config.env.example"):
            shutil.copy("config.env.example", "config.env")
            print("✅ Created config.env from example")
            print("⚠️  Please edit config.env and add your Zerodha Kite Connect credentials")
        else:
            print("❌ config.env.example not found!")
            return False
    else:
        print("✅ config.env already exists")
    
    print(f"\n🐍 Python Version: {sys.version}")
    if sys.version_info < (3, 8):
        print("❌ Python 3.8+ required")
        return False
    
    venv_path = Path("zerodha_mcp_env")
    if venv_path.exists():
        print("✅ Virtual environment found")
    else:
        print("⚠️  Virtual environment not found at zerodha_mcp_env/")
        print("   Create one with: python -m venv zerodha_mcp_env")
    
    try:
        import mcp
        print("✅ MCP library installed")
    except ImportError:
        print("❌ MCP library not found. Install with: pip install -r requirements.txt")
    
    try:
        import kiteconnect
        print("✅ Kite Connect library installed")
    except ImportError:
        print("❌ Kite Connect library not found. Install with: pip install -r requirements.txt")
    
    print("\n🎯 Next Steps:")
    print("1. Activate virtual environment: source zerodha_mcp_env/bin/activate")
    print("2. Install dependencies: pip install -r requirements.txt")
    print("3. Edit config.env with your Kite Connect credentials")
    print("4. Generate access token: python generate_access_token.py")
    print("5. Start MCP server: python zerodha_mcp_server.py")
    
    print("\n📚 Documentation:")
    print("- README.md for detailed setup instructions")
    print("- USAGE_EXAMPLES.md for trading examples")
    
    return True

if __name__ == "__main__":
    main()