# Changelog
All notable changes to this project will be documented in this file.
The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).
## [Unreleased]
### Added
- Renamed project to "Adonis" - Trading MCP Server
- Comprehensive README with GitHub-ready formatting
- Professional badges and documentation structure
- Contributing guidelines and code of conduct
- MIT License
- Installation script for easy setup
- Setup verification script
### Changed
- Improved project structure and organization
- Enhanced security with proper .gitignore
- Updated documentation with detailed examples
### Removed
- All test files for clean distribution
- Sensitive log and audit files
- Hardcoded credentials from configuration
## [1.0.0] - 2025-09-09
### Added
- Initial release of Adonis - Trading MCP Server
- 12 comprehensive MCP tools for trading
- Real-time market data integration
- F&O (Futures & Options) support
- Technical indicators calculation
- Sequential thinking AI analysis
- Risk management system
- Order placement and monitoring
- Portfolio tracking capabilities
- Comprehensive error handling
- Environment-based configuration
- Daily access token generation
### Features
- **Market Data Tools**
- `get_market_data` - Real-time and historical data
- `get_fno_data` - Futures and Options data
- `get_options_chain` - Complete options chain
- `calculate_technical_indicators` - Technical analysis
- **Trading Tools**
- `place_order` - Buy/Sell order placement
- `monitor_orders` - Order status tracking
- `set_stop_loss` - Risk management orders
- `monitor_stop_orders` - Stop order monitoring
- **Portfolio Tools**
- `get_positions` - Current positions
- `get_margins` - Account margins
- `get_risk_status` - Risk management status
### Technical
- Python 3.8+ compatibility
- MCP (Model Context Protocol) compliant
- Zerodha Kite Connect API integration
- Virtual environment support
- Comprehensive logging
- Error handling and recovery
### Security
- Environment variable configuration
- Credential isolation
- Git ignore for sensitive files
- Sandbox mode support
- Daily token refresh
## [0.1.0] - Development
### Added
- Initial project structure
- Basic MCP server implementation
- Zerodha API integration
- Core trading functions
---
## Release Notes
### Version 1.0.0 Highlights
This is the first production-ready release of Adonis - Trading MCP Server. Key highlights include:
**Production Ready**: Fully tested and operational with comprehensive error handling
**Complete Trading Suite**: 12 MCP tools covering all aspects of trading
**AI Integration**: Sequential thinking capabilities for market analysis
**Risk Management**: Built-in safety controls and position limits
**Secure**: Professional credential management and security practices
### Breaking Changes
- None (initial release)
### Migration Guide
- Not applicable (initial release)
### Known Issues
- Access tokens need daily regeneration (Zerodha limitation)
- Real-time data requires active market hours
- F&O data availability depends on market sessions
### Upgrade Instructions
- Not applicable (initial release)
### Contributors
- Initial development and architecture
- MCP protocol implementation
- Trading logic and risk management
- Documentation and examples
---
For more details about any release, please check the [GitHub releases page](https://github.com/yourusername/adonis-trading-mcp/releases).
