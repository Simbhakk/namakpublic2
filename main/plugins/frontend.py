#Github.com/mrinvisible7

import time, os

import logging
from .. import bot as Invix
from .. import userbot, Bot
from .. import FORCESUB as fs
from main.plugins.pyroplug import get_msg
from main.plugins.helpers import get_link, screenshot
from main.plugins.database import add_user, del_user, full_userbase, present_user
from telethon import events
from pyrogram.errors import FloodWait

#from ethon.telefunc import force_sub
from main.plugins.helpers import force_sub

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
logging.getLogger("pyrogram").setLevel(logging.INFO)
logging.getLogger("telethon").setLevel(logging.INFO)

ft = f"You have to join @RajZ_bots & @{fs} to use me.\nFirst join these channel then use this bot."

message = "Send me the message link you want to start saving from, as a reply to this message."
          
process=[]
timer=[]
user=[]
last_message_time = {}
# Define the time limit in seconds
time_limit = 00
 

@Invix.on(events.NewMessage(incoming=True, func=lambda e: e.is_private))
async def clone(event):
    logging.info(event)
    file_name = ''
    if event.is_reply:
        reply = await event.get_reply_message()
        if reply.text == message:
            return
    lit=event.text
    li=lit.split("\n")
    if len(li) > 1:
        await event.reply("max 1 links per message")
        return
    for li in li:
        #1239
    
        try:
            link = get_link(li)
            if not link:
                return
    
        except TypeError:
            return
        s, r = await force_sub(event.client, fs, event.sender_id, ft)
        if s == True:
            await event.reply(ft)
            return
        edit = await event.reply("Processing!")
        id = message.from_user.id
        if not await present_user(id):
            try:
                await add_user(id)
           except:
               pass
        text = message.text
        if link.startswith("http") or link.startswith("www"):
            # Check if the user has sent a message before
            if event.sender_id in last_message_time:
                # Get the time difference between now and the last message time
                time_diff = time.time() - last_message_time[event.sender_id]
                # Check if the time difference is less than the time limit
                if time_diff < time_limit:
                    # Calculate the time remaining until the user can send another message
                    time_remaining = int(time_limit - time_diff)
                    # Send a message to the user with the time remaining
                    await edit.edit(f"Send next link after {time_remaining} seconds.")
                    return
            # Store the current time as the last message time for the user
            last_message_time[event.sender_id] = time.time()
      
        if "|" in li:
            url = li
            url_parts = url.split("|")
            if len(url_parts) == 2:
            
                file_name = url_parts[1]
        if file_name is not None:
            file_name = file_name.strip()                
        try:
            if 't.me/' not in link:
                await edit.edit("invalid link")
                ind = user.index(f'{int(event.sender_id)}')
                user.pop(int(ind))
                return
            if 't.me/' in link:
                msg_id = 0
                try:
                    msg_id = int(link.split("/")[-1])
                except ValueError:
                    if '?single' in link:
                        link_ = link.split("?single")[0]
                        msg_id = int(link_.split("/")[-1])
                    else:
                        msg_id = -1
                m = msg_id
                await get_msg(userbot, Bot, event.sender_id, edit.id, link, m, file_name)
        except FloodWait as fw:
            await Invix.send_message(event.sender_id, f'Try again after {fw.value} seconds due to floodwait from Telegram.\n Or use our second bot:- @Save_Restricted_Content_Raj_Bot 🤭')
            await edit.delete()
        except Exception as e:
            logging.info(e)
            await Invix.send_message(event.sender_id, f"An error occurred during cloning of `{link}`\n\n**Error:** {str(e)}")
            await edit.delete()
