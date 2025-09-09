#!/usr/bin/env python3
"""
Wrapper script for Zerodha MCP Server
This ensures the server can be found by Cursor
"""

import os
import sys
import subprocess

# Set the correct working directory
ZERODHA_DIR = os.path.dirname(os.path.abspath(__file__))
PYTHON_PATH = os.path.join(ZERODHA_DIR, "zerodha_mcp_env", "bin", "python")
SERVER_SCRIPT = os.path.join(ZERODHA_DIR, "zerodha_mcp_server.py")

def main():
    """Main wrapper function"""
    
    # Change to the correct directory
    os.chdir(ZERODHA_DIR)
    
    # Set environment variables
    env = os.environ.copy()
    env['VIRTUAL_ENV'] = f"{ZERODHA_DIR}/zerodha_mcp_env"
    env['PATH'] = f"{ZERODHA_DIR}/zerodha_mcp_env/bin:" + env.get('PATH', '')
    
    # Execute the server
    try:
        subprocess.run([PYTHON_PATH, SERVER_SCRIPT], env=env, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error running server: {e}", file=sys.stderr)
        sys.exit(1)
    except FileNotFoundError as e:
        print(f"File not found: {e}", file=sys.stderr)
        print(f"Python path: {PYTHON_PATH}", file=sys.stderr)
        print(f"Server script: {SERVER_SCRIPT}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
