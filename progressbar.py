import time
from pyrogram import Client, filters
from command import fox_command, fox_sudo, who_message
import os

@Client.on_message(fox_command("progressbar", "Progressbar", os.path.basename(__file__), "[text]") & fox_sudo())
async def progressbar(client, message):
    message = await who_message(client, message)
    try:
        text = ' '.join(message.text.split()[1:])

        total = 100
        bar_length = 10
        for i in range(total + 1):
            percent = 100.0 * i / total
            time.sleep(0.1)
            await message.edit(
                text + "\n[{:{}}] {:>3}%".format("█" * int(percent / (100.0 / bar_length)), bar_length, int(percent)))
    except IndexError:
        message.edit('No text here!')
