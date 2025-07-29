import asyncio
import random

from pyrogram import Client, filters
from modules.plugins_1system.settings.main_settings import module_list, file_list
from prefix import my_prefix
from modules.plugins_1system.restarter import restart 

def load_config():
    try:
        with open("userdata/nekoeditor_enabled", "r", encoding="utf-8") as f:
            enabled = f.read().strip().lower() == "true"
    except FileNotFoundError:
        enabled = False
    return {"enabled": enabled}

def save_config(enabled):
    with open("userdata/nekoeditor_enabled", "w", encoding="utf-8") as f:
        f.write(str(enabled))

@Client.on_message(filters.command("nekoed", prefixes=my_prefix()) & filters.me)
async def nekoedcmd(client, message):
    args = message.text.split(maxsplit=1)
    arg = args[1].lower() if len(args) > 1 else ""
    me = await client.get_me()
    is_premium = getattr(me, "is_premium", False)
    config = load_config()
    status = config["enabled"]

    if not arg:
        current_status = "включён" if status else "выключен"
        return await message.edit(f"🐱 NekoEditor: {current_status}")

    if arg in ["on", "вкл", "1"]:
        save_config(True)
        if is_premium:
            await message.edit('<emoji id=5335044582218412321>☺️</emoji> Режим включён! Nya~')
        else:
            await message.edit("🐾 Режим включён! Nya~")
    elif arg in ["off", "выкл", "0"]:
        save_config(False)
        if is_premium:
            await message.edit('<emoji id=5377309873614627829>👌</emoji> Режим выключен... >_<')
        else:
            await message.edit("🌀 Режим выключен... >_<")
    else:
        return await message.edit("🚫 Неверный аргумент. Используйте: <code>nekoed [on/off]</code>")
    
    await restart(message, restart_type="restart")

@Client.on_message(
    filters.outgoing 
    & ~filters.forwarded 
    & filters.text 
    & ~filters.media 
    & filters.me
    & ~filters.command("", prefixes=my_prefix())  # Игнорировать команды с префиксом
)
async def watcher(client, message):
    config = load_config()
    if not config["enabled"] or "nekoed" in message.text.lower():
        return

    modified_text = message.text
    replacements = {
        "р": "w",
        "л": "w",
        "но": "ня",
        "на": "ня"
    }
    for old, new in replacements.items():
        modified_text = modified_text.replace(old, new)

    neko_words = ["Nya~", "UwU", "OwO", ".>_<.", "^^", "(≧▽≦)"]
    neko_word = random.choice(neko_words)
    if random.random() < 0.5:
        modified_text = f"{neko_word} {modified_text}"
    else:
        modified_text = f"{modified_text} {neko_word}"

    try:
        await message.edit(modified_text)
    except Exception:
        pass


module_list['NekoEditor'] = f'{my_prefix()}nekoed [on/off]'
file_list['NekoEditor'] = 'nekomod.py'