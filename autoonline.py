import asyncio
from pyrogram import Client, filters
from modules.plugins_1system.restarter import restart
from command import fox_command
import os

@Client.on_message(fox_command("online", "AutoOnline", os.path.basename(__file__)) & filters.me)
async def online_now(client, message):
    await message.edit("AutoOnline activated")
    while True:
        iii = await client.send_message("me", "bruh")
        await client.delete_messages("me", iii.id)
        await asyncio.sleep(45)

@Client.on_message(fox_command("offline", "AutoOnline", os.path.basename(__file__)) & filters.me)
async def offline_now(client, message):
    await message.edit("AutoOnline deactivated")
