#!/usr/bin/env python3
"""
Debug startup script for the MCP server
This will help identify any issues with server startup
"""

import sys
import os
import logging

# Set up debug logging
logging.basicConfig(level=logging.DEBUG, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

def debug_startup():
    """Debug the server startup process"""
    
    print("🔍 MCP Server Debug Startup")
    print("=" * 30)
    
    # Check Python version
    print(f"Python: {sys.version}")
    
    # Check current directory
    print(f"Working Dir: {os.getcwd()}")
    
    # Check environment
    print(f"Virtual Env: {os.environ.get('VIRTUAL_ENV', 'None')}")
    
    # Test imports
    print("\n📦 Testing imports...")
    try:
        import mcp
        print("✅ mcp imported")
        
        import kiteconnect
        print("✅ kiteconnect imported")
        
        from dotenv import load_dotenv
        print("✅ dotenv imported")
        
        # Load config
        load_dotenv('config.env')
        api_key = os.getenv('KITE_API_KEY')
        print(f"✅ Config loaded (API key: {api_key[:8] if api_key else 'None'}...)")
        
    except Exception as e:
        print(f"❌ Import error: {e}")
        return False
    
    # Try to import our server
    print("\n🚀 Testing server import...")
    try:
        from zerodha_mcp_server import app, init_kite
        print("✅ Server imported successfully")
        
        # Test Kite initialization  
        kite = init_kite()
        print("✅ Kite Connect initialized")
        
        print("\n🎉 Server is ready to start!")
        print("✅ All checks passed")
        
        return True
        
    except Exception as e:
        print(f"❌ Server import/init error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = debug_startup()
    
    if success:
        print(f"\n🚀 Starting MCP server...")
        
        # Import and run the server
        from zerodha_mcp_server import main
        import asyncio
        
        try:
            asyncio.run(main())
        except KeyboardInterrupt:
            print(f"\n👋 Server stopped by user")
        except Exception as e:
            print(f"\n❌ Server error: {e}")
            import traceback
            traceback.print_exc()
    else:
        print(f"\n❌ Pre-flight checks failed")
        sys.exit(1)

