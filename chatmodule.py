
import asyncio
import os
import json
import logging
from datetime import datetime, timedelta
from pyrogram import Client, filters
from pyrogram.types import Chat, User, Message, ChatPermissions
from pyrogram.enums import ChatType, ChatMemberStatus, ChatMembersFilter
from command import fox_command, fox_sudo, who_message, my_prefix

logger = logging.getLogger(__name__)

def load_config():
    try:
        with open("userdata/chatmodule_roles", "r", encoding="utf-8") as f:
            return json.loads(f.read().strip())
    except FileNotFoundError:
        return {}

def save_config(roles):
    with open("userdata/chatmodule_roles", "w", encoding="utf-8") as f:
        json.dump(roles, f, ensure_ascii=False, indent=2)

@Client.on_message(fox_command("id", "ChatModule", os.path.basename(__file__), "[reply]") & fox_sudo())
async def id_handler(client, message):
    message = await who_message(client, message)
    ids = []
    
    me = await client.get_me()
    ids.append(f"<b>Ваш ID:</b> <code>{me.id}</code>")
    
    if message.chat.type == ChatType.PRIVATE:
        ids.append(f"<b>Чат ID:</b> <code>{message.chat.id}</code>")
        return await message.edit("\n".join(ids))
    

    ids.append(f"<b>Чат ID:</b> <code>{message.chat.id}</code>")
    

    if message.reply_to_message and message.reply_to_message.from_user.id != me.id:
        user_id = message.reply_to_message.from_user.id
        ids.append(f"<b>ID пользователя:</b> <code>{user_id}</code>")
    
    await message.edit("\n".join(ids))

@Client.on_message(fox_command("rights", "ChatModule", os.path.basename(__file__), "[-u username/id]") & fox_sudo())
async def rights_handler(client, message):
    message = await who_message(client, message)
    if message.chat.type == ChatType.PRIVATE:
        return await message.edit("<b>❌ Эта команда работает только в группах и каналах!</b>")
    
    args = message.text.split()[1:] if len(message.command) > 1 else []
    user = None
    

    for arg in args:
        if arg.startswith("-u") or arg.startswith("username"):
            user = arg.split(" ", 1)[1] if " " in arg else None
            break
    
    if not user and message.reply_to_message:
        user = message.reply_to_message.from_user.id
    
    if not user:
        return await message.edit("<b>❌ Укажите пользователя!</b>")
    
    try:
        user_obj = await client.get_users(user)
        chat_member = await client.get_chat_member(message.chat.id, user_obj.id)
        
        if chat_member.status not in [ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.OWNER]:
            return await message.edit(f"<b>❌ {user_obj.first_name} не является администратором!</b>")
        
        rights = []
        if hasattr(chat_member, 'privileges'):
            privileges = chat_member.privileges
            if privileges.can_manage_chat:
                rights.append("Управление чатом")
            if privileges.can_delete_messages:
                rights.append("Удаление сообщений")
            if privileges.can_manage_video_chats:
                rights.append("Управление видеочатами")
            if privileges.can_restrict_members:
                rights.append("Ограничение участников")
            if privileges.can_promote_members:
                rights.append("Назначение администраторов")
            if privileges.can_change_info:
                rights.append("Изменение информации")
            if privileges.can_invite_users:
                rights.append("Приглашение пользователей")
            if privileges.can_post_messages:
                rights.append("Создание сообщений")
            if privileges.can_edit_messages:
                rights.append("Редактирование сообщений")
            if privileges.can_pin_messages:
                rights.append("Закрепление сообщений")
        
        if not rights:
            rights_text = "Нет специальных прав"
        else:
            rights_text = "\n".join([f"✅ {right}" for right in rights])
        
        rank = chat_member.title if hasattr(chat_member, 'title') and chat_member.title else "Администратор"
        
        await message.edit(f"<b>Права администратора {user_obj.first_name}:</b>\n\n{rights_text}\n\n<b>Должность:</b> {rank}")
        
    except Exception as e:
        logger.error(f"Ошибка при проверке прав: {e}")
        await message.edit("<b>❌ Ошибка при получении информации о пользователе!</b>")

@Client.on_message(fox_command("leave", "ChatModule", os.path.basename(__file__)) & fox_sudo())
async def leave_handler(client, message):
    message = await who_message(client, message)
    if message.chat.type == ChatType.PRIVATE:
        return await message.edit("<b>❌ Эта команда работает только в группах и каналах!</b>")
    
    await message.delete()
    await client.leave_chat(message.chat.id)

