import asyncio
import json
import random
from random import choice
from pyrogram import Client, filters
from command import fox_command
from requirements_installer import install_library
import os

install_library("aiohttp -U")

import aiohttp

@Client.on_message(fox_command("rfact", "HistoryFacts", os.path.basename(__file__)) & filters.me)
async def rfact(client, message):
    url = "https://raw.githubusercontent.com/KorenbZla/HikkaModules/main/HistoryFacts.json"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                response_text = await response.text()
                try:
                    data = json.loads(response_text)
                    if "RandomFact" in data and isinstance(data["RandomFact"], list) and data["RandomFact"]:
                        text = choice(data["RandomFact"])
                        await message.edit(
                            "<b><emoji id=5386596911463541476>📚</emoji> Random interesting fact about the Great Patriotic War:\n{}</b>".format(
                                text))
                    else:
                        await message.edit(
                            "<b><i>Error: Key not found.</i></b>")
                except json.JSONDecodeError:
                    await message.edit(
                        "<b><i>Error: The JSON could not be decoded.</i></b>")
            else:
                await message.edit(
                    "<b><i>Error loading data</i></b>: {}".format(response.status))

@Client.on_message(fox_command("hfact", "HistoryFacts", os.path.basename(__file__)) & filters.me)
async def hfact(client, message):
    url = "https://raw.githubusercontent.com/KorenbZla/HikkaModules/main/HistoryFacts.json"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                response_text = await response.text()
                try:
                    data = json.loads(response_text)
                    if "AdolfFact" in data and isinstance(data["AdolfFact"], list) and data["AdolfFact"]:
                        text = choice(data["AdolfFact"])
                        await message.edit(
                            "<b><emoji id=5386596911463541476>📚</emoji> Random fact about Adolf Hitler:\n{}</b>".format(
                                text))
                    else:
                        await message.edit(
                            "<b><i>Error: Key not found.</i></b>")
                except json.JSONDecodeError:
                    await message.edit(
                        "<b><i>Error: The JSON could not be decoded.</i></b>")
            else:
                await message.edit(
                    "<b><i>Error loading data</i></b>: {}".format(response.status))

@Client.on_message(fox_command("mfact", "HistoryFacts", os.path.basename(__file__)) & filters.me)
async def mfact(client, message):
    url = "https://raw.githubusercontent.com/KorenbZla/HikkaModules/main/HistoryFacts.json"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                response_text = await response.text()
                try:
                    data = json.loads(response_text)
                    if "MussoliniFact" in data and isinstance(data["MussoliniFact"], list) and data["MussoliniFact"]:
                        text = choice(data["MussoliniFact"])
                        await message.edit(
                            "<b><emoji id=5386596911463541476>📚</emoji> Random fact about Benito Mussolini:\n{}</b>".format(
                                text))
                    else:
                        await message.edit(
                            "<b><i>Error: Key not found.</i></b>")
                except json.JSONDecodeError:
                    await message.edit(
                        "<b><i>Error: The JSON could not be decoded.</i></b>")
            else:
                await message.edit(
                    "<b><i>Error loading data</i></b>: {}".format(response.status))

@Client.on_message(fox_command("sfact", "HistoryFacts", os.path.basename(__file__)) & filters.me)
async def sfact(client, message):
    url = "https://raw.githubusercontent.com/KorenbZla/HikkaModules/main/HistoryFacts.json"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                response_text = await response.text()
                try:
                    data = json.loads(response_text)
                    if "StalinFact" in data and isinstance(data["StalinFact"], list) and data["StalinFact"]:
                        text = choice(data["StalinFact"])
                        await message.edit(
                            "<b><emoji id=5386596911463541476>📚</emoji> Random fact about Iosif Stalin:\n{}</b>".format(
                                text))
                    else:
                        await message.edit(
                            "<b><i>Error: Key not found.</i></b>")
                except json.JSONDecodeError:
                    await message.edit(
                        "<b><i>Error: The JSON could not be decoded.</i></b>")
            else:
                await message.edit(
                    "<b><i>Error loading data</i></b>: {}".format(response.status))