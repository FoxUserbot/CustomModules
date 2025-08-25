from pyrogram import Client, filters
from command import fox_command, fox_sudo, who_message
import os

@Client.on_message(fox_command("wait", "WaitDoksBlyaaa", os.path.basename(__file__)) & fox_sudo())
async def wait_command(client, message):
    message = await who_message(client, message)
    video_url = "https://0x0.st/X9S-.mp4"
    if message.reply_to_message:
        id_m = message.reply_to_message.id
    else:
        id_m = message.id
    try:
        await message.delete()
        await client.send_video(
        chat_id=message.chat.id,
        video=video_url,
        reply_to_message_id=id_m,
        message_thread_id=message.message_thread_id)
    except Exception as e:
        message.reply(f"Error | {e}")