@Client.on_message(fox_command("pin", "ChatModule", os.path.basename(__file__), "[reply]") & fox_sudo())
async def pin_handler(client, message):
    message = await who_message(client, message)
    if not message.reply_to_message:
        return await message.edit("<b>❌ Ответьте на сообщение для закрепления!</b>")
    
    try:
        await client.pin_chat_message(
            message.chat.id,
            message.reply_to_message.id,
            disable_notification=False
        )
        await message.edit("<b>✅ Сообщение закреплено!</b>")
    except Exception as e:
        logger.error(f"Ошибка при закреплении: {e}")
        await message.edit("<b>❌ Не удалось закрепить сообщение!</b>")

@Client.on_message(fox_command("unpin", "ChatModule", os.path.basename(__file__), "[reply]") & fox_sudo())
async def unpin_handler(client, message):
    message = await who_message(client, message)
    if not message.reply_to_message:
        return await message.edit("<b>❌ Ответьте на сообщение для открепления!</b>")
    
    try:
        await client.unpin_chat_message(message.chat.id, message.reply_to_message.id)
        await message.edit("<b>✅ Сообщение откреплено!</b>")
    except Exception as e:
        logger.error(f"Ошибка при откреплении: {e}")
        await message.edit("<b>❌ Не удалось открепить сообщение!</b>")

@Client.on_message(fox_command("unpinall", "ChatModule", os.path.basename(__file__)) & fox_sudo())
async def unpinall_handler(client, message):
    message = await who_message(client, message)
    if message.chat.type == ChatType.PRIVATE:
        return await message.edit("<b>❌ Эта команда работает только в группах и каналах!</b>")
    
    try:
        await client.unpin_all_chat_messages(message.chat.id)
        await message.edit("<b>✅ Все сообщения откреплены!</b>")
    except Exception as e:
        logger.error(f"Ошибка при откреплении всех сообщений: {e}")
        await message.edit("<b>❌ Не удалось открепить сообщения!</b>")

@Client.on_message(fox_command("admins", "ChatModule", os.path.basename(__file__)) & fox_sudo())
async def admins_handler(client, message):
    message = await who_message(client, message)
    if message.chat.type == ChatType.PRIVATE:
        return await message.edit("<b>❌ Эта команда работает только в группах и каналах!</b>")
    
    try:
        admins = []
        async for member in client.get_chat_members(message.chat.id, filter=ChatMembersFilter.ADMINISTRATORS):
            if member.status == ChatMemberStatus.OWNER:
                admins.insert(0, f"👑 <a href='tg://user?id={member.user.id}'>{member.user.first_name}</a> | <code>{member.user.id}</code> - Создатель")
            elif member.status == ChatMemberStatus.ADMINISTRATOR:
                rank = member.custom_title if member.custom_title else "Администратор"
                admins.append(f"✅ <a href='tg://user?id={member.user.id}'>{member.user.first_name}</a> | <code>{member.user.id}</code> - {rank}")
        
        if not admins:
            await message.edit("<b>❌ Администраторы не найдены!</b>")
        else:
            await message.edit(f"<b>Список администраторов:</b>\n\n" + "\n".join(admins))
            
    except Exception as e:
        logger.error(f"Ошибка при получении администраторов: {e}")
        await message.edit("<b>❌ Ошибка при получении списка администраторов!</b>")

@Client.on_message(fox_command("ban", "ChatModule", os.path.basename(__file__), "[reply] [время]") & fox_sudo())
async def ban_handler(client, message):
    message = await who_message(client, message)
    if message.chat.type == ChatType.PRIVATE:
        return await message.edit("<b>❌ Эта команда работает только в группах и каналах!</b>")
    
    if not message.reply_to_message:
        return await message.edit("<b>❌ Ответьте на сообщение пользователя для бана!</b>")
    
    user_id = message.reply_to_message.from_user.id
    args = message.text.split()[1:] if len(message.command) > 1 else []
    
    ban_time = None
    time_text = ""
    
    for arg in args:
        if arg.isdigit():
            ban_time = int(arg)
            if ban_time < 60:
                time_text = f"{ban_time} секунд"
            elif ban_time < 3600:
                time_text = f"{ban_time // 60} минут"
            elif ban_time < 86400:
                time_text = f"{ban_time // 3600} часов"
            else:
                time_text = f"{ban_time // 86400} дней"
            break
    
    try:
        user = await client.get_users(user_id)
        
        if ban_time:
            until_date = datetime.now() + timedelta(seconds=ban_time)
            await client.ban_chat_member(
                message.chat.id,
                user_id,
                until_date=until_date
            )
        else:
            await client.ban_chat_member(message.chat.id, user_id)
        
        time_info = f" на {time_text}" if time_text else " навсегда"
        await message.edit(f"<b>✅ Пользователь {user.first_name} забанен{time_info}!</b>")
        
    except Exception as e:
        logger.error(f"Ошибка при бане: {e}")
        await message.edit("<b>❌ Не удалось забанить пользователя!</b>")

