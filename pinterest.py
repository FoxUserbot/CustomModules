from pyrogram import Client, filters
from modules.plugins_1system.settings.main_settings import module_list, file_list
from prefix import my_prefix

from requirements_installer import install_library
install_library("requests bs4 -U") 

import requests
from bs4 import BeautifulSoup


@Client.on_message(filters.command("pinterest", prefixes=my_prefix()) & filters.me)
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
        


module_list['Pinterest'] = f'{my_prefix()}pinterest [link]'
file_list['Pinterest'] = 'pinterest.py'
