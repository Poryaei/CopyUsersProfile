# ------- Import Library's
import asyncio
import re
from telethon.tl import types as tl_telethon_types
from telethon.tl.types import MessageMediaPoll, ReplyInlineMarkup
from telethon.tl.functions.messages import ImportChatInviteRequest
from telethon.tl.custom import Button, button
from telethon.tl.functions.account import UpdateUsernameRequest
from telethon.tl.types.auth import SentCodeTypeApp
from telethon.sync import TelegramClient, functions, types, events, errors, connection
from telethon.client import buttons
from asyncio import tasks
from telethon.tl.functions.channels import JoinChannelRequest, LeaveChannelRequest, DeleteMessagesRequest
from telethon.tl.functions.messages import ImportChatInviteRequest, GetBotCallbackAnswerRequest

import os
import sys
import time
import datetime
import psutil
import json
import requests
from pathlib import Path
import cv2
import random
from faker import Faker
# --------- Connect Bot
bot = TelegramClient('8801882917239', 1210549, '40c4bb8ee22346e4fa8c69565cb87440')
bot.start()

#--------- alert
print('Bot Connected Successfully !')


#--------- Data
botData = {
    'startTime': time.time()
}
admin = 591922827

#--- C
if len(sys.argv) > 1:
    if sys.argv[1] == "re":
        bot.send_message(admin, "🔄 Bot Restarted")
# -------- Functions
def size_format(b):
    if b < 1000:
              return '%i' % b + 'B'
    elif 1000 <= b < 1000000:
        return '%.1f' % float(b/1000) + 'KB'
    elif 1000000 <= b < 1000000000:
        return '%.1f' % float(b/1000000) + 'MB'
    elif 1000000000 <= b < 1000000000000:
        return '%.1f' % float(b/1000000000) + 'GB'
    elif 1000000000000 <= b:
        return '%.1f' % float(b/1000000000000) + 'TB'

def getMemoryUsage():
    process = psutil.Process(os.getpid())
    # print(process.stringify())
    return size_format(process.memory_info().rss)  # in bytes 

async def getAllDialogsC():
    #--- Data
    dictData = {
        'channels': 0,
        'megaGroups': 0,
        'groups': 0,
        'users': 0,
        'bots': 0,
    }

    #--- Get Dialogs
    async for dialog in bot.iter_dialogs():

        #--- Channel
        if not dialog.is_group and dialog.is_channel:
            dictData['channels'] += 1
        
        #--- Mega Group
        elif dialog.is_group and dialog.is_channel:
            dictData['megaGroups'] += 1
        
        #--- Groups
        elif dialog.is_group and not dialog.is_channel:
            dictData['groups'] += 1
        
        #--- Users
        elif dialog.is_user and not dialog.entity.bot:
            dictData['users'] += 1
        
        #--- Bots
        elif dialog.entity.bot:
            dictData['bots'] += 1
        
        #--- Else
        else:
            print(dialog)
        
    #--- return Data
    return dictData

async def getRandomDialogID():
    #--- Data
    data = {}
    data['gps'] = [] 
    data['pv'] = [] 

    #--- Get Dialogs
    async for dialog in bot.iter_dialogs():
        
        #--- Mega Group
        if dialog.is_group and dialog.is_channel:
            data['gps'].append(dialog.id)
        
        #--- Groups
        elif dialog.is_group and not dialog.is_channel:
            data['gps'].append(dialog.id)

        
        #--- Users
        elif dialog.is_user and not dialog.entity.bot:
            data['pv'].append(dialog.id)
        
    #--- return Data
    return data

async def delByHistory(history, chatid, delid, dontdelmid):
    id_List = []
    print(f"Getting: ", len(history.messages))
    for message in history.messages:
        try:
            if message.from_id.user_id == delid and message.id != dontdelmid:
                id_List.append(message.id)
        except Exception as e:
            print(e)
    await bot(DeleteMessagesRequest(int(chatid), id=id_List))
    return id_List

