from xml.dom import minidom
import urllib.request
import time
import threading
import requests
import random
import os
import asyncio
from pyrogram import Client, filters
from command import fox_command

currentUsername = ""
try:
    with open("userdata/lastfm_username", "r+", encoding="utf-8") as file:
        currentUsername = file.readline().strip()
        if not currentUsername:
            raise ValueError
except Exception as fff:
    currentUsername = "None"

userName = str(currentUsername)
apiKey = "460cda35be2fbf4f28e8ea7a38580730"
currentTrackURL = f'http://ws.audioscrobbler.com/2.0/?method=user.getrecenttracks&nowplaying=true&user={userName}&api_key={apiKey}'
runCheck = True
waitTime = 15
noSongPlaying = "Nothing Currently Playing"
killprocess = False

proxylist = ["127.0.0.1:2080"]
workproxy = []

def get_proxy():
    if proxylist:
        return workproxy + proxylist
    else:
        try:
            url = "https://api.proxyscrape.com/v3/free-proxy-list/get?request=displayproxies&protocol=http&proxy_format=ipport&format=text&timeout=3000"
            response = requests.get(url, timeout=2)
            proxies_text = response.text
        except:
            url = "http://rootjazz.com/proxies/proxies.txt"
            response = requests.get(url, timeout=4)
            proxies_text = response.text

        proxies_list = [x.strip() for x in proxies_text.split("\n") if x.strip()]
        proxies_list = proxies_list[:200]
        proxylist.extend(proxies_list)
        return proxies_list

def send_request(url):
    try:
        try:
            with urllib.request.urlopen(url, timeout=1) as response:
                return response.read()
        except:
            proxies = get_proxy()
            proxy_host = proxies[0]
            proxy_support = urllib.request.ProxyHandler({'http': proxy_host})
            opener = urllib.request.build_opener(proxy_support)
            
            req = urllib.request.Request(url, headers={'Cache-Control': 'no-cache'})

            with opener.open(req, timeout=5) as response:
                result = response.read()
                if proxy_host not in workproxy:
                    workproxy.append(proxy_host)
                return result
    except:
        if proxy_host in workproxy:
            workproxy.remove(proxy_host)
        if proxy_host in proxylist:
            proxylist.remove(proxy_host)
        return None

def checkForNewSong():
    global runCheck, waitTime, currentTrackURL

    if userName != "None":
        while runCheck:
            try:
                currentTrackXML = None
                while currentTrackXML is None:
                    currentTrackXML = send_request(currentTrackURL)

                currentTrack = minidom.parseString(currentTrackXML)
                songName = currentTrack.getElementsByTagName('name')[0].firstChild.nodeValue
                songArtist = currentTrack.getElementsByTagName('artist')[0].firstChild.nodeValue
                songInfo = f"{songName} — {songArtist}"
                encoding = 'cp1251' if os.name == 'nt' else 'utf-8'
                songInfo = songInfo.encode(encoding, errors='ignore').decode(encoding)
                try:
                    with open("userdata/lastfm_current_song", "r+", encoding="utf-8") as file:
                        currentSongFile = file.readline()
                except:
                    currentSongFile = "Nothing Currently Playing"

                if currentSongFile != songInfo:
                    with open("userdata/lastfm_current_song", "w+", encoding="utf-8") as file:
                        file.write(songInfo)

                time.sleep(waitTime)

            except Exception as fff:
                print(fff)
    else:
        print("Sleep...")

try:
    try:
        currentUsername = open("userdata/lastfm_username", "r+", encoding="utf-8").readline() 
        if len(currentUsername) == 0:
            raise ValueError
    except Exception as fff:
        currentUsername = "None"
        
    if currentUsername == "None":
        pass
    else:    
        newSongThread = threading.Thread(target=checkForNewSong)
        newSongThread.daemon = True  
        newSongThread.start()
except KeyboardInterrupt:
    raise ValueError

@Client.on_message(fox_command("nowplayed", "LastFM", os.path.basename(__file__)) & filters.me)
async def nowplayed(client, message):
    try:
        currentSong = open("userdata/lastfm_current_song", "r+", encoding="utf-8").readline() 
        await message.edit(f"[🎶] Now playing: `{currentSong}`")
    except FileNotFoundError:
        with open("userdata/lastfm_current_song", "w+", encoding="utf-8") as f:
            f.write("")
        try:
            currentSong = open("userdata/lastfm_current_song", "r+", encoding="utf-8").readline() 
            await message.edit(f"[🎶] Now playing: `{currentSong}`")
        except Exception as e:
            await message.edit(f"[❌] Ошибка при создании файла: {e}")

@Client.on_message(fox_command("lastfm_config", "LastFM", os.path.basename(__file__), "[LastFM Nickname] [Username/ID Channel] [ID Message] [Autostart: True/False]") & filters.me)
async def lastfm_config(client, message):
    
    open("userdata/lastfm_username", "w+", encoding="utf-8")
    username = message.text.split()[1]
    
    usernameF = open("userdata/lastfm_username", "w+", encoding="utf-8")
    usernameF.write(username)
    usernameF.close()
    
    channel_telegram = message.text.split()[2]
    
    channel_telegramF = open("userdata/lastfm_channel", "w+", encoding="utf-8")
    channel_telegramF.write(channel_telegram)
    channel_telegramF.close()
    
    id_in_channel_telegram = message.text.split()[3]
    
    id_in_channel_telegramF = open("userdata/lastfm_id_in_channel_telegram", "w+", encoding="utf-8")
    id_in_channel_telegramF.write(id_in_channel_telegram)
    id_in_channel_telegramF.close()
    
    autostart = message.text.split()[4]
    
    if autostart == "True":
        autostartF = open("triggers/lastfm_autostart", "w+", encoding="utf-8")
        autostartF.write("last_fm_trigger_start")
        autostartF.close()
    else:
        autostart = "False"
        try:
            os.remove("triggers/lastfm_autostart")
        except:
            pass
    
    await message.edit(f"LastFM: {username}\nChannel: {channel_telegram}\nID: {id_in_channel_telegram}\nAutostart: {autostart}")

@Client.on_message((fox_command("autoplayed", "LastFM", os.path.basename(__file__)) & filters.me) | (filters.command("last_fm_trigger_start", prefixes="") & filters.me & filters.chat("me")))
async def autoplayed(client, message):
    await message.edit("STARTED!")
    await asyncio.sleep(5)
    await message.delete()
    while True:
        channel = open("userdata/lastfm_channel", "r+", encoding="utf-8").readline() 
        try:
            channel = int(channel)
        except:
            channel = str(channel)

        id_in_channel_telegram = int(open("userdata/lastfm_id_in_channel_telegram", "r+", encoding="utf-8").readline())
        try:
            currentSong = open("userdata/lastfm_current_song", "r+", encoding="utf-8").readline() 
        except:
            open("userdata/lastfm_current_song", "w+", encoding="utf-8").write("")
            currentSong = open("userdata/lastfm_current_song", "r+", encoding="utf-8").readline() 
        
        text = f"Now playing: `{currentSong}`"
        try:
            cache = open("temp/lastfm_cache.txt", "r+", encoding="utf-8").readline() 
        except:
            cache = "None"
        
        if str(cache) == str(text):
            pass
        else:
            try:
                await client.edit_message_text(
                    chat_id=channel,
                    message_id=id_in_channel_telegram,
                    text=F"[🎶] {text}",
                )
                cache = open("temp/lastfm_cache.txt", "w+", encoding="utf-8")
                cache.write(text)
                cache.close()
            except Exception as ff:
                print(ff)
        
        await asyncio.sleep(5)

