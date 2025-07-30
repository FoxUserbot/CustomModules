from pyrogram import Client, filters
from command import fox_command
import os

@Client.on_message(fox_command("spamban", "SpamBan", os.path.basename(__file__)) & filters.me)
async def spamban(client, message):
    await message.edit("Checking your account for Spamban...")
    await client.unblock_user("spambot")
    await client.send_message("spambot", "/start")
    async for iii in client.get_chat_history("spambot", limit=1):
        await message.edit(iii.text)
