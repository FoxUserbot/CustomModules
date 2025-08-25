import asyncio
from pyrogram import Client, filters
from command import fox_command, fox_sudo, who_message
import os

username_dem = "KlounsBot"

@Client.on_message(fox_command("dem", "Demotivator", os.path.basename(__file__), "[text]") & fox_sudo())
async def demotivator(client, message):
    message = await who_message(client, message)
    await message.edit("Creating demotivator..")
    if message.reply_to_message.photo:
        await client.unblock_user(username_dem)
        capt = ' '.join(message.text.split()[1:])
        await client.send_photo(
            chat_id=username_dem,
            photo=message.reply_to_message.photo.file_id,
            caption=capt
        )
        photo = False

        while not photo:
            try:
                await asyncio.sleep(2)
                async for iii in client.get_chat_history(username_dem, limit=1):
                    await client.send_photo(chat_id=message.chat.id, photo=iii.photo.file_id)
                photo = True
                await message.delete()
            except Exception as f:
                await message.edit(f)
                await asyncio.sleep(2)
    else:
        await message.edit("Please, reply to photo")
