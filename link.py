from pyrogram import Client, filters
from command import fox_command
import os

@Client.on_message(fox_command("link", "LinkInText", os.path.basename(__file__), "[url] [text]") & filters.me)
async def link(client, message):
    try:
        link = message.command[1]
        text = " ".join(message.command[2:])
        await message.delete()
        await client.send_message(message.chat.id, f'<a href="{link}">{text}</a>', disable_web_page_preview=True)
    except IndexError:
        message.edit('No text here!')
