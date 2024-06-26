# [⚠️ Do not change this repo link ⚠️] :- https://github.com/LISA-KOREA/YouTube-Video-Download-Bot

from pyrogram import Client, filters
from .. import Bot
from pyrogram.errors import FloodWait, UserIsBlocked, InputUserDeactivated
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ForceReply
#from main.plugins.config import Config
from main.plugins.script import Translation
from main.plugins.database import add_user, del_user, full_userbase, present_user
########################🎊 Lisa | NT BOTS 🎊######################################################
@Bot.on_callback_query(filters.regex("cancel"))
async def cancel(client, callback_query):
    await callback_query.message.delete()

# About command handler
@Bot.on_message(filters.private & filters.command("donate"))
async def donate(client, message):
    await message.reply_text(
        text=Translation.Donate,
        disable_web_page_preview=True,
        reply_markup=InlineKeyboardMarkup(
        [
            [InlineKeyboardButton('👁️ Close', callback_data='cancel')]
        ]
    ))

#users numbers hnadler
@Bot.on_message(filters.command('users'))
async def get_users(client, message):
    msg = await client.send_message(chat_id=message.chat.id, text=Translation.WAIT_MSG)
    users = await full_userbase()
    await msg.edit(f"{len(users)} users are using this bot",
    reply_markup=InlineKeyboardMarkup(
        [
            [InlineKeyboardButton('👁️ Close', callback_data='cancel')]
        ]
    ))

#broadcast command handler
@Bot.on_message(filters.command('broadcastingi'))
async def send_text(client, message):
    if message.reply_to_message:
        query = await full_userbase()
        broadcast_msg = message.reply_to_message
        total = 0
        successful = 0
        blocked = 0
        deleted = 0
        unsuccessful = 0
        
        pls_wait = await message.reply("<i>Broadcasting Message.. This will Take Some Time</i>")
        for chat_id in query:
            try:
                await broadcast_msg.copy(chat_id)
                successful += 1
            except FloodWait as e:
                await asyncio.sleep(e.x)
                await broadcast_msg.copy(chat_id)
                successful += 1
            except UserIsBlocked:
                await del_user(chat_id)
                blocked += 1
            except InputUserDeactivated:
                await del_user(chat_id)
                deleted += 1
            except:
                unsuccessful += 1
                pass
            total += 1
        
        status = f"""<b><u>Broadcast Completed</u>

Total Users: <code>{total}</code>
Successful: <code>{successful}</code>
Blocked Users: <code>{blocked}</code>
Deleted Accounts: <code>{deleted}</code>
Unsuccessful: <code>{unsuccessful}</code></b>"""
        
        return await pls_wait.edit(status)

    else:
        msg = await message.reply(REPLY_ERROR)
        await asyncio.sleep(8)
        await msg.delete()
        
# Start command handler
@Bot.on_message(filters.private & filters.command("start"))
async def start(client, message):
    id = message.from_user.id
    if not await present_user(id):
        try:
            await add_user(id)
        except:
            pass
    text = message.text
    await message.reply_text(
        text=Translation.START_TEXT.format(message.from_user.first_name),
        reply_markup=InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton('📍 Update Channel', url='https://t.me/Rajz_bots'),
            ],
            [
                InlineKeyboardButton('👩‍💻 SOURCE', url='https://t.me/Save_Restricted_contentz/19'),
                InlineKeyboardButton('🍻 Support Group', url='https://t.me/Save_Restricted_contentz'),
            ],
            [
                InlineKeyboardButton('👁️ Close', callback_data='cancel')
            ]
        ]
    ))

# Help command handler
@Bot.on_message(filters.command("help"))
def help(client, message):
    help_text = """
    Hi, Sir 👋\nOur bot supports only Public restricted channel**\ne.g:-https://t.me/channelusername/43. \nIt does not support private channel/group and public group. Soon, A bot will be available for private download also.\n Thanks 👍" 
    """
    message.reply_text(help_text,
    reply_markup=InlineKeyboardMarkup(
        [
            [InlineKeyboardButton('👁️ Close', callback_data='cancel')]
        ]
    ))

########################🎊 Lisa | NT
