# Port With Wine Hikka
# Original Code By https://mods.xdesai.top/stats.py
import asyncio
import os
from pyrogram import Client
from pyrogram.enums import ChatType
from command import fox_command, fox_sudo, who_message, get_text

filename = os.path.basename(__file__)
Module_Name = "Stats"

LANGUAGES = {
    "en": {
        "stats": """
<emoji id=5774022692642492953>✅</emoji><b> Account Statistics</b>

</b><emoji id=5208454037531280484>💜</emoji><b> Total chats: </b><code>{all_chats}</code><b>

</b><emoji id=6035084557378654059>👤</emoji><b> Private chats: </b><code>{users}</code><b>
</b><emoji id=6030400221232501136>🤖</emoji><b> Bots: </b><code>{bots}</code><b>
</b><emoji id=6032609071373226027>👥</emoji><b> Groups: </b><code>{groups}</code><b>
</b><emoji id=5870886806601338791>👥</emoji><b> Channels: </b><code>{channels}</code><b>
</b><emoji id=5870563425628721113>📨</emoji><b> Archived chats: </b><code>{archived}</code>""",
        "loading_stats": "<b><emoji id=5309893756244206277>🫥</emoji> Loading statistics...</b>",
    },
    "ru": {
        "stats": """
<emoji id=5774022692642492953>✅</emoji><b> Статистика аккаунта

</b><emoji id=5208454037531280484>💜</emoji><b> Всего чатов: </b><code>{all_chats}</code><b>

</b><emoji id=6035084557378654059>👤</emoji><b> Личных чатов: </b><code>{users}</code><b>
</b><emoji id=6030400221232501136>🤖</emoji><b> Ботов: </b><code>{bots}</code><b>
</b><emoji id=6032609071373226027>👥</emoji><b> Групп: </b><code>{groups}</code><b>
</b><emoji id=5870886806601338791>👥</emoji><b> Каналов: </b><code>{channels}</code><b>
</b><emoji id=5870563425628721113>📨</emoji><b> Архивированных чатов: </b><code>{archived}</code>""",
        "loading_stats": "<b><emoji id=5309893756244206277>🫥</emoji> Загрузка статистики...</b>",
    },
    "ua": {
        "stats": """
<emoji id=5774022692642492953>✅</emoji><b> Статистика аккаунта

</b><emoji id=5208454037531280484>💜</emoji><b> Всього чатів: </b><code>{all_chats}</code><b>

</b><emoji id=6035084557378654059>👤</emoji><b> Особистих чатів: </b><code>{users}</code><b>
</b><emoji id=6030400221232501136>🤖</emoji><b> Ботів: </b><code>{bots}</code><b>
</b><emoji id=6032609071373226027>👥</emoji><b> Груп: </b><code>{groups}</code><b>
</b><emoji id=5870886806601338791>👥</emoji><b> Каналів: </b><code>{channels}</code><b>
</b><emoji id=5870563425628721113>📨</emoji><b> Архівованих чатів: </b><code>{archived}</code>""",
        "loading_stats": "<b><emoji id=5309893756244206277>🫥</emoji> Завантаження статистики...</b>",
    }
}

@Client.on_message(fox_command("stats_xdesai", Module_Name, filename) & fox_sudo())
async def stats_handler(client, message):
    message = await who_message(client, message)

    loading_text = get_text(Module_Name, "loading_stats", LANGUAGES=LANGUAGES)
    await message.edit(loading_text)
    
    users = 0
    bots = 0
    groups = 0
    channels = 0
    all_chats = 0
    archived = 0
    

    async for dialog in client.get_dialogs():
        chat = dialog.chat
        if chat.is_forum and dialog.top_message and dialog.top_message.id == 0:
            archived += 1
        if chat.type == ChatType.BOT:
            bots += 1
            all_chats += 1
        elif chat.type == ChatType.PRIVATE:
            users += 1
            all_chats += 1
        elif chat.type == ChatType.GROUP or chat.type == ChatType.SUPERGROUP:
            groups += 1
            all_chats += 1
        elif chat.type == ChatType.CHANNEL:
            channels += 1
            all_chats += 1
    
    stats_text = get_text(Module_Name, "stats", LANGUAGES=LANGUAGES,
                         users=users, bots=bots, channels=channels, groups=groups,
                         all_chats=all_chats, archived=archived)
    
    await message.edit(stats_text)
