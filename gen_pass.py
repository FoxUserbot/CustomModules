import string
from random import choice
from pyrogram import Client, filters
from command import fox_command
import os

@Client.on_message(fox_command('gen_password', 'GeneratePassword', os.path.basename(__file__), "[length]") & filters.me)
async def gen_pass(client, message):
    try:
        char = message.command[1]
        alphabet = string.ascii_letters + string.digits
        password = ''
        for _ in range(int(char)):
            password = password + choice(alphabet)
        await message.edit(f"**Generated password:** {password}`")
    except ValueError:
        await message.edit(f'Input a number!')
    except IndexError:
        await message.edit(f'Not input a argument!')
