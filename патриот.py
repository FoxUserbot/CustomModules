import asyncio
from pyrogram import Client, filters
from modules.plugins_1system.settings.main_settings import module_list, file_list
from prefix import my_prefix

translate_map = {
    ord("з"): "Z",
    ord("З"): "Z",
    ord("z"): "Z",
    ord("о"): "O",
    ord("o"): "О",
    ord("в"): "V",
    ord("В"): "V",
    ord("v"): "V"
}

patriot_enabled = False

@Client.on_message(filters.command("patriot", prefixes=my_prefix()) & filters.me)
async def patriotcmd(client, message):
    global patriot_enabled
    patriot_enabled = not patriot_enabled
    
    if patriot_enabled:
        return await message.edit("<b>🇷🇺 Патриот успешно включен. Страна может спать спокойно</b>")
    else:
        return await message.edit("❌ <b>Патриот выключен</b>")

@Client.on_message(filters.command("pat", prefixes=my_prefix()) & filters.me)
async def patcmd(client, message):
    reply = message.reply_to_message
    if not reply:
        return await message.edit("<b>Ответьте на сообщение с помощью </b><code>pat</code>")
    
    translated_text = reply.text.translate(translate_map)
    await message.edit(f"🇷🇺 <b>Патриот отредактировал сообщение</b>:\n\n{translated_text}")

@Client.on_message(filters.outgoing & filters.me)
async def watcher(client, message):
    if patriot_enabled:
        translated_text = message.text.translate(translate_map)
        if message.text != translated_text:
            await message.edit(translated_text)

module_list['Патриот'] = f'{my_prefix()}patriot, {my_prefix()}pat [реплай]'
file_list['Патриот'] = 'патриот.py'