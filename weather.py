from pyrogram import Client, filters
from command import fox_command, fox_sudo, who_message
from requirements_installer import install_library
import os

install_library("requests") 
import requests

def get_pic(city):
    city = city.lower()
    file_name = f"{city}.png"
    with open(file_name, "wb") as pic:
        response = requests.get(f"http://wttr.in/{city}_2&lang=en.png", stream=True)
        if not response.ok:
            print(response)
        for block in response.iter_content(1024):
            if not block:
                break
            pic.write(block)
        return file_name

@Client.on_message(fox_command("weather", "Weather", os.path.basename(__file__), "[city]") & fox_sudo())
async def weather(client, message):
    message = await who_message(client, message)
    try:
        city = message.command[1]
        await message.edit("Check weather...")
        r = requests.get(f"https://wttr.in/{city}?m?M?0?q?T&lang=en")
        await message.edit(f"🗺 You sity/village: {city}\n{r.text}")
        await client.send_photo(
        chat_id=message.chat.id,
        photo=get_pic(city),
        reply_to_message_id=message.id)
        os.remove(f"{city}.png")
    except Exception as e:
        await message.edit(f"Error | {e}")
