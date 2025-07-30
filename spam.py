import asyncio
from pyrogram import Client, filters
from command import fox_command
import os

@Client.on_message(fox_command("stspam", "Spam", os.path.basename(__file__), "[count] [delay] [sticker_id]") & filters.me)
async def sticker_spam(client, message):
    if not message.text.split("stspam", maxsplit=1)[1]:
        await message.edit("<i>Error</i>")

    sticker = message.command[3]
    count = int(message.command[1])
    sleep = int(message.command[2])
    await message.delete()

    for _ in range(count):
        await client.send_sticker(message.chat.id, sticker)
        await asyncio.sleep(sleep)

@Client.on_message(fox_command("spam", "Spam", os.path.basename(__file__), "[count] [delay] [text]") & filters.me)
async def spam(client, message):
    if not message.text.split("spam", maxsplit=1)[1]:
        await message.edit("<i>Error</i>")
        return
    count = message.command[1]
    text = " ".join(message.command[3:])
    count = int(count)
    try:
        sleep = int(message.command[2])
    except Exception as error:
        await message.edit(error)
        sleep = float(message.command[2])
    await message.delete()

    for _ in range(count):
        await client.send_message(message.chat.id, text)
        await asyncio.sleep(sleep)

@Client.on_message(fox_command("help_spam", "Spam", os.path.basename(__file__)) & filters.me)
async def help_spam(client, message):
    await message.edit(f""".stspam [ID] [Count] [Delay] - Start sticker spam.
```.spam [Count] [Delay] [Text]``` -Start message spam.""")
