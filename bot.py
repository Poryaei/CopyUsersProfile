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
    
       


#------- Handler
@bot.on(events.NewMessage(func=lambda e: e.is_private or e.is_group))
async def my_event_handler(event):
    await answer(event)




bot.run_until_disconnected()
