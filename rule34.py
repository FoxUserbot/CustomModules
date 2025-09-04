from pyrogram import Client, filters
from command import fox_command, fox_sudo, who_message
from requirements_installer import install_library
import os

install_library("requests -U")

import requests
import re
import random

proxylist = []
result = []

def get_proxy():
    if proxylist:
        return proxylist
    else:
        temp_proxy = []
        try:
            url = "https://api.proxyscrape.com/v3/free-proxy-list/get?request=displayproxies&protocol=http&proxy_format=ipport&format=text&timeout=3000"
            response = requests.get(url, timeout=2)
            proxies_text = response.text
            temp_proxies_list = [x.strip() for x in proxies_text.split("\n") if x.strip()]
            for _ in temp_proxies_list:
                temp_proxy.append(_)
        except:
            pass
        
        try:
            url = "http://rootjazz.com/proxies/proxies.txt"
            response = requests.get(url, timeout=4)
            proxies_text = response.text
            temp_proxies_list = [x.strip() for x in proxies_text.split("\n") if x.strip()]
            for _ in temp_proxies_list:
                temp_proxy.append(_)
        except:
            pass
        
        proxies_list = temp_proxy[:200]
        proxylist.extend(proxies_list)
        return proxies_list

def get_picture(tegs):
    tags = (tegs).replace(" ", "%20")
    url = f"http://api.rule34.xxx/index.php?page=dapi&s=post&q=index&tags={tags}&api_key=d82f6db279ce94313e629e791533d456a4309dfeb528ddab6eee4b7472156f0def07ebfd3e64b9dddbf0d3b78f227ba8a5f386533ef1ccb1377d8a97481811dc&user_id=5255009"
    try:
        print("[DEBUG] No proxy")
        response = requests.get(url, timeout=5)
        text_data = response.text
        
        file_urls = re.findall(r'(file_url="([^"]+)")', text_data)
        for file_url in file_urls:
            result.append(file_url[1])
            
        try:
            if result is None:
                raise RuntimeError
            if len(result) == 0:
                raise RuntimeError
        except:
            raise RuntimeError
    except:
        while len(result) == 0:
            try:
                print("[DEBUG] Start proxy")
                proxies = get_proxy()
                proxy_host = proxies[0]

                response = requests.get(url, proxies={"http": proxy_host}, timeout=1)
                text_data = response.text
                print("[DEBUG] TEXT YEA")
                
                file_urls = re.findall(r'(file_url="([^"]+)")', text_data)
                for file_url in file_urls:
                    result.append(file_url[1])

                if result is None:
                    raise RuntimeError

                if len(result) == 0:
                    raise RuntimeError
            except Exception as fff:
                print(f"ERROR: {fff}")
                print(f"[DEBUG] FUCK {proxy_host}")
                print(f"[DEBUG] I have {len(proxies)} proxy")
                if proxy_host in proxylist:
                    proxylist.remove(proxy_host)

    print("GO!")
    print(result)
    result_random = random.choice(result)
    return str(result_random)

@Client.on_message(fox_command("rule34", "Rule34", os.path.basename(__file__), "[tags]") & fox_sudo())
async def rule34(client, message):
    message = await who_message(client, message)
    result.clear()
    await message.edit("Search. The module may be slow, nya~, due to limitations of your fucking ISP 😡~")
    orig_text = ' '.join(message.text.split()[1:])
    get_pic = get_picture(orig_text)
    await message.edit("I'm sending it, nya...~")
    
    try:
        await client.send_photo(message.chat.id, photo=get_pic, caption=f"Tags: {orig_text}")
        await message.delete()
    except:
        await message.edit(f"Fucking telegram, nya..~\nTags: {orig_text}\nLink: {get_pic}")
