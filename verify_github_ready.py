"""
GitHub Readiness Verification Script
====================================
This script verifies that the repository is ready for GitHub publication.
It checks for all required files, proper structure, and security considerations.
"""
import os
import sys
from pathlib import Path
def check_file_exists(filepath, description=""):
    """Check if a file exists and report status."""
    if os.path.exists(filepath):
        print(f"✅ {description or filepath}")
        return True
    else:
        print(f"❌ Missing: {description or filepath}")
        return False
def check_file_content(filepath, required_content, description=""):
    """Check if file contains required content."""
    try:
        with open(filepath, 'r') as f:
            content = f.read()
            if all(item in content for item in required_content):
                print(f"✅ {description or filepath} - Content verified")
                return True
            else:
                print(f"⚠️  {description or filepath} - Missing required content")
                return False
    except FileNotFoundError:
        print(f"❌ {description or filepath} - File not found")
        return False
def main():
    print("🔍 GitHub Readiness Verification")
    print("=" * 40)
    
    all_checks_passed = True
    
    print("\n📋 Essential Files:")
    essential_files = [
        ("README.md", "README documentation"),
        ("LICENSE", "License file"),
        ("requirements.txt", "Python dependencies"),
        (".gitignore", "Git ignore file"),
        ("config.env.example", "Example configuration"),
    ]
    
    for filepath, description in essential_files:
        if not check_file_exists(filepath, description):
            all_checks_passed = False
    
    print("\n📚 Documentation:")
    docs = [
        ("CONTRIBUTING.md", "Contributing guidelines"),
        ("CHANGELOG.md", "Change log"),
        ("USAGE_EXAMPLES.md", "Usage examples"),
    ]
    
    for filepath, description in docs:
        if not check_file_exists(filepath, description):
            all_checks_passed = False
    
    print("\n🔧 GitHub Templates:")
    github_files = [
        (".github/ISSUE_TEMPLATE/bug_report.md", "Bug report template"),
        (".github/ISSUE_TEMPLATE/feature_request.md", "Feature request template"),
        (".github/pull_request_template.md", "Pull request template"),
        (".github/workflows/ci.yml", "CI/CD workflow"),
    ]
    
    for filepath, description in github_files:
        if not check_file_exists(filepath, description):
            all_checks_passed = False
    
    print("\n⚙️  Setup Scripts:")
    scripts = [
        ("setup.py", "Setup verification script"),
        ("install.sh", "Installation script"),
    ]
    
    for filepath, description in scripts:
        if not check_file_exists(filepath, description):
            all_checks_passed = False
    
    print("\n🚀 Core Files:")
    core_files = [
        ("zerodha_mcp_server.py", "Main MCP server"),
        ("zerodha_mcp_wrapper.py", "MCP wrapper"),
        ("risk_manager.py", "Risk manager"),
        ("trading_config.py", "Trading configuration"),
        ("generate_access_token.py", "Token generator"),
    ]
    
    for filepath, description in core_files:
        if not check_file_exists(filepath, description):
            all_checks_passed = False
    
    print("\n📄 Content Verification:")
    
    readme_sections = [
        "# Zerodha Kite MCP Server",
        "## ✨ Features",
        "## 📦 Installation", 
        "## 🏁 Quick Start",
        "## 🛠️ MCP Tools",
        "## 🔒 Security"
    ]
    
    if not check_file_content("README.md", readme_sections, "README sections"):
        all_checks_passed = False
    
    gitignore_patterns = [
        "config.env",
        "__pycache__/",
        "*.log",
        "zerodha_mcp_env/"
    ]
    
    if not check_file_content(".gitignore", gitignore_patterns, ".gitignore patterns"):
        all_checks_passed = False
    
    print("\n🔒 Security Checks:")
    
    sensitive_patterns = ["api_key", "api_secret", "access_token"]
    secure_files = True
    
    for pattern in sensitive_patterns:
        try:
            with open("config.env", 'r') as f:
                content = f.read().lower()
                if any(word in content for word in ["xxx", "your_", "placeholder"]):
                    print(f"✅ config.env appears secure (has placeholders)")
                    break
                else:
                    print(f"⚠️  config.env may contain real credentials")
                    secure_files = False
                    break
        except FileNotFoundError:
            pass
    
    test_files = ["test_", "TEST_", "testing"]
    has_test_files = False
    
    for root, dirs, files in os.walk("."):
        if "zerodha_mcp_env" in root:
            continue
        for file in files:
            if any(pattern in file.lower() for pattern in test_files):
                print(f"⚠️  Found test file: {os.path.join(root, file)}")
                has_test_files = True
    
    if not has_test_files:
        print("✅ No test files found (clean distribution)")
    
    print("\n🏁 Final Status:")
    if all_checks_passed and secure_files and not has_test_files:
        print("🎉 Repository is GitHub-ready!")
        print("\n📋 Next Steps:")
        print("1. Create GitHub repository")
        print("2. Add collaborators if needed")
        print("3. Set up branch protection rules")
        print("4. Configure repository settings")
        print("5. Create first release")
        return True
    else:
        print("❌ Repository needs attention before GitHub publication")
        print("\n🔧 Please address the issues above")
        return False
def check_executable_permissions():
    """Check if scripts have proper permissions."""
    print("\n🔐 Permission Checks:")
    scripts = ["install.sh", "verify_github_ready.py"]
    
    for script in scripts:
        if os.path.exists(script):
            if os.access(script, os.X_OK):
                print(f"✅ {script} is executable")
            else:
                print(f"⚠️  {script} is not executable (run: chmod +x {script})")
if __name__ == "__main__":
    print("GitHub Readiness Verification for Zerodha Kite MCP Server")
    print("=" * 60)
    
    success = main()
    check_executable_permissions()
    
    if success:
        sys.exit(0)
    else:
        sys.exit(1)
