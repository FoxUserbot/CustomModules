import asyncio
from datetime import datetime
from pyrogram import Client, filters
from modules.plugins_1system.settings.main_settings import module_list, file_list
from prefix import my_prefix
from requirements_installer import install_library
install_library("aiohttp -U")
import aiohttp


def load_config():
    try:
        with open("userdata/sharkhost_api_token", "r", encoding="utf-8") as f:
            api_token = f.read().strip()
    except FileNotFoundError:
        api_token = ""
    
    try:
        with open("userdata/sharkhost_api_url", "r", encoding="utf-8") as f:
            api_url = f.read().strip()
    except FileNotFoundError:
        api_url = "https://api.sharkhost.space"
    
    return {"api_token": api_token, "api_url": api_url}

@Client.on_message(filters.command("sharkhost_config", prefixes=my_prefix()) & filters.me)
async def sharkhost_config(client, message):
    args = message.text.split()
    if len(args) < 2:
        return await message.edit("🚫 <b>Использование:</b> <code>sharkhost_config [API_TOKEN] [API_URL]</code>\n\n"
                                "<b>Пример:</b> <code>sharkhost_config ArThirtyFour:1863611627:8fd522a8da016928e6a131e333fd678e0067 https://api.sharkhost.space</code>")
    
    api_token = args[1]
    api_url = args[2] if len(args) > 2 else "https://api.sharkhost.space"
    
    with open("userdata/sharkhost_api_token", "w", encoding="utf-8") as f:
        f.write(api_token)
    
    with open("userdata/sharkhost_api_url", "w", encoding="utf-8") as f:
        f.write(api_url)
    
    await message.edit(f"✅ <b>Конфигурация SharkHost сохранена:</b>\n\n"
                      f"<b>API Token:</b> <code>{api_token[:20]}...</code>\n"
                      f"<b>API URL:</b> <code>{api_url}</code>")

@Client.on_message(filters.command("sstatus", prefixes=my_prefix()) & filters.me)
async def sstatuscmd(client, message):
    args = message.text.split(maxsplit=1)
    args = args[1] if len(args) > 1 else ""
    params = {"code": args} if args else {}
    
    await message.edit("🔄 <b>Запрашиваю статусы...</b>")
    
    config = load_config()
    if not config.get("api_token"):
        return await message.edit("🚫 <b>API токен не установлен!</b>\n\n"
                                f"Используйте: <code>{my_prefix()}sharkhost_config [API_TOKEN] [API_URL]</code>")
        
    headers = {"X-API-Token": config["api_token"]}
    url = f"{config['api_url'].strip('/')}/api/v1/servers/status"
    
    try:
        async with aiohttp.ClientSession(headers=headers) as session:
            async with session.get(url, params=params) as resp:
                if resp.status == 429:
                    return await message.edit("⏳ <b>Не флуди!</b>\n<blockquote>Вы отправляете запросы слишком часто.</blockquote>")
                data = await resp.json()
                if data.get("success"):
                    response = data.get("data")
                else:
                    error = data.get("error", {})
                    error_message = error.get("message", "Нет деталей")
                    return await message.edit(f"🚫 <b>API Ошибка:</b> <code>{error.get('code', 'UNKNOWN')}</code>\n"
                                            f"<blockquote>🗒️ <b>Сообщение:</b> {error_message}</blockquote>")
    except aiohttp.ClientError as e:
        return await message.edit(f"🚫 <b>Ошибка сети:</b> <blockquote>{e}</blockquote>")
    
    servers = response.get("servers", [])
    if not servers:
        return await message.edit("✅ <b>Серверы не найдены.</b>")
    
    result = "📡 <b>Статус серверов SharkHost:</b>\n"
    for server in servers:
        result += (f"\n<blockquote>{server['flag']} <b>{server['name']}</b> (<code>{server['code']}</code>)\n\n"
                   f"📍 <b>Локация:</b> <i>{server['location']}</i>\n"
                   f"🚦 <b>Статус:</b> <code>{server['status']}</code>\n"
                   f"⚙️ <b>CPU:</b> {server['cpu_usage']} | <b>RAM:</b> {server['ram_usage']}\n"
                   f"💾 <b>Диск:</b> {server['disk_usage']}\n"
                   f"🤖 <b>Юзерботы:</b> {server['slots']}</blockquote>")
    
    await message.edit(result)

