import asyncio
from pyrogram import Client, filters
from command import fox_command, fox_sudo, who_message
import os

@Client.on_message(fox_command("tagallone", "Tagall", os.path.basename(__file__), "[delay] [text]") & fox_sudo())
async def tagallone(client, message):
    message = await who_message(client, message)
    try:
        delay = message.command[1]
    except:
        delay = 0

    if len(message.text.split()) >= 2:
        text = f'{" ".join(message.command[2:])}'
    else:
        text = ""

    await message.edit("Loading...")
    chat_id = message.chat.id
    gg = client.get_chat_members(chat_id)

    await message.delete()
    async for member in gg:
        string = f"{member.user.mention('*')} "
        await client.send_message(chat_id, text=(f"||{string}|| | {text}"), link_preview_options=False, message_thread_id=message.message_thread_id)
        try:
            delay = int(delay)
        except ValueError:
            delay = float(delay)
        await asyncio.sleep(delay)

@Client.on_message(fox_command("tagall", "Tagall", os.path.basename(__file__), "[delay] [text]") & fox_sudo())
async def tagall(client, message):
    message = await who_message(client, message)
    maxTag = 5
    try:
        delay = message.command[1]
    except:
        delay = 0

    if len(message.text.split()) >= 2:
        text = f'{" ".join(message.command[2:])}'
    else:
        text = ""

    await message.edit("Loading...")
    icm = []
    chat_id = message.chat.id
    gg = client.get_chat_members(chat_id)
    async for member in gg:
        icm.append(member)

    useres = len(icm)
    limit = 0
    i = useres // maxTag
    g = useres % maxTag
    l = 0
    string = ""

    await message.delete()
    for member in icm:
        if int(l) == int(i):
            if int(limit) == (g - 1):
                await client.send_message(chat_id, text=(f"{text}\n||{string}||"), link_preview_options=False, message_thread_id=message.message_thread_id)
                string = ""
                limit = 0
            else:
                string += f"{member.user.mention('*')} "
                limit += 1
        else:
            if limit < maxTag:
                string += f"{member.user.mention('*')} "
                limit += 1
            else:
                await client.send_message(chat_id, text=(f"{text}\n||{string}||"), link_preview_options=False, message_thread_id=message.message_thread_id)
                string = ""
                limit = 0
                l += 1
        try:
            delay = int(delay)
        except ValueError:
            delay = float(delay)
        await asyncio.sleep(delay)

