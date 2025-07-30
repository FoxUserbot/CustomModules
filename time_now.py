import datetime
from pyrogram import Client, filters
from command import fox_command
import os

@Client.on_message(fox_command("time", "TimeNow", os.path.basename(__file__)) & filters.me)
async def time(client, message):
    now = datetime.datetime.now()
    now = now.strftime("%Y-%m-%d - %H:%M:%S")
    now = datetime.datetime.now().strftime("Date: %d/%m/%Y\nTime: %H:%M:%S")
    await message.edit(now)
