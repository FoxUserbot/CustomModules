import random
from pyrogram import Client, filters
from command import fox_command, fox_sudo, who_message
import os

@Client.on_message(fox_command("chance", "Chance", os.path.basename(__file__), "[text]") & fox_sudo())
async def chance(client, message):
    message = await who_message(client, message)
    text = ' '.join(message.text.split()[1:])
    await message.edit(f"{text}\nChance: {random.randint(1, 100)}%")
