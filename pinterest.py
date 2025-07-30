from pyrogram import Client, filters
from command import fox_command
from requirements_installer import install_library
import os

install_library("requests bs4 -U") 

import requests
from bs4 import BeautifulSoup

@Client.on_message(fox_command("pinterest", "Pinterest", os.path.basename(__file__), "[link]") & filters.me)
async def pinterest(client, message):
    await message.edit("<emoji id='5397755618750653196'>🌟</emoji> Searching..")
    link = message.command[1]
    try:
        resp = requests.get(link)
        soup = BeautifulSoup(resp.text, "html.parser")
        pic = soup.find_all("img")
        print(f"DEBUG: {pic}")
        link = pic[0].get('src')
        print(f"DEBUG: {link}")
        await client.send_photo(message.chat.id, photo=link,caption=f"<emoji id='5397755618750653196'>🌟</emoji> <b>Your Link:</b>\n{link}",message_thread_id=message.message_thread_id)
        await message.delete()
    except Exception as f:
        await message.edit(f"<emoji id='5397755618750653196'>🌟</emoji> **Error:** {f}")
