import asyncio
from pyrogram import Client, filters
from command import fox_command
import os

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

@Client.on_message(fox_command("patriot", "Патриот", os.path.basename(__file__)) & filters.me)
async def patriotcmd(client, message):
    global patriot_enabled
    patriot_enabled = not patriot_enabled
    
    if patriot_enabled:
        return await message.edit("<b>🇷🇺 Патриот успешно включен. Страна может спать спокойно</b>")
    else:
        return await message.edit("❌ <b>Патриот выключен</b>")

@Client.on_message(fox_command("pat", "Патриот", os.path.basename(__file__), "[reply]") & filters.me)
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