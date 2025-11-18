
# ©️ qq_shark, 2025
# 🌐 https://github.com/qqshark/Modules/blob/main/media2gif.py
# Licensed under GNU AGPL v3.0
# Ported with Wine Hikka
import os
import subprocess
import asyncio
from pyrogram import Client, filters
from pyrogram.types import ReplyParameters
from command import fox_command, fox_sudo, who_message
from requirements_installer import install_library
install_library("Pillow -U")
from PIL import Image

def cleanup_temp_files(*files):
    """Удаляет временные файлы."""
    for f in files:
        if f and os.path.exists(f):
            try:
                os.remove(f)
            except Exception:
                pass

def convert_video_to_gif(video_path: str, gif_path: str) -> None:
    """Конвертирует видео в GIF с оптимальными параметрами."""
    command = [
        "ffmpeg",
        "-y",
        "-i",
        video_path,
        "-vf",
        "fps=30,scale=640:-1:flags=lanczos",
        "-c:v",
        "gif",
        gif_path,
    ]
    subprocess.run(command, check=True)

@Client.on_message(fox_command("media2gif", "Media2Gif", os.path.basename(__file__), "[reply to photo or video]") & fox_sudo())
async def media2gif(client, message):
    message = await who_message(client, message)
    reply = message.reply_to_message
    
    if not reply or not (reply.photo or reply.video):
        return await message.edit("⚠️ Ответьте на фото или видео!")
    
    status_msg = await message.edit("⏳ Начинаю...")
    
    # Фото в гиф
    if reply.photo:
        try:
            await status_msg.edit("⏬ Загружаю файл...")
            photo_path = await reply.download(file_name="pic2gif_in.jpg")
            gif_path = "pic2gif_out.gif"
            
            await status_msg.edit("🔄 Конвертирую...")
            img = Image.open(photo_path).convert("RGB")
            img.save(
                gif_path,
                save_all=True,
                append_images=[],
                duration=100,
                loop=0,
                format="GIF"
            )
            
            await status_msg.edit("📤 Отправляю...")
            await client.send_animation(
                chat_id=message.chat.id,
                animation=gif_path,
                reply_parameters=ReplyParameters(message_id=reply.id),
                message_thread_id=message.message_thread_id
            )
            
        except Exception as e:
            await status_msg.edit("❌ Ошибка при преобразовании в GIF.")
            print(f"Error during photo2gif: {e}")
        finally:
            await status_msg.edit("🧹 Завершаю...")
            cleanup_temp_files("pic2gif_in.jpg", "pic2gif_out.gif")
            await status_msg.delete()
            await message.delete()
        return
    
    # Видео в гиф
    if reply.video:
        try:
            await status_msg.edit("⏬ Загружаю файл...")
            video_path = await reply.download(file_name="pic2gif_in.mp4")
            gif_path = "pic2gif_out.gif"
            
            await status_msg.edit("🔄 Конвертирую...")
            convert_video_to_gif(video_path, gif_path)
            
            await status_msg.edit("📤 Отправляю...")
            await client.send_animation(
                chat_id=message.chat.id,
                animation=gif_path,
                reply_parameters=ReplyParameters(message_id=reply.id),
                message_thread_id=message.message_thread_id
            )
            
        except Exception as e:
            await status_msg.edit("❌ Ошибка при преобразовании в GIF.")
            print(f"Error during video2gif: {e}")
        finally:
            await status_msg.edit("🧹 Завершаю...")
            cleanup_temp_files("pic2gif_in.mp4", "pic2gif_out.gif")
            await status_msg.delete()
            await message.delete()
        return