# -------- Start Receiving Message's
async def answer(event):
    text = event.raw_text
    user_id = event.sender_id
    chat_id = event.chat_id
    msgid = event.message.id

    #--- Filter Messages
    if user_id != admin:
        return
    
    # await bot.forward_messages(int(user_id), messages=event.message)
    
    #--- RandomMsg
    elif text == "/rmsg":
        d = await getRandomDialogID()
        id = random.choice(d['gps'])
        print(id)
        fake = Faker()
        firstName = str(fake.name()).split(' ')[0]
        lastName = str(fake.name()).split(' ')[1]
        bio = fake.job()
        msg = f"{firstName} {lastName} {bio}"
        await bot.send_message(id, msg)
    #--- Ping
    if text == "/ping":
        await event.edit('Pong ;)')
        return
    
    #--- Restart
    elif text == "/re":
        pid = os.getpid()
        fileName = sys.argv[0]
        await event.edit('Restarting Bot...')
        os.system(f"Taskkill /PID {pid} /F && python {fileName} re")
    
    #--- Status
    elif text == "/status":

        #--- Get All Dia
        allDialogs = await getAllDialogsC()
        channels = allDialogs['channels']
        megaGroups = allDialogs['megaGroups']
        groups = allDialogs['groups']
        users = allDialogs['users']
        bots = allDialogs['bots']
        
        #--- Get UpTime
        upTimeSecond = int(str(time.time()).split('.')[0]) - int(str(botData['startTime']).split('.')[0])
        upTime = str(datetime.timedelta(seconds=upTimeSecond))
        
        #--- Memory Usage
        memoryUsage = getMemoryUsage()

        #--- data
        sendText = "📊 Bot Status\n\n"
        sendText += f"channels: `{channels}`\n"
        sendText += f"super groups: `{megaGroups}`\n"
        sendText += f"groups: `{groups}`\n"
        sendText += f"pv: `{users}`\n"
        sendText += f"bots `{bots}`\n"
        sendText += f"\n➖➖➖➖➖\n"
        sendText += f"Robot Memory Usage: `{memoryUsage}`\n"
        sendText += f"Robot UpTime: `{upTime}`"

        await event.edit(sendText)
    
    #--- ping
    elif text.startswith('/ping '):
        ip = text.split(' ')[1]
        h = {
            'Accept': "application/json"
        }
        r = requests.get(f"https://check-host.net/check-ping?host={ip}", headers=h).text
        js = json.loads(r)
        id = js['permanent_link'].split('/')[-1]
        print(id)
        await event.edit(f'Check Result: `/res {id}`')
    
    #--- checkHost
    elif text.startswith('/checkhost '):
        type = text.split(' ')[1]
        ip = text.split(' ')[2]
        h = {
            'Accept': "application/json"
        }
        r = requests.get(f"https://check-host.net/check-{type}?host={ip}", headers=h).text
        js = json.loads(r)
        id = js['permanent_link'].split('/')[-1]
        print(id)
        await event.edit(f'Check Result:\n\ntype: {type}\nhost: {ip}\ncode: `/c{type} {id}`')
    
    #--- res ping
    elif text.startswith('/cping '):
        h = {
            'Accept': "application/json"
        }
        id = text.split(' ')[1]
        r = requests.get(f"https://check-host.net/check-result/{id}", headers=h).text
        js = json.loads(r)
        t = ""
        for con in js:
            try:
                result = str(js[con][0][0][1])[0:8]
                t += f"`{con}: {result}`\n"
            except:
                continue
        if t == "":
            t = "ERROR"
        await event.edit(t)
    
    #--- res http
    elif text.startswith('/chttp '):
        h = {
            'Accept': "application/json"
        }
        id = text.split(' ')[1]
        r = requests.get(f"https://check-host.net/check-result/{id}", headers=h).text
        js = json.loads(r)
        t = ""
        for con in js:
            try:
                result_Time = str(js[con][0][1])[0:5]
                result_d = str(js[con][0][2])
                result_c = str(js[con][0][3])
                t += f"`{con}`: [\n`Time: {result_Time}`\n`Code: {result_c} ({result_d})`\n]\n"
            except:
                continue
        if t == "":
            t = "ERROR"
        await event.edit(t)
    
    #--- Delete Self Messages in group
    elif text.startswith('/adel '):
        await event.edit('OK Wait . . .')
        c = int(text.split(' ')[1]) + 1
        d = 0
        offset = 0
        if c > 100:
            x = 100
            while c - offset >= 100:
                print(f"1: Get History: lim: {x} ** offset: {offset}")
                history = await bot(functions.messages.GetHistoryRequest(peer=int(chat_id), offset_id=0, offset_date=None, add_offset=offset, limit=100, max_id=0, min_id=0, hash=0))
                zz = await delByHistory(history, chat_id, admin, msgid)
                d += len(zz)
                offset += 100
            if c - offset < 100:
                m = c - offset
                print(f"2: Get History: lim: {m} ** offset: {offset}")
                history = await bot(functions.messages.GetHistoryRequest(peer=int(chat_id), offset_id=0, offset_date=None, add_offset=offset, limit=m, max_id=0, min_id=0, hash=0))
                zz = await delByHistory(history, chat_id, admin, msgid)
                d += len(zz)
        else:      
            history = await bot(functions.messages.GetHistoryRequest(peer=int(chat_id), offset_id=0, offset_date=None, add_offset=0, limit=c, max_id=0, min_id=0, hash=0))
            zz = await delByHistory(history, chat_id, admin, msgid)
            d += len(zz)

        await event.edit(f'{d} Message Deleted!')
                
        
    
    #--- screen shot frm video 
    elif text.startswith('/screen^'):
        url = text.split('^')[1]
        second = int(text.split('^')[2])*1000
        vidcap = cv2.VideoCapture(url)
        vidcap.set(cv2.CAP_PROP_POS_MSEC,second)  
        success,image = vidcap.read()
        count = 0
        while success:
            cv2.imwrite("pic.jpg", image) # save frame as JPEG file      
            success,image = vidcap.read()
            print('Read a new frame: ', success)
            count += 1
            break
        await event.delete()
        await bot.send_file(int(event.chat_id), file="pic.jpg", caption="Screenshot :)")
            
    #--- Downlaod part of file
    elif text.startswith('/dl^'):
        url = text.split('^')[1]
        chunkSize = int(text.split('^')[2])
        fileName = url.split('/')[-1]
        fileType = url.split('.')[-1]
        await event.edit(f'Downloading {fileName}')
        response = requests.get(url, stream = True)
        total_length = int(response.headers.get('content-length'))
        Path("dl."+fileType).touch()
        text_file = open("dl."+fileType,"wb")
        for chunk in response.iter_content(chunk_size=chunkSize):
            text_file.write(chunk)
        await event.edit('Downlaod end')
        await bot.send_file(int(event.chat_id), file="dl."+fileType, caption=".,")
        
    #--- Eval
    elif text.startswith('/trun'):
        code = text.split('/trun')[1]
        await eval(code)
    
    #---
    elif text == "/dev":
        all_participants = []
        offset = 0
        limit = 100
        while True:
            participants = await bot(functions.channels.GetParticipantsRequest(
                "CofeSource", types.ChannelParticipantsSearch(''), offset, limit,
                hash=0
            ))
            if not participants.users:
                break
            all_participants.extend(participants.users)
            offset += len(participants.users)
            for item in participants.users:
                if item.username == None:
                    status = item.status
                    print(item.stringify())
                    await bot.kick_participant("CofeSource", item.id)        


#------- Handler
@bot.on(events.NewMessage(func=lambda e: e.is_private or e.is_group))
async def my_event_handler(event):
    await answer(event)




bot.run_until_disconnected()
