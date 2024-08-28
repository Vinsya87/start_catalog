# import asyncio

from asgiref.sync import async_to_sync
from django.conf import settings
from telegram import Bot

# bot = Bot(token=settings.TELEGRAM_BOT_TOKEN)
system_bot = Bot(token=settings.SYSTEM_BOT_TOKEN)
system_user_id = settings.SYSTEM_USER_ID


@async_to_sync
async def system_telegram_message(message):
    bot = Bot(token=settings.SYSTEM_BOT_TOKEN)
    chat_id = settings.SYSTEM_USER_ID
    try:
        await bot.send_message(chat_id, message)
        print("Сообщение успешно отправлено в телеграм")
    except Exception as e:
        print(f"Ошибка при отправке сообщения в телеграм: {e}")
