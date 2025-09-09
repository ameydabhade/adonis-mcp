"""
Risk Management System for Production Trading
Validates orders, monitors positions, and enforces safety limits
"""

import time
import json
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
import logging

from trading_config import config

logging.basicConfig(
    level=getattr(logging, config.log_level),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(config.log_file),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

@dataclass
class TradeRecord:
    """Record of a trade for tracking and analytics"""
    timestamp: datetime
    order_id: str
    symbol: str
    transaction_type: str  # BUY/SELL
    quantity: int
    price: float
    order_type: str
    status: str
    pnl: float = 0.0
    strategy: str = "unknown"

@dataclass
class PositionInfo:
    """Current position information"""
    symbol: str
    quantity: int
    average_price: float
    current_price: float
    pnl: float
    instrument_type: str  # EQUITY, FUT, CE, PE

class RiskManager:
    """Production-grade risk management system"""
    
    def __init__(self):
        self.daily_pnl = 0.0
        self.daily_trades = 0
        self.order_timestamps = []  # For rate limiting
        self.positions: Dict[str, PositionInfo] = {}
        self.trade_history: List[TradeRecord] = []
        self.circuit_breaker_triggered = False
        self.last_order_time = 0
        
        logger.info("Risk Manager initialized with production safety controls")
    
    def validate_order(self, order_params: Dict) -> Tuple[bool, str]:
        """Comprehensive order validation before execution"""
        
        if config.dry_run_mode:
            logger.info("DRY RUN MODE: Order validation only, no execution")
        
        if not self._check_market_hours():
            return False, "Market is closed for trading"
        
        if self.circuit_breaker_triggered:
            return False, "Circuit breaker active - trading suspended"
        
        if not self._check_daily_limits():
            return False, "Daily trading limits exceeded"
        
        if not self._check_rate_limits():
            return False, "Order rate limit exceeded"
        
        if not self._validate_position_size(order_params):
            return False, "Position size exceeds risk limits"
        
        if not self._validate_order_value(order_params):
            return False, "Order value exceeds maximum allowed"
        
        if order_params.get('exchange') == 'NFO':
            if not self._validate_fno_order(order_params):
                return False, "F&O order validation failed"
        
        current_time = time.time()
        if current_time - self.last_order_time < config.risk_limits.cooldown_between_orders:
            return False, f"Cooldown period active, wait {config.risk_limits.cooldown_between_orders} seconds"
        
        logger.info(f"Order validation passed for {order_params.get('tradingsymbol')}")
        return True, "Order validation successful"
    
    def record_order(self, order_params: Dict, order_id: str, status: str) -> None:
        """Record order for tracking and analytics"""
        trade = TradeRecord(
            timestamp=datetime.now(),
            order_id=order_id,
            symbol=order_params.get('tradingsymbol', ''),
            transaction_type=order_params.get('transaction_type', ''),
            quantity=order_params.get('quantity', 0),
            price=order_params.get('price', 0),
            order_type=order_params.get('order_type', ''),
            status=status
        )
        
        self.trade_history.append(trade)
        self.daily_trades += 1
        self.last_order_time = time.time()
        
        self.order_timestamps.append(time.time())
        
        logger.info(f"Trade recorded: {trade.symbol} {trade.transaction_type} {trade.quantity} @ {trade.price}")
        
        if config.enable_trade_logging:
            self._save_trade_log(trade)
    
    def update_pnl(self, pnl_change: float) -> None:
        """Update daily PnL and check risk limits"""
        self.daily_pnl += pnl_change
        
        if self.daily_pnl <= -config.risk_limits.max_daily_loss:
            self.trigger_circuit_breaker("Daily loss limit exceeded")
        
        logger.info(f"Daily PnL updated: ₹{self.daily_pnl:.2f}")
    
    def trigger_circuit_breaker(self, reason: str) -> None:
        """Trigger emergency trading halt"""
        self.circuit_breaker_triggered = True
        logger.critical(f"🚨 CIRCUIT BREAKER TRIGGERED: {reason}")
        logger.critical("All trading suspended until manual reset")
        
        with open("emergency_log.txt", "a") as f:
            f.write(f"{datetime.now()}: CIRCUIT BREAKER - {reason}\n")
    
    def reset_circuit_breaker(self) -> bool:
        """Reset circuit breaker (manual intervention required)"""
        if self.circuit_breaker_triggered:
            self.circuit_breaker_triggered = False
            logger.warning("Circuit breaker reset - trading resumed")
            return True
        return False
    
    def get_risk_status(self) -> Dict:
        """Get current risk status and metrics"""
        return {
            "daily_pnl": self.daily_pnl,
            "daily_trades": self.daily_trades,
            "circuit_breaker_active": self.circuit_breaker_triggered,
            "positions_count": len(self.positions),
            "market_open": config.is_market_open(),
            "daily_loss_limit": config.risk_limits.max_daily_loss,
            "daily_trade_limit": config.risk_limits.max_daily_trades,
            "remaining_loss_buffer": config.risk_limits.max_daily_loss + self.daily_pnl,
            "remaining_trade_buffer": config.risk_limits.max_daily_trades - self.daily_trades
        }
    
    def _check_market_hours(self) -> bool:
        """Check if market is open for trading"""
        return config.is_market_open()
    
    def _check_daily_limits(self) -> bool:
        """Check daily trading limits"""
        if self.daily_trades >= config.risk_limits.max_daily_trades:
            logger.warning("Daily trade limit reached")
            return False
        
        if self.daily_pnl <= -config.risk_limits.max_daily_loss:
            logger.warning("Daily loss limit reached")
            return False
        
        return True
    
    def _check_rate_limits(self) -> bool:
        """Check order rate limiting"""
        current_time = time.time()
        self.order_timestamps = [ts for ts in self.order_timestamps if current_time - ts < 60]
        
        if len(self.order_timestamps) >= config.risk_limits.max_orders_per_minute:
            logger.warning("Order rate limit exceeded")
            return False
        
        return True
    
    def _validate_position_size(self, order_params: Dict) -> bool:
        """Validate position size against risk limits"""
        quantity = order_params.get('quantity', 0)
        price = order_params.get('price', 0)
        
        if price == 0:  # Market order, estimate with some buffer
            price = 1000  # Conservative estimate
        
        order_value = quantity * price
        
        if order_value > config.risk_limits.max_order_value:
            logger.warning(f"Order value ₹{order_value} exceeds limit ₹{config.risk_limits.max_order_value}")
            return False
        
        return True
    
    def _validate_order_value(self, order_params: Dict) -> bool:
        """Validate total order value"""
        quantity = order_params.get('quantity', 0)
        price = order_params.get('price', 0)
        
        if quantity <= 0:
            return False
        
        if price < 0:
            return False
        
        return True
    
    def _validate_fno_order(self, order_params: Dict) -> bool:
        """Additional validations for F&O orders"""
        symbol = order_params.get('tradingsymbol', '')
        
        if not any(x in symbol for x in ['FUT', 'CE', 'PE']):
            logger.warning(f"Invalid F&O symbol format: {symbol}")
            return False
        
        quantity = order_params.get('quantity', 0)
        if quantity > 1000:  # Conservative limit for F&O
            logger.warning(f"F&O quantity {quantity} seems too high")
            return False
        
        return True
    
    def _save_trade_log(self, trade: TradeRecord) -> None:
        """Save trade to audit log file"""
        try:
            log_entry = {
                "timestamp": trade.timestamp.isoformat(),
                "order_id": trade.order_id,
                "symbol": trade.symbol,
                "type": trade.transaction_type,
                "quantity": trade.quantity,
                "price": trade.price,
                "status": trade.status
            }
            
            with open("trades_audit.jsonl", "a") as f:
                f.write(json.dumps(log_entry) + "\n")
                
        except Exception as e:
            logger.error(f"Failed to save trade log: {e}")

risk_manager = RiskManager()