@Client.on_message(fox_command("unban", "ChatModule", os.path.basename(__file__), "[reply]") & fox_sudo())
async def unban_handler(client, message):
    message = await who_message(client, message)
    if message.chat.type == ChatType.PRIVATE:
        return await message.edit("<b>❌ Эта команда работает только в группах и каналах!</b>")
    
    if not message.reply_to_message:
        return await message.edit("<b>❌ Ответьте на сообщение пользователя для разбана!</b>")
    
    try:
        user = await client.get_users(message.reply_to_message.from_user.id)
        await client.unban_chat_member(message.chat.id, user.id)
        await message.edit(f"<b>✅ Пользователь {user.first_name} разбанен!</b>")
        
    except Exception as e:
        logger.error(f"Ошибка при разбане: {e}")
        await message.edit("<b>❌ Не удалось разбанить пользователя!</b>")

@Client.on_message(fox_command("kick", "ChatModule", os.path.basename(__file__), "[reply]") & fox_sudo())
async def kick_handler(client, message):
    message = await who_message(client, message)
    if message.chat.type == ChatType.PRIVATE:
        return await message.edit("<b>❌ Эта команда работает только в группах и каналах!</b>")
    
    if not message.reply_to_message:
        return await message.edit("<b>❌ Ответьте на сообщение пользователя для кика!</b>")
    
    try:
        user = await client.get_users(message.reply_to_message.from_user.id)
        await client.ban_chat_member(message.chat.id, user.id)
        await asyncio.sleep(1)
        await client.unban_chat_member(message.chat.id, user.id)
        await message.edit(f"<b>✅ Пользователь {user.first_name} кикнут!</b>")
        
    except Exception as e:
        logger.error(f"Ошибка при кике: {e}")
        await message.edit("<b>❌ Не удалось кикнуть пользователя!</b>")

@Client.on_message(fox_command("mute", "ChatModule", os.path.basename(__file__), "[reply] [время]") & fox_sudo())
async def mute_handler(client, message):
    message = await who_message(client, message)
    if message.chat.type == ChatType.PRIVATE:
        return await message.edit("<b>❌ Эта команда работает только в группах и каналах!</b>")
    
    if not message.reply_to_message:
        return await message.edit("<b>❌ Ответьте на сообщение пользователя для мута!</b>")
    
    user_id = message.reply_to_message.from_user.id
    args = message.text.split()[1:] if len(message.command) > 1 else []
    
    mute_time = None
    time_text = ""
    
    for arg in args:
        if arg.isdigit():
            mute_time = int(arg)
            if mute_time < 60:
                time_text = f"{mute_time} секунд"
            elif mute_time < 3600:
                time_text = f"{mute_time // 60} минут"
            elif mute_time < 86400:
                time_text = f"{mute_time // 3600} часов"
            else:
                time_text = f"{mute_time // 86400} дней"
            break
    
    try:
        user = await client.get_users(user_id)
        permissions = ChatPermissions()
        
        if mute_time:
            until_date = datetime.now() + timedelta(seconds=mute_time)
            await client.restrict_chat_member(
                message.chat.id,
                user_id,
                permissions=permissions,
                until_date=until_date
            )
        else:
            await client.restrict_chat_member(
                message.chat.id,
                user_id,
                permissions=permissions
            )
        
        time_info = f" на {time_text}" if time_text else " навсегда"
        await message.edit(f"<b>✅ Пользователь {user.first_name} замучен{time_info}!</b>")
        
    except Exception as e:
        logger.error(f"Ошибка при муте: {e}")
        await message.edit("<b>❌ Не удалось замутить пользователя!</b>")

