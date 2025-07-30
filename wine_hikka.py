from pyrogram import Client, filters
from command import fox_command
import base64
import os
import shutil

from requirements_installer import install_library
install_library('openai requests')
from openai import AsyncOpenAI
import requests

async def create_module(module_text, module_name):
    prompt = (
        f"""
{requests.get("https://pastebin.com/raw/uT0MjKCY").text}
{module_name}.py
========
Вот код модуля: 
```python
{module_text}
```
"""
    )
    
    client_ai  = AsyncOpenAI(
                base_url="https://openrouter.ai/api/v1",
                api_key=str(base64.b64decode("c2stb3ItdjEtNjg1YzZiMDc2YjJhNDE4M2VkNTUzOWIyMTk3ZWY4MTk3YjkxYTE1ZDMxOTAxZjQ2YTQ5MTk0NTFjYzkxYzRmZQ==").decode('utf-8'))
            )
    response = await client_ai.chat.completions.create(
                model="qwen/qwen3-235b-a22b-07-25:free",
                messages=[{"role": "user", "content": prompt}]
            )
    return response.choices[0].message.content.replace("```python", "").replace("```", "")

@Client.on_message(fox_command("wine_hikka", "WineHikka", os.path.basename(__file__), "[Link/Reply]") & filters.me)
async def wine_hikka(client, message):
    file_content = None
    module_name = None
    if message.reply_to_message and message.reply_to_message.document:
        await message.edit(f"🦊 | Loading module from reply...")
        file = await client.download_media(message.reply_to_message.document)
        with open(file, "r", encoding="utf-8") as f:
            file_content = f.read()
        os.remove(file)
        if os.path.exists("downloads"):
            shutil.rmtree("downloads")
        module_name = message.reply_to_message.document.file_name.replace(".py", "")
    elif len(message.command) > 1 and (message.command[1].startswith("http") or message.command[1].startswith("https")):
        url = message.command[1]
        await message.edit(f"🦊 | Loading module from URL: {url}")
        try:
            response = requests.get(url)
            if response.status_code != 200:
                await message.edit(f"🦊 | Error loading module from URL: {response.status_code}")
                return
            file_content = response.text
            module_name = url.split("/")[-1].replace(".py", "")
        except requests.exceptions.RequestException as e:
            await message.edit(f"🦊 | Error loading module from URL: {e}")
            return
    else:
        await message.edit("🦊 | Reply to a module file or provide a link!")
        return

    if file_content is None:
        await message.edit("🦊 | Failed to get module content.")
        return

    await message.edit(f"🦊 | Generating module...")
    answer = await create_module(file_content, module_name)
    file_path = f"modules/plugins_2custom/{module_name}.py"
    if answer is not None:
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(answer)
        await message.edit(f"🦊 | Module generated at <code>{file_path}</code>")
    else:
        await message.edit(f"🦊 | Error generating module :(")
