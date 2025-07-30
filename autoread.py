import re
from pyrogram import Client, filters
from command import fox_command
import os

the_regex = r"^r\/([^\s\/])+"
i = filters.chat([])

@Client.on_message(i)
async def auto_read(client, message):
    await client.read_history(message.chat.id)
    message.continue_propagation()

@Client.on_message(fox_command("autoread", "AutoReadChat", os.path.basename(__file__)) & filters.me)
async def add_to_auto_read(client, message):
    if message.chat.id in i:
        i.remove(message.chat.id)
        await message.edit("Autoread deactivated")
    else:
        i.add(message.chat.id)
        await message.edit("Autoread activated")


