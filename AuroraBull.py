
# *      _                             __  __           _       _
# *     / \  _   _ _ __ ___  _ __ __ _|  \/  | ___   __| |_   _| | ___  ___ 
# *    / _ \| | | | '__/ _ \| '__/ _` | |\/| |/ _ \ / _` | | | | |/ _ \/ __|
# *   / ___ \ |_| | | | (_) | | | (_| | |  | | (_) | (_| | |_| | |  __/\__ \
# *  /_/   \_\__,_|_|  \___/|_|  \__,_|_|  |_|\___/ \__,_|\__,_|_|\___||___/
# *
# *                          © Copyright 2024
# *
# *                      https://t.me/AuroraModules
# *
# * 🔒 Code is licensed under GNU AGPLv3
# * 🌐 https://www.gnu.org/licenses/agpl-3.0.html
# * ⛔️ You CANNOT edit this file without direct permission from the author.
# * ⛔️ You CANNOT distribute this file if you have modified it without the direct permission of the author.
# * Ported With Wine Hikka
import asyncio
import json
import os
from random import choice
from pyrogram import Client, filters
from command import fox_command, fox_sudo, who_message, my_prefix
from requirements_installer import install_library
install_library("aiohttp -U")
import aiohttp

@Client.on_message(fox_command("abull", "AuroraBull", os.path.basename(__file__)) & fox_sudo())
async def abull(client, message):
    message = await who_message(client, message)
    url = "https://raw.githubusercontent.com/KorenbZla/HikkaModules/main/AuroraBull.json"
    
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                response_text = await response.text()
                try:
                    data = json.loads(response_text)
                    if "BullText" in data and isinstance(data["BullText"], list) and data["BullText"]:
                        text = choice(data["BullText"])
                        await message.edit(text)
                    else:
                        await message.edit("<b><i>Error: Key 'BullText' not found.</i></b>")
                except json.JSONDecodeError:
                    await message.edit("<b><i>Error: The JSON could not be decoded.</i></b>")
            else:
                await message.edit(f"<b><i>Error loading data</i></b>: {response.status}")

@Client.on_message(fox_command("abullspam", "AuroraBull", os.path.basename(__file__), "[time] [text]") & fox_sudo())
async def abullspam(client, message):
    message = await who_message(client, message)
    url = "https://raw.githubusercontent.com/KorenbZla/HikkaModules/main/AuroraBull.json"
    args = message.text.split()[1:]

    if not args:
        await message.edit("<b><i>Please enter valid arguments!</i></b>")
        return
    
    with open("userdata/aurorabull_state", "w", encoding="utf-8") as f:
        f.write("1")

    try:
        time = float(args[0])
        text = ' '.join(args[1:]) + " " if len(args) > 1 else ""
    except ValueError:
        await message.edit("<b><i>Please enter valid arguments!</i></b>")
        return

    await message.edit(f"<b><i>AuroraBull launched!</i></b>\n\n<b><i>Use <code>{my_prefix()}abulloff</code> to stop the attack.</i></b>")
    
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                response_text = await response.text()
                
                data = json.loads(response_text)
                if "BullText" in data and isinstance(data["BullText"], list) and data["BullText"]:
                    while True:
                        try:
                            with open("userdata/aurorabull_state", "r", encoding="utf-8") as f:
                                state = f.read().strip()
                        except FileNotFoundError:
                            state = "0"
                        
                        if state != "1":
                            break
                            
                        bull_text = choice(data["BullText"])
                        await message.reply(text + bull_text)
                        await asyncio.sleep(time)
                    return
                else:
                    await message.edit("<b><i>Error: Key 'BullText' not found.</i></b>")
                    return
            else:
                await message.edit(f"<b><i>Error loading data</i></b>: {response.status}")
                return

@Client.on_message(fox_command("abulloff", "AuroraBull", os.path.basename(__file__)) & fox_sudo())
async def abulloff(client, message):
    message = await who_message(client, message)
    with open("userdata/aurorabull_state", "w", encoding="utf-8") as f:
        f.write("0")
    await message.edit("<b><i>AuroraBull has stopped.</i></b>")
