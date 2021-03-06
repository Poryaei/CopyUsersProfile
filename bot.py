# ------- Import Library's
import asyncio
from asyncio.windows_events import NULL
import threading
from telethon.tl import types as tl_telethon_types
from telethon.sync import TelegramClient, functions, types, events, errors
from telethon.tl.functions.messages import ImportChatInviteRequest

import os
import sys
import time
import requests
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
maxRuningTasks = 10
runingTasks = 0
process = False

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
    
def findTelegramPhoto(username):
    username = username.replace("@", "")
    try:
        r = requests.get(f'https://t.me/{username}', timeout=10)
        if not 'tgme_page_photo_image' in r.text:
            return NULL
        return r.text.split('<img class="tgme_page_photo_image" src="')[1].split('"')[0]
    except Exception as e:
        print(e)
        
    return NULL


def saveImgFromUrl(url, filename):
    try:
        r = requests.get(url, allow_redirects=True)
        open(filename, 'wb').write(r.content)
    except:
        pass

def botprocess(username):
    global runingTasks
    global botData
    try:
        url = findTelegramPhoto(username)
        if url != NULL:
            saveImgFromUrl(url, f'saves/{username}.jpg')
            botData['saved'] += 1
    except Exception as e:
        print(e)
        botData['problem'] += 1
    runingTasks -= 1
    return runingTasks

def startSavingProcess(usernameList):
    global runingTasks
    global process
    global botData
    botData['saved'] = 0
    botData['problem'] = 0
    botData['total'] = len(usernameList)
    botData['lastedit'] = time.time()
    print('[!] Task starting')
    while len(usernameList) != 0 and process:
        for user in usernameList:
            if runingTasks > maxRuningTasks:
                continue
            threading.Thread(target=botprocess, args=(user,)).start()
            runingTasks += 1
            usernameList.remove(user)
            if len(usernameList) == 0 or process == False:
                break
        if len(usernameList) == 0 or process == False:
            break
    process = False



# -------- Start Receiving Message's
async def answer(event):
    global process
    global botData
    text = event.raw_text
    user_id = event.sender_id

    #--- Filter Messages
    if user_id != admin:
        return
    
    
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
            usernameList = []
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
                        # await bot.download_profile_photo(item.username, file=f'saves/{item.username}.jpg')
                        # url = findTelegramPhoto(item.username)
                        # if url != NULL:
                        #     saveImgFromUrl(url, f'saves/{item.username}.jpg')
                        usernameList.append(item.username)
            process = True
            await m.edit('Saving Profile started! send /cancel to stop')
            botData['event'] = m
            botData['saved'] = 0
            botData['problem'] = 0
            botData['total'] = len(usernameList)
            threading.Thread(target=startSavingProcess, args=(usernameList,)).start()
            asyncio.create_task(showProcess())
            print("H")
            # startSavingProcess(usernameList)

            
    
    # Cancel
    elif text == '/cancel':
        process = False
        await event.reply('OK')
       
async def showProcess():
    global process
    global botData
    startT = time.time()
    startA = time.time()
    print('[!] Alert Starting')
    while True :
        if not time.time() - botData['lastedit'] >= 5:
            continue
        if process:
            total = botData['total']
            saved = botData['saved']
            error = botData['problem']
            try:
                await botData['event'].edit(f'total: {total}\nsaved: {saved}\nerror: {error}\n\nsend /cancel to stop')
            except:
                pass
            botData['lastedit'] = time.time()
        else:
            await botData['event'].edit(f'total: {total}\nsaved: {saved}\nerror: {error}\n\nend')
            break
        

#------- Handler
@bot.on(events.NewMessage(func=lambda e: e.is_private or e.is_group))
async def my_event_handler(event):
    await answer(event)

    


bot.run_until_disconnected()
