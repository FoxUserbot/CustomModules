from random import randint
from time import sleep
from pyrogram import Client, filters
from command import fox_command, fox_sudo, who_message
from requirements_installer import install_library
import os

install_library('faker')
from faker import Faker

@Client.on_message(fox_command("doxx", "Doxx", os.path.basename(__file__)) & fox_sudo())
async def hack(client, message):
    message = await who_message(client, message)
    fake = Faker('ru_RU')
    await message.edit('Доксим тя пидор')
    if randint(0, 1) == 0:
        name = 'Артур Ламаев'
    else:
        name = fake.name()
    pasta = f'''
Докс на тя:
- - - - - - 
ФИО : {name}
Адрес электронной почты : {fake.email()}
Телефон : {fake.phone_number()}
Адрес регистрации : {fake.street_address()}
Пароль к почте : {fake.password()}
Карта : {fake.credit_card_full()}
Паспорт: {fake.passport_number()}
- - - - - -
Жди докс бошеее
'''
    sleep(2)
    await message.edit(pasta)