@Client.on_message(fox_command("unmute", "ChatModule", os.path.basename(__file__), "[reply]") & fox_sudo())
async def unmute_handler(client, message):
    message = await who_message(client, message)
    if message.chat.type == ChatType.PRIVATE:
        return await message.edit("<b>❌ Эта команда работает только в группах и каналах!</b>")
    
    if not message.reply_to_message:
        return await message.edit("<b>❌ Ответьте на сообщение пользователя для размута!</b>")
    
    try:
        user = await client.get_users(message.reply_to_message.from_user.id)
        permissions = ChatPermissions(
            can_send_messages=True,
            can_send_media_messages=True,
            can_send_other_messages=True,
            can_add_web_page_previews=True
        )
        await client.restrict_chat_member(
            message.chat.id,
            user.id,
            permissions=permissions
        )
        await message.edit(f"<b>✅ Пользователь {user.first_name} размучен!</b>")
        
    except Exception as e:
        logger.error(f"Ошибка при размуте: {e}")
        await message.edit("<b>❌ Не удалось размутить пользователя!</b>")

@Client.on_message(fox_command("rename", "ChatModule", os.path.basename(__file__), "[название]") & fox_sudo())
async def rename_handler(client, message):
    message = await who_message(client, message)
    if message.chat.type == ChatType.PRIVATE:
        return await message.edit("<b>❌ Эта команда работает только в группах и каналах!</b>")
    
    args = message.text.split()[1:] if len(message.command) > 1 else []
    if not args:
        return await message.edit("<b>❌ Укажите новое название!</b>")
    
    new_title = " ".join(args)
    
    try:
        await client.set_chat_title(message.chat.id, new_title)
        chat_type = "группу" if message.chat.type == ChatType.SUPERGROUP else "канал"
        await message.edit(f"<b>✅ {chat_type} переименована в {new_title}!</b>")
        
    except Exception as e:
        logger.error(f"Ошибка при переименовании: {e}")
        await message.edit("<b>❌ Не удалось переименовать чат!</b>")

@Client.on_message(fox_command("create", "ChatModule", os.path.basename(__file__), "[-g|--group name] [-c|--channel name]") & fox_sudo())
async def create_handler(client, message):
    message = await who_message(client, message)
    args = message.text.split()[1:] if len(message.command) > 1 else []
    
    if not args:
        return await message.edit("<b>❌ Используйте:</b> <code>create -g название</code> или <code>create -c название</code>")
    
    group_name = None
    channel_name = None
    
    i = 0
    while i < len(args):
        if args[i] in ['-g', '--group'] and i + 1 < len(args):
            group_name = args[i + 1]
            i += 2
        elif args[i] in ['-c', '--channel'] and i + 1 < len(args):
            channel_name = args[i + 1]
            i += 2
        else:
            i += 1
    
    try:
        if channel_name:
            chat = await client.create_channel(channel_name, "")
            await message.edit(f"<b>✅ Канал {channel_name} создан!</b>\n<b>Ссылка:</b> {chat.invite_link}")
        elif group_name:
            chat = await client.create_group(group_name, "")
            await message.edit(f"<b>✅ Группа {group_name} создана!</b>\n<b>Ссылка:</b> {chat.invite_link}")
        else:
            await message.edit("<b>❌ Неверные аргументы!</b>")
            
    except Exception as e:
        logger.error(f"Ошибка при создании чата: {e}")
        await message.edit("<b>❌ Не удалось создать чат!</b>")

@Client.on_message(fox_command("geturl", "ChatModule", os.path.basename(__file__), "[reply]") & fox_sudo())
async def geturl_handler(client, message):
    message = await who_message(client, message)
    if not message.reply_to_message:
        return await message.edit("<b>❌ Ответьте на сообщение для получения ссылки!</b>")
    
    try:
        reply = message.reply_to_message
        chat = message.chat
        
        if chat.type == ChatType.SUPERGROUP:
            link = f"https://t.me/c/{str(chat.id)[4:]}/{reply.id}"
        else:
            link = f"https://t.me/{chat.username}/{reply.id}" if chat.username else f"https://t.me/c/{chat.id}/{reply.id}"
        
        await message.edit(f"<b>🔗 Ссылка на сообщение:</b> {link}")
        
    except Exception as e:
        logger.error(f"Ошибка при получении ссылки: {e}")
        await message.edit("<b>❌ Не удалось получить ссылку!</b>")

