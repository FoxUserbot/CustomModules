from pyrogram import Client, filters
from command import fox_command, fox_sudo, who_message , get_text
from requirements_installer import install_library
import os
import json

install_library("requests bs4 -U") 

LANGUAGES = { 
    "en": {
        "searching": "<emoji id='5397755618750653196'>🌟</emoji> Searching..",
        "error": "<emoji id='5397755618750653196'>🌟</emoji> **Error:** {error}",
        "video": "<emoji id='5397755618750653196'>🌟</emoji> <b>Your Video:</b>\n{video_url}",
        "image": "<emoji id='5397755618750653196'>🌟</emoji> <b>Your Link:</b>\n{link}",
    },
    "ru": {
        "searching":"<emoji id='5397755618750653196'>🌟</emoji> Поиск..",
        "error": "<emoji id='5397755618750653196'>🌟</emoji> **Ошибка:** {error}",
        "video": "<emoji id='5397755618750653196'>🌟</emoji> <b>Ваше видео:</b>\n{video_url}",
        "image": "<emoji id='5397755618750653196'>🌟</emoji> <b>Ваша ссылка:</b>\n{link}",
    },
    "ua": {
        "searching":"<emoji id='5397755618750653196'>🌟</emoji> Пошук..",
        "error": "<emoji id='5397755618750653196'>🌟</emoji> **Помилка:** {error}",
        "video": "<emoji id='5397755618750653196'>🌟</emoji> <b>Ваше видео:</b>\n{video_url}",
        "image": "<emoji id='5397755618750653196'>🌟</emoji> <b>Ваша посилання:</b>\n{link}",
    }
}



import requests
from bs4 import BeautifulSoup

@Client.on_message(fox_command("pinterest", "Pinterest", os.path.basename(__file__), "[link]") & fox_sudo())
async def pinterest(client, message):
    message = await who_message(client, message)
    await message.edit(get_text("Pinterest", "searching", LANGUAGES=LANGUAGES))
    link = message.text.split()[1]
    
    try:
        resp = requests.get(link)
        soup = BeautifulSoup(resp.text, "html.parser")

        video_url = None
        pin_data = None 

        scripts = soup.find_all("script", type="application/json")
        for i, script in enumerate(scripts):
            try:
                data = json.loads(script.string)
                if "response" in data and "data" in data["response"]:
                    pin_data = data["response"]["data"].get("v3GetPinQuery", {}).get("data", {})
                    
                    if "videos" in pin_data:
                        videos = pin_data["videos"]
                        
                        if "videoUrls" in videos and videos["videoUrls"]:
                            for url in videos["videoUrls"]:
                                if url.endswith('.mp4'):
                                    video_url = url
                                    break
                            if not video_url:
                                video_url = videos["videoUrls"][0]
                            break
                        elif "videoList" in videos:
                            video_list = videos["videoList"]
                            
                            if "v720P" in video_list:
                                video_url = video_list["v720P"]["url"]
                                break
                            elif "vHLSV4" in video_list:
                                video_url = video_list["vHLSV4"]["url"]
                                break
            except (json.JSONDecodeError, KeyError, TypeError) as e:
                continue
        
        if not video_url:
            json_ld_scripts = soup.find_all("script", type="application/ld+json")
            for i, script in enumerate(json_ld_scripts):
                try:
                    data = json.loads(script.string)
                    
                    if data.get("@type") == "VideoObject" and "contentUrl" in data:
                        content_url = data["contentUrl"]
                        if content_url.endswith('.mp4'):
                            video_url = content_url
                            break
                except (json.JSONDecodeError, KeyError, TypeError) as e:
                    continue
        
        if not video_url:
            video_tags = soup.find_all("video")
            
            for i, video in enumerate(video_tags):
                if video.get("src"):
                    video_url = video["src"]
                    break
        
        if video_url:
            if video_url.endswith('.m3u8') or 'hls' in video_url.lower():
                if "videos" in pin_data:
                    videos = pin_data["videos"]
                    if "videoUrls" in videos:
                        for url in videos["videoUrls"]:
                            if url.endswith('.mp4') and '720p' in url.lower():
                                video_url = url
                                break
                        else:
                            video_url = None
            
            if video_url:
                try:
                    await client.send_video(
                        message.chat.id, 
                        video=video_url,
                        caption=f"{get_text("Pinterest", "video", LANGUAGES=LANGUAGES, video_url=video_url)}",
                        message_thread_id=message.message_thread_id
                    )
                    await message.delete()
                    return
                except Exception as video_error:
                    await message.edit(f"{get_text("Pinterest", "error", LANGUAGES=LANGUAGES, error=video_error)}")
                    video_url = None

        pic = soup.find_all("img")
        if pic:
            link = pic[0].get('src')
            try:
                await client.send_photo(
                    message.chat.id, 
                    photo=link,
                    caption=f"{get_text("Pinterest", "image", LANGUAGES=LANGUAGES, link=link)}",
                    message_thread_id=message.message_thread_id
                )
                await message.delete()
            except Exception as image_error:
                await message.edit(f"{get_text("Pinterest", "error", LANGUAGES=LANGUAGES, error=image_error)}")
        else:
            await message.edit(f"{get_text("Pinterest", "error", LANGUAGES=LANGUAGES, error="No image or video found")}")
            
    except Exception as f:
        await message.edit(f"{get_text("Pinterest", "error", LANGUAGES=LANGUAGES, error=f)}")
