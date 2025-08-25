from pyrogram import Client, filters
from command import fox_command, fox_sudo, who_message
import os

@Client.on_message(fox_command("ladder", "Ladder", os.path.basename(__file__), "[text]") & fox_sudo())
async def ladder(client, message):
    message = await who_message(client, message)
    try:
        orig_text = ' '.join(message.text.split()[1:])
        text = orig_text
        output = []
        for i in range(len(text) + 1):
            output.append(text[:i])
        ot = "\n".join(output)
        await message.edit(ot)
    except:
        await message.edit('Error in processing your request.')
