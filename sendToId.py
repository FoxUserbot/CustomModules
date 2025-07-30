from pyrogram import Client, filters
from command import fox_command
import os

@Client.on_message(fox_command("send", "SendToId", os.path.basename(__file__), "[ID/Username]") & filters.me)
async def sendtoid(client, message):
    try:
        await client.unblock_user(message.command[1])
        await client.send_message(message.command[1], "Hi")
        await message.edit(f"Message send to {message.command[1]}")
    except:
        await message.edit("I can't send message!")
