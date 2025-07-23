import asyncio
import os
import logging
import random
import requests
import datetime

from pyrogram import Client, filters
from modules.plugins_1system.settings.main_settings import module_list, file_list
from prefix import my_prefix

logger = logging.getLogger("MediaPics")

@Client.on_message(filters.command("anime", prefixes=my_prefix()) & filters.me)
async def anime(client, message):
    try:
        response = requests.get("https://api.waifu.pics/nsfw/waifu")
        response.raise_for_status()
        data = response.json()
        await client.send_photo(
            chat_id=message.chat.id,
            photo=data['url'],
            reply_to_message_id=message.reply_to_message.id if message.reply_to_message else None,
            message_thread_id=message.message_thread_id
        )
        await message.delete()
    except Exception:
        await message.edit("Произошла ошибка при получении картинки.")

@Client.on_message(filters.command("cat", prefixes=my_prefix()) & filters.me)
async def cat(client, message):
    try:
        response = requests.get("https://api.thecatapi.com/v1/images/search")
        response.raise_for_status()
        data = response.json()
        if data:
            image_url = data[0]['url']
            await client.send_photo(
                chat_id=message.chat.id,
                photo=image_url,
                reply_to_message_id=message.reply_to_message.id if message.reply_to_message else None,
                message_thread_id=message.message_thread_id
            )
            await message.delete()
        else:
            await message.edit("Произошла ошибка при получении фото.")
    except Exception:
        await message.edit("Произошла ошибка при получении фото.")

@Client.on_message(filters.command("lolic", prefixes=my_prefix()) & filters.me)
async def lolic(client, message):
    await message.edit("⏳ загрузка вашей лоли фотографии...")
    await asyncio.sleep(0.5)
    chat = "hdjrkdjrkdkd"
    try:
        messages = []
        async for msg in client.get_chat_history(chat, limit=1, offset=random.choice(range(1, 851, 2))):
            messages.append(msg)
        if messages:
            media = None
            if messages[0].photo:
                media = messages[0].photo
                await client.send_photo(
                    chat_id=message.chat.id,
                    photo=media.file_id,
                    reply_to_message_id=message.reply_to_message.id if message.reply_to_message else None,
                    message_thread_id=message.message_thread_id
                )
            elif messages[0].video:
                media = messages[0].video
                await client.send_video(
                    chat_id=message.chat.id,
                    video=media.file_id,
                    reply_to_message_id=message.reply_to_message.id if message.reply_to_message else None,
                    message_thread_id=message.message_thread_id
                )
            elif messages[0].document:
                media = messages[0].document
                await client.send_document(
                    chat_id=message.chat.id,
                    document=media.file_id,
                    reply_to_message_id=message.reply_to_message.id if message.reply_to_message else None,
                    message_thread_id=message.message_thread_id
                )
            elif messages[0].animation:
                media = messages[0].animation
                await client.send_animation(
                    chat_id=message.chat.id,
                    animation=media.file_id,
                    reply_to_message_id=message.reply_to_message.id if message.reply_to_message else None,
                    message_thread_id=message.message_thread_id
                )
            if media:
                await message.delete()
            else:
                await message.edit("Не удалось получить фотографии. Пожалуйста, разблокируйте @ferganteusbot")
        else:
            await message.edit("Не удалось получить фотографии. Пожалуйста, разблокируйте @ferganteusbot")
    except Exception:
        await message.edit("Не удалось получить фотографии. Пожалуйста, разблокируйте @ferganteusbot")

