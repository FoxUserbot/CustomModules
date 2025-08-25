import random
import os
from pyrogram import Client, filters
from command import fox_command, fox_sudo, who_message
from requirements_installer import install_library

install_library("gTTS") 
from gtts import gTTS

@Client.on_message(fox_command("voice", "TextToVoice", os.path.basename(__file__), "[text]") & fox_sudo())
async def voice(client, message):
    message = await who_message(client, message)
    lang_code = os.environ.get("lang_code", "en")
    rnd = random.randint(10000, 99999)
    await message.delete()
    text = message.text.split(None, 1)[1]
    tts = gTTS(text, lang=lang_code)
    tts.save(f"temp/voice{rnd}.mp3")
    if message.reply_to_message:
        await client.send_voice(
            message.chat.id,
            voice=f"temp/voice{rnd}.mp3",
            reply_to_message_id=message.reply_to_message.id,
        )
    else:
        await client.send_voice(message.chat.id, voice=f"temp/voice{rnd}.mp3")
    os.remove(f"temp/voice{rnd}.mp3")

@Client.on_message(fox_command("voice_ru", "TextToVoice", os.path.basename(__file__), "[text]") & fox_sudo())
async def ru_voice(client, message):
    message = await who_message(client, message)
    lang_code = os.environ.get("lang_code", "ru")
    rnd = random.randint(10000, 99999)
    await message.delete()
    text = message.text.split(None, 1)[1]
    tts = gTTS(text, lang=lang_code)
    tts.save(f"temp/voice{rnd}.mp3")
    if message.reply_to_message:
        await client.send_voice(
            message.chat.id,
            voice=f"temp/voice{rnd}.mp3",
            reply_to_message_id=message.reply_to_message.id,
        )
    else:
        await client.send_voice(message.chat.id, voice=f"temp/voice{rnd}.mp3")
    os.remove(f"temp/voice{rnd}.mp3")
