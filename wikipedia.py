from pyrogram import Client, filters
from command import fox_command, fox_sudo, who_message
from requirements_installer import install_library
import os

install_library("wikipedia") 
import wikipedia

@Client.on_message(fox_command("wiki", "Wikipedia", os.path.basename(__file__), "[RU/EN] [WORD]") & fox_sudo())
async def wiki(client, message):
    message = await who_message(client, message)
    try:
        lang = message.command[1]
        user_request = " ".join(message.command[2:])
        await message.edit("<b>Search info</b>")
        if user_request == "":
            wikipedia.set_lang("en")
            user_request = " ".join(message.command[1:])
        try:
            if lang == "ru":
                wikipedia.set_lang("ru")

            result = wikipedia.summary(user_request)
            await message.edit(
            f"""<b>Слово:</b>
<code>{user_request}</code>

<b>Info:</b>
<code>{result}</code>""")
        except Exception as exc:
            await message.edit(
            f"""<b>Request:</b>
<code>{user_request}</code>
<b>Result:</b>
<code>{exc}</code>"""
        )
    except:
        await message.edit("Dosen't have arguments!")