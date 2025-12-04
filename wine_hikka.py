from pyrogram import Client
from command import fox_command, fox_sudo, who_message, my_prefix, get_text
import base64
import os
import shutil
from requirements_installer import install_library
install_library('openai requests')
from openai import AsyncOpenAI
from openai import RateLimitError, APIError, APIConnectionError, APITimeoutError
import requests
import asyncio
import time

filename = os.path.basename(__file__)
Module_Name = 'WineHikka'

LANGUAGES = {
    "en": {
        "loading_reply": "<emoji id='5283051451889756068'>🦊</emoji> | Loading module from reply...",
        "loading_url": "<emoji id='5283051451889756068'>🦊</emoji> | Loading module from URL: {url}",
        "error_status": "<emoji id='5283051451889756068'>🦊</emoji> | Error loading module from URL: {status}",
        "error_request": "<emoji id='5283051451889756068'>🦊</emoji> | Error loading module from URL: {error}",
        "no_input": "<emoji id='5283051451889756068'>🦊</emoji> | Reply to a module file or provide a link!",
        "no_content": "<emoji id='5283051451889756068'>🦊</emoji> | Failed to get module content.",
        "generating": "<emoji id='5283051451889756068'>🦊</emoji> | Generating module...",
        "generated": "<emoji id='5283051451889756068'>🦊</emoji> | Generated module: <code>{module_name}</code>",
        "error_generate": "<emoji id='5283051451889756068'>🦊</emoji> | Error generating module :(",
        "rate_limit": "<emoji id='5283051451889756068'>🦊</emoji> | Rate limit exceeded. Please try again later or add your own API key.",
        "api_error": "<emoji id='5283051451889756068'>🦊</emoji> | API error: {error}",
        "connection_error": "<emoji id='5283051451889756068'>🦊</emoji> | Connection error. Please check your internet connection.",
        "timeout_error": "<emoji id='5283051451889756068'>🦊</emoji> | Request timeout. Please try again.",
        "current_model": "<emoji id='5283051451889756068'>🦊</emoji> | **Current model:** `{model}`\n\n**Usage:**\n`{prefix}wine_config [model_name]`\n\n**Example models:**\n• `qwen/qwen2.5-72b-instruct`\n• `anthropic/claude-3.5-sonnet`\n• `meta-llama/llama-3.1-8b-instruct`\n• `google/gemini-pro-1.5`\n\n <a href='https://openrouter.ai/models?max_price=0'><b>You can get models here</b></a>",
        "no_model": "<emoji id='5283051451889756068'>🦊</emoji> | <b>Please specify a model name! \n You can get models <a href='https://openrouter.ai/models?max_price=0'>here</a></b>",
        "not_free": "<emoji id='5283051451889756068'>🦊</emoji> | <b>Please specify a free model! \n You can get models <a href='https://openrouter.ai/models?max_price=0'>here</a></b>",
        "success": "<emoji id='5283051451889756068'>🦊</emoji> | **Model successfully changed!**\n\n**New model:** `{model}`\n\nNow all requests will use this model.",
        "error_save": "<emoji id='5283051451889756068'>🦊</emoji> | **Error saving model:**\n`{error}`"
    },
    "ru": {
        "loading_reply": "<emoji id='5283051451889756068'>🦊</emoji> | Загрузка модуля из ответа...",
        "loading_url": "<emoji id='5283051451889756068'>🦊</emoji> | Загрузка модуля с URL: {url}",
        "error_status": "<emoji id='5283051451889756068'>🦊</emoji> | Ошибка загрузки модуля с URL: {status}",
        "error_request": "<emoji id='5283051451889756068'>🦊</emoji> | Ошибка загрузки модуля с URL: {error}",
        "no_input": "<emoji id='5283051451889756068'>🦊</emoji> | Ответьте на файл модуля или предоставьте ссылку!",
        "no_content": "<emoji id='5283051451889756068'>🦊</emoji> | Не удалось получить содержимое модуля.",
        "generating": "<emoji id='5283051451889756068'>🦊</emoji> | Генерирование модуля...",
        "generated": "<emoji id='5283051451889756068'>🦊</emoji> | Сгенерированный модуль: <code>{module_name}</code>",
        "error_generate": "<emoji id='5283051451889756068'>🦊</emoji> | Ошибка при генерировании модуля :(",
        "rate_limit": "<emoji id='5283051451889756068'>🦊</emoji> | Превышен лимит запросов. Попробуйте позже или добавьте свой API ключ.",
        "api_error": "<emoji id='5283051451889756068'>🦊</emoji> | Ошибка API: {error}",
        "connection_error": "<emoji id='5283051451889756068'>🦊</emoji> | Ошибка подключения. Проверьте интернет-соединение.",
        "timeout_error": "<emoji id='5283051451889756068'>🦊</emoji> | Таймаут запроса. Попробуйте снова.",
        "current_model": "<emoji id='5283051451889756068'>🦊</emoji> | **Текущая модель:** `{model}`\n\n**Использование:**\n`{prefix}wine_config [имя_модели]`\n\n**Примеры моделей:**\n• `qwen/qwen2.5-72b-instruct`\n• `anthropic/claude-3.5-sonnet`\n• `meta-llama/llama-3.1-8b-instruct`\n• `google/gemini-pro-1.5`\n\n <a href='https://openrouter.ai/models?max_price=0'><b>Вы можете получить модели здесь</b></a>",
        "no_model": "<emoji id='5283051451889756068'>🦊</emoji> | <b>Укажите имя модели! \n Вы можете получить модели <a href='https://openrouter.ai/models?max_price=0'>здесь</a></b>",
        "not_free": "<emoji id='5283051451889756068'>🦊</emoji> | <b>Укажите бесплатную модель! \n Вы можете получить модели <a href='https://openrouter.ai/models?max_price=0'>здесь</a></b>",
        "success": "<emoji id='5283051451889756068'>🦊</emoji> | **Модель успешно изменена!**\n\n**Новая модель:** `{model}`\n\nТеперь все запросы будут использовать эту модель.",
        "error_save": "<emoji id='5283051451889756068'>🦊</emoji> | **Ошибка сохранения модели:**\n`{error}`"
    },
    "ua": {
        "loading_reply": "<emoji id='5283051451889756068'>🦊</emoji> | Завантаження модуля з відповіді...",
        "loading_url": "<emoji id='5283051451889756068'>🦊</emoji> | Завантаження модуля з URL: {url}",
        "error_status": "<emoji id='5283051451889756068'>🦊</emoji> | Помилка завантаження модуля з URL: {status}",
        "error_request": "<emoji id='5283051451889756068'>🦊</emoji> | Помилка завантаження модуля з URL: {error}",
        "no_input": "<emoji id='5283051451889756068'>🦊</emoji> | Відповідьте на файл модуля або надайте посилання!",
        "no_content": "<emoji id='5283051451889756068'>🦊</emoji> | Не вдалося отримати вміст модуля.",
        "generating": "<emoji id='5283051451889756068'>🦊</emoji> | Генерування модуля...",
        "generated": "<emoji id='5283051451889756068'>🦊</emoji> | Згенерований модуль: <code>{module_name}</code>",
        "error_generate": "<emoji id='5283051451889756068'>🦊</emoji> | Помилка при генеруванні модуля :(",
        "rate_limit": "<emoji id='5283051451889756068'>🦊</emoji> | Перевищено ліміт запитів. Спробуйте пізніше або додайте свій API ключ.",
        "api_error": "<emoji id='5283051451889756068'>🦊</emoji> | Помилка API: {error}",
        "connection_error": "<emoji id='5283051451889756068'>🦊</emoji> | Помилка підключення. Перевірте інтернет-з'єднання.",
        "timeout_error": "<emoji id='5283051451889756068'>🦊</emoji> | Таймаут запиту. Спробуйте знову.",
        "current_model": "<emoji id='5283051451889756068'>🦊</emoji> | **Поточна модель:** `{model}`\n\n**Використання:**\n`{prefix}wine_config [назва_моделі]`\n\n**Приклади моделей:**\n• `qwen/qwen2.5-72b-instruct`\n• `anthropic/claude-3.5-sonnet`\n• `meta-llama/llama-3.1-8b-instruct`\n• `google/gemini-pro-1.5`\n\n <a href='https://openrouter.ai/models?max_price=0'><b>Ви можете отримати моделі тут</b></a>",
        "no_model": "<emoji id='5283051451889756068'>🦊</emoji> | <b>Вкажіть назву моделі! \n Ви можете отримати моделі <a href='https://openrouter.ai/models?max_price=0'>тут</a></b>",
        "not_free": "<emoji id='5283051451889756068'>🦊</emoji> | <b>Вкажіть безплатну модель! \n Ви можете отримати моделі <a href='https://openrouter.ai/models?max_price=0'>тут</a></b>",
        "success": "<emoji id='5283051451889756068'>🦊</emoji> | **Модель успішно змінена!**\n\n**Нова модель:** `{model}`\n\nТепер усі запити будуть використовувати цю модель.",
        "error_save": "<emoji id='5283051451889756068'>🦊</emoji> | **Помилка збереження моделі:**\n`{error}`"
    }
}

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
    
    max_retries = 5
    base_delay = 1
    
    for attempt in range(max_retries):
        try:
            response = await client_ai.chat.completions.create(
                model=get_wine_model(),
                messages=[{"role": "user", "content": prompt}]
            )
            return response.choices[0].message.content.replace("```python", "").replace("```", "")
        
        except RateLimitError as e:
            if attempt < max_retries - 1:
                delay = base_delay * (2 ** attempt) + (time.time() % 1)
                await asyncio.sleep(delay)
                continue
            else:
                return None
        
        except APIConnectionError as e:
            if attempt < max_retries - 1:
                delay = base_delay * (2 ** attempt)
                await asyncio.sleep(delay)
                continue
            else:
                return None
        
        except APITimeoutError as e:
            if attempt < max_retries - 1:
                delay = base_delay * (2 ** attempt)
                await asyncio.sleep(delay)
                continue
            else:
                return None
    
    return None 

