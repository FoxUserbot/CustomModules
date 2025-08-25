import asyncio
from pyrogram import Client, filters
from command import fox_command, fox_sudo, who_message
import os

bot_tag = "thojkrpthrptbot"

@Client.on_message(fox_command("eye", "EyeGod", os.path.basename(__file__), "[phone]") & fox_sudo())
async def spamban(client, message):
    message = await who_message(client, message)
    number = message.command[1]
    await message.edit(f"⏳ | Проверяем аккаунт {number} на наличие данных. Это может занять некоторое время...")
    await client.unblock_user(bot_tag)
    await client.send_message(bot_tag, number)
    await asyncio.sleep(20)
    await message.edit("Вот что удалось найти:")
    async for iii in client.get_chat_history(bot_tag, limit=1):
        await client.forward_messages(message.chat.id, bot_tag, iii.id)
