
import asyncio
import os
import json
import base64
import re
from pyrogram import Client, filters
from pyrogram.types import User
from command import fox_command, fox_sudo, who_message
from requirements_installer import install_library

install_library("google-generativeai -U")
import google.generativeai as genai

def load_config():
    try:
        with open("userdata/gemini_api_key", "r", encoding="utf-8") as f:
            api_key = f.read().strip()
    except FileNotFoundError:
        api_key = None
    
    try:
        with open("userdata/gemini_model", "r", encoding="utf-8") as f:
            model_name = f.read().strip()
    except FileNotFoundError:
        model_name = "gemini-pro"
    
    return {"api_key": api_key, "model": model_name}

@Client.on_message(fox_command("gemini", "Gemini", os.path.basename(__file__), "[текст]") & fox_sudo())
async def gemini_handler(client, message):
    message = await who_message(client, message, message.reply_to_message)
    config = load_config()
    
    if not config["api_key"]:
        return await message.edit("🚫 <b>API ключ не установлен!</b>\n\nИспользуйте: <code>gemini_api [ваш_api_ключ]</code>")
    
    args = message.text.split(maxsplit=1)
    if len(args) < 2:
        return await message.edit("🚫 <b>Использование:</b> <code>gemini [текст]</code>")
    
    query = args[1]
    
    try:
        genai.configure(api_key=config["api_key"])
        model = genai.GenerativeModel(config["model"])
        response = model.generate_content(query)
        
        if response.text:
            if len(response.text) > 4096:
                chunks = [response.text[i:i+4096] for i in range(0, len(response.text), 4096)]
                for chunk in chunks:
                    await message.reply(chunk)
                    await asyncio.sleep(0.5)
                await message.delete()
            else:
                await message.edit(response.text)
        else:
            await message.edit("❌ <b>Gemini не вернул ответ</b>")
            
    except Exception as e:
        await message.edit(f"❌ <b>Ошибка:</b> <code>{str(e)}</code>")

@Client.on_message(fox_command("gemini_api", "Gemini", os.path.basename(__file__), "[api_ключ]") & fox_sudo())
async def gemini_api_handler(client, message):
    message = await who_message(client, message, message.reply_to_message)
    args = message.text.split(maxsplit=1)
    if len(args) < 2:
        return await message.edit("🚫 <b>Использование:</b> <code>gemini_api [ваш_api_ключ]</code>")
    
    api_key = args[1]
    
    with open("userdata/gemini_api_key", "w", encoding="utf-8") as f:
        f.write(api_key)
    
    await message.edit("✅ <b>API ключ сохранен</b>")

@Client.on_message(fox_command("gemini_model", "Gemini", os.path.basename(__file__), "[название_модели]") & fox_sudo())
async def gemini_model_handler(client, message):
    message = await who_message(client, message, message.reply_to_message)
    args = message.text.split(maxsplit=1)
    if len(args) < 2:
        return await message.edit("🚫 <b>Использование:</b> <code>gemini_model [название_модели]</code>")
    
    model_name = args[1]
    
    with open("userdata/gemini_model", "w", encoding="utf-8") as f:
        f.write(model_name)
    
    await message.edit(f"✅ <b>Модель сохранена:</b> <code>{model_name}</code>")

@Client.on_message(fox_command("gemini_chat", "Gemini", os.path.basename(__file__), "[текст]") & fox_sudo())
async def gemini_chat_handler(client, message):
    message = await who_message(client, message, message.reply_to_message)
    config = load_config()
    
    if not config["api_key"]:
        return await message.edit("🚫 <b>API ключ не установлен!</b>\n\nИспользуйте: <code>gemini_api [ваш_api_ключ]</code>")
    
    args = message.text.split(maxsplit=1)
    if len(args) < 2:
        return await message.edit("🚫 <b>Использование:</b> <code>gemini_chat [текст]</code>")
    
    query = args[1]
    
    try:
        chat_history_file = "userdata/gemini_chat_history.json"
        try:
            with open(chat_history_file, "r", encoding="utf-8") as f:
                chat_history = json.load(f)
        except FileNotFoundError:
            chat_history = []
        
        genai.configure(api_key=config["api_key"])
        model = genai.GenerativeModel(config["model"])
        chat = model.start_chat(history=chat_history)
        response = chat.send_message(query)
        
        chat_history.extend([
            {"role": "user", "parts": [query]},
            {"role": "model", "parts": [response.text]}
        ])
        
        with open(chat_history_file, "w", encoding="utf-8") as f:
            json.dump(chat_history, f, ensure_ascii=False, indent=2)
        
        if response.text:
            if len(response.text) > 4096:
                chunks = [response.text[i:i+4096] for i in range(0, len(response.text), 4096)]
                for chunk in chunks:
                    await message.reply(chunk)
                    await asyncio.sleep(0.5)
                await message.delete()
            else:
                await message.edit(response.text)
        else:
            await message.edit("❌ <b>Gemini не вернул ответ</b>")
            
    except Exception as e:
        await message.edit(f"❌ <b>Ошибка:</b> <code>{str(e)}</code>")

@Client.on_message(fox_command("gemini_clear", "Gemini", os.path.basename(__file__)) & fox_sudo())
async def gemini_clear_handler(client, message):
    message = await who_message(client, message, message.reply_to_message)
    
    chat_history_file = "userdata/gemini_chat_history.json"
    try:
        os.remove(chat_history_file)
        await message.edit("✅ <b>История чата очищена</b>")
    except FileNotFoundError:
        await message.edit("ℹ️ <b>История чата уже пуста</b>")
    except Exception as e:
        await message.edit(f"❌ <b>Ошибка:</b> <code>{str(e)}</code>")
