
import io
import json
from pyrogram import Client, filters
from command import fox_command
from requirements_installer import install_library
import os

install_library("requests -U")
import requests

@Client.on_message(fox_command("catbox", "Uploader", os.path.basename(__file__)) & filters.me)
async def catbox_handler(client, message):
    await message.edit("⚡ <b>Uploading file...</b>")
    file = await get_file(client, message)
    if not file:
        return
    try:
        response = requests.post(
            "https://catbox.moe/user/api.php",
            files={"fileToUpload": file},
            data={"reqtype": "fileupload"}
        )
        if response.ok:
            await message.edit("❤️ <b>File uploaded!</b>\n\n🔥 <b>URL:</b> <code>{}</code>".format(response.text))
        else:
            await message.edit("❌ <b>Error while uploading: {}</b>".format(response.status_code))
    except Exception as e:
        await message.edit("❌ <b>Error while uploading: {}</b>".format(str(e)))

@Client.on_message(fox_command("envs", "Uploader", os.path.basename(__file__)) & filters.me)
async def envs_handler(client, message):
    await message.edit("⚡ <b>Uploading file...</b>")
    file = await get_file(client, message)
    if not file:
        return
    try:
        response = requests.post("https://envs.sh", files={"file": file})
        if response.ok:
            await message.edit("❤️ <b>File uploaded!</b>\n\n🔥 <b>URL:</b> <code>{}</code>".format(response.text))
        else:
            await message.edit("❌ <b>Error while uploading: {}</b>".format(response.status_code))
    except Exception as e:
        await message.edit("❌ <b>Error while uploading: {}</b>".format(str(e)))

@Client.on_message(fox_command("kappa", "Uploader", os.path.basename(__file__)) & filters.me)
async def kappa_handler(client, message):
    await message.edit("⚡ <b>Uploading file...</b>")
    file = await get_file(client, message)
    if not file:
        return
    try:
        response = requests.post("https://kappa.lol/api/upload", files={"file": file})
        if response.ok:
            data = response.json()
            url = f"https://kappa.lol/{data['id']}"
            await message.edit("❤️ <b>File uploaded!</b>\n\n🔥 <b>URL:</b> <code>{}</code>".format(url))
        else:
            await message.edit("❌ <b>Error while uploading: {}</b>".format(response.status_code))
    except Exception as e:
        await message.edit("❌ <b>Error while uploading: {}</b>".format(str(e)))

@Client.on_message(fox_command("0x0", "Uploader", os.path.basename(__file__)) & filters.me)
async def oxo_handler(client, message):
    await message.edit("⚡ <b>Uploading file...</b>")
    file = await get_file(client, message)
    if not file:
        return
    try:
        response = requests.post(
            "https://0x0.st",
            files={"file": file},
            data={"secret": True}
        )
        if response.ok:
            await message.edit("❤️ <b>File uploaded!</b>\n\n🔥 <b>URL:</b> <code>{}</code>".format(response.text))
        else:
            await message.edit("❌ <b>Error while uploading: {}</b>".format(response.status_code))
    except Exception as e:
        await message.edit("❌ <b>Error while uploading: {}</b>".format(str(e)))

@Client.on_message(fox_command("x0", "Uploader", os.path.basename(__file__)) & filters.me)
async def x0_handler(client, message):
    await message.edit("⚡ <b>Uploading file...</b>")
    file = await get_file(client, message)
    if not file:
        return
    try:
        response = requests.post("https://x0.at", files={"file": file})
        if response.ok:
            await message.edit("❤️ <b>File uploaded!</b>\n\n🔥 <b>URL:</b> <code>{}</code>".format(response.text))
        else:
            await message.edit("❌ <b>Error while uploading: {}</b>".format(response.status_code))
    except Exception as e:
        await message.edit("❌ <b>Error while uploading: {}</b>".format(str(e)))

@Client.on_message(fox_command("tmpfiles", "Uploader", os.path.basename(__file__)) & filters.me)
async def tmpfiles_handler(client, message):
    await message.edit("⚡ <b>Uploading file...</b>")
    file = await get_file(client, message)
    if not file:
        return
    try:
        response = requests.post(
            "https://tmpfiles.org/api/v1/upload",
            files={"file": file}
        )
        if response.ok:
            data = json.loads(response.text)
            url = data["data"]["url"]
            await message.edit("❤️ <b>File uploaded!</b>\n\n🔥 <b>URL:</b> <code>{}</code>".format(url))
        else:
            await message.edit("❌ <b>Error while uploading: {}</b>".format(response.status_code))
    except Exception as e:
        await message.edit("❌ <b>Error while uploading: {}</b>".format(str(e)))

@Client.on_message(fox_command("pomf", "Uploader", os.path.basename(__file__)) & filters.me)
async def pomf_handler(client, message):
    await message.edit("⚡ <b>Uploading file...</b>")
    file = await get_file(client, message)
    if not file:
        return
    try:
        response = requests.post(
            "https://pomf.lain.la/upload.php",
            files={"files[]": file}
        )
        if response.ok:
            data = json.loads(response.text)
            url = data["files"][0]["url"]
            await message.edit("❤️ <b>File uploaded!</b>\n\n🔥 <b>URL:</b> <code>{}</code>".format(url))
        else:
            await message.edit("❌ <b>Error while uploading: {}</b>".format(response.status_code))
    except Exception as e:
        await message.edit("❌ <b>Error while uploading: {}</b>".format(str(e)))

@Client.on_message(fox_command("bash", "Uploader", os.path.basename(__file__)) & filters.me)
async def bash_handler(client, message):
    await message.edit("⚡ <b>Uploading file...</b>")
    file = await get_file(client, message)
    if not file:
        return
    try:
        response = requests.put(
            "https://bashupload.com",
            data=file.read()
        )
        if response.ok:
            urls = [line for line in response.text.split("\n") if "wget" in line]
            if urls:
                url = urls[0].split()[-1]
                await message.edit("❤️ <b>File uploaded!</b>\n\n🔥 <b>URL:</b> <code>{}</code>".format(url))
            else:
                await message.edit("❌ <b>Error while uploading: Could not find URL</b>")
        else:
            await message.edit("❌ <b>Error while uploading: {}</b>".format(response.status_code))
    except Exception as e:
        await message.edit("❌ <b>Error while uploading: {}</b>".format(str(e)))

async def get_file(client, message):
    reply = message.reply_to_message
    if not reply:
        await message.edit("❌ <b>Reply to file!</b>")
        return None
    if reply.media:
        downloaded = await reply.download(in_memory=True)
        if reply.document:
            downloaded.name = reply.document.file_name or f"file_{reply.document.file_size}"
        else:
            downloaded.name = f"file_{reply.id}.jpg"
        return downloaded
    else:
        text = reply.text or reply.caption or ""
        file = io.BytesIO(text.encode("utf-8"))
        file.name = "text.txt"
        return file