@Client.on_message(filters.command("loli", prefixes=my_prefix()) & filters.me)
async def loli(client, message):
    await message.edit("⏳ загрузка вашей лоли фотографии...")
    bot_username = "@ferganteusbot"
    command = "/lh"
    try:
        sent_message = await client.send_message(bot_username, command)
        response = None
        for _ in range(15):
            await asyncio.sleep(1)
            async for msg in client.get_chat_history(bot_username, limit=1):
                if msg.from_user and msg.from_user.id == sent_message.from_user.id and msg.id != sent_message.id:
                    response = msg
                    break
            if response:
                break
        if response and response.media:
            await client.send_message(
                chat_id=message.chat.id,
                text=response.text if not response.media else None,
                reply_to_message_id=message.reply_to_message.id if message.reply_to_message else None,
                message_thread_id=message.message_thread_id
            )
            if response.photo:
                await client.send_photo(
                    chat_id=message.chat.id,
                    photo=response.photo.file_id,
                    message_thread_id=message.message_thread_id
                )
            elif response.video:
                await client.send_video(
                    chat_id=message.chat.id,
                    video=response.video.file_id,
                    message_thread_id=message.message_thread_id
                )
            elif response.document:
                await client.send_document(
                    chat_id=message.chat.id,
                    document=response.document.file_id,
                    message_thread_id=message.message_thread_id
                )
            elif response.animation:
                await client.send_animation(
                    chat_id=message.chat.id,
                    animation=response.animation.file_id,
                    message_thread_id=message.message_thread_id
                )
            await client.delete_messages(bot_username, [sent_message.id, response.id])
            await message.delete()
        else:
            await message.edit("Не удалось получить фотографии. Пожалуйста, разблокируйте @ferganteusbot")
            await client.delete_messages(bot_username, [sent_message.id])
    except Exception:
        await message.edit("Не удалось получить фотографии. Пожалуйста, разблокируйте @ferganteusbot")

@Client.on_message(filters.command("lolih", prefixes=my_prefix()) & filters.me)
async def lolih(client, message):
    await message.edit("⏳ загрузка вашей лоли фотографии...")
    bot_username = "@ferganteusbot"
    command = "/lh"
    try:
        sent_message = await client.send_message(bot_username, command)
        response = None
        for _ in range(15):
            await asyncio.sleep(1)
            async for msg in client.get_chat_history(bot_username, limit=1):
                if msg.from_user and msg.from_user.id == sent_message.from_user.id and msg.id != sent_message.id:
                    response = msg
                    break
            if response:
                break
        if response and response.media:
            await client.send_message(
                chat_id=message.chat.id,
                text=response.text if not response.media else None,
                reply_to_message_id=message.reply_to_message.id if message.reply_to_message else None,
                message_thread_id=message.message_thread_id
            )
            if response.photo:
                await client.send_photo(
                    chat_id=message.chat.id,
                    photo=response.photo.file_id,
                    message_thread_id=message.message_thread_id
                )
            elif response.video:
                await client.send_video(
                    chat_id=message.chat.id,
                    video=response.video.file_id,
                    message_thread_id=message.message_thread_id
                )
            elif response.document:
                await client.send_document(
                    chat_id=message.chat.id,
                    document=response.document.file_id,
                    message_thread_id=message.message_thread_id
                )
            elif response.animation:
                await client.send_animation(
                    chat_id=message.chat.id,
                    animation=response.animation.file_id,
                    message_thread_id=message.message_thread_id
                )
            await client.delete_messages(bot_username, [sent_message.id, response.id])
            await message.delete()
        else:
            await message.edit("Не удалось получить фотографии. Пожалуйста, разблокируйте @ferganteusbot")
            await client.delete_messages(bot_username, [sent_message.id])
    except Exception:
        await message.edit("Не удалось получить фотографии. Пожалуйста, разблокируйте @ferganteusbot")

