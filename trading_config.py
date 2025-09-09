#!/usr/bin/env python3
"""
Trading Configuration and Risk Management System
Production-ready settings for live trading with safety controls
"""

import os
from datetime import time, datetime
from dataclasses import dataclass, field
from typing import Dict, List, Optional
from dotenv import load_dotenv

load_dotenv('config.env')

@dataclass
class RiskLimits:
    """Risk management limits for safe trading"""
    # Daily limits
    max_daily_loss: float = 10000.0  # Maximum daily loss in INR
    max_daily_trades: int = 50  # Maximum trades per day
    max_position_value: float = 100000.0  # Maximum single position value
    
    # Position limits
    max_equity_positions: int = 10
    max_fno_positions: int = 5
    max_options_positions: int = 8
    
    # Order limits
    max_order_value: float = 50000.0  # Maximum single order value
    max_quantity_multiplier: float = 5.0  # Max quantity as multiple of average volume
    
    # Time-based limits
    max_orders_per_minute: int = 10
    cooldown_between_orders: int = 2  # seconds
    
    # Margin requirements
    min_margin_buffer: float = 0.2  # Keep 20% margin buffer
    max_leverage: float = 5.0  # Maximum leverage allowed

@dataclass
class MarketHours:
    """Market timing configuration"""
    # Regular market hours (IST)
    market_open: time = time(9, 15)  # 9:15 AM
    market_close: time = time(15, 30)  # 3:30 PM
    
    # Pre-market and post-market
    pre_market_start: time = time(9, 0)   # 9:00 AM
    pre_market_end: time = time(9, 15)    # 9:15 AM
    post_market_start: time = time(15, 40)  # 3:40 PM
    post_market_end: time = time(16, 0)   # 4:00 PM
    
    # Trading allowed periods
    allow_pre_market: bool = False
    allow_post_market: bool = False
    allow_extended_hours: bool = False

@dataclass 
class TradingConfig:
    """Complete trading configuration"""
    # Environment
    environment: str = field(default_factory=lambda: os.getenv('TRADING_ENV', 'sandbox'))
    
    # API Configuration
    api_key: str = field(default_factory=lambda: os.getenv('KITE_API_KEY', ''))
    api_secret: str = field(default_factory=lambda: os.getenv('KITE_API_SECRET', ''))
    access_token: str = field(default_factory=lambda: os.getenv('KITE_ACCESS_TOKEN', ''))
    
    # Risk Management
    risk_limits: RiskLimits = field(default_factory=RiskLimits)
    market_hours: MarketHours = field(default_factory=MarketHours)
    
    # Logging
    log_level: str = 'INFO'
    log_file: str = 'trading.log'
    enable_trade_logging: bool = True
    
    # Safety features
    enable_risk_checks: bool = True
    enable_market_hours_check: bool = True
    enable_circuit_breaker: bool = True
    dry_run_mode: bool = False  # If True, no actual orders placed
    
    # Performance monitoring
    enable_pnl_tracking: bool = True
    enable_analytics: bool = True
    
    def validate(self) -> List[str]:
        """Validate configuration and return any errors"""
        errors = []
        
        if not self.api_key:
            errors.append("KITE_API_KEY not configured")
        if not self.api_secret:
            errors.append("KITE_API_SECRET not configured") 
        if not self.access_token:
            errors.append("KITE_ACCESS_TOKEN not configured")
            
        if self.risk_limits.max_daily_loss <= 0:
            errors.append("max_daily_loss must be positive")
        if self.risk_limits.max_position_value <= 0:
            errors.append("max_position_value must be positive")
            
        return errors
    
    def is_market_open(self, current_time: Optional[datetime] = None) -> bool:
        """Check if market is currently open for trading"""
        if not self.enable_market_hours_check:
            return True
            
        if current_time is None:
            current_time = datetime.now()
            
        current_time_only = current_time.time()
        
        # Check regular market hours
        if self.market_hours.market_open <= current_time_only <= self.market_hours.market_close:
            return True
            
        # Check extended hours if enabled
        if self.market_hours.allow_pre_market:
            if self.market_hours.pre_market_start <= current_time_only < self.market_hours.market_open:
                return True
                
        if self.market_hours.allow_post_market:
            if self.market_hours.post_market_start <= current_time_only <= self.market_hours.post_market_end:
                return True
                
        return False

# Global configuration instance
config = TradingConfig()

# Validate configuration on import
config_errors = config.validate()
if config_errors:
    print("⚠️ Configuration errors found:")
    for error in config_errors:
        print(f"  - {error}")
else:
    print(f"✅ Trading configuration loaded - Environment: {config.environment}")
