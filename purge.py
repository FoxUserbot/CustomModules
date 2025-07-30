from pyrogram import Client, filters
from command import fox_command
import os

@Client.on_message(fox_command("del", "Purge", os.path.basename(__file__), "[reply]") & filters.me)
async def delete_messages(client, message):
    if message.reply_to_message:
        message_id = message.reply_to_message.id
        await client.delete_messages(message.chat.id, message_id)
    await message.delete()

@Client.on_message(fox_command("purge", "Purge", os.path.basename(__file__), "[reply/group_id] [start_id] [stop_id]") & filters.me)
async def purge(client, message):
    try:
        try:
            g = message.command[1]
            try:
                g = int(g)
            except:
                g = str(g)
            r = int(message.command[2])
            m = int(message.command[3])
        except:
            if message.reply_to_message:
                r = message.reply_to_message.id
                m = message.id
                g = message.chat.id
            else:
                await message.edit("<i>I don't see reply</i>")

        await message.delete()
        while r != m:
            try:
                await client.delete_messages(g, int(r))
            except:
                pass
            r += 1

        await client.send_message(message.chat.id, f"<b>Messages deleted!</b>")
    except Exception as f:
        await message.edit(f"<i>Don't have permision.</i>{f}")
