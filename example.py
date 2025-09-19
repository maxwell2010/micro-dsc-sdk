#!/usr/bin/env python3
"""
Пример использования Minimal Decimal SDK
"""

import asyncio
from minimal_sdk import (
    get_del_balance,
    get_token_balance_by_symbol,
    send_del,
    send_token_by_symbol,
    get_private_key_from_seed
)

async def main():
    """Основная функция примера"""
    print("🚀 Пример использования Minimal Decimal SDK")
    print("=" * 50)
    
    # Параметры для тестирования
    seed_phrase = "Ваша сид фраза"
    recipient = "0x40900a48273644768c09183e00e43528c17a29f6"
    
    try:
        # Получаем приватный ключ и адрес
        private_key = get_private_key_from_seed(seed_phrase)
        from eth_account import Account
        account = Account.from_key(private_key)
        sender_address = account.address
        
        print(f"📤 Адрес отправителя: {sender_address}")
        print(f"📥 Адрес получателя: {recipient}")
        
        # Проверяем баланс DEL
        print(f"\n💰 Проверка баланса DEL...")
        del_balance = await get_del_balance(sender_address)
        print(f"   Баланс DEL: {del_balance}")
        
        # Проверяем баланс токена
        print(f"\n🪙 Проверка баланса токена...")
        token_info = await get_token_balance_by_symbol("fridaycoin", sender_address)
        if token_info:
            print(f"   Токен: {token_info['symbol']}")
            print(f"   Адрес: {token_info['address']}")
            print(f"   Баланс: {token_info['balance']}")
        else:
            print(f"   Токен fridaycoin не найден")
        
        # Отправляем DEL
        print(f"\n📤 Отправка DEL...")
        del_result = await send_del(
            seed_phrase=seed_phrase,
            recipient_address=recipient,
            amount=5,
            message="Тестовое сообщение из Minimal Python SDK"
        )

        if del_result['success']:
            print(f"   ✅ DEL отправлен успешно!")
            print(f"   📋 Хеш: {del_result['tx_hash']}")
            print(f"   🔢 Блок: {del_result['block_number']}")
            print(f"   ⛽ Газ: {del_result['gas_used']}")
            print(f"   💰 Баланс после: {del_result['balance_after']} DEL")
        else:
            print(f"   ❌ Ошибка отправки DEL: {del_result['error']}")
        
        # Отправляем токен
        print(f"\n🪙 Отправка токена...")
        token_result = await send_token_by_symbol(
            seed_phrase=seed_phrase,
            token_symbol="fridaycoin",
            recipient_address=recipient,
            amount=11
        )
        
        if token_result['success']:
            print(f"   ✅ Токен отправлен успешно!")
            print(f"   📋 Хеш: {token_result['tx_hash']}")
            print(f"   🔢 Блок: {token_result['block_number']}")
            print(f"   ⛽ Газ: {token_result['gas_used']}")
            print(f"   🪙 Баланс токена после: {token_result['token_balance_after']}")
            print(f"   📝 Информация о токене: {token_result['token_info']['symbol']}")
        else:
            print(f"   ❌ Ошибка отправки токена: {token_result['error']}")
        
        print(f"\n✅ Пример завершен успешно!")
        
    except Exception as e:
        print(f"❌ Ошибка в примере: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(main())
