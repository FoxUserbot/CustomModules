from random import randint, choice
from time import sleep
from pyrogram import Client, filters
from command import fox_command, fox_sudo, who_message
import os

@Client.on_message(fox_command("stream", "Stream", os.path.basename(__file__)) & fox_sudo())
async def stream_kangel(client, message):
    message = await who_message(client, message)
    actions = ['💵 Получаем донат!','🛍 Делаем обзор...','💻 Играем в игру','🍰 Кушаем...','💊 Принимаем Эмбиан...']
    try:
        await message.edit('💅 Перевоплощаемся!')
        sleep(2)
        await message.edit('⌨️ Запускаем стрим...')
        for _ in range(2):
            sleep(2)
            c = choice(actions)
            await message.edit(c)
            actions.remove(c)
        num_subs = randint(100,1000)
        await message.edit('❤️ Отключаем стрим и прощаемся с отаку...')
        sleep(2)
        await message.edit(f'''
			👋 Стрим окончен!
			Вы получили {num_subs} новых подписчиков.
			''')
    except Exception as e:
        await client.send_message(message.chat.id, f'❌ Случилась ошибка! | {e}')
