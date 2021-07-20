# © @Mr_Dark_Prince

from config import *
from pyrogram.types.bots_and_keyboards import reply_keyboard_markup
from pyrogram import idle, filters
from pyrogram.types import InlineKeyboardMarkup
from pyrogram.types import InlineKeyboardButton

from AlexaSongBot.mrdarkprince import ignore_blacklisted_users
from AlexaSongBot.sql.chat_sql import add_chat_to_db

from AlexaSongBot.sql.chat_sql import load_chats_list, remove_chat_from_db
from io import BytesIO
from pyrogram.errors import BadRequest
import AlexaSongBot.sql.blacklist_sql as sql
from AlexaSongBot.mrdarkprince import get_arg
import io
import sys
from AlexaSongBot import *
from pyrogram import Client, filters
from config import OWNER_ID



owner_help = """
/blacklist user_id
/unblacklist user_id
/broadcast اذاعة
/sbs مشتركين البوت
/chatlist الكروبات 
"""



@app.on_message(filters.create(ignore_blacklisted_users)  & filters.command("start") )
async def start (client, message):
    chat_id = message.chat.id
    user_id = message.from_user["id"]
    add_chat_to_db(str(chat_id))

@app.on_message(filters.create(ignore_blacklisted_users) & filters.command("help"))
async def help(client, message):
    if message.from_user["id"] == OWNER_ID:
        await message.reply(owner_help)
        return ""
    text = "ارسل صورة للتعديل عليها🌈🏞"
    await message.reply(text)

@app.on_message(filters.user(OWNER_ID) & filters.command("broadcast"))
async def broadcast(client, message):
    to_send = get_arg(message)
    chats = load_chats_list()
    success = 0
    failed = 0
    for chat in chats:
        
        try:
            await app.send_message(int(chat), to_send)

            success += 1
        except:
            failed += 1
            remove_chat_from_db(str(chat))
            pass
    await message.reply(
        f"Message sent to {success} chat(s). {failed} chat(s) failed recieve message"
    )


@app.on_message(filters.user(OWNER_ID) & filters.command("chatlist"))
async def chatlist(client, message):
    chats = []
    all_chats = load_chats_list()
    for i in all_chats:
        if str(i).startswith("-"):
            chats.append(i)
    chatfile = "List of chats.\n0. Chat ID | Members count | Invite Link\n"
    P = 1
    for chat in chats:
        try:
            link = await app.export_chat_invite_link(int(chat))
        except:
            link = "Null"
        try:
            members = await app.get_chat_members_count(int(chat))
        except:
            members = "Null"
        try:
            chatfile += "{}. {} | {} | {}\n".format(P, chat, members, link)
            P = P + 1
        except:
            pass
    with BytesIO(str.encode(chatfile)) as output:
        output.name = "chatlist.txt"
        await message.reply_document(document=output, disable_notification=True)


@app.on_message(filters.user(OWNER_ID) & filters.command("blacklist"))
async def blacklist(client, message):
    if message.reply_to_message:
        user_id = message.reply_to_message.from_user["id"]
    else:
        arg = get_arg(message)
        if len(arg) != 1:
            await message.reply(
                "pass a user id or user name or reply to a user message"
            )
            return ""
        if arg.startswith("@"):
            try:
                user = await app.get_users(arg)
                user_id = user.id
            except BadRequest as ex:
                await message.reply("not a valid user")
                print(ex)
                return ""
        else:
            user_id = int(arg)
        sql.add_user_to_bl(int(user_id))
        await message.reply(f"[blacklisted](tg://user?id={user_id})")


@app.on_message(filters.user(OWNER_ID) & filters.command("unblacklist"))
async def unblacklist(client, message):
    if message.reply_to_message:
        user_id = message.reply_to_message.from_user["id"]
    else:
        arg = get_arg(message)
        if len(arg) != 1:
            await message.reply(
                "pass a user id or user name or reply to a user message"
            )
            return ""
        if arg.startswith("@"):
            try:
                user = await app.get_users(arg)
                user_id = user.id
            except BadRequest:
                await message.reply("not a valid user")
                return ""
        else:
            user_id = int(arg)
        sql.rem_user_from_bl(int(user_id))
        await message.reply(f"[unblacklisted](tg://user?id={user_id})")


@app.on_message(filters.user(OWNER_ID) & filters.command("sbs"))
async def eval(client, message):
    chats = load_chats_list()
    sbs= len(chats)
    await message.reply(
        f"الاحصائيات : \n\n عدد المشتركين في البوت  {sbs}"

    )



@app.on_message( filters.photo & filters.private)
async def sentphot (client, message):
    chat_id = message.chat.i
    add_chat_to_db(str(chat_id))
 








app.start()
LOGGER.info("Your bot is now online.")
idle()
