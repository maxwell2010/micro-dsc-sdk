# Установка Minimal Decimal SDK

## Способ 1: Копирование папки

Самый простой способ - скопировать папку `minimal_sdk` в ваш проект:

```bash
# Скопируйте папку minimal_sdk в ваш проект
cp -r minimal_sdk /path/to/your/project/
```

Затем установите зависимости:

```bash
pip install -r minimal_sdk/requirements.txt
```

## Способ 2: Установка как пакет

```bash
cd minimal_sdk
pip install -e .
```

## Способ 3: Прямая установка зависимостей

```bash
pip install web3>=6.0.0 eth-account>=0.8.0 mnemonic>=0.20
```

## Проверка установки

```python
import asyncio
from minimal_sdk import get_del_balance

async def test():
    balance = await get_del_balance("0x40900a48273644768c09183e00e43528c17a29f6")
    print(f"Баланс: {balance} DEL")

asyncio.run(test())
```

## Требования

- Python 3.7+
- web3>=6.0.0
- eth-account>=0.8.0
- mnemonic>=0.20

## Структура папки

```
minimal_sdk/
├── __init__.py          # Экспорты функций
├── core.py              # Основные функции
├── example.py           # Пример использования
├── README.md            # Документация
├── requirements.txt     # Зависимости
├── setup.py             # Установочный скрипт
└── INSTALL.md           # Инструкции по установке
```

## Использование в проекте

```python
# Импорт функций
from minimal_sdk import (
    get_del_balance,
    get_token_balance_by_symbol,
    send_del,
    send_token_by_symbol,
    get_private_key_from_seed
)

# Использование
async def main():
    balance = await get_del_balance("0x...")
    print(f"Баланс: {balance} DEL")

asyncio.run(main())
```
