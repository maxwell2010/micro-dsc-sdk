"""
Minimal Decimal SDK

Минимальный SDK для работы с блокчейном Decimal.
Содержит только необходимые функции без лишних зависимостей.
"""

from .core import (
    get_del_balance,
    get_token_balance_by_symbol,
    send_del,
    send_token_by_symbol,
    get_private_key_from_seed
)

__version__ = "1.0.0"
__author__ = "Maxwell2019"

__all__ = [
    "get_del_balance",
    "get_token_balance_by_symbol", 
    "send_del",
    "send_token_by_symbol",
    "get_private_key_from_seed"
]