@Client.on_message(filters.command("fem", prefixes=my_prefix()) & filters.me)
async def fem(client, message):
    await message.edit("🔴 загрузка вашего медиа...")
    bot_username = "@ferganteusbot"
    command = "/fm"
    try:
        sent_message = await client.send_message(bot_username, command)
        response = None
        for _ in range(15):
            await asyncio.sleep(1)
            async for msg in client.get_chat_history(bot_username, limit=1):
                if msg.from_user and msg.from_user.id == sent_message.from_user.id and msg.id != sent_message.id:
                    response = msg
                    break
            if response:
                break
        if response and response.media:
            await client.send_message(
                chat_id=message.chat.id,
                text=response.text if not response.media else None,
                reply_to_message_id=message.reply_to_message.id if message.reply_to_message else None,
                message_thread_id=message.message_thread_id
            )
            if response.photo:
                await client.send_photo(
                    chat_id=message.chat.id,
                    photo=response.photo.file_id,
                    message_thread_id=message.message_thread_id
                )
            elif response.video:
                await client.send_video(
                    chat_id=message.chat.id,
                    video=response.video.file_id,
                    message_thread_id=message.message_thread_id
                )
            elif response.document:
                await client.send_document(
                    chat_id=message.chat.id,
                    document=response.document.file_id,
                    message_thread_id=message.message_thread_id
                )
            elif response.animation:
                await client.send_animation(
                    chat_id=message.chat.id,
                    animation=response.animation.file_id,
                    message_thread_id=message.message_thread_id
                )
            await client.delete_messages(bot_username, [sent_message.id, response.id])
            await message.delete()
        else:
            await message.edit("Не удалось получить фотографии. Пожалуйста, разблокируйте @ferganteusbot")
            await client.delete_messages(bot_username, [sent_message.id])
    except Exception:
        await message.edit("Не удалось получить фотографии. Пожалуйста, разблокируйте @ferganteusbot")

@Client.on_message(filters.command("sfw", prefixes=my_prefix()) & filters.me)
async def sfw(client, message):
    await message.edit("🔴 загрузка вашего медиа...")
    bot_username = "@ferganteusbot"
    command = "/rc"
    try:
        sent_message = await client.send_message(bot_username, command)
        response = None
        for _ in range(15):
            await asyncio.sleep(1)
            async for msg in client.get_chat_history(bot_username, limit=1):
                if msg.from_user and msg.from_user.id == sent_message.from_user.id and msg.id != sent_message.id:
                    response = msg
                    break
            if response:
                break
        if response and response.media:
            await client.send_message(
                chat_id=message.chat.id,
                text=response.text if not response.media else None,
                reply_to_message_id=message.reply_to_message.id if message.reply_to_message else None,
                message_thread_id=message.message_thread_id
            )
            if response.photo:
                await client.send_photo(
                    chat_id=message.chat.id,
                    photo=response.photo.file_id,
                    message_thread_id=message.message_thread_id
                )
            elif response.video:
                await client.send_video(
                    chat_id=message.chat.id,
                    video=response.video.file_id,
                    message_thread_id=message.message_thread_id
                )
            elif response.document:
                await client.send_document(
                    chat_id=message.chat.id,
                    document=response.document.file_id,
                    message_thread_id=message.message_thread_id
                )
            elif response.animation:
                await client.send_animation(
                    chat_id=message.chat.id,
                    animation=response.animation.file_id,
                    message_thread_id=message.message_thread_id
                )
            await client.delete_messages(bot_username, [sent_message.id, response.id])
            await message.delete()
        else:
            await message.edit("Не удалось получить фотографии. Пожалуйста, разблокируйте @ferganteusbot")
            await client.delete_messages(bot_username, [sent_message.id])
    except Exception:
        await message.edit("Не удалось получить фотографии. Пожалуйста, разблокируйте @ferganteusbot")

