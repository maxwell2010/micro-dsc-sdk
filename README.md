# Minimal Decimal SDK

Минимальный SDK для работы с блокчейном Decimal. Содержит только необходимые функции без лишних зависимостей.

## Установка

```bash
pip install -r requirements.txt
```

## Зависимости

- `web3>=6.0.0` - для работы с блокчейном
- `eth-account>=0.8.0` - для работы с аккаунтами
- `mnemonic>=0.20` - для работы с сид фразами

## Функции

### `get_del_balance(address: str) -> float`
Получение баланса DEL для указанного адреса.

```python
from minimal_sdk import get_del_balance

balance = await get_del_balance("0x40900a48273644768c09183e00e43528c17a29f6")
print(f"Баланс: {balance} DEL")
```

### `get_token_balance_by_symbol(symbol: str, wallet_address: str) -> Optional[Dict]`
Получение баланса токена по символу.

```python
from minimal_sdk import get_token_balance_by_symbol

token_info = await get_token_balance_by_symbol("fridaycoin", "0x40900a48273644768c09183e00e43528c17a29f6")
if token_info:
    print(f"Баланс {token_info['symbol']}: {token_info['balance']}")
    print(f"Адрес токена: {token_info['address']}")
else:
    print("Токен не найден")
```

### `send_del(seed_phrase: str, recipient_address: str, amount: float, message: str = "") -> Dict`
Отправка DEL с валидацией.

```python
from minimal_sdk import send_del

result = await send_del(
    seed_phrase="your seed phrase",
    recipient_address="0x40900a48273644768c09183e00e43528c17a29f6",
    amount=0.01,
    message="Тестовое сообщение"
)

if result['success']:
    print(f"Успешно! Хеш: {result['tx_hash']}")
    print(f"Баланс после: {result['balance_after']} DEL")
else:
    print(f"Ошибка: {result['error']}")
```

### `send_token_by_symbol(seed_phrase: str, token_symbol: str, recipient_address: str, amount: float) -> Dict`
Отправка токена по символу с валидацией.

```python
from minimal_sdk import send_token_by_symbol

result = await send_token_by_symbol(
    seed_phrase="your seed phrase",
    token_symbol="fridaycoin",
    recipient_address="0x40900a48273644768c09183e00e43528c17a29f6",
    amount=0.1
)

if result['success']:
    print(f"Успешно! Хеш: {result['tx_hash']}")
    print(f"Баланс токена после: {result['token_balance_after']}")
else:
    print(f"Ошибка: {result['error']}")
```

### `get_private_key_from_seed(seed_phrase: str, derivation_path: str = "m/44'/60'/0'/0/0") -> str`
Получение приватного ключа из сид фразы.

```python
from minimal_sdk import get_private_key_from_seed

private_key = get_private_key_from_seed("your seed phrase")
print(f"Приватный ключ: {private_key}")
```

## Полный пример

```python
import asyncio
from minimal_sdk import (
    get_del_balance,
    get_token_balance_by_symbol,
    send_del,
    send_token_by_symbol,
    get_private_key_from_seed
)

async def main():
    # Параметры
    seed_phrase = "your seed phrase"
    recipient = "0x40900a48273644768c09183e00e43528c17a29f6"
    
    # Получаем приватный ключ и адрес
    private_key = get_private_key_from_seed(seed_phrase)
    from eth_account import Account
    account = Account.from_key(private_key)
    sender_address = account.address
    
    print(f"Адрес отправителя: {sender_address}")
    
    # Проверяем баланс DEL
    del_balance = await get_del_balance(sender_address)
    print(f"Баланс DEL: {del_balance}")
    
    # Проверяем баланс токена
    token_info = await get_token_balance_by_symbol("fridaycoin", sender_address)
    if token_info:
        print(f"Баланс {token_info['symbol']}: {token_info['balance']}")
    
    # Отправляем DEL
    del_result = await send_del(seed_phrase, recipient, 0.01, "Тестовое сообщение")
    if del_result['success']:
        print(f"DEL отправлен! Хеш: {del_result['tx_hash']}")
    else:
        print(f"Ошибка отправки DEL: {del_result['error']}")
    
    # Отправляем токен
    token_result = await send_token_by_symbol(seed_phrase, "fridaycoin", recipient, 0.1)
    if token_result['success']:
        print(f"Токен отправлен! Хеш: {token_result['tx_hash']}")
    else:
        print(f"Ошибка отправки токена: {token_result['error']}")

if __name__ == "__main__":
    asyncio.run(main())
```

## Возвращаемые данные

### `send_del` и `send_token_by_symbol` возвращают:

```python
{
    'success': bool,           # Успешность операции
    'tx_hash': str or None,    # Хеш транзакции
    'error': str or None,      # Сообщение об ошибке
    'block_number': int,       # Номер блока (при успехе)
    'gas_used': int,          # Использованный газ (при успехе)
    'balance_after': float,    # Баланс после отправки (для DEL)
    'token_balance_after': float,  # Баланс токена после отправки
    'token_info': dict        # Информация о токене (для токенов)
}
```

### `get_token_balance_by_symbol` возвращает:

```python
{
    'symbol': str,        # Символ токена
    'address': str,       # Адрес контракта токена
    'decimals': int,      # Количество десятичных знаков
    'balance': float      # Баланс токена
}
```

## Особенности

- ✅ Минимальные зависимости
- ✅ Автоматическая валидация балансов
- ✅ Проверка успешности транзакций
- ✅ Поддержка сообщений для DEL
- ✅ Работа с токенами по символу
- ✅ Автоматическое управление газом
- ✅ Ожидание подтверждения транзакций

## Ограничения

- Только основные функции (балансы, отправка)
- Нет поддержки NFT
- Нет поддержки делегирования
- Нет поддержки мультисенда
- Сообщения для токенов не поддерживаются
