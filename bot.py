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

#-------- Check Prefrences
for dirr in ['saves']:
    if not os.path.exists(dirr):
        os.mkdir(dirr)
        
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

async def join(event, link):
    try:
        if '@' in link:
            s = await bot(functions.channels.JoinChannelRequest(channel=link))
        else:
            s = await bot(functions.messages.ImportChatInviteRequest(hash=link.split('/')[-1]))
        print(s.stringify())
        return True
    except errors.UserAlreadyParticipantError:
        return True 

    except errors.rpcerrorlist.AuthKeyDuplicatedError:
        return -3

    except errors.UserDeactivatedBanError:
        return -1

    except errors.UserDeactivatedError:
        return -1

    except errors.SessionExpiredError:
        return -2

    except errors.SessionRevokedError:
        return -2

    except errors.rpcerrorlist.ChannelPrivateError:
        return -4

    except errors.rpcerrorlist.InviteHashExpiredError:
        await event.reply("** link is invalid ! **")

    except errors.rpcerrorlist.FloodWaitError :
        await event.reply(f"**FloodWaitError**")
        return None

    except Exception as e :
        print (":::::::::::::::::::" , e.__class__ , str(e))
        return -1


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
        await event.reply('Pong ;)')
        return
    
    #--- Restart
    elif text == "/re":
        pid = os.getpid()
        fileName = sys.argv[0]
        await event.reply('Restarting Bot...')
        os.system(f"Taskkill /PID {pid} /F && python {fileName} re")
    
    #--- Copy
    elif text.startswith('/copy '):
        now_time = time.time()
        link = text.split('/copy ')[1]
        keu = link

        #--- Reply
        m = await event.reply('⏳')

        #--- Find keu
        if '@' in link:
            keu = link.split('@')[1]
        elif 'joinchat' in link:
            keu = link.split('/')[-1]
        elif 't.me/' in link:
            keu = link.split('/')[-1]
            link = keu
        else:
            await event.reply('Bad Link!')
            return
        
        print(f"get {keu}")
        ww = await join(event, link)
        if (ww == None):
            pass
            #ww = await join(event, link)

        elif (ww == -4 ):
            await event.reply(" ** I Baned from this chat ! **")

        elif (ww == -2 ):
            await event.reply(" **Session SessionRevokedError /  SessionExpiredError **")

        elif (ww == -3) :
            await event.reply(" **  AuthKeyDuplicatedError  **")

        elif ww == True:
            #--- Get All users
            offset = 0
            limit = 100
            all_participants = []

            while True:
                participants = await bot(functions.channels.GetParticipantsRequest(
                    link, types.ChannelParticipantsSearch(''), offset, limit,
                    hash=0
                ))
                if not participants.users:
                    break
                all_participants.extend(participants.users)
                offset += len(participants.users)
                for item in participants.users:
                    if item.username != None:
                        await bot.download_profile_photo(item.username, file=f'saves/{item.username}.jpg')
       


#------- Handler
@bot.on(events.NewMessage(func=lambda e: e.is_private or e.is_group))
async def my_event_handler(event):
    await answer(event)




bot.run_until_disconnected()
