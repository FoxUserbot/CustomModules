import subprocess
import time
import asyncio
from pyrogram import Client, filters
from command import fox_command
from requirements_installer import install_library
import os

install_library("db0mb3r -U") 

@Client.on_message(fox_command("bomber", "Db0mb3r", os.path.basename(__file__)) & filters.me)
async def b0mb3r(client, message):
    await message.edit("Starting dbomber")
    global bomber

    bomber = subprocess.Popen(["db0mb3r"], stdout=subprocess.PIPE)
    await asyncio.sleep(5)
    await message.edit("Bomber started![localhost]\nLink: 127.0.0.1:8080")

@Client.on_message(fox_command("sbomber", "Db0mb3r", os.path.basename(__file__)) & filters.me)
async def sbomber(client, message):
    bomber.terminate()
    await message.edit("dbomber stopped!")