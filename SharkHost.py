
import aiohttp
import asyncio
import os
import datetime
from requirements_installer import install_library
install_library("aiohttp -U")
from pyrogram import Client, filters
from command import fox_command, fox_sudo, who_message

def days_ago_text(dt_str: str, strings: dict, lang: str) -> str:
    if not dt_str:
        return strings["unknown_date"]
    try:
        dt = datetime.datetime.fromisoformat(dt_str)
        now = datetime.datetime.now(dt.tzinfo)
        days = (now.date() - dt.date()).days
        if days < 0:
            days = 0

        word = strings["day_one"] if days == 1 else strings["day_many"]
        return f"{days} {word} {strings['ago']}"
    except (ValueError, TypeError):
        return dt_str

def load_config():
    config = {}
    try:
        with open("userdata/sharkhost_api_url", "r", encoding="utf-8") as f:
            config["api_url"] = f.read().strip()
    except FileNotFoundError:
        config["api_url"] = "https://api.sharkhost.space"
    
    try:
        with open("userdata/sharkhost_api_token", "r", encoding="utf-8") as f:
            config["api_token"] = f.read().strip()
    except FileNotFoundError:
        config["api_token"] = None
    
    return config

def check_config():
    try:
        with open("userdata/sharkhost_api_token", "r", encoding="utf-8") as f:
            token = f.read().strip()
            return bool(token)
    except FileNotFoundError:
        return False

@Client.on_message(fox_command("sstatus", "SharkHost", os.path.basename(__file__), "[code]") & fox_sudo())
async def sstatus_handler(client, message):
    message = await who_message(client, message, message.reply_to_message)
    config = load_config()
    if not config["api_token"]:
        return await message.edit("🚫 <b>API token not set.</b>")
    
    await message.edit("🔄 <b>Requesting statuses...</b>")
    url = "https://api.sharkhost.space/api/v1/servers/status"
    headers = {"X-API-Token": config["api_token"]}
    try:
        async with aiohttp.ClientSession(headers=headers) as session:
            async with session.get(url) as resp:
                response_data = await resp.json()
                if not response_data.get("success"):
                    error = response_data.get("error", {})
                    return await message.edit(f"🚫 <b>API Error:</b> {error.get('message', 'No details')}")
                response = response_data.get("data", {})
    except aiohttp.ClientError as e:
        return await message.edit(f"🚫 <b>Network error:</b> {e}")
    
    servers = response.get("servers", [])
    if not servers:
        return await message.edit("✅ <b>Servers not found.</b>")
    
    status_map = {
        "true": "✅ Online",
        "premium": "⭐ Premium",
        "test": "🛠️ Test",
        "false": "❌ Offline",
        "noub": "🔒 Closed for new"
    }
    
    result = "📡 <b>SharkHost Servers Status:</b>"
    for server in servers:
        status = server.get("status", "N/A")
        slots = server.get("slots", {})
        result += (f"\n<blockquote>{server.get('flag', '🏴‍☠️')} <b>{server.get('code', 'N/A')}</b>\n\n"
                   f"<b>📍 Location:</b> <i>{server.get('location', 'N/A')}</i>\n"
                   f"<b>🚦 Status:</b> <code>{status_map.get(status, status)}</code>\n"
                   f"<b>⚙️ CPU:</b> {server.get('cpu_usage', 'N/A')}\n"
                   f"<b>💾 Disk:</b> {server.get('disk_usage', 'N/A')}\n"
                   f"<b>🤖 Slots:</b> {slots.get('used', 'N/A')} / {slots.get('total', 'N/A')}</blockquote>")
    
    await message.edit(result)

async def _request(config, method: str, path: str, **kwargs):
    if not config["api_token"]:
        return "🚫 <b>API token not set.</b>"
    headers = kwargs.pop("headers", {})
    headers["X-API-Token"] = config["api_token"]
    url = f"{config['api_url'].strip('/')}/api/v1/{path}"
    async with aiohttp.ClientSession() as session:
        try:
            async with session.request(method, url, headers=headers, **kwargs) as resp:
                if resp.status == 429:
                    return "⏳ <b>Flood wait!</b>\n<blockquote>Too many requests.</blockquote>"
                data = await resp.json()
                if data.get("success"):
                    return data.get("data")
                error = data.get("error", {})
                error_message = error.get("message", "No details")
                return f"🚫 <b>API Error:</b> <code>{error.get('code', 'UNKNOWN')}</code>\n<blockquote>{error_message}</blockquote>"
        except aiohttp.ClientError as e:
            return f"🚫 <b>Network error:</b> <blockquote>{e}</blockquote>"

async def _get_my_userbot(client, config):
    me = await client.get_me()
    response = await _request(config, "GET", f"users/{me.id}")
    if isinstance(response, str):
        return response
    userbot = response.get("userbot")
    if not userbot:
        return "🚫 <b>You have no active userbots.</b>"
    return userbot

