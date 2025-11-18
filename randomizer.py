import asyncio
import os
import random
from pyrogram import Client, filters
from command import fox_command, fox_sudo, who_message, my_prefix

def load_config():
    try:
        with open("userdata/randomizer_min", "r", encoding="utf-8") as f:
            min_value = f.read().strip()
    except FileNotFoundError:
        min_value = None
    
    try:
        with open("userdata/randomizer_max", "r", encoding="utf-8") as f:
            max_value = f.read().strip()
    except FileNotFoundError:
        max_value = None
    
    return {"min_value": int(min_value) if min_value else None, "max_value": int(max_value) if max_value else None}

@Client.on_message(fox_command("rnd", "Randomizer", os.path.basename(__file__), "[min] [max]") & fox_sudo())
async def rnd_handler(client, message):
    message = await who_message(client, message)
    args = message.text.split()[1:]
    
    if len(args) == 2:
        try:
            min_value = int(args[0])
            max_value = int(args[1])
        except ValueError:
            return await message.edit("🚫 Пожалуйста, введите два целых числа.")
    else:
        config = load_config()
        min_value = config["min_value"]
        max_value = config["max_value"]
    
    if min_value is None or max_value is None:
        return await message.edit("🚫 Необходимо указать диапазон чисел в аргументах команды или в конфигурации модуля.")
    
    if min_value > max_value:
        return await message.edit("🚫 Минимальное значение не может быть больше максимального.")
    
    random_number = random.randint(min_value, max_value)
    await message.edit(f"✅ Случайное число между <code>{min_value}</code> и <code>{max_value}</code>: <code>{random_number}</code>")

@Client.on_message(fox_command("randomizer_config", "Randomizer", os.path.basename(__file__), "[min] [max]") & fox_sudo())
async def randomizer_config_handler(client, message):
    message = await who_message(client, message)
    args = message.text.split()[1:]
    
    if len(args) != 2:
        return await message.edit(f"🚫 Использование: <code>{my_prefix()}randomizer_config [MIN] [MAX]</code>")
    
    try:
        min_value = int(args[0])
        max_value = int(args[1])
    except ValueError:
        return await message.edit("🚫 Пожалуйста, введите два целых числа.")
    
    if min_value > max_value:
        return await message.edit("🚫 Минимальное значение не может быть больше максимального.")
    
    with open("userdata/randomizer_min", "w", encoding="utf-8") as f:
        f.write(str(min_value))
    
    with open("userdata/randomizer_max", "w", encoding="utf-8") as f:
        f.write(str(max_value))
    
    await message.edit(f"✅ Конфигурация сохранена: <code>{min_value} - {max_value}</code>")