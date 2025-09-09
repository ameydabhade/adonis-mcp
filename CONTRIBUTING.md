# Contributing to Adonis

Thank you for your interest in contributing to Adonis - Trading MCP Server! We welcome contributions from the community and are grateful for your support.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [Making Changes](#making-changes)
- [Submitting Changes](#submitting-changes)
- [Coding Standards](#coding-standards)
- [Testing](#testing)
- [Documentation](#documentation)

## Code of Conduct

This project adheres to a Code of Conduct. By participating, you are expected to uphold this code. Please report unacceptable behavior to the project maintainers.

### Our Standards

- Use welcoming and inclusive language
- Be respectful of differing viewpoints and experiences
- Gracefully accept constructive criticism
- Focus on what is best for the community
- Show empathy towards other community members

## Getting Started

### Prerequisites

- Python 3.8 or higher
- Git
- Zerodha Kite Connect account (for testing)
- Familiarity with MCP (Model Context Protocol)

### Development Setup

1. **Fork the repository**
   ```bash
   # Fork on GitHub, then clone your fork
   git clone https://github.com/yourusername/adonis-trading-mcp.git
   cd adonis-trading-mcp
   ```

2. **Set up development environment**
   ```bash
   # Create virtual environment
   python3 -m venv dev_env
   source dev_env/bin/activate  # On Windows: dev_env\Scripts\activate
   
   # Install dependencies
   pip install -r requirements.txt
   pip install -r requirements-dev.txt  # If available
   ```

3. **Configure development settings**
   ```bash
   # Copy example configuration
   cp config.env.example config.env
   
   # Add your test credentials (use sandbox/test account)
   # Edit config.env with your development API keys
   ```

4. **Verify setup**
   ```bash
   # Run setup check
   python3 setup.py
   
   # Run basic tests
   python3 -m pytest tests/ -v  # If tests exist
   ```

## Making Changes

### Branch Naming Convention

Use descriptive branch names:
- `feature/add-new-indicator` - New features
- `fix/authentication-error` - Bug fixes  
- `docs/update-readme` - Documentation updates
- `refactor/cleanup-utils` - Code refactoring

### Development Workflow

1. **Create a branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes**
   - Write clean, readable code
   - Follow the existing code style
   - Add tests for new functionality
   - Update documentation as needed

3. **Test your changes**
   ```bash
   # Run linting
   flake8 .
   
   # Format code
   black .
   
   # Run tests
   python3 -m pytest tests/
   
   # Test manually with MCP client
   python3 zerodha_mcp_server.py
   ```

4. **Commit your changes**
   ```bash
   git add .
   git commit -m "feat: add new technical indicator support"
   ```

## Submitting Changes

### Pull Request Process

1. **Push your branch**
   ```bash
   git push origin feature/your-feature-name
   ```

2. **Create Pull Request**
   - Go to GitHub and create a pull request
   - Use a clear, descriptive title
   - Provide detailed description of changes
   - Reference any related issues

3. **PR Template**
   ```markdown
   ## Description
   Brief description of changes made.
   
   ## Type of Change
   - [ ] Bug fix
   - [ ] New feature
   - [ ] Documentation update
   - [ ] Refactoring
   
   ## Testing
   - [ ] Tests pass locally
   - [ ] New tests added for new functionality
   - [ ] Manual testing completed
   
   ## Checklist
   - [ ] Code follows style guidelines
   - [ ] Self-review completed
   - [ ] Documentation updated
   - [ ] No sensitive data exposed
   ```

### Review Process

- Maintainers will review your PR
- Address any feedback or requested changes
- Once approved, your PR will be merged
- Your contribution will be acknowledged

## Coding Standards

### Python Style Guide

We follow PEP 8 with some modifications:

```python
# ✅ Good: Clear function names and documentation
def calculate_technical_indicators(symbol: str, days: int = 20) -> dict:
    """
    Calculate technical indicators for a given symbol.
    
    Args:
        symbol: Trading symbol (e.g., "RELIANCE")
        days: Number of days for calculation
        
    Returns:
        Dictionary containing calculated indicators
    """
    pass

# ✅ Good: Type hints and error handling
def get_market_data(symbol: str) -> dict:
    try:
        # Implementation here
        return data
    except Exception as e:
        logger.error(f"Failed to fetch data for {symbol}: {e}")
        raise
```

### Code Organization

```
adonis-trading-mcp/
├── zerodha_mcp_server.py      # Main server implementation
├── zerodha_mcp_wrapper.py     # MCP wrapper
├── risk_manager.py            # Risk management
├── trading_config.py          # Configuration
├── utils/                     # Utility functions
│   ├── __init__.py
│   ├── market_data.py
│   └── technical_analysis.py
├── tests/                     # Test files
│   ├── __init__.py
│   ├── test_server.py
│   └── test_trading.py
└── docs/                      # Documentation
    ├── api.md
    └── examples.md
```

### Documentation Standards

- Use clear, concise docstrings
- Include type hints for all functions
- Add inline comments for complex logic
- Update README for new features

```python
def place_order(
    symbol: str,
    transaction_type: str,
    quantity: int,
    order_type: str = "MARKET",
    price: float = None
) -> dict:
    """
    Place a trading order through Kite Connect API.
    
    Args:
        symbol: Trading symbol (e.g., "RELIANCE")
        transaction_type: "BUY" or "SELL"
        quantity: Number of shares to trade
        order_type: Order type - "MARKET", "LIMIT", "SL", "SL-M"
        price: Price for limit orders (required for LIMIT orders)
        
    Returns:
        dict: Order response with order_id and status
        
    Raises:
        ValueError: If required parameters are missing
        KiteException: If API call fails
        
    Example:
        >>> place_order("RELIANCE", "BUY", 10, "MARKET")
        {"order_id": "123456", "status": "COMPLETE"}
    """
```

## Testing

### Test Categories

1. **Unit Tests**: Test individual functions
2. **Integration Tests**: Test API interactions
3. **MCP Tests**: Test MCP protocol compliance
4. **Security Tests**: Test credential handling

### Writing Tests

```python
import pytest
from unittest.mock import Mock, patch

def test_get_market_data_success():
    """Test successful market data retrieval."""
    # Arrange
    mock_kite = Mock()
    mock_kite.quote.return_value = {"NSE:RELIANCE": {"last_price": 2500}}
    
    # Act
    with patch('zerodha_mcp_wrapper.kite', mock_kite):
        result = get_market_data("RELIANCE")
    
    # Assert
    assert result["last_price"] == 2500
    mock_kite.quote.assert_called_once_with("NSE:RELIANCE")

def test_place_order_invalid_symbol():
    """Test order placement with invalid symbol."""
    with pytest.raises(ValueError, match="Invalid symbol"):
        place_order("", "BUY", 10)
```

### Running Tests

```bash
# Run all tests
python3 -m pytest tests/ -v

# Run specific test file
python3 -m pytest tests/test_trading.py -v

# Run with coverage
python3 -m pytest tests/ --cov=. --cov-report=html
```

## Documentation

### Types of Documentation

1. **Code Documentation**: Docstrings and comments
2. **API Documentation**: Function and tool descriptions
3. **User Documentation**: README and usage guides
4. **Developer Documentation**: Contributing and architecture

### Documentation Updates

When making changes:

- Update docstrings for modified functions
- Add examples for new features
- Update README if public API changes
- Add entries to CHANGELOG.md

## Security Considerations

### Sensitive Data

- Never commit API keys or secrets
- Use placeholder values in examples
- Test with sandbox/demo accounts
- Review PRs for exposed credentials

### Safe Practices

```python
# ✅ Good: Use environment variables
import os
api_key = os.getenv("KITE_API_KEY")

# ❌ Bad: Hardcoded secrets
api_key = "abc123def456"  # NEVER DO THIS

# ✅ Good: Input validation
def validate_symbol(symbol: str) -> bool:
    if not symbol or len(symbol) > 20:
        raise ValueError("Invalid symbol")
    return True

# ✅ Good: Error handling without exposing internals
try:
    result = api_call()
except Exception:
    logger.error("API call failed")
    return {"error": "Service temporarily unavailable"}
```

## Questions or Need Help?

- 📖 Check existing documentation
- 🔍 Search existing issues
- 💬 Open a new issue for questions
- 📧 Contact maintainers

Thank you for contributing to make trading more accessible through AI! 🚀
