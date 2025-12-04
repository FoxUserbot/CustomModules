# Original: https://raw.githubusercontent.com/KOTmodules/FREEmodules/main/KOTaiwaifu.py
# Ported with Wine_Hikka
import asyncio
import os
import random
from urllib.parse import quote_plus

from requirements_installer import install_library
install_library("requests -U")
import requests
from pyrogram.errors import WebpageCurlFailed
from pyrogram import Client
from command import fox_command, fox_sudo, who_message, get_text

phrases = ["Kawaii!", "Daisuki!", "Sugoi!", "Hai!", "Arigato!", "Moe!", "Yoroshiku!", "Oishii!"]
categories = ["maid", "waifu", "marin-kitagawa", "mori-calliope", "raiden-shogun", "oppai", "selfies", "uniform", "kamisato-ayaka", "neko"]
list_categories = ", ".join([f"<code>{s}</code>" for s in categories])
LANGUAGES = {
    "en": {
        "no_image": "No image found.",
        "categories": f"Available categories: {list_categories}",
    },
    "ru": {
        "no_image": "Изображение не найдено.",
        "phrases": f"Доступные категории: {list_categories}"
    },
    "ua": {
        "no_image": "Зображення не знайдено.",
         "categories": f"Доступні категорії: {list_categories}",
    }
}

async def get_image_url(api_url: str) -> str | None:
    try:
        response = await asyncio.to_thread(requests.get, api_url)
        response.raise_for_status()
        data = response.json()
        if "url" in data:
            return data["url"]
        elif "images" in data and data["images"]:
            return data["images"][0]["url"]
        elif "results" in data and data["results"]:
            return data["results"][0]["url"]
        return None
    except:
        return None


@Client.on_message(fox_command("waf", "KOTaiwaifu", os.path.basename(__file__), "[category]") & fox_sudo())
async def wafcmd(client: Client, message):
    message = await who_message(client, message)
    args = message.text.split(maxsplit=1)
    if len(args) > 1:
        arg = args[1].strip().lower()
    else:
        text = get_text("KOTaiwaifu", "phrases", LANGUAGES=LANGUAGES)
        await message.edit(text)
        return

    arg = "waifu" if arg not in categories else arg
    image_url = await get_image_url(f"https://api.waifu.im/search?included_tags={quote_plus(arg)}")
    if not image_url:
        text = get_text("KOTaiwaifu", "no_image", LANGUAGES=LANGUAGES)
        await message.edit(text)
        return
    caption = f"<i>{random.choice(phrases)}</i> (¬‿¬)"
    try:
        await client.send_photo(
        message.chat.id,
        image_url,
        caption=caption,
        message_thread_id=message.message_thread_id
    )
    except WebpageCurlFailed:
        path = f'temp/{random.randint(1,1000)}.png'
        with open(path,"rb+") as file:
            file.write(requests.get(image_url).text)
        await client.send_photo(
        message.chat.id,
        path,
        caption=caption,
        message_thread_id=message.message_thread_id)
        os.remove(path)
    await message.delete()
