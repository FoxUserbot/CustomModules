from pyrogram import Client, filters
from pyrogram.types import Message
from command import fox_command
import os

@Client.on_message(fox_command("user_info", "Userinfo", os.path.basename(__file__), "[user_id/@username]") & filters.me)
async def get_user_inf(client: Client, message: Message):
    await message.edit("<code>Receiving the information...</code>")

    if len(message.text.split()) >= 2:
        if message.text.split()[1][0] == '@':
            us = message.text.split()[1]
            user = await client.get_users(us)
            user = user.id
        else:
            try:
                user = message.text.split()[1]
                user = int(user)
            except:
                try:
                    user = message.reply_to_message.from_user.id
                except:
                    user = message.from_user.id
    else:
        try:
            user = message.reply_to_message.from_user.id
        except:
            user = message.from_user.id
    user_info = await client.get_users(user)
    try:
        username = f"@{user_info.username}"
    except:
        username = "None"

    user_info = f"""==========
[$] Username: <b>{username}</b>
[$] Id: <code>{str(user_info.id)}</code>
[$] Bot: <code>{str(user_info.is_bot)}</code>
[$] Scam: <code>{str(user_info.is_scam)}</code>
[$] Name: <code>{str(user_info.first_name)}</code>
</b>"""
    await message.edit(user_info)

@Client.on_message(fox_command("user_info_full", "Userinfo", os.path.basename(__file__), "[user_id/@username]") & filters.me)
async def get_full_user_inf(client: Client, message: Message):
    await message.edit("<code>Receiving the information...</code>")

    if len(message.text.split()) >= 2:
        if message.text.split()[1][0] == '@':
            us = message.text.split()[1]
            user = await client.get_users(us)
            user = user.id
        else:
            try:
                user = message.text.split()[1]
                user = int(user)
            except:
                try:
                    user = message.reply_to_message.from_user.id
                except:
                    user = message.from_user.id
    else:
        try:
            user = message.reply_to_message.from_user.id
        except:
            user = message.from_user.id

    try:
        user_info = await client.get_users(user)

        try:
            username = f"@{user_info.username}"
        except:
            username = "None"

        user_info = f"""==========
[$] Username: <b>{username}</b>
[$] Mention: <b>{user_info.mention}</b>
[$] Id: <code>{str(user_info.id)}</code>
[$] Bot: <code>{str(user_info.is_bot)}</code>
[$] Scam: <code>{str(user_info.is_scam)}</code>
[$] Name: <code>{str(user_info.first_name)}</code>
[$] Deleted: <code>{str(user_info.is_deleted)}</code>
[$] Contact: <code>{str(user_info.is_contact)}</code>
[$] Mutual contact: <code>{str(user_info.is_mutual_contact)}</code>
[$] Verified: <code>{str(user_info.is_verified)}</code>
[$] DC: <code>{str(user_info.dc_id)}</code>"""
        await message.edit(user_info)
    except Exception as f:
        await message.edit(f"**An error occured...**\n\n{f}")
