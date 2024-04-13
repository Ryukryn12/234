import requests,random,time,json
from random import *

try:
    with open ("automessage_config.json", 'r') as f:
        setup = json.load(f)
        token, cooldown, Cid = setup['TOKEN'], setup['COOLDOWN'], setup['CHANNEL_ID']
except:
    print("[Error] Json file not found. Try unzipping this file or downloading the config file")

if not token:
    token = input("[!] Discord Token?: ")
try:
    if not Cid:
        Cid = input("[!] Target Channel Id?: ")
    e = int(Cid)
    Cid = str(Cid)
    spam_times = input("[!] How Many Time Will The Message Be Sent?: ")
    spam_times = int(spam_times)
    if not cooldown:
        cooldown = input("[!] Cooldown between message?: ")
    try:
        cooldown = int(cooldown)
    except:
        cooldown = float(cooldown)
except:
    print("[Error] Please input the right things or check the config file")
    exit()
message = input("[!] Message Content?: ")

global_headers = {
    'authorization' : token,
    'authority': 'discord.com',
    'accept': '*/*',
    'accept-language': 'sv,sv-SE;q=0.9',
    'content-type': 'application/json',
    'origin': 'https://discord.com',
    'referer': 'https://discord.com/',
    'sec-ch-ua': '"Not?A_Brand";v="8", "Chromium";v="108"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) discord/1.0.9016 Chrome/108.0.5359.215 Electron/22.3.12 Safari/537.36',
    'x-debug-options': 'bugReporterEnabled',
    'x-discord-locale': 'sv-SE',
    'x-discord-timezone': 'Europe/Stockholm',
}    
error_exit = 0

for i in(range(int(spam_times))): 
    payload ={
    "content": message,
    "nonce": randint(1, 100000),
    "tts": False
    }
    r = requests.request("POST", f"https://discord.com/api/v9/channels/{Cid}/messages", json = payload, headers = global_headers)
    if r.status_code == 200:
        print(f"[Sucess] Message Sent in {Cid}")
    elif r.status_code == 401:
        print("[Error] Your token might be invalid! Please check it")
        exit()
    elif r.status_code == 403:
        print("[Error] You might have been kicked out of the guild the token was previously sending message in, retrying...")
        error_exit +1
        if error_exit == 5:
            print("[Error] Exiting due to token being kicked from the guide")
            exit()
    elif r.status_code == 429:
        print("[Error] Spamming messages to fast! retrying...")
    else:
        zzz = r.json()
        print(f"[Error] Error while performing, error staus code: {r.status_code}, here is the error: {zzz}")
        error_exit + 1
        if error_exit == 5:
            print("[Error] Too many errors while requests, exiting.")
            exit()
    time.sleep(cooldown)
print("[Sucess] Finished Sending messages, exiting")
exit()