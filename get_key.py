# Module by AR34 for FoxUserBot
# Powered by EtoNeYa Project
import asyncio
from pyrogram import Client
from command import fox_command, fox_sudo, who_message , get_text
import base64
import os 

from requirements_installer import install_library

install_library('requests -U')
import requests

headers = { 
    "User-Agent": "Happ/3.9.1",
}

LANGUAGES = { 
    "en": {
        "need_link": "<emoji id='5265027299509553081'>🩷</emoji> Give me a subscription link!",
        "searching": "<emoji id='5264949504766921879'>🌐</emoji> Searching...",
        "empty_response": "<emoji id='5264980750653997092'>⚰️</emoji> Empty response from the link.",
        "fetch_decode_fail": "<emoji id='5264980750653997092'>⚰️</emoji> Failed to fetch or decode subscription.",
        "caption": "<emoji id='5267392860122006833'>📝</emoji> Here is the file",
    },
    "ru": {
        "need_link": "<emoji id='5265027299509553081'>🩷</emoji> Дай ссылку на подписку!",
        "searching": "<emoji id='5264949504766921879'>🌐</emoji> Ищу подписку...",
        "empty_response": "<emoji id='5264980750653997092'>⚰️</emoji> Пустой ответ по ссылке.",
        "fetch_decode_fail": "<emoji id='5264980750653997092'>⚰️</emoji> Не удалось получить или декодировать подписку.",
        "caption": "<emoji id='5267392860122006833'>📝</emoji> Лови файл",
    },
    "ua": {
        "need_link": "<emoji id='5265027299509553081'>🩷</emoji> Дай посилання на підписку!",
        "searching": "<emoji id='5264949504766921879'>🌐</emoji> Шукаю підписку...",
        "empty_response": "<emoji id='5264980750653997092'>⚰️</emoji> Порожня відповідь за посиланням.",
        "fetch_decode_fail": "<emoji id='5264980750653997092'>⚰️</emoji> Не вдалося отримати або декодувати підписку.",
        "caption": "<emoji id='5267392860122006833'>📝</emoji> Лови файл",
    }
}



@Client.on_message(fox_command("get_keys", "GetKeys", os.path.basename(__file__), "[link to sub]") & fox_sudo())
async def get_config(client, message):
    message = await who_message(client, message)
    args = (message.text or "").split(maxsplit=1)
    arg = args[1].strip() if len(args) > 1 else None
    if not arg:
        await message.edit(get_text("get_keys", "need_link", LANGUAGES=LANGUAGES))
        return
    await message.edit(get_text("get_keys", "searching", LANGUAGES=LANGUAGES))
    try:
        req = await asyncio.to_thread(requests.get, arg, headers=headers, timeout=30)
        req.raise_for_status()
        ans = (req.text or "").strip()
        if not ans:
            await message.edit(get_text("get_keys", "empty_response", LANGUAGES=LANGUAGES))
            return

        padded = ans + ("=" * (-len(ans) % 4))
        decoded = base64.b64decode(padded).decode("utf-8", errors="replace")
    except Exception:
        await message.edit(get_text("get_keys", "fetch_decode_fail", LANGUAGES=LANGUAGES))
        return
    file_path = 'temp/keys.txt'
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(decoded)

    await client.send_document(message.chat.id, file_path, caption=get_text("get_keys", "caption", LANGUAGES=LANGUAGES), message_thread_id=message.message_thread_id)
    try:
        os.remove(file_path)
    except OSError:
        pass