@Client.on_message(fox_command("addrole", "ChatModule", os.path.basename(__file__), "-n название_роли -p число") & fox_sudo())
async def addrole_handler(client, message):
    message = await who_message(client, message)
    args = message.text.split()[1:] if len(message.command) > 1 else []
    
    if len(args) < 4:
        return await message.edit("<b>❌ Используйте:</b> <code>addrole -n имя_роли -p число</code>")
    
    name = None
    perms = None
    
    i = 0
    while i < len(args):
        if args[i] in ['-n', 'name'] and i + 1 < len(args):
            name = args[i + 1]
            i += 2
        elif args[i] in ['-p', 'perms'] and i + 1 < len(args):
            try:
                perms = int(args[i + 1])
                i += 2
            except ValueError:
                i += 1
        else:
            i += 1
    
    if not name or perms is None:
        return await message.edit("<b>❌ Неверные аргументы!</b>")
    
    roles = load_config()
    roles[name] = perms
    save_config(roles)
    
    await message.edit(f"<b>✅ Роль {name} создана с правами {perms}!</b>")

@Client.on_message(fox_command("delrole", "ChatModule", os.path.basename(__file__), "-n название_роли") & fox_sudo())
async def delrole_handler(client, message):
    message = await who_message(client, message)
    args = message.text.split()[1:] if len(message.command) > 1 else []
    
    if len(args) < 2:
        return await message.edit("<b>❌ Используйте:</b> <code>delrole -n имя_роли</code>")
    
    name = None
    
    i = 0
    while i < len(args):
        if args[i] in ['-n', 'name'] and i + 1 < len(args):
            name = args[i + 1]
            i += 2
        else:
            i += 1
    
    if not name:
        return await message.edit("<b>❌ Укажите имя роли!</b>")
    
    roles = load_config()
    if name not in roles:
        return await message.edit(f"<b>❌ Роль {name} не найдена!</b>")
    
    del roles[name]
    save_config(roles)
    
    await message.edit(f"<b>✅ Роль {name} удалена!</b>")

@Client.on_message(fox_command("roles", "ChatModule", os.path.basename(__file__), "[-n имя_роли]") & fox_sudo())
async def roles_handler(client, message):
    message = await who_message(client, message)
    args = message.text.split()[1:] if len(message.command) > 1 else []
    
    roles = load_config()
    if not roles:
        return await message.edit("<b>❌ Роли не найдены!</b>")
    
    if not args:
        role_list = "\n".join([f"➡️ <code>{role}</code>" for role in roles.keys()])
        await message.edit(f"<b>Доступные роли:</b>\n{role_list}")
    else:
        role_name = " ".join(args)
        if role_name not in roles:
            return await message.edit(f"<b>❌ Роль {role_name} не найдена!</b>")
        

        await message.edit(f"<b>Роль {role_name}:</b>\n<b>Права:</b> <code>{roles[role_name]}</code>")

@Client.on_message(fox_command("chatinfo", "ChatModule", os.path.basename(__file__)) & fox_sudo())
async def chatinfo_handler(client, message):
    message = await who_message(client, message)
    if message.chat.type == ChatType.PRIVATE:
        return await message.edit("<b>❌ Эта команда работает только в группах и каналах!</b>")
    
    try:
        chat = await client.get_chat(message.chat.id)
        
        members_count = 0
        online_count = 0
        async for _ in client.get_chat_members(chat.id):
            members_count += 1
        
        admins_count = 0
        async for _ in client.get_chat_members(chat.id, filter=ChatMembersFilter.ADMINISTRATORS):
            admins_count += 1
        
        info_text = f"""<b>📊 Информация о чате:</b>

🆔 <b>ID:</b> <code>{chat.id}</code>
📝 <b>Название:</b> {chat.title}
👥 <b>Участников:</b> {members_count}
👤 <b>Администраторов:</b> {admins_count}
🌐 <b>Username:</b> @{chat.username} if chat.username else "Нет"
🔗 <b>Ссылка:</b> {chat.invite_link if chat.invite_link else "Нет"}
        """
        
        await message.edit(info_text)
        
    except Exception as e:
        logger.error(f"Ошибка при получении информации: {e}")
        await message.edit("<b>❌ Ошибка при получении информации о чате!</b>")
