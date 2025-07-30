from pyrogram import Client, filters
from command import fox_command
import os

i = filters.user([])

@Client.on_message(i & ~filters.me)
async def ignored(client, message):
    await message.delete()

@Client.on_message(fox_command("ignore", "IgnoreUser", os.path.basename(__file__), "[user_id/@username]") & filters.me)
async def add_ignore(client, message):
    try:
        try:
            users = int(message.command[1])
        except:
            users = str(message.command[1]).replace("@", "")
            users = int((await client.get_users(str(users))).id)
    except:
        users = message.reply_to_message.from_user.id

    print(users)

    if users in i:
        i.remove(int(users))
        await message.edit(f"`{str(users)}` no longer ignored")
    else:
        i.add(int(users))
        await message.edit(f"`{str(users)}` ignored")
