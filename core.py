"""
Основные функции минимального SDK
"""

import asyncio
from typing import Dict, Optional, Tuple
from web3 import Web3
from eth_account import Account
from mnemonic import Mnemonic

# Константы для Decimal Chain
RPC_URLS = [
    "https://node.decimalchain.com/web3",
    "http://94.130.66.14/web3/",
    "http://168.119.212.76/web3/",
]
DECIMAL_RPC_URL = "http://94.130.66.14/web3/"
DECIMAL_CHAIN_ID = 75

# Минимальный ABI для ERC-20 токенов
MINIMAL_ERC20_ABI = [
    {
        "constant": True,
        "inputs": [],
        "name": "decimals",
        "outputs": [{"name": "", "type": "uint8"}],
        "type": "function"
    },
    {
        "constant": True,
        "inputs": [{"name": "_owner", "type": "address"}],
        "name": "balanceOf",
        "outputs": [{"name": "balance", "type": "uint256"}],
        "type": "function"
    },
    {
        "constant": False,
        "inputs": [
            {"name": "_to", "type": "address"},
            {"name": "_value", "type": "uint256"}
        ],
        "name": "transfer",
        "outputs": [{"name": "", "type": "bool"}],
        "type": "function"
    }
]

# ABI для Token Center (получение информации о токенах)
TOKEN_CENTER_ABI = [
    {
        "constant": True,
        "inputs": [{"name": "symbol", "type": "string"}],
        "name": "tokens",
        "outputs": [{"name": "", "type": "address"}],
        "type": "function"
    }
]

# Адреса контрактов Decimal
TOKEN_CENTER_ADDRESS = "0x9113ba675aa8f2ef0c068cee2cdabab95b6437fb"

class MinimalDecimalClient:
    """Минимальный клиент для работы с Decimal Chain"""
    
    def __init__(self, rpc_url: str = DECIMAL_RPC_URL):
        self.w3 = Web3(Web3.HTTPProvider(rpc_url))
        if not self.w3.is_connected():
            raise Exception("Не удалось подключиться к Decimal Chain")
    
    async def get_del_balance(self, address: str) -> float:
        """Получение баланса DEL"""
        try:
            balance_wei = self.w3.eth.get_balance(Web3.to_checksum_address(address))
            return float(Web3.from_wei(balance_wei, 'ether'))
        except Exception as e:
            raise Exception(f"Ошибка получения баланса DEL: {e}")
    
    async def get_token_info(self, symbol: str) -> Optional[Dict]:
        """Получение информации о токене по символу"""
        try:
            token_center = self.w3.eth.contract(
                address=Web3.to_checksum_address(TOKEN_CENTER_ADDRESS),
                abi=TOKEN_CENTER_ABI
            )
            
            # Вызываем функцию tokens (как в основном SDK)
            token_address = token_center.functions.tokens(symbol).call()
            if token_address == "0x0000000000000000000000000000000000000000":
                return None
            
            # Получаем информацию о токене
            token_contract = self.w3.eth.contract(
                address=Web3.to_checksum_address(token_address),
                abi=MINIMAL_ERC20_ABI
            )
            decimals = token_contract.functions.decimals().call()
            
            return {
                'address': token_address,
                'symbol': symbol,
                'decimals': decimals
            }
        except Exception as e:
            print(f"Ошибка получения информации о токене {symbol}: {e}")
            return None
    
    async def get_token_balance(self, token_address: str, wallet_address: str) -> float:
        """Получение баланса токена"""
        try:
            contract = self.w3.eth.contract(
                address=Web3.to_checksum_address(token_address),
                abi=MINIMAL_ERC20_ABI
            )
            
            decimals = contract.functions.decimals().call()
            balance_wei = contract.functions.balanceOf(
                Web3.to_checksum_address(wallet_address)
            ).call()
            
            return float(balance_wei) / (10 ** decimals)
        except Exception as e:
            raise Exception(f"Ошибка получения баланса токена: {e}")
    
    async def send_del_transaction(self, to_address: str, amount: float, private_key: str, message: str = "") -> Dict:
        """Отправка DEL"""
        try:
            account = Account.from_key(private_key)
            sender_address = account.address
            
            # Проверяем баланс
            balance = await self.get_del_balance(sender_address)
            if balance < amount:
                return {
                    'success': False,
                    'error': f'Недостаточно средств. Нужно: {amount} DEL, есть: {balance} DEL'
                }
            
            # Создаем транзакцию
            tx_params = {
                'from': sender_address,
                'to': Web3.to_checksum_address(to_address),
                'value': Web3.to_wei(amount, 'ether'),
                'gas': 21000,
                'gasPrice': self.w3.eth.gas_price,
                'nonce': self.w3.eth.get_transaction_count(sender_address),
                'chainId': DECIMAL_CHAIN_ID
            }
            
            # Добавляем сообщение в data если есть
            if message:
                tx_params['data'] = Web3.to_hex(text=message)
                tx_params['gas'] = 25000  # Больше газа для сообщения
            
            # Подписываем и отправляем
            signed_tx = self.w3.eth.account.sign_transaction(tx_params, private_key)
            tx_hash = self.w3.eth.send_raw_transaction(signed_tx.raw_transaction)
            
            # Ждем подтверждения
            receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash, timeout=60)
            
            if receipt.status == 1:
                return {
                    'success': True,
                    'tx_hash': tx_hash.hex(),
                    'block_number': receipt.blockNumber,
                    'gas_used': receipt.gasUsed
                }
            else:
                return {
                    'success': False,
                    'error': 'Транзакция не подтверждена'
                }
                
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    async def send_token_transaction(self, token_address: str, to_address: str, amount: float, private_key: str) -> Dict:
        """Отправка токена"""
        try:
            account = Account.from_key(private_key)
            sender_address = account.address
            
            # Получаем информацию о токене
            contract = self.w3.eth.contract(
                address=Web3.to_checksum_address(token_address),
                abi=MINIMAL_ERC20_ABI
            )
            
            decimals = contract.functions.decimals().call()
            amount_wei = int(amount * (10 ** decimals))
            
            # Проверяем баланс токена
            balance_wei = contract.functions.balanceOf(sender_address).call()
            if balance_wei < amount_wei:
                return {
                    'success': False,
                    'error': f'Недостаточно токенов. Нужно: {amount}, есть: {balance_wei / (10 ** decimals)}'
                }
            
            # Создаем транзакцию
            transfer_func = contract.functions.transfer(
                Web3.to_checksum_address(to_address),
                amount_wei
            )
            
            tx_params = {
                'from': sender_address,
                'to': Web3.to_checksum_address(token_address),
                'value': 0,
                'gas': 100000,
                'gasPrice': self.w3.eth.gas_price,
                'nonce': self.w3.eth.get_transaction_count(sender_address),
                'chainId': DECIMAL_CHAIN_ID,
                'data': transfer_func.build_transaction({'gas': 0, 'gasPrice': 0})['data']
            }
            
            # Подписываем и отправляем
            signed_tx = self.w3.eth.account.sign_transaction(tx_params, private_key)
            tx_hash = self.w3.eth.send_raw_transaction(signed_tx.raw_transaction)
            
            # Ждем подтверждения
            receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash, timeout=60)
            
            if receipt.status == 1:
                return {
                    'success': True,
                    'tx_hash': tx_hash.hex(),
                    'block_number': receipt.blockNumber,
                    'gas_used': receipt.gasUsed
                }
            else:
                return {
                    'success': False,
                    'error': 'Транзакция не подтверждена'
                }
                
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }

