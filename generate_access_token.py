"""
Zerodha Kite Connect Access Token Generator
This script helps generate and update access tokens for the MCP server.
Run this script daily to refresh your access token.
"""

import os
import webbrowser
from kiteconnect import KiteConnect
from dotenv import load_dotenv, set_key

def generate_access_token():
    """Generate access token for Kite Connect"""
    
    load_dotenv('config.env')
    
    api_key = os.getenv('KITE_API_KEY')
    api_secret = os.getenv('KITE_API_SECRET')
    
    if not api_key or not api_secret:
        print("❌ Error: KITE_API_KEY and KITE_API_SECRET must be set in config.env")
        return False
    
    kite = KiteConnect(api_key=api_key)
    
    login_url = kite.login_url()
    print(f"🌐 Opening login URL in browser...")
    print(f"Login URL: {login_url}")
    
    try:
        webbrowser.open(login_url)
    except:
        print("⚠️ Could not open browser automatically. Please copy the URL above and open it manually.")
    
    print("\n📝 After logging in, you'll be redirected to a URL with 'request_token' parameter.")
    print("Copy the request_token value from the redirected URL.")
    print("Example: https://example.com?request_token=ABC123&action=login&status=success")
    print("In this case, your request_token is: ABC123")
    
    request_token = input("\n🔑 Enter the request_token: ").strip()
    
    if not request_token:
        print("❌ Error: Request token is required")
        return False
    
    try:
        data = kite.generate_session(request_token, api_secret=api_secret)
        access_token = data["access_token"]
        
        set_key('config.env', 'KITE_ACCESS_TOKEN', access_token)
        
        print(f"\n✅ Success! Access token generated and saved to config.env")
        print(f"🔑 Access Token: {access_token}")
        print(f"👤 User ID: {data.get('user_id', 'N/A')}")
        print(f"📧 Email: {data.get('email', 'N/A')}")
        print(f"📱 Phone: {data.get('phone', 'N/A')}")
        
        kite.set_access_token(access_token)
        profile = kite.profile()
        print(f"\n🎯 Connection test successful!")
        print(f"📊 Account: {profile.get('user_name', 'N/A')} ({profile.get('user_id', 'N/A')})")
        
        return True
        
    except Exception as e:
        print(f"❌ Error generating access token: {str(e)}")
        return False

def main():
    """Main function"""
    print("🚀 Zerodha Kite Connect Access Token Generator")
    print("=" * 50)
    
    if generate_access_token():
        print("\n✨ Setup complete! You can now run the MCP server.")
        print("Command: python zerodha_mcp_server.py")
    else:
        print("\n❌ Setup failed. Please check your credentials and try again.")

if __name__ == "__main__":
    main()
