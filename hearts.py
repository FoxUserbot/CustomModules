# By AmokDev
# Refactor and optimising A9FM
# https://github.com/AmokDEV/lordnet/blob/main/modules/hearts.py

import asyncio
import random
from pyrogram import Client, filters
from command import fox_command, fox_sudo, who_message
from pyrogram.errors.exceptions.flood_420 import FloodWait
import os

R = "❤️"
W = "🤍"

heart_list = [
    W * 9,
    W * 2 + R * 2 + W + R * 2 + W * 2,
    W + R * 7 + W,
    W + R * 7 + W,
    W + R * 7 + W,
    W * 2 + R * 5 + W * 2,
    W * 3 + R * 3 + W * 3,
    W * 4 + R + W * 4,
    W * 9,
]
joined_heart = "\n".join(heart_list)
heartlet_len = joined_heart.count(R)
SLEEP = 0.1

async def _wrap_edit(message, text: str):
    try:
        await message.edit(text)
    except FloodWait as fl:
        await asyncio.sleep(fl.x)

async def phase1(message):
    BIG_SCROLL = "🧡💛💚💙💜🖤🤎"
    await _wrap_edit(message, joined_heart)
    for heart in BIG_SCROLL:
        await _wrap_edit(message, joined_heart.replace(R, heart))
        await asyncio.sleep(SLEEP)

async def phase2(message):
    ALL = ["❤️"] + list("🧡💛💚💙💜🤎🖤")

    format_heart = joined_heart.replace(R, "{}")
    for _ in range(5):
        heart = format_heart.format(*random.choices(ALL, k=heartlet_len))
        await _wrap_edit(message, heart)
        await asyncio.sleep(SLEEP)

async def phase3(message):
    await _wrap_edit(message, joined_heart)
    await asyncio.sleep(SLEEP * 2)
    repl = joined_heart
    for _ in range(joined_heart.count(W)):
        repl = repl.replace(W, R, 1)
        await _wrap_edit(message, repl)
        await asyncio.sleep(SLEEP)

async def phase4(message):
    for i in range(7, 0, -1):
        heart_matrix = "\n".join([R * i] * i)
        await _wrap_edit(message, heart_matrix)
        await asyncio.sleep(SLEEP)

@Client.on_message(fox_command(["hearts", "magic", "love"], "Hearts", os.path.basename(__file__)) & fox_sudo())
async def hearts(client, message):
    message = await who_message(client, message)
    await phase1(message)
    await phase2(message)
    await phase3(message)
    await phase4(message)
    await asyncio.sleep(SLEEP * 3)

    await message.edit("**❤️ I**")
    await asyncio.sleep(0.5)
    await message.edit("**❤️ I love**")
    await asyncio.sleep(0.5)
    await message.edit("**❤️ I love you**")
    await asyncio.sleep(3)
    await message.edit("**❤️ I love you <3**")
