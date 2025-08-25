from pyrogram import Client, filters
from command import fox_command, fox_sudo, who_message
import os

@Client.on_message(fox_command("spamban", "SpamBan", os.path.basename(__file__)) & fox_sudo())
async def spamban(client, message):
    message = await who_message(client, message)
    await message.edit("Checking your account for Spamban...")
    await client.unblock_user("spambot")
    await client.send_message("spambot", "/start")
    async for iii in client.get_chat_history("spambot", limit=1):
        await message.edit(iii.text)
