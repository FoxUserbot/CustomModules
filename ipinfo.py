#Ported With Wine Hikka
# Original Code By https://mods.xdesai.top/ipinfo.py
import os
import re
from requirements_installer import install_library
install_library("requests -U")
import requests

from pyrogram import Client, filters
from command import fox_command, fox_sudo, who_message, get_text, get_global_lang, set_global_lang

filename = os.path.basename(__file__)
Module_Name = "IPInfo"

LANGUAGES = {
    "en": {
        "invalid_ip": "❌ <b>Specify IP address</b>",
        "no_data": "😢 <b>No data available</b>",
        "data": "<blockquote><emoji id=5447410659077661506>🌐</emoji><b> Information about IP</b></blockquote>\n<blockquote><emoji id=6334617384782923882>📟</emoji><b> IP: <code>{ip}</code></b></blockquote>\n<blockquote><emoji id=5235794253149394263>🗺</emoji><b> Country: {country}</b></blockquote>\n<blockquote><emoji id=5247209275494769660>🕓</emoji><b> Timezone: {timezone}</b></blockquote>\n<blockquote><emoji id=5330371855368866588>🌇</emoji><b> City: {city}</b></blockquote>\n<blockquote><emoji id=5308028293033764449>⚡️</emoji><b> Region: {region}</b></blockquote>\n<blockquote><emoji id=5391032818111363540>📍</emoji><b> Coordinates: <code>{coordinates}</code></b></blockquote>\n<blockquote><emoji id=5447410659077661506>🌐</emoji> <b>Provider: {provider}</b></blockquote>",
    },
    "ru": {
        "invalid_ip": "❌ <b>Укажите ip адрес</b>",
        "no_data": "😢 <b>Нет данных</b>",
        "data": "<blockquote><emoji id=5447410659077661506>🌐</emoji><b> Информация об IP</b></blockquote>\n<blockquote><emoji id=6334617384782923882>📟</emoji><b> IP: <code>{ip}</code></b></blockquote>\n<blockquote><emoji id=5235794253149394263>🗺</emoji><b> Страна: {country}</b></blockquote>\n<blockquote><emoji id=5247209275494769660>🕓</emoji><b> Часовой пояс: {timezone}</b></blockquote>\n<blockquote><emoji id=5330371855368866588>🌇</emoji><b> Город: {city}</b></blockquote>\n<blockquote><emoji id=5308028293033764449>⚡️</emoji><b> Регион: {region}</b></blockquote>\n<blockquote><emoji id=5391032818111363540>📍</emoji><b> Координаты: <code>{coordinates}</code></b></blockquote>\n<blockquote><emoji id=5447410659077661506>🌐</emoji> <b>Провайдер: {provider}</b></blockquote>",
    },
    "ua": {
        "invalid_ip": "❌ <b>Вкажіть ip адресу</b>",
        "no_data": "😢 <b>Немає даних</b>",
        "data": "<blockquote><emoji id=5447410659077661506>🌐</emoji><b> Інформація про IP</b></blockquote>\n<blockquote><emoji id=6334617384782923882>📟</emoji><b> IP: <code>{ip}</code></b></blockquote>\n<blockquote><emoji id=5235794253149394263>🗺</emoji><b> Країна: {country}</b></blockquote>\n<blockquote><emoji id=5247209275494769660>🕓</emoji><b> Часовий пояс: {timezone}</b></blockquote>\n<blockquote><emoji id=5330371855368866588>🌇</emoji><b> Місто: {city}</b></blockquote>\n<blockquote><emoji id=5308028293033764449>⚡️</emoji><b> Регіон: {region}</b></blockquote>\n<blockquote><emoji id=5391032818111363540>📍</emoji><b> Координати: <code>{coordinates}</code></b></blockquote>\n<blockquote><emoji id=5447410659077661506>🌐</emoji> <b>Провайдер: {provider}</b></blockquote>",
    }
}

def is_valid_ip(ip):
    """Перевірка валідності IP-адреси"""
    ipv4_pattern = re.compile(r'^(\d{1,3}\.){3}\d{1,3}$')
    ipv6_pattern = re.compile(r'^([0-9a-fA-F]{1,4}:){7}[0-9a-fA-F]{1,4}$')
    
    if ipv4_pattern.match(ip):
        parts = ip.split('.')
        return all(0 <= int(part) <= 255 for part in parts)
    elif ipv6_pattern.match(ip):
        return True
    return False

async def get_location_by_ip(ip_address):
    """Отримання географічної інформації за IP-адресою"""
    url = f"http://ip-api.com/json/{ip_address}"
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            data = response.json()
            if data.get("status") == "fail":
                return get_text(Module_Name, "no_data", LANGUAGES=LANGUAGES)
            else:
                return get_text(Module_Name, "data", LANGUAGES=LANGUAGES,
                              ip=data.get("query", ""),
                              country=data.get("country", ""),
                              timezone=data.get("timezone", ""),
                              city=data.get("city", ""),
                              region=data.get("regionName", ""),
                              coordinates=f"{data.get('lat', '')}, {data.get('lon', '')}",
                              provider=data.get("isp", ""))
        else:
            return get_text(Module_Name, "no_data", LANGUAGES=LANGUAGES)
    except Exception:
        return get_text(Module_Name, "no_data", LANGUAGES=LANGUAGES)

@Client.on_message(fox_command("ipi", Module_Name, filename, "[ip]") & fox_sudo())
async def ipi_handler(client, message):
    message = await who_message(client, message)
    args = message.text.split()
    if len(args) < 2:
        return await message.edit(get_text(Module_Name, "invalid_ip", LANGUAGES=LANGUAGES))
    
    ip = args[1].strip()
    if not is_valid_ip(ip):
        return await message.edit(get_text(Module_Name, "invalid_ip", LANGUAGES=LANGUAGES))
    
    result = await get_location_by_ip(ip)
    await message.edit(result)

@Client.on_message(fox_command("ipinfo", Module_Name, filename, "[ip]") & fox_sudo())
async def ipinfo_handler(client, message):
    message = await who_message(client, message)
    args = message.text.split()
    if len(args) < 2:
        return await message.edit(get_text(Module_Name, "invalid_ip", LANGUAGES=LANGUAGES))
    
    ip = args[1].strip()
    if not is_valid_ip(ip):
        return await message.edit(get_text(Module_Name, "invalid_ip", LANGUAGES=LANGUAGES))
    
    result = await get_location_by_ip(ip)
    await message.edit(result)