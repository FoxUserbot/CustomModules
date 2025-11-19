# Port With Wine Hikka
# Original Code By https://mods.xdesai.top/weather.py


import os
from pyrogram import Client
from command import fox_command, fox_sudo, who_message, get_text
from requirements_installer import install_library
install_library("requests -U")
import requests

def load_config():
    try:
        with open("userdata/weather_setting", "r", encoding="utf-8") as f:
            api_key = f.read().strip()
    except FileNotFoundError:
        api_key = "934e9392018dd900103f54e50b870c02"  
    
    return {"api_key": api_key}

def save_config(api_key):
    with open("userdata/weather_setting", "w", encoding="utf-8") as f:
        f.write(api_key)

LANGUAGES = {
    "en": {
        "weather_info": """<emoji id=5884330496619450755>☁️</emoji> <b>Weather in {city}, {country}:</b>
<emoji id=5199707727475007907>🌡️</emoji> <b>Temperature: {temperature}°C (feels like {feels_like}°C)</b>
<emoji id=6050944866580435869>💧</emoji> <b>Humidity: {humidity}%</b>
<emoji id=5415843564280107382>🌀</emoji> <b>Wind speed: {wind_speed} m/s</b>
<emoji id=5417937876232983047>⛅️</emoji> <b>Sky: {description}</b>""",
        "error": "<b>Error:</b> <code>{e}</code>",
        "api_error": "<b>City not found: {city}\nAPI response:</b> <code>{data}</code>",
        "invalid_args": "<emoji id=5019523782004441717>❌</emoji> <b>Specify the city.</b>",
        "config_saved": "✅ <b>API key saved:</b> <code>{api_key}</code>",
        "current_config": "🔑 <b>Current API key:</b> <code>{api_key}</code>",
        "help_text": """🌤️ <b>Weather Module</b>

<code>weather [city]</code> - Check weather in specified city
<code>weather_config [api_key]</code> - Set OpenWeatherMap API key

API key can be obtained from: https://openweathermap.org/api"""
    },
    "ru": {
        "weather_info": """<emoji id=5884330496619450755>☁️</emoji> <b>Погода в городе {city}, {country}:</b>
<emoji id=5199707727475007907>🌡️</emoji> <b>Температура: {temperature}°C (ощущается как {feels_like}°C)</b>
<emoji id=6050944866580435869>💧</emoji> <b>Влажность: {humidity}%</b>
<emoji id=5415843564280107382>🌀</emoji> <b>Скорость ветра: {wind_speed} м/с</b>
<emoji id=5417937876232983047>⛅️</emoji> <b>Небо: {description}</b>""",
        "error": "<b>Ошибка:</b> <code>{e}</code>",
        "api_error": "<b>Город не найден: {city}\nОтвет API:</b> <code>{data}</code>",
        "invalid_args": "<emoji id=5019523782004441717>❌</emoji> <b>Укажите город.</b>",
        "config_saved": "✅ <b>API ключ сохранен:</b> <code>{api_key}</code>",
        "current_config": "🔑 <b>Текущий API ключ:</b> <code>{api_key}</code>",
        "help_text": """🌤️ <b>Модуль погоды</b>

<code>weather [city]</code> - Проверить погоду в указанном городе
<code>weather_config [api_key]</code> - Установить API ключ OpenWeatherMap

API ключ можно получить здесь: https://openweathermap.org/api"""
    },
    "ua": {
        "weather_info": """<emoji id=5884330496619450755>☁️</emoji> <b>Погода у місті {city}, {country}:</b>
<emoji id=5199707727475007907>🌡️</emoji> <b>Температура: {temperature}°C (відчувається як {feels_like}°C)</b>
<emoji id=6050944866580435869>💧</emoji> <b>Вологість: {humidity}%</b>
<emoji id=5415843564280107382>🌀</emoji> <b>Швидкість вітру: {wind_speed} м/с</b>
<emoji id=5417937876232983047>⛅️</emoji> <b>Небо: {description}</b>""",
        "error": "<b>Помилка:</b> <code>{e}</code>",
        "api_error": "<b>Місто не знайдено: {city}\nВідповідь API:</b> <code>{data}</code>",
        "invalid_args": "<emoji id=5019523782004441717>❌</emoji> <b>Вкажіть місто.</b>",
        "config_saved": "✅ <b>API ключ збережено:</b> <code>{api_key}</code>",
        "current_config": "🔑 <b>Поточний API ключ:</b> <code>{api_key}</code>",
        "help_text": """🌤️ <b>Модуль погоди</b>

<code>weather [city]</code> - Перевірити погоду в указаному місті
<code>weather_config [api_key]</code> - Встановити API ключ OpenWeatherMap

API ключ можна отримати тут: https://openweathermap.org/api"""
    }
}

filename = os.path.basename(__file__)
Module_Name = "Weather"

@Client.on_message(fox_command("weather", Module_Name, filename, "[city]") & fox_sudo())
async def weather_handler(client, message):
    message = await who_message(client, message)
    
    args = message.text.split()
    if len(args) < 2:
        text = get_text(Module_Name, "invalid_args", LANGUAGES=LANGUAGES)
        return await message.edit(text)
    
    city = " ".join(args[1:])
    config = load_config()
    api_key = config["api_key"]
    
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric&lang=en"
    
    try:
        response = requests.get(url)
        data = response.json()
        
        if data.get("cod") != 200:
            text = get_text(Module_Name, "api_error", LANGUAGES=LANGUAGES, city=city, data=str(data))
            return await message.edit(text)

        country = data["sys"]["country"]
        weather_data = data["main"]
        temperature = weather_data["temp"]
        feels_like = weather_data["feels_like"]
        wind_speed = data["wind"]["speed"]
        humidity = weather_data["humidity"]
        description = data["weather"][0]["description"].capitalize()
        
        text = get_text(Module_Name, "weather_info", LANGUAGES=LANGUAGES,
                       city=city.capitalize(),
                       country=country,
                       description=description,
                       temperature=temperature,
                       feels_like=feels_like,
                       humidity=humidity,
                       wind_speed=wind_speed)
        
        await message.edit(text)
        
    except Exception as e:
        text = get_text(Module_Name, "error", LANGUAGES=LANGUAGES, e=str(e))
        await message.edit(text)

@Client.on_message(fox_command("weather_config", Module_Name, filename, "[api_key]") & fox_sudo())
async def weather_config_handler(client, message):
    message = await who_message(client, message)
    
    args = message.text.split()
    if len(args) < 2:
        config = load_config()
        text = get_text(Module_Name, "current_config", LANGUAGES=LANGUAGES, api_key=config["api_key"])
        return await message.edit(text)
    
    api_key = args[1]
    save_config(api_key)
    
    text = get_text(Module_Name, "config_saved", LANGUAGES=LANGUAGES, api_key=api_key)
    await message.edit(text)

@Client.on_message(fox_command("weather_help", Module_Name, filename) & fox_sudo())
async def weather_help_handler(client, message):
    message = await who_message(client, message)
    
    text = get_text(Module_Name, "help_text", LANGUAGES=LANGUAGES)
    await message.edit(text)
