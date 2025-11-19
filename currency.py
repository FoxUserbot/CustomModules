# Ported With Wine Hikka
# Original Code:  https://mods.xdesai.top/currency.py
import asyncio
import os
import json
from pyrogram import Client, filters
from command import fox_command, fox_sudo, who_message, get_text, get_global_lang, set_global_lang
from requirements_installer import install_library
install_library("aiohttp -U")
import aiohttp

filename = os.path.basename(__file__)
Module_Name = "Currency"

LANGUAGES = {
    "en": {
        "rate": "<b>Rates for {amount} {currency}:\n<blockquote expandable>{rates}</blockquote></b>",
        "err": "Error: <code>{error}</code>",
        "currency": "{cur}: {converted}",
        "invalid_args": "<emoji id=5017058788604117831>❌</emoji> <b>Invalid args</b>",
    },
    "ru": {
        "rate": "<b>Курсы для {amount} {currency}:\n<blockquote expandable>{rates}</blockquote></b>",
        "err": "Ошибка: <code>{error}</code>",
        "currency": "{cur}: {converted}",
        "invalid_args": "<emoji id=5017058788604117831>❌</emoji> <b>Неверные аргументы</b>",
    },
    "ua": {
        "rate": "<b>Курси для {amount} {currency}:\n<blockquote expandable>{rates}</blockquote></b>",
        "err": "Помилка: <code>{error}</code>",
        "currency": "{cur}: {converted}",
        "invalid_args": "<emoji id=5017058788604117831>❌</emoji> <b>Невірні аргументи</b>",
    }
}

api_endpoints = [
    "https://open.er-api.com/v6/latest/{}",
]

def load_config():
    try:
        with open("userdata/currency_setting", "r", encoding="utf-8") as f:
            currencies = f.read().strip().split()
            if not currencies:
                currencies = ["PLN", "AZN", "USD", "EUR", "RUB", "UAH"]
    except FileNotFoundError:
        currencies = ["PLN", "AZN", "USD", "EUR", "RUB", "UAH"]
    
    return {"currency": currencies}

@Client.on_message(fox_command("cr", Module_Name, filename, "[amount] [currency]") & fox_sudo())
async def cr_handler(client, message):
    message = await who_message(client, message)
    args = message.text.split()[1:]
    if len(args) < 2:
        text = get_text(Module_Name, "invalid_args", LANGUAGES=LANGUAGES)
        return await message.edit(text)

    try:
        amount = float(args[0])
        base_currency = args[1].upper()
    except Exception as e:
        text = get_text(Module_Name, "err", LANGUAGES=LANGUAGES, error=str(e))
        return await message.edit(text)

    config = load_config()
    
    async with aiohttp.ClientSession() as session:
        rates = await fetch_rates(session, base_currency)
        if not rates:
            text = get_text(Module_Name, "err", LANGUAGES=LANGUAGES, error="Failed to get rates")
            return await message.edit(text)

    result_lines = []
    for cur in config["currency"]:
        cur_up = cur.upper()
        if cur_up == base_currency:
            continue
        else:
            rate = rates.get(cur_up)
            if rate is None:
                converted = "N/A"
            else:
                converted = amount * rate

        if isinstance(converted, float):
            converted_str = f"{converted:.2f}"
        else:
            converted_str = str(converted)

        currency_text = get_text(Module_Name, "currency", LANGUAGES=LANGUAGES, cur=cur_up, converted=converted_str)
        result_lines.append(currency_text)

    text = get_text(Module_Name, "rate", LANGUAGES=LANGUAGES, amount=amount, currency=base_currency, rates="\n".join(result_lines))
    await message.edit(text)

async def fetch_rates(session, base_currency):
    for url in api_endpoints:
        try:
            async with session.get(url.format(base_currency.upper()), timeout=aiohttp.ClientTimeout(total=10)) as response:
                if response.status == 200:
                    data = await response.json()
                    if "rates" in data and data["rates"]:
                        return data["rates"]
                    else:
                        print("No rates in response")
                        return None
                else:
                    print(f"HTTP {response.status}")
                    return None
        except Exception as e:
            print(f"API error ({url.format(base_currency.upper())}): {e}")
            return None

@Client.on_message(fox_command("currency_config", Module_Name, filename, "[currencies]") & fox_sudo())
async def currency_config(client, message):
    message = await who_message(client, message)
    args = message.text.split()[1:]
    if len(args) < 1:
        config = load_config()
        currencies = " ".join(config["currency"])
        text = get_text(Module_Name, "current_currencies", LANGUAGES=LANGUAGES, currencies=currencies)
        return await message.edit(text)

    currencies = args[0].split()
    
    with open("userdata/currency_setting", "w", encoding="utf-8") as f:
        f.write(" ".join(currencies))
    
    text = get_text(Module_Name, "config_saved", LANGUAGES=LANGUAGES, currencies=" ".join(currencies))
    await message.edit(text)