def parse_ps_etime_to_human(etime: str) -> str:
    etime = etime.strip()
    days, hours, minutes = 0, 0, 0
    if '-' in etime:
        try:
            days_part, time_part = etime.split('-', 1)
            days = int(days_part)
        except ValueError:
            time_part = etime
    else:
        time_part = etime
    
    parts = time_part.split(':')
    try:
        if len(parts) == 3:
            hours, minutes, _ = map(int, parts)
        elif len(parts) == 2:
            minutes, _ = map(int, parts)
            if minutes >= 60:
                hours, minutes = divmod(minutes, 60)
        elif len(parts) == 1:
            minutes = int(parts[0])
            if minutes >= 60:
                hours, minutes = divmod(minutes, 60)
    except (ValueError, IndexError):
        pass

    result = [f"{days}д" if days else "", f"{hours}ч" if hours else "", f"{minutes}м" if minutes else ""]
    return ' '.join(filter(None, result)) or '~1м'

def days_ago_text(dt_str: str) -> str:
    if not dt_str:
        return "Неизвестно"
    try:
        dt = datetime.fromisoformat(dt_str)
        now = datetime.now(dt.tzinfo)
        days = (now.date() - dt.date()).days
        if days < 0:
            days = 0
        if days % 10 == 1 and days % 100 != 11:
            word = 'день'
        elif 2 <= days % 10 <= 4 and (days % 100 < 10 or days % 100 >= 20):
            word = 'дня'
        else:
            word = 'дней'
        return f"{days} {word} назад"
    except (ValueError, TypeError):
        return dt_str

async def _get_my_userbot():
    config = load_config()
    if not config.get("api_token"):
        return "🚫 <b>API токен не установлен!</b>\n\n"
    
    headers = {"X-API-Token": config["api_token"]}
    url = f"{config['api_url'].strip('/')}/api/v1/userbots"
    
    try:
        async with aiohttp.ClientSession(headers=headers) as session:
            async with session.get(url) as resp:
                if resp.status == 429:
                    return "⏳ <b>Не флуди!</b>\n<blockquote>Вы отправляете запросы слишком часто.</blockquote>"
                data = await resp.json()
                if data.get("success"):
                    response = data.get("data")
                    userbots = response.get("userbots", [])
                    if not userbots:
                        return "🚫 <b>У вас нет активных юзерботов.</b>"
                    return userbots[0]
                else:
                    error = data.get("error", {})
                    error_message = error.get("message", "Нет деталей")
                    return (f"🚫 <b>API Ошибка:</b> <code>{error.get('code', 'UNKNOWN')}</code>\n"
                            f"<blockquote>🗒️ <b>Сообщение:</b> {error_message}</blockquote>")
    except aiohttp.ClientError as e:
        return f"🚫 <b>Ошибка сети:</b> <blockquote>{e}</blockquote>"

@Client.on_message(filters.command("scheck", prefixes=my_prefix()) & filters.me)
async def scheckcmd(client, message):
    args = message.text.split(maxsplit=1)
    identifier = args[1] if len(args) > 1 else ""
    
    if not identifier:
        if message.reply_to_message:
            identifier = str(message.reply_to_message.from_user.id)
        else:
            return await message.edit("🚫 <b>Укажите ID/юзернейм или ответьте на сообщение.</b>")
    
    await message.edit("🔄 <b>Запрашиваю информацию...</b>")
    
    config = load_config()
    if not config.get("api_token"):
        return await message.edit("🚫 <b>API токен не установлен!</b>\n\n"
                                f"Используйте: <code>{my_prefix()}sharkhost_config [API_TOKEN] [API_URL]</code>")
    
    headers = {"X-API-Token": config["api_token"]}
    url = f"{config['api_url'].strip('/')}/api/v1/users/{identifier}"
    
    try:
        async with aiohttp.ClientSession(headers=headers) as session:
            async with session.get(url) as resp:
                if resp.status == 429:
                    return await message.edit("⏳ <b>Не флуди!</b>\n<blockquote>Вы отправляете запросы слишком часто.</blockquote>")
                data = await resp.json()
                if data.get("success"):
                    response = data.get("data")
                else:
                    error = data.get("error", {})
                    error_message = error.get("message", "Нет деталей")
                    return await message.edit(f"🚫 <b>API Ошибка:</b> <code>{error.get('code', 'UNKNOWN')}</code>\n"
                                            f"<blockquote>🗒️ <b>Сообщение:</b> {error_message}</blockquote>")
    except aiohttp.ClientError as e:
        return await message.edit(f"🚫 <b>Ошибка сети:</b> <blockquote>{e}</blockquote>")
    
    owner = response.get('owner', {})
    userbot = response.get('userbot')
    owner_username = owner.get('username') or str(owner.get('id', 'N/A'))
    
    result = (f"👤 <b>Инфо о пользователе</b> <a href=\"tg://user?id={owner.get('id')}\">{owner_username}</a>:\n\n"
              f"<blockquote><b> • ID:</b> <code>{owner.get('id', 'N/A')}</code>\n"
              f"<b> • Полное имя:</b> <i>{owner.get('full_name') or 'Не указано'}</i>\n"
              f"<b> • Зарегистрирован:</b> <i>{days_ago_text(owner.get('registered_at'))}</i></blockquote>\n")
    
    if userbot:
        result += ("\n🤖 <b>Инфо о юзерботе:</b>\n<blockquote>"
                   f"<b> • Системное имя:</b> <code>{userbot.get('ub_username')}</code>\n"
                   f"<b> • Тип:</b> <code>{userbot.get('ub_type')}</code>\n"
                   f"<b> • Статус:</b> <code>{userbot.get('status')}</code>\n"
                   f"<b> • Сервер:</b> <code>{userbot.get('server_code')}</code>\n"
                   f"<b> • Создан:</b> <i>{days_ago_text(userbot.get('created_at'))}</i>")
        if uptime := userbot.get('uptime'):
            result += f"\n<b> • Аптайм:</b> <code>{parse_ps_etime_to_human(uptime)}</code>"
        result += "</blockquote>"
    else:
        result += "<blockquote>ℹ️ <i>У этого пользователя нет активного юзербота.</i></blockquote>"
    
    await message.edit(result)