@Client.on_message(fox_command("wine_hikka", Module_Name, filename, "[Link/Reply]") & fox_sudo())
async def wine_hikka(client, message):
    message = await who_message(client, message)
    file_content = None
    module_name = None
    if message.reply_to_message and message.reply_to_message.document:
        loading_text = get_text("wine_hikka", "loading_reply", LANGUAGES=LANGUAGES)
        await message.edit(loading_text)
        file = await client.download_media(message.reply_to_message.document)
        with open(file, "r", encoding="utf-8") as f:
            file_content = f.read()
        os.remove(file)
        if os.path.exists("downloads"):
            shutil.rmtree("downloads")
        module_name = message.reply_to_message.document.file_name.replace(".py", "")
    elif len(message.command) > 1 and (message.text.split()[1].startswith("http") or message.text.split()[1].startswith("https")):
        url = message.text.split()[1]
        loading_text = get_text("wine_hikka", "loading_url", LANGUAGES=LANGUAGES, url=url)
        await message.edit(loading_text)
        try:
            response = requests.get(url,headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"},verify=False)
            if response.status_code != 200:
                error_text = get_text("wine_hikka", "error_status", LANGUAGES=LANGUAGES, status=response.status_code)
                await message.edit(error_text)
                return
            file_content = response.text
            module_name = url.split("/")[-1].replace(".py", "")
        except requests.exceptions.RequestException as e:
            error_text = get_text("wine_hikka", "error_request", LANGUAGES=LANGUAGES, error=str(e))
            await message.edit(error_text)
            return
    else:
        no_input_text = get_text("wine_hikka", "no_input", LANGUAGES=LANGUAGES)
        await message.edit(no_input_text)
        return

    if file_content is None:
        no_content_text = get_text("wine_hikka", "no_content", LANGUAGES=LANGUAGES)
        await message.edit(no_content_text)
        return

    generating_text = get_text("wine_hikka", "generating", LANGUAGES=LANGUAGES)
    await message.edit(generating_text)
    
    try:
        answer = await create_module(file_content, module_name)
    except RateLimitError:
        error_text = get_text("wine_hikka", "rate_limit", LANGUAGES=LANGUAGES)
        await message.edit(error_text)
        return
    except APIConnectionError:
        error_text = get_text("wine_hikka", "connection_error", LANGUAGES=LANGUAGES)
        await message.edit(error_text)
        return
    except APITimeoutError:
        error_text = get_text("wine_hikka", "timeout_error", LANGUAGES=LANGUAGES)
        await message.edit(error_text)
        return
    except APIError as e:
        error_text = get_text("wine_hikka", "api_error", LANGUAGES=LANGUAGES, error=str(e))
        await message.edit(error_text)
        return
    except Exception as e:
        error_text = get_text("wine_hikka", "error_generate", LANGUAGES=LANGUAGES)
        await message.edit(error_text)
        return
    
    if answer is not None:
        file_path = f"modules/loaded/{module_name}.py"
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(answer)
    
        caption_text = get_text("wine_hikka", "generated", LANGUAGES=LANGUAGES, module_name=module_name)
        await client.send_document(
            message.chat.id,
            file_path,
            caption=caption_text,
        )
        os.remove(file_path)
    else:
        error_text = get_text("wine_hikka", "error_generate", LANGUAGES=LANGUAGES)
        await message.edit(error_text)

@Client.on_message(fox_command("wine_config", Module_Name, filename, "[Model]") & fox_sudo())
async def wine_config(client, message):
    message = await who_message(client, message)
    if len(message.command) < 2:
        current_model = get_wine_model()
        current_text = get_text("wine_hikka", "current_model", LANGUAGES=LANGUAGES, model=current_model, prefix=my_prefix())
        await message.edit(current_text)
        return
    
    new_model = message.text.split()[1]
    if not new_model or new_model.strip() == "":
        no_model_text = get_text("wine_hikka", "no_model", LANGUAGES=LANGUAGES)
        await message.edit(no_model_text)
        return
    try:
        save_wine_model(new_model)
        success_text = get_text("wine_hikka", "success", LANGUAGES=LANGUAGES, model=new_model)
        await message.edit(success_text)
    except Exception as e:
        error_text = get_text("wine_hikka", "error_save", LANGUAGES=LANGUAGES, error=str(e))
        await message.edit(error_text)
