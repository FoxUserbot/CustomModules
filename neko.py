from pyrogram import Client, filters
from command import fox_command
from requirements_installer import install_library
import os

install_library("requests -U") 

import requests

@Client.on_message(fox_command("neko", "Neko", os.path.basename(__file__)) & filters.me)
async def neko(client, message):
    await message.edit("Neko tyan..~")
    try:
        resp = requests.get("https://nekos.best/api/v2/neko")
        data = resp.json()
        url = data["results"][0]["url"]
        await client.send_photo(message.chat.id, photo=str(url),message_thread_id=message.message_thread_id)
        await message.delete()
    except Exception as f:
        await message.edit(f"Oops..~\n{f}")