@Client.on_message(filters.command("smanage", prefixes=my_prefix()) & filters.me)
async def smanagecmd(client, message):
    await message.edit("🔄 <b>Узнаю информацию ...</b>")
    userbot_data = await _get_my_userbot()
    if isinstance(userbot_data, str):
        return await message.edit(userbot_data)
    ub_username = userbot_data.get("ub_username")
    ub_status = userbot_data.get("status")
    if not ub_username or not ub_status:
        return await message.edit("🚫 <b>Ошибка, не найдено имя юзербота.</b>")
    
    text = (f"🕹️ <b>Управление юзерботом</b> <code>{ub_username}</code>\n"
            f"<b>Текущий статус:</b> <code>{ub_status}</code>\n\n"
            f"<b>Команды управления:</b>\n"
            f"• <code>{my_prefix()}sstart</code> - Запустить юзербота\n"
            f"• <code>{my_prefix()}sstop</code> - Остановить юзербота\n"
            f"• <code>{my_prefix()}srestart</code> - Перезапустить юзербота")
    
    await message.edit(text)

@Client.on_message(filters.command("sstart", prefixes=my_prefix()) & filters.me)
async def sstartcmd(client, message):
    await message.edit("🔄 <b>Узнаю информацию ...</b>")
    userbot_data = await _get_my_userbot()
    if isinstance(userbot_data, str):
        return await message.edit(userbot_data)
    ub_username = userbot_data.get("ub_username")
    if not ub_username:
        return await message.edit("🚫 <b>Ошибка, не найдено имя юзербота.</b>")
    
    await _direct_manage_action(ub_username, "start")
    await message.edit("✅ Started")

@Client.on_message(filters.command("sstop", prefixes=my_prefix()) & filters.me)
async def sstopcmd(client, message):
    await message.edit("🔄 <b>Узнаю информацию ...</b>")
    userbot_data = await _get_my_userbot()
    if isinstance(userbot_data, str):
        return await message.edit(userbot_data)
    ub_username = userbot_data.get("ub_username")
    if not ub_username:
        return await message.edit("🚫 <b>Ошибка, не найдено имя юзербота.</b>")
    
    await _direct_manage_action(ub_username, "stop")
    await message.edit("❌ Stopped")

@Client.on_message(filters.command("srestart", prefixes=my_prefix()) & filters.me)
async def srestartcmd(client, message):
    await message.edit("🔄 <b>Узнаю информацию ...</b>")
    userbot_data = await _get_my_userbot()
    if isinstance(userbot_data, str):
        return await message.edit(userbot_data)
    ub_username = userbot_data.get("ub_username")
    if not ub_username:
        return await message.edit("🚫 <b>Ошибка, не найдено имя юзербота.</b>")
    
    await _direct_manage_action(ub_username, "restart")
    await message.edit("🔄 Restarted")

async def _direct_manage_action(ub_username: str, action: str):
    config = load_config()
    headers = {"X-API-Token": config["api_token"]}
    url = f"{config['api_url'].strip('/')}/api/v1/userbots/{ub_username}/manage"
    json_data = {"action": action}
    
    try:
        async with aiohttp.ClientSession(headers=headers) as session:
            async with session.post(url, json=json_data) as resp:
                await resp.text()
    except aiohttp.ClientError:
        pass



module_list['SharkHost'] = f'{my_prefix()}sharkhost_config [API_TOKEN] [API_URL], {my_prefix()}sstatus [код], {my_prefix()}scheck [ID/юзернейм], {my_prefix()}smanage, {my_prefix()}sstart, {my_prefix()}sstop, {my_prefix()}srestart'
file_list['SharkHost'] = 'SharkHost.py'