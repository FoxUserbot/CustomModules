# Port With Wine Hikka
# Original Code By https://mods.xdesai.top/url.py
import asyncio
import os
import socket
from pyrogram import Client, filters
from command import fox_command, fox_sudo, who_message, get_text

from requirements_installer import install_library
install_library("aiohttp aiodns -U")
import aiohttp
import aiodns

filename = os.path.basename(__file__)
Module_Name = "URLModule"

LANGUAGES = {
    "en": {
        "no_url": "<emoji id=5416076321442777828>❌</emoji> <b>Please provide a shortened URL to expand.</b>",
        "err": '<emoji id=5416076321442777828>❌</emoji> <b>An error occurred:</b> <pre><code class="language-Error">{err}</code></pre>',
        "expanded_url": "<emoji id=5816580359642421388>➡️</emoji> <b>Expanded URL:</b> <a href='{expanded_url}'>{expanded_url}</a>",
        "ip_addr": "<emoji id=5447410659077661506>🌐</emoji> <b>The IP address of {url}:</b> <code>{ip_address}</code>",
    },
    "ru": {
        "no_url": "<emoji id=5416076321442777828>❌</emoji> <b>Пожалуйста, предоставьте сокращённую URL для расширения.</b>",
        "err": '<emoji id=5416076321442777828>❌</emoji> <b>Произошла ошибка:</b> <pre><code class="language-Error">{err}</code></pre>',
        "expanded_url": "<emoji id=5816580359642421388>➡️</emoji> <b>Расширенный URL:</b> <a href='{expanded_url}'>{expanded_url}</a>",
        "ip_addr": "<emoji id=5447410659077661506>🌐</emoji> <b>IP-адрес для {url}:</b> <code>{ip_address}</code>",
    },
    "ua": {
        "no_url": "<emoji id=5416076321442777828>❌</emoji> <b>Будь ласка, надайте скорочену URL для розширення.</b>",
        "err": '<emoji id=5416076321442777828>❌</emoji> <b>Сталася помилка:</b> <pre><code class="language-Error">{err}</code></pre>',
        "expanded_url": "<emoji id=5816580359642421388>➡️</emoji> <b>Розширений URL:</b> <a href='{expanded_url}'>{expanded_url}</a>",
        "ip_addr": "<emoji id=5447410659077661506>🌐</emoji> <b>IP-адрес для {url}:</b> <code>{ip_address}</code>",
    }
}

@Client.on_message(fox_command("expandurl", Module_Name, filename, "[URL]") & fox_sudo())
async def expandurl_handler(client, message):
    message = await who_message(client, message)
    args = message.text.split(maxsplit=1)
    if len(args) < 2:
        text = get_text(Module_Name, "no_url", LANGUAGES=LANGUAGES)
        return await message.edit(text)
    
    short_url = args[1].strip()
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
        }
        async with aiohttp.ClientSession(headers=headers) as session:
            async with session.get(short_url, allow_redirects=True) as response:
                response.raise_for_status()
                expanded_url = str(response.url)
                text = get_text(Module_Name, "expanded_url", LANGUAGES=LANGUAGES, expanded_url=expanded_url)
                await message.edit(text)
    except aiohttp.ClientError as e:
        text = get_text(Module_Name, "err", LANGUAGES=LANGUAGES, err=e)
        await message.edit(text)

@Client.on_message(fox_command("ipurl", Module_Name, filename, "[URL]") & fox_sudo())
async def ipurl_handler(client, message):
    message = await who_message(client, message)
    args = message.text.split(maxsplit=1)
    if len(args) < 2:
        text = get_text(Module_Name, "no_url", LANGUAGES=LANGUAGES)
        return await message.edit(text)
    
    url = args[1].strip()
    resolver = aiodns.DNSResolver()

    try:
        hostname = url.split("//")[-1].split("/")[0]
        response = await resolver.gethostbyname(hostname, socket.AF_INET)
        ip_address = response.addresses[0]
        text = get_text(Module_Name, "ip_addr", LANGUAGES=LANGUAGES, url=url, ip_address=ip_address)
        await message.edit(text)
    except aiodns.error.DNSError as e:
        text = get_text(Module_Name, "err", LANGUAGES=LANGUAGES, err=e)
        await message.edit(text)