@Client.on_message(fox_command("scheck", "SharkHost", os.path.basename(__file__), "[user]") & fox_sudo())
async def scheck_handler(client, message):
    message = await who_message(client, message, message.reply_to_message)
    config = load_config()
    if not config["api_token"]:
        return await message.edit("🚫 <b>API token not set.</b>")
    
    args = message.text.split(maxsplit=1)
    identifier = args[1] if len(args) > 1 else ""
    
    if not identifier:
        if message.reply_to_message:
            reply = message.reply_to_message
            identifier = str(reply.from_user.id)
        else:
            return await message.edit("🚫 <b>Specify user ID / username or reply to a message.</b>")
    
    await message.edit("🔄 <b>Requesting info...</b>")
    response = await _request(config, "GET", f"users/{identifier}")
    
    if isinstance(response, str):
        return await message.edit(response)
    
    owner = response.get('owner', {})
    userbot = response.get('userbot')
    owner_username = owner.get('username') or owner.get('id', 'N/A')
    
    strings = {
        "unknown_date": "Unknown",
        "day_one": "day",
        "day_many": "days",
        "ago": "ago"
    }
    
    result = (f"<b>👤 User Info for</b> {owner_username}:\n\n"
              f"<blockquote><b>• ID:</b> <code>{owner.get('id', 'N/A')}</code>\n"
              f"<b>• Full name:</b> <i>{owner.get('full_name') or 'Not specified'}</i>\n"
              f"<b>• Registered:</b> <i>{days_ago_text(owner.get('registered_at'), strings, 'en')}</i></blockquote>\n")
    
    if userbot:
        result += (f"\n<b>🤖 Userbot Info:</b>\n<blockquote>"
                   f"<b>• System name:</b> <code>{userbot.get('ub_username')}</code>\n"
                   f"<b>• Type:</b> <code>{userbot.get('ub_type')}</code>\n"
                   f"<b>• Status:</b> <code>{userbot.get('status')}</code>\n"
                   f"<b>• Server:</b> <code>{userbot.get('server_code')}</code>\n"
                   f"<b>• Created:</b> <i>{days_ago_text(userbot.get('created_at'), strings, 'en')}</i></blockquote>")
    else:
        result += "<blockquote>ℹ️ <i>This user does not have an active userbot.</i></blockquote>"
    
    await message.edit(result)

@Client.on_message(fox_command("smanage", "SharkHost", os.path.basename(__file__)) & fox_sudo())
async def smanage_handler(client, message):
    message = await who_message(client, message, message.reply_to_message)
    config = load_config()
    if not config["api_token"]:
        return await message.edit("🚫 <b>API token not set.</b>")
    
    await message.edit("🔄 <b>Getting info...</b>")
    userbot_data = await _get_my_userbot(client, config)
    
    if isinstance(userbot_data, str):
        return await message.edit(userbot_data)
    
    ub_username = userbot_data.get("ub_username")
    ub_status = userbot_data.get("status")
    
    if not ub_username or not ub_status:
        return await message.edit("🚫 <b>Error, userbot name not found.</b>")
    
    text = (f"<b>🕹️ Manage Userbot</b> <code>{ub_username}</code>\n"
            f"<b>Current status:</b> <code>{ub_status}</code>\n\n<i>Choose an action:</i>")
    
    if ub_status == "running":
        await message.edit(f"{text}\n\n🛑 Stop\n🔄 Restart")
    else:
        await message.edit(f"{text}\n\n🚀 Start\n🔄 Restart")
    
    with open("triggers/sharkhost_manage", "w", encoding="utf-8") as f:
        f.write(f"{ub_username}|{ub_status}")

async def _direct_manage_action(client, message, action: str, success_string: str):
    message = await who_message(client, message, message.reply_to_message)
    config = load_config()
    if not config["api_token"]:
        return await message.edit("🚫 <b>API token not set.</b>")
    
    await message.edit("🔄 <b>Getting info...</b>")
    userbot_data = await _get_my_userbot(client, config)
    if isinstance(userbot_data, str):
        return await message.edit(userbot_data)
    
    ub_username = userbot_data.get("ub_username")
    if not ub_username:
        return await message.edit("🚫 <b>Error, userbot name not found.</b>")
    
    response = await _request(config, "POST", f"userbots/{ub_username}/manage", headers={"Action": action})
    if isinstance(response, str):
        return await message.edit(response)
    
    await message.edit(success_string)

@Client.on_message(fox_command("sstart", "SharkHost", os.path.basename(__file__)) & fox_sudo())
async def sstart_handler(client, message):
    message = await who_message(client, message, message.reply_to_message)
    await _direct_manage_action(client, message, "start", "✅ Started")

@Client.on_message(fox_command("sstop", "SharkHost", os.path.basename(__file__)) & fox_sudo())
async def sstop_handler(client, message):
    message = await who_message(client, message, message.reply_to_message)
    await _direct_manage_action(client, message, "stop", "✅ Stoped")

@Client.on_message(fox_command("srestart", "SharkHost", os.path.basename(__file__)) & fox_sudo())
async def srestart_handler(client, message):
    message = await who_message(client, message, message.reply_to_message)
    await _direct_manage_action(client, message, "restart", "🔄 Restarted")

@Client.on_message(fox_command("shconfig", "SharkHost", os.path.basename(__file__), "[api_token]") & fox_sudo())
async def shconfig_handler(client, message):
    message = await who_message(client, message, message.reply_to_message)
    args = message.text.split()
    if len(args) < 2:
        return await message.edit("🚫 <b>Usage:</b> <code>shconfig [API_TOKEN]</code>")
    
    api_token = args[1]
    
    with open("userdata/sharkhost_api_token", "w", encoding="utf-8") as f:
        f.write(api_token)
    
    await message.edit(f"✅ <b>API token saved:</b> <code>{api_token}</code>")
