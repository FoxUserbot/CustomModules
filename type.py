import asyncio
from pyrogram import Client, filters
from command import fox_command
import os

@Client.on_message(fox_command("type", "Type", os.path.basename(__file__), "[text]") & filters.me)
async def types(client, message):
    try:
        orig_text = ' '.join(message.text.split()[1:])
        text = orig_text
        tbp = ""
        typing_symbol = "▒"
        while tbp != orig_text:
            await message.edit(str(tbp + typing_symbol))
            await asyncio.sleep(0.10)
            tbp = tbp + text[0]
            text = text[1:]
            await message.edit(str(tbp))
            await asyncio.sleep(0.10)
    except IndexError:
        message.edit('No text here!')
