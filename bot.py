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
        bot.send_message("admin", "🔄 Bot Restarted")
# -------- Functions


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