# Глобальный клиент
_client = None

def get_client() -> MinimalDecimalClient:
    """Получение глобального клиента"""
    global _client
    if _client is None:
        _client = MinimalDecimalClient()
    return _client

# Основные функции для экспорта

async def get_del_balance(address: str) -> float:
    """Получение баланса DEL"""
    client = get_client()
    return await client.get_del_balance(address)

async def get_token_balance_by_symbol(symbol: str, wallet_address: str) -> Optional[Dict]:
    """Получение баланса токена по символу"""
    client = get_client()
    
    # Получаем информацию о токене
    token_info = await client.get_token_info(symbol)
    if not token_info:
        return None
    
    # Получаем баланс
    balance = await client.get_token_balance(token_info['address'], wallet_address)
    
    return {
        'symbol': token_info['symbol'],
        'address': token_info['address'],
        'decimals': token_info['decimals'],
        'balance': balance
    }

async def send_del(seed_phrase: str, recipient_address: str, amount: float, message: str = "") -> Dict:
    """Отправка DEL с валидацией"""
    client = get_client()
    
    # Получаем приватный ключ
    private_key = get_private_key_from_seed(seed_phrase)
    
    # Отправляем
    result = await client.send_del_transaction(recipient_address, amount, private_key, message)
    
    if result['success']:
        # Проверяем баланс после отправки
        account = Account.from_key(private_key)
        balance_after = await client.get_del_balance(account.address)
        result['balance_after'] = balance_after
    
    return result

async def send_token_by_symbol(seed_phrase: str, token_symbol: str, recipient_address: str, amount: float) -> Dict:
    """Отправка токена по символу с валидацией"""
    client = get_client()
    
    # Получаем информацию о токене
    token_info = await client.get_token_info(token_symbol)
    if not token_info:
        return {
            'success': False,
            'error': f'Токен {token_symbol} не найден'
        }
    
    # Получаем приватный ключ
    private_key = get_private_key_from_seed(seed_phrase)
    
    # Отправляем
    result = await client.send_token_transaction(
        token_info['address'], 
        recipient_address, 
        amount, 
        private_key
    )
    
    if result['success']:
        # Проверяем баланс после отправки
        account = Account.from_key(private_key)
        balance_after = await client.get_token_balance(token_info['address'], account.address)
        result['token_balance_after'] = balance_after
        result['token_info'] = token_info
    
    return result

def get_private_key_from_seed(seed_phrase: str, derivation_path: str = "m/44'/60'/0'/0/0") -> str:
    """Получение приватного ключа из сид фразы"""
    try:
        # Включаем нестабильные функции HD wallet
        Account.enable_unaudited_hdwallet_features()
        
        mnemo = Mnemonic("english")
        if not mnemo.check(seed_phrase):
            raise Exception("Неверная сид фраза")
        
        account = Account.from_mnemonic(seed_phrase, account_path=derivation_path)
        return account.key.hex()
    except Exception as e:
        raise Exception(f"Ошибка получения приватного ключа: {e}")
