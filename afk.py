import asyncio
import datetime
from pyrogram import Client, filters, types
from command import fox_command
import os

afk_info = {
    "start": datetime.datetime.now(),
    "is_afk": False,
    "reason": "",
}

is_afk = filters.create(lambda _, __, ___: afk_info["is_afk"])

@Client.on_message(is_afk & ~filters.me & ((filters.private & ~filters.bot) | (filters.mentioned & filters.group)))
async def afk_handler(_, message: types.Message):
    end = datetime.datetime.now().replace(microsecond=0)
    afk_time = end - afk_info["start"]
    await message.reply_text(
        f"❕ This user <b>AFK</b>.\n💬 Reason:</b> <i>{afk_info['reason']}</i>\n<b>⏳ Duration:</b> {afk_time}"
    )

@Client.on_message(fox_command("afk", "AFK", os.path.basename(__file__), "[reason]") & filters.me)
async def afk(_, message):
    if len(message.text.split()) >= 2:
        reason = ' '.join(message.text.split()[1:])
    else:
        reason = "None"

    afk_info["start"] = datetime.datetime.now().replace(microsecond=0)
    afk_info["is_afk"] = True
    afk_info["reason"] = reason

    await message.edit(f"❕ I'm going <b>AFK</b>.\n<b>💬 Reason:</b> <i>{reason}</i>.")

@Client.on_message(fox_command("unafk", "AFK", os.path.basename(__file__)) & filters.me)
async def unafk(_, message):
    if afk_info["is_afk"]:
        end = datetime.datetime.now().replace(microsecond=0)
        afk_time = end - afk_info["start"]
        await message.edit(f"<b>❕ I'm not <b>AFK</b> anymore.\n" f"⏳ I was <b>AFK:</b> {afk_time}")
        afk_info["is_afk"] = False
    else:
        await message.edit("<b>❌ You weren't afk</b>")
