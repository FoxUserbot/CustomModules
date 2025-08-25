import asyncio
import os
import time
from datetime import datetime
from pyrogram import Client, filters
from command import fox_command, fox_sudo, who_message
from requirements_installer import install_library

install_library("aiohttp -U")
import aiohttp

def load_config():
    try:
        with open("userdata/speedtest_language", "r", encoding="utf-8") as f:
            language = f.read().strip()
    except FileNotFoundError:
        language = "en"
    
    return {"language": language}

def check_config():
    try:
        with open("userdata/speedtest_language", "r", encoding="utf-8") as f:
            return f.read().strip()
    except FileNotFoundError:
        return None

@Client.on_message(fox_command(command="speedconfig", module_name="SpeedTest", filename=os.path.basename(__file__), arguments="en/ru/uk") & fox_sudo())
async def speed_config(client, message):
    message = await who_message(client, message)
    args = message.text.split()
    if len(args) < 2:
        return await message.edit("🚫 <b>Использование:</b> <code>speedconfig [en/ru/uk]</code>")
    
    language = args[1].lower()
    if language not in ["en", "ru", "uk"]:
        return await message.edit("🚫 <b>Язык должен быть en, ru или uk</b>")
    
    with open("userdata/speedtest_language", "w", encoding="utf-8") as f:
        f.write(language)
    
    await message.edit(f"✅ <b>Язык сохранен:</b> <code>{language}</code>")

def format_speed(bytes_per_sec):
    if bytes_per_sec <= 0:
        return "0 Mbps"
    mbits = (bytes_per_sec * 8) / (1024 * 1024)
    return f"{mbits:.1f} Mbps" if mbits >= 1 else f"{mbits * 1000:.1f} Kbps"

async def upload_test(session):
    url = "https://speed.cloudflare.com/__up"
    try:
        data = b"0" * (1024 * 1024 * 10)  # 10 MB
        start = time.time()
        async with session.post(url, data=data) as response:
            await response.read()
        duration = time.time() - start
        return len(data) / duration if duration > 0 else 0
    except:
        return 0

async def measure_ping(session):
    try:
        start = time.time()
        async with session.get("https://www.google.com") as response:
            await response.read()
        return int((time.time() - start) * 1000)
    except:
        return 0

async def get_network_info(session):
    try:
        async with session.get("https://ipinfo.io/json") as response:
            data = await response.json()
            return {
                "location": f"{data.get('city', 'N/A')}, {data.get('country', 'N/A')}",
                "org": data.get('org', 'N/A').replace('AS', '')
            }
    except:
        return {"location": "N/A", "org": "N/A"}

@Client.on_message(fox_command(command="speedtest", module_name="SpeedTest", filename=os.path.basename(__file__)) & fox_sudo())
async def speedtest_handler(client, message):
    message = await who_message(client, message)
    config = load_config()
    if not config.get("language"):
        return await message.edit("🚫 <b>Язык не установлен!</b>\n\n"
                                f"Используйте: <code>speedconfig [en/ru/uk]</code>")
    
    lang = config["language"]
    strings = {
        "testing_en": "🔄 <b>Testing upload speed...</b>",
        "testing_ru": "🔄 <b>Тестирование отдачи...</b>",
        "testing_uk": "🔄 <b>Тестування віддачі...</b>",
        "error_en": "❌ <b>Test error:</b>\n<code>{}</code>",
        "error_ru": "❌ <b>Ошибка при тестировании:</b>\n<code>{}</code>",
        "error_uk": "❌ <b>Помилка тестування:</b>\n<code>{}</code>"
    }
    
    await message.edit(strings.get(f"testing_{lang}", "🔄 <b>Testing...</b>"))
    start_time = time.time()
    
    timeout = aiohttp.ClientTimeout(total=30)
    async with aiohttp.ClientSession(timeout=timeout) as session:
        try:
            network_info = await get_network_info(session)
            ping = await measure_ping(session)
            upload_speed = await upload_test(session)
            duration = time.time() - start_time

            result_template = {
                "en": """<b>📊 Internet Upload Test:</b>

<b>📤 Upload:</b> <code>{}</code>
<b>🕒 Ping:</b> <code>{}</code>

<b>🌐 Server:</b> <code>{}</code>
<b>📡 Provider:</b> <code>{}</code>

<b>⌚️ Test took:</b> <code>{}</code>
<b>📅 Time:</b> <code>{}</code>""",
                "ru": """<b>📊 Тест только отдачи:</b>

<b>📤 Отдача:</b> <code>{}</code>
<b>🕒 Пинг:</b> <code>{}</code>

<b>🌐 Сервер:</b> <code>{}</code>
<b>📡 Провайдер:</b> <code>{}</code>

<b>⌚️ Тест занял:</b> <code>{}</code>
<b>📅 Время:</b> <code>{}</code>""",
                "uk": """<b>📊 Тест лише віддачі:</b>

<b>📤 Віддача:</b> <code>{}</code>
<b>🕒 Пінг:</b> <code>{}</code>

<b>🌐 Сервер:</b> <code>{}</code>
<b>📡 Провайдер:</b> <code>{}</code>

<b>⌚️ Тест тривав:</b> <code>{}</code>
<b>📅 Час:</b> <code>{}</code>"""
            }

            result = result_template.get(lang, result_template["en"]).format(
                format_speed(upload_speed),
                f"{ping}ms",
                network_info["location"],
                network_info["org"],
                f"{duration:.1f} sec",
                datetime.now().strftime("%d.%m.%Y %H:%M:%S")
            )

            await message.edit(result)

        except Exception as e:
            await message.edit(strings.get(f"error_{lang}", "❌ <b>Error:</b>\n<code>{}</code>").format(str(e)))