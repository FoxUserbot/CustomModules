from pyrogram import Client
from command import fox_command, fox_sudo, who_message , my_prefix
import base64
import os
import shutil
from requirements_installer import install_library
install_library('openai requests')
from openai import AsyncOpenAI
import requests

def get_wine_model():
    try:
        with open("userdata/wine_model", "r+", encoding="utf-8") as f:
            model = f.read().strip()
            if model:
                return model
    except:
        return "qwen/qwen3-coder:free"

def save_wine_model(model):
    with open("userdata/wine_model", "w+", encoding="utf-8") as f:
        f.write(model)


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
                model=get_wine_model(),
                messages=[{"role": "user", "content": prompt}]
            )
    return response.choices[0].message.content.replace("```python", "").replace("```", "")

@Client.on_message(fox_command("wine_hikka", "WineHikka", os.path.basename(__file__), "[Link/Reply]") & fox_sudo())
async def wine_hikka(client, message):
    message = await who_message(client, message)
    file_content = None
    module_name = None
    if message.reply_to_message and message.reply_to_message.document:
        await message.edit(f"<emoji id='5283051451889756068'>🦊</emoji> | Loading module from reply...")
        file = await client.download_media(message.reply_to_message.document)
        with open(file, "r", encoding="utf-8") as f:
            file_content = f.read()
        os.remove(file)
        if os.path.exists("downloads"):
            shutil.rmtree("downloads")
        module_name = message.reply_to_message.document.file_name.replace(".py", "")
    elif len(message.command) > 1 and (message.command[1].startswith("http") or message.command[1].startswith("https")):
        url = message.command[1]
        await message.edit(f"<emoji id='5283051451889756068'>🦊</emoji> | Loading module from URL: {url}")
        try:
            response = requests.get(url)
            if response.status_code != 200:
                await message.edit(f"<emoji id='5283051451889756068'>🦊</emoji> | Error loading module from URL: {response.status_code}")
                return
            file_content = response.text
            module_name = url.split("/")[-1].replace(".py", "")
        except requests.exceptions.RequestException as e:
            await message.edit(f"<emoji id='5283051451889756068'>🦊</emoji> | Error loading module from URL: {e}")
            return
    else:
        await message.edit("<emoji id='5283051451889756068'>🦊</emoji> | Reply to a module file or provide a link!")
        return

    if file_content is None:
        await message.edit("<emoji id='5283051451889756068'>🦊</emoji> | Failed to get module content.")
        return

    await message.edit(f"<emoji id='5283051451889756068'>🦊</emoji> | Generating module...")
    answer = await create_module(file_content, module_name)
    
    if answer is not None:
        file_path = f"modules/loaded/{module_name}.py"
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(answer)
    
        await client.send_document(
            message.chat.id,
            file_path,
            caption=f"<emoji id='5283051451889756068'>🦊</emoji> | Generated module: <code>{module_name}</code>",
        )
        os.remove(file_path)
    else:
        await message.edit(f"<emoji id='5283051451889756068'>🦊</emoji> | Error generating module :(")

@Client.on_message(fox_command("wine_config", "WineHikka", os.path.basename(__file__), "[Model]") & fox_sudo())
async def wine_config(client, message):
    message = await who_message(client, message)
    if len(message.command) < 2:
        current_model = get_wine_model()
        await message.edit(f"<emoji id='5283051451889756068'>🦊</emoji> | **Current model:** `{current_model}`\n\n**Usage:**\n`{my_prefix()}wine_config [model_name]`\n\n**Example models:**\n• `qwen/qwen2.5-72b-instruct`\n• `anthropic/claude-3.5-sonnet`\n• `meta-llama/llama-3.1-8b-instruct`\n• `google/gemini-pro-1.5`\n\n <a href='https://openrouter.ai/models?max_price=0'><b>You can get models here</b></a>")
    new_model = message.command[1]
    if not new_model or new_model.strip() == "":
        await message.edit("<emoji id='5283051451889756068'>🦊</emoji> | <b>Please specify a model name! \n You can get models <a href='https://openrouter.ai/models?max_price=0'>here</a></b>")
        return
    if not "free" in new_model:
        await message.edit("<emoji id='5283051451889756068'>🦊</emoji> | <b>Please specify a free model! \n You can get models <a href='https://openrouter.ai/models?max_price=0'>here</a>    </b>")
        return
    try:
        save_wine_model(new_model)
        await message.edit(f"<emoji id='5283051451889756068'>🦊</emoji> | **Model successfully changed!**\n\n**New model:** `{new_model}`\n\nNow all requests will use this model.")
    except Exception as e:
        await message.edit(f"<emoji id='5283051451889756068'>🦊</emoji> | **Error saving model:**\n`{str(e)}`")