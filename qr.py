from pyrogram import Client, filters
from command import fox_command
import os

@Client.on_message(fox_command("qr", "QRcode", os.path.basename(__file__), "[text]") & filters.me)
async def qr(client, message):
    try:
        texts = ""
        if message.reply_to_message:
            texts = message.reply_to_message.text
        elif len(message.text.split(maxsplit=1)) == 2:
            texts = message.text.split(maxsplit=1)[1]
        text = texts.replace(' ', '%20')
        QRcode = f"https://api.qrserver.com/v1/create-qr-code/?size=300x300&data={text}"
        await message.delete()
        await client.send_photo(message.chat.id, QRcode)
    except Exception as e:
        await message.edit(f'Error: {e}')
