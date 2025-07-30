from pyrogram import Client, filters
from command import fox_command
from requirements_installer import install_library
import os

install_library("requests")
import requests

@Client.on_message(fox_command("short", "ShortURL", os.path.basename(__file__), "[Reply/Link]") & filters.me)
async def shorten_link_command(client, message):
    try:
        await message.edit("Shorting...")
        if message.reply_to_message:
            link = message.reply_to_message.text
        else:
            link = message.command[1]

        full_url = link.replace("https://", "").replace("http://", "")
        response = requests.get('https://tinyurl.com/api-create.php?url=' + full_url)

        short_url = response.text
        await message.edit(f"Short URL: {short_url}")
    except Exception as error:
        await message.edit(f"Error: {error}")
