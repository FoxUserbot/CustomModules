
try:
    from PIL import Image, ImageFilter
    import aiohttp
    import subprocess
    FFMPEG_AVAILABLE = True
except ImportError:
    from requirements_installer import install_library
    install_library("Pillow aiohttp")
    
    from PIL import Image, ImageFilter
    FFMPEG_AVAILABLE = True if subprocess else False

import asyncio
import re
import os
import json
import warnings
import functools
import logging
import tempfile
import shutil
from io import BytesIO
from urllib.parse import urljoin, urlparse
from typing import Union, Optional, List, Dict, Any
from dataclasses import dataclass
from pyrogram import Client, filters
from command import fox_command

@dataclass
class TTData:
    dir_name: str
    media: Union[str, List[str]]
    type: str

class TikTokAPI:
    def __init__(self, host: Optional[str] = None):
        self.headers = {
            "User-Agent": "Mozilla/5.0 (iPad; U; CPU OS 3_2 like Mac OS X; en-us) AppleWebKit/531.21.10 (KHTML, like Gecko) Version/4.0.4 Mobile/7B334b Safari/531.21.10"
        }
        self.host = host or "https://www.tikwm.com/"
        self.session = aiohttp.ClientSession()
        self.progress_message = None

    async def close_session(self):
        await self.session.close()

    async def _update_progress(self, text: str):
        if self.progress_message:
            try:
                await self.progress_message.edit(text)
            except:
                pass

    async def _download_file(self, url: str, path: str):
        async with self.session.get(url) as response:
            response.raise_for_status()
            with open(path, "wb") as file:
                async for chunk in response.content.iter_chunked(1024):
                    file.write(chunk)

    async def download(self, link: str, video_filename: Optional[str] = None, hd: bool = True) -> TTData:
        async with self.session.get(f"{self.host}api", params={"url": link, "hd": int(hd)}) as response:
            data = await response.json()
            if not data.get("data"):
                raise Exception("No data found")

            result = data["data"]
            if "images" in result:
                os.makedirs("tt_download", exist_ok=True)
                image_paths = []
                for i, url in enumerate(result["images"]):
                    path = f"tt_download/image_{i}.jpg"
                    await self._download_file(url, path)
                    image_paths.append(path)
                return TTData("tt_download", image_paths, "images")
            elif "play" in result:
                url = result["hdplay"] if hd else result["play"]
                filename = video_filename or f"{result['id']}.mp4"
                await self._download_file(url, filename)
                return TTData(os.path.dirname(filename), filename, "video")
            else:
                raise Exception("Unsupported content type")

@Client.on_message(fox_command("tt", "SocialMediaDL", os.path.basename(__file__), "[url]") & filters.me)
async def tt_download(client, message):
    try:
        url = None
        if message.reply_to_message:
            text = message.reply_to_message.text or message.reply_to_message.caption or ""
            matches = re.findall(r"https?://(?:www\.)?(?:vm|vt|tiktok)\.com/[^\s]+", text)
            if matches:
                url = matches[0]
        elif len(message.command) > 1:
            url = message.command[1]

        if not url:
            await message.edit("<b>No TikTok URL found</b>")
            return

        api = TikTokAPI()
        progress = await message.edit("<b>Downloading...</b>")
        api.progress_message = progress

        try:
            result = await api.download(url)
            if result.type == "video":
                await client.send_video(message.chat.id, result.media)
            else:
                await client.send_media_group(message.chat.id, [InputMediaPhoto(media=file) for file in result.media])
            await progress.delete()
        finally:
            await api.close_session()
            if os.path.exists("tt_download"):
                shutil.rmtree("tt_download")
            if "result" in locals() and os.path.exists(result.media):
                os.remove(result.media)

    except Exception as e:
        await message.edit(f"<b>Error:</b> {str(e)}")