@Client.on_message(filters.command("furry", prefixes=my_prefix()) & filters.me)
async def furry(client, message):
    await message.edit("🔴 загрузка вашего медиа...")
    await asyncio.sleep(0.5)
    chat = "furrylov"
    try:
        messages = []
        async for msg in client.get_chat_history(chat, limit=1, offset=random.choice(range(1, 12436, 2))):
            messages.append(msg)
        if messages:
            media = None
            if messages[0].photo:
                media = messages[0].photo
                await client.send_photo(
                    chat_id=message.chat.id,
                    photo=media.file_id,
                    reply_to_message_id=message.reply_to_message.id if message.reply_to_message else None,
                    message_thread_id=message.message_thread_id
                )
            elif messages[0].video:
                media = messages[0].video
                await client.send_video(
                    chat_id=message.chat.id,
                    video=media.file_id,
                    reply_to_message_id=message.reply_to_message.id if message.reply_to_message else None,
                    message_thread_id=message.message_thread_id
                )
            elif messages[0].document:
                media = messages[0].document
                await client.send_document(
                    chat_id=message.chat.id,
                    document=media.file_id,
                    reply_to_message_id=message.reply_to_message.id if message.reply_to_message else None,
                    message_thread_id=message.message_thread_id
                )
            elif messages[0].animation:
                media = messages[0].animation
                await client.send_animation(
                    chat_id=message.chat.id,
                    animation=media.file_id,
                    reply_to_message_id=message.reply_to_message.id if message.reply_to_message else None,
                    message_thread_id=message.message_thread_id
                )
            if media:
                await message.delete()
            else:
                await message.edit("Не удалось получить фотографии. Пожалуйста, разблокируйте @ferganteusbot")
        else:
            await message.edit("Не удалось получить фотографии. Пожалуйста, разблокируйте @ferganteusbot")
    except Exception:
        await message.edit("Не удалось получить фотографии. Пожалуйста, разблокируйте @ferganteusbot")

@Client.on_message(filters.command("nsfw", prefixes=my_prefix()) & filters.me)
async def nsfw(client, message):
    await message.edit("🔴 загрузка вашего медиа...")
    await asyncio.sleep(0.5)
    chat = "hdjrkdjrkdkd"
    try:
        messages = []
        async for msg in client.get_chat_history(chat, limit=1, offset=random.choice(range(1, 851, 2))):
            messages.append(msg)
        if messages:
            media = None
            if messages[0].photo:
                media = messages[0].photo
                await client.send_photo(
                    chat_id=message.chat.id,
                    photo=media.file_id,
                    reply_to_message_id=message.reply_to_message.id if message.reply_to_message else None,
                    message_thread_id=message.message_thread_id
                )
            elif messages[0].video:
                media = messages[0].video
                await client.send_video(
                    chat_id=message.chat.id,
                    video=media.file_id,
                    reply_to_message_id=message.reply_to_message.id if message.reply_to_message else None,
                    message_thread_id=message.message_thread_id
                )
            elif messages[0].document:
                media = messages[0].document
                await client.send_document(
                    chat_id=message.chat.id,
                    document=media.file_id,
                    reply_to_message_id=message.reply_to_message.id if message.reply_to_message else None,
                    message_thread_id=message.message_thread_id
                )
            elif messages[0].animation:
                media = messages[0].animation
                await client.send_animation(
                    chat_id=message.chat.id,
                    animation=media.file_id,
                    reply_to_message_id=message.reply_to_message.id if message.reply_to_message else None,
                    message_thread_id=message.message_thread_id
                )
            if media:
                await message.delete()
            else:
                await message.edit("Не удалось получить фотографии. Пожалуйста, разблокируйте @ferganteusbot")
        else:
            await message.edit("Не удалось получить фотографии. Пожалуйста, разблокируйте @ferganteusbot")
    except Exception:
        await message.edit("Не удалось получить фотографии. Пожалуйста, разблокируйте @ferganteusbot")

module_list['MediaPics'] = f'{my_prefix()}anime, {my_prefix()}cat, {my_prefix()}lolic, {my_prefix()}loli [текст], {my_prefix()}lolih [текст], {my_prefix()}fem [текст], {my_prefix()}sfw [текст], {my_prefix()}furry [текст], {my_prefix()}nsfw [текст]'
file_list['MediaPics'] = 'mediapics.py'