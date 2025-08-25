import string
from random import choice
from pyrogram import Client, filters
from command import fox_command, fox_sudo, who_message
import os

@Client.on_message(fox_command('gen_password', 'GeneratePassword', os.path.basename(__file__), "[length]") & fox_sudo())
async def gen_pass(client, message):
    message = await who_message(client, message)
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
