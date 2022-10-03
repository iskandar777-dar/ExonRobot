"""
MIT License

Copyright (c) 2022 Aʙɪsʜɴᴏɪ

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import html
from typing import Optional

from telegram import Chat, ChatPermissions, Message, ParseMode, User
from telegram.error import BadRequest
from telegram.ext import CommandHandler, Filters, MessageHandler
from telegram.utils.helpers import mention_html

from Exon import dispatcher
from Exon.modules.connection import connected
from Exon.modules.helper_funcs.alternate import send_message, typing_action
from Exon.modules.helper_funcs.chat_status import is_user_admin, user_admin
from Exon.modules.helper_funcs.string_handling import extract_time
from Exon.modules.log_channel import loggable
from Exon.modules.sql import antiflood_sql as sql
from Exon.modules.sql.approve_sql import is_approved

FLOOD_GROUP = 3


@loggable
def check_flood(update, context) -> str:
    user = update.effective_user  # type: Optional[User]
    chat = update.effective_chat  # type: Optional[Chat]
    msg = update.effective_message  # type: Optional[Message]

    if is_approved(chat.id, user.id):
        sql.update_flood(chat.id, None)
        return

    if not user:  # ignore channels
        return ""

    # ignore admins
    if is_user_admin(chat, user.id):
        sql.update_flood(chat.id, None)
        return ""

    should_ban = sql.update_flood(chat.id, user.id)
    if not should_ban:
        return ""

    try:
        getmode, getvalue = sql.get_flood_setting(chat.id)
        if getmode == 1:
            chat.ban_member(user.id)
            execstrings = "ʙᴀɴɴᴇᴅ"
            tag = "BANNED"
        elif getmode == 2:
            chat.ban_member(user.id)
            chat.unban_member(user.id)
            execstrings = "ᴋɪᴄᴋᴇᴅ"
            tag = "KICKED"
        elif getmode == 3:
            context.bot.restrict_chat_member(
                chat.id, user.id, permissions=ChatPermissions(can_send_messages=False)
            )
            execstrings = "ᴍᴜᴛᴇᴅ"
            tag = "MUTED"
        elif getmode == 4:
            bantime = extract_time(msg, getvalue)
            chat.ban_member(user.id, until_date=bantime)
            execstrings = f"ʙᴀɴɴᴇᴅ ғᴏʀ {getvalue}"
            tag = "TBAN"
        elif getmode == 5:
            mutetime = extract_time(msg, getvalue)
            context.bot.restrict_chat_member(
                chat.id,
                user.id,
                until_date=mutetime,
                permissions=ChatPermissions(can_send_messages=False),
            )
            execstrings = f"ᴍᴜᴛᴇᴅ ғᴏʀ {getvalue}"
            tag = "TMUTE"
        send_message(
            update.effective_message,
            f"ᴍᴀᴜ sᴘᴀᴍ ?, ᴍᴀᴀꜰ ɪᴛᴜ ʙᴜᴋᴀɴ ʀᴜᴍᴀʜᴍᴜ ᴋᴀᴡᴀɴ!\n{execstrings}!",
        )

        return f"<b>{html.escape(chat.title)}:</b>\n#{tag}\n<b>User:</b> {mention_html(user.id, user.first_name)}\nᴍᴇᴍʙᴀɴᴊɪʀɪ ɢʀᴜᴘ."

    except BadRequest:
        msg.reply_text(
            "sᴀʏᴀ ᴛɪᴅᴀᴋ ᴅᴀᴘᴀᴛ ᴍᴇᴍʙᴀᴛᴀsɪ ᴏʀᴀɴɢ ᴅɪ sɪɴɪ, ʙᴇʀɪ sᴀʏᴀ ɪᴢɪɴ ᴛᴇʀʟᴇʙɪʜ ᴅᴀʜᴜʟᴜ, sᴀᴍᴘᴀɪ sᴀᴀᴛ ɪᴛᴜ sᴀʏᴀ ᴀᴋᴀɴ ᴍᴇɴᴏɴᴀᴋᴛɪꜰᴋᴀɴ ᴀɴᴛɪ-ʙᴀɴᴊɪʀ."
        )
        sql.set_flood(chat.id, 0)
        return f"<b>{chat.title}:</b>\n#INFO\nᴛɪᴅᴀᴋ ᴍᴇᴍɪʟɪᴋɪ ɪᴢɪɴ ʏᴀɴɢ ᴄᴜᴋᴜᴘ ᴜɴᴛᴜᴋ ᴍᴇᴍʙᴀᴛᴀsɪ ᴘᴇɴɢɢᴜɴᴀ, ᴊᴀᴅɪ ɴᴏɴᴀᴋᴛɪꜰᴋᴀɴ ᴀɴᴛɪ-ʙᴀɴᴊɪʀ sᴇᴄᴀʀᴀ ᴏᴛᴏᴍᴀᴛɪs"


@user_admin
@loggable
@typing_action
def set_flood(update, context) -> str:
    chat = update.effective_chat  # type: Optional[Chat]
    user = update.effective_user  # type: Optional[User]
    message = update.effective_message  # type: Optional[Message]
    args = context.args

    conn = connected(context.bot, update, chat, user.id, need_admin=True)
    if conn:
        chat_id = conn
        chat_name = dispatcher.bot.getChat(conn).title
    else:
        if update.effective_message.chat.type == "private":
            send_message(
                update.effective_message,
                "ᴘᴇʀɪɴᴛᴀʜ ɪɴɪ ᴅɪᴍᴀᴋsᴜᴅᴋᴀɴ ᴜɴᴛᴜᴋ ᴅɪɢᴜɴᴀᴋᴀɴ ᴅᴀʟᴀᴍ ɢʀᴜᴘ ʙᴜᴋᴀɴ ᴅɪ ᴘᴍ",
            )
            return ""
        chat_id = update.effective_chat.id
        chat_name = update.effective_message.chat.title

    if len(args) >= 1:
        val = args[0].lower()
        if val in ("off", "no", "0"):
            sql.set_flood(chat_id, 0)
            if conn:
                text = message.reply_text(
                    f"ᴀɴᴛɪꜰʟᴏᴏᴅ ᴛᴇʟᴀʜ ᴍᴇɴᴏɴᴀᴋᴛɪꜰᴋᴀɴ ʟᴇʙᴀʜ ᴅɪ {chat_name}."
                )
            else:
                text = message.reply_text("ᴀɴᴛɪғʟᴏᴏᴅ ʜᴀs ʙᴇᴇɴ ᴅɪsᴀʙʟᴇᴅ.")
            send_message(update.effective_message, text, parse_mode="markdown")

        elif val.isdigit():
            amount = int(val)
            if amount <= 0:
                sql.set_flood(chat_id, 0)
                if conn:
                    text = message.reply_text(
                        f"ᴀɴᴛɪꜰʟᴏᴏᴅ ᴛᴇʟᴀʜ ᴍᴇɴᴏɴᴀᴋᴛɪꜰᴋᴀɴ ʟᴇʙᴀʜ ᴅɪ {chat_name}."
                    )
                else:
                    text = message.reply_text("ᴀɴᴛɪғʟᴏᴏᴅ ʜᴀs ʙᴇᴇɴ ᴅɪsᴀʙʟᴇᴅ.")
                return f"<b>{html.escape(chat_name)}:</b>\n#sᴇᴛғʟᴏᴏᴅ\n<b>Admin:</b> {mention_html(user.id, user.first_name)}\nᴍᴇɴᴏɴᴀᴋᴛɪꜰᴋᴀɴ ᴀɴᴛɪꜰʟᴏᴏᴅ."

            if amount < 3:
                send_message(
                    update.effective_message,
                    "ᴀɴᴛɪꜰʟᴏᴏᴅ ʜᴀʀᴜs sᴀʟᴀʜ sᴀᴛᴜ 0 (ᴍᴇɴᴏɴᴀᴋᴛɪꜰᴋᴀɴ) ᴀᴛᴀᴜ ᴀɴɢᴋᴀɴʏᴀ ʟᴇʙɪʜ ʙᴇsᴀʀ ᴅᴀʀɪ 3!",
                )
                return ""
            sql.set_flood(chat_id, amount)
            if conn:
                text = message.reply_text(
                    f"ᴀɴᴛɪ-ꜰʟᴏᴏᴅ ᴛᴇʟᴀʜ ᴅɪᴀᴛᴜʀ ᴋᴇ {amount} ᴅɪ ɢʀᴜᴘ: {chat_name}"
                )

            else:
                text = message.reply_text(
                    f"ʙᴇʀʜᴀsɪʟ ᴍᴇᴍᴘᴇʀʙᴀʀᴜɪ ʙᴀᴛᴀs ᴀɴᴛɪ-ꜰʟᴏᴏᴅ ᴋᴇ {amount}!"
                )

            send_message(update.effective_message, text, parse_mode="markdown")
            return f"<b>{html.escape(chat_name)}:</b>\n#SETFLOOD\n<b>Admin:</b> {mention_html(user.id, user.first_name)}\nSet antiflood to <code>{amount}</code>."

        else:
            message.reply_text("argumen tidak valid silakan gunakan nomor, 'off' ᴏʀ 'no'")
    else:
        message.reply_text(
            (
                "ᴜsᴇ `/setflood ɴᴏᴍᴏʀ ᴜɴᴛᴜᴋ ᴍᴇɴɢᴀᴋᴛɪꜰᴋᴀɴ ᴀɴᴛɪ-ꜰʟᴏᴏᴅ.\nᴀᴛᴀᴜ ᴍᴇɴɢɢᴜɴᴀᴋᴀɴ `/setflood off` ᴍᴇɴᴏɴᴀᴋᴛɪꜰᴋᴀɴ ᴀɴᴛɪꜰʟᴏᴏᴅ!."
            ),
            parse_mode="markdown",
        )
    return ""


@typing_action
def flood(update, context):
    chat = update.effective_chat  # type: Optional[Chat]
    user = update.effective_user  # type: Optional[User]
    msg = update.effective_message

    conn = connected(context.bot, update, chat, user.id, need_admin=False)
    if conn:
        chat_id = conn
        chat_name = dispatcher.bot.getChat(conn).title
    else:
        if update.effective_message.chat.type == "private":
            send_message(
                update.effective_message,
                "ᴛʜɪs ᴄᴏᴍᴍᴀɴᴅ ɪs ᴍᴇᴀɴᴛ ᴛᴏ ᴜsᴇ ɪɴ ɢʀᴏᴜᴘ ɴᴏᴛ ɪɴ PM",
            )
            return
        chat_id = update.effective_chat.id
        chat_name = update.effective_message.chat.title

    limit = sql.get_flood_limit(chat_id)
    if limit == 0:
        text = (
            msg.reply_text(f"sᴀʏᴀ ᴛɪᴅᴀᴋ ᴍᴇᴍʙᴇʀʟᴀᴋᴜᴋᴀɴ ᴀɴᴛɪꜰʟᴏᴏᴅ ᴘᴀᴅᴀ {chat_name}!")
            if conn
            else msg.reply_text("sᴀʏᴀ ᴛɪᴅᴀᴋ ᴍᴇɴᴇʀᴀᴘᴋᴀɴ ᴋᴏɴᴛʀᴏʟ ᴀɴᴛɪꜰʟᴏᴏᴅ ᴅɪ sɪɴɪ!")
        )

    elif conn:
        text = msg.reply_text(
            f"sᴀʏᴀ ᴍᴇᴍʙᴀᴛᴀsɪ {ʟɪᴍɪᴛ} sᴇᴄᴜᴛꞮᴠᴇ sᴀɢᴇs sᴀᴀᴛ ɪɴɪ sᴀʏᴀ ᴍᴇᴍʙᴀᴛᴀsɪ ᴀɴɢɢᴏᴛᴀ sᴇᴛᴇʟᴀʜ {ʟɪᴍɪᴛ} ᴘᴇsᴀɴ ʙᴇʀᴛᴜʀᴜᴛ-ᴛᴜʀᴜᴛ ᴅɪ {chat_name}."
        )

    else:
        text = msg.reply_text(
            f"sᴀʏᴀ ᴍᴇᴍʙᴀᴛᴀsɪ {ʟɪᴍɪᴛ} sᴇᴄᴜᴛꞮᴠᴇ sᴀɢᴇs sᴀᴀᴛ ɪɴɪ sᴀʏᴀ ᴍᴇᴍʙᴀᴛᴀsɪ ᴀɴɢɢᴏᴛᴀ sᴇᴛᴇʟᴀʜ {ʟɪᴍɪᴛ} ᴘᴇsᴀɴ."
        )

    send_message(update.effective_message, text, parse_mode="markdown")


@user_admin
@loggable
@typing_action
def set_flood_mode(update, context):
    chat = update.effective_chat  # type: Optional[Chat]
    user = update.effective_user  # type: Optional[User]
    msg = update.effective_message  # type: Optional[Message]
    args = context.args

    conn = connected(context.bot, update, chat, user.id, need_admin=True)
    if conn:
        chat = dispatcher.bot.getChat(conn)
        chat_id = conn
        chat_name = dispatcher.bot.getChat(conn).title
    else:
        if update.effective_message.chat.type == "private":
            send_message(
                update.effective_message,
                "ᴘᴇʀɪɴᴛᴀʜ ɪɴɪ ᴅɪᴍᴀᴋsᴜᴅᴋᴀɴ ᴜɴᴛᴜᴋ ᴅɪɢᴜɴᴀᴋᴀɴ ᴅᴀʟᴀᴍ ʀᴏᴜᴘ ʙᴜᴋᴀɴ ᴅɪ ᴘᴍ",
            )
            return ""
        chat = update.effective_chat
        chat_id = update.effective_chat.id
        chat_name = update.effective_message.chat.title

    if args:
        if args[0].lower() == "ban":
            settypeflood = "ʙᴀɴ"
            sql.set_flood_strength(chat_id, 1, "0")
        elif args[0].lower() == "kick":
            settypeflood = "ᴋɪᴄᴋ"
            sql.set_flood_strength(chat_id, 2, "0")
        elif args[0].lower() == "mute":
            settypeflood = "ᴍᴜᴛᴇ"
            sql.set_flood_strength(chat_id, 3, "0")
        elif args[0].lower() == "tban":
            if len(args) == 1:
                teks = """sᴇᴘᴇʀᴛɪɴʏᴀ ᴀɴᴅᴀ ʟᴇʟᴀʜ ᴍᴇɴɢᴀᴛᴜʀ ɴɪʟᴀɪ ᴛɪᴍʀ ᴜɴᴛᴜᴋ ᴀɴᴛɪꜰʟᴏᴏᴅ ᴛᴇᴛᴀᴘɪ ᴀɴᴅᴀ ᴛɪᴅᴀᴋ ᴍᴇɴᴇɴᴛᴜᴋᴀɴ ᴡᴀᴋᴛᴜ; ᴛʀʏ, `/setfloodmode tban <timevalue>`.
    ᴇxᴀᴍᴘʟᴇs ᴏғ ᴛɪᴍᴇ ᴠᴀʟᴜᴇ: 4ᴍ = 4 ᴍɪɴᴜᴛᴇs, 3h = 3 ʜᴏᴜʀs, 6d = 6 ᴅᴀʏs, 5w = 5 ᴡᴇᴇᴋs."""
                send_message(update.effective_message, teks, parse_mode="markdown")
                return
            settypeflood = f"ᴛʙᴀɴ ғᴏʀ {args[1]}"
            sql.set_flood_strength(chat_id, 4, str(args[1]))
        elif args[0].lower() == "tmute":
            if len(args) == 1:
                teks = """It ʟᴏᴏᴋs ʟɪᴋᴇ ʏᴏᴜ ᴛʀɪᴇᴅ ᴛᴏ sᴇᴛ ᴛɪᴍᴇ ᴠᴀʟᴜᴇ ғᴏʀ ᴀɴᴛɪғʟᴏᴏᴅ ʙᴜᴛ ʏᴏᴜ ᴅɪᴅɴ'ᴛ sᴘᴇᴄɪғɪᴇᴅ ᴛɪᴍᴇ; ᴛʀʏ, `/setfloodmode tmute <timevalue>`.
    ᴇxᴀᴍᴘʟᴇs ᴏғ ᴛɪᴍᴇ ᴠᴀʟᴜᴇ: 4m = 4 ᴍɪɴᴜᴛᴇs, 3h = 3 ʜᴏᴜʀs, 6d = 6 ᴅᴀʏs, 5w = 5 ᴡᴇᴇᴋs."""
                send_message(update.effective_message, teks, parse_mode="markdown")
                return
            settypeflood = f"ᴛᴍᴜᴛᴇ ғᴏʀ {args[1]}"
            sql.set_flood_strength(chat_id, 5, str(args[1]))
        else:
            send_message(
                update.effective_message, "I ᴏɴʟʏ ᴜɴᴅᴇʀsᴛᴀɴᴅ ban/kick/mute/tban/tmute!"
            )
            return
        if conn:
            text = msg.reply_text(
                f"ᴇxᴄᴇᴇᴅɪɴɢ ᴄᴏɴsᴇᴄᴜᴛɪᴠᴇ ғʟᴏᴏᴅ ʟɪᴍɪᴛ ᴡɪʟʟ ʀᴇsᴜʟᴛ ɪɴ {settypeflood} ɪɴ {chat_name}!"
            )

        else:
            text = msg.reply_text(
                f"ᴇxᴄᴇᴇᴅɪɴɢ ᴄᴏɴsᴇᴄᴜᴛɪᴠᴇ ғʟᴏᴏᴅ ʟɪᴍɪᴛ ᴡɪʟʟ ʀᴇsᴜʟᴛ ɪɴ {settypeflood}!"
            )

        send_message(update.effective_message, text, parse_mode="markdown")
        return f"<b>{settypeflood}:</b>\n<b>Admin:</b> {html.escape(chat.title)}\nHas changed antiflood mode. User will {mention_html(user.id, user.first_name)}."

    getmode, getvalue = sql.get_flood_setting(chat.id)
    if getmode == 1:
        settypeflood = "ʙᴀɴ"
    elif getmode == 2:
        settypeflood = "ᴋɪᴄᴋ"
    elif getmode == 3:
        settypeflood = "ᴍᴜᴛᴇ"
    elif getmode == 4:
        settypeflood = f"ᴛʙᴀɴ ғᴏʀ {getvalue}"
    elif getmode == 5:
        settypeflood = f"ᴛᴍᴜᴛᴇ ғᴏʀ {getvalue}"
    if conn:
        text = msg.reply_text(
            f"ᴘᴇsᴀɴ ᴅᴀʀɪ ʙᴀᴛᴀs ꜰʟᴏᴏᴅ ᴀᴋᴀɴ ᴍᴇɴɢᴀᴋɪʙᴀᴛᴋᴀɴ {settypeflood} ᴅᴀʟᴀᴍ {chat_name}."
        )

    else:
        text = msg.reply_text(
            f"ᴍᴇɴɢɪʀɪᴍ ʟᴇʙɪʜ ʙᴀɴʏᴀᴋ ᴍsᴇ ᴅᴀʀɪᴘᴀᴅᴀ ʙᴀᴛᴀs ʙᴀɴᴊɪʀ ᴀᴋᴀɴ ᴍᴇɴɢʜᴀsɪʟᴋᴀɴ {settypeflood}."
        )

    send_message(update.effective_message, text, parse_mode=ParseMode.MARKDOWN)
    return ""


def __migrate__(old_chat_id, new_chat_id):
    sql.migrate_chat(old_chat_id, new_chat_id)


def __chat_settings__(chat_id, user_id):
    limit = sql.get_flood_limit(chat_id)
    if limit == 0:
        return "ɴᴏᴛ ᴇɴғᴏʀᴄɪɴɢ ᴛᴏ ғʟᴏᴏᴅ ᴄᴏɴᴛʀᴏʟ."
    return f"ᴀɴᴛɪғʟᴏᴏᴅ ʜᴀs ʙᴇᴇɴ sᴇᴛ ᴛᴏ`{limit}`."


__help__ = """
*ᴍᴇᴍᴜɴɢᴋɪɴᴋᴀɴ ᴀɴᴅᴀ ᴍᴇɴɢᴀᴍʙɪʟ ᴛɪɴᴅᴀᴋᴀɴ ᴘᴀᴅᴀ ᴘᴇɴɢɢᴜɴᴀ ʏᴀɴɢ ᴍᴇɴɢɪʀɪᴍ ʟᴇʙɪʜ ᴅᴀʀɪ x ᴘᴇsᴀɴ ʙᴇʀᴛᴜʀᴜᴛ-ᴛᴜʀᴜᴛ. ᴍᴇʟᴇʙɪʜɪ ʙᴀɴᴊɪʀ ʏᴀɴɢ ᴅɪᴛᴇᴛᴀᴘᴋᴀɴ \nᴀᴋᴀɴ ᴍᴇɴɢᴀᴋɪʙᴀᴛᴋᴀɴ ᴘᴇᴍʙᴀᴛᴀsᴀɴ ᴘᴇɴɢɢᴜɴᴀ ᴛᴇʀsᴇʙᴜᴛ. ɪɴɪ ᴀᴋᴀɴ ᴍᴇ-ᴍɪᴜᴛᴇ ᴘᴇɴɢɢᴜɴᴀ ᴊɪᴋᴀ ᴍᴇʀᴇᴋᴀ ᴍᴇɴɢɪʀɪᴍ ʟᴇʙɪʜ ᴅᴀʀɪ 5 ᴘᴇsᴀɴ ʙᴇʀᴛᴜʀᴜᴛ-ᴛᴜʀᴜᴛ, ʙᴏᴛ, ᴅɪᴀʙᴀɪᴋᴀɴ.*

➥ /flood *:* `ᴅᴀᴘᴀᴛᴋᴀɴ ᴘᴇɴɢᴇɴᴅᴀʟɪᴀɴ ꜰʟᴏᴏᴅ sᴀᴀᴛ ɪɴɪ`

 • *ʜᴀɴʏᴀ ᴀᴅᴍɪɴ:*
 
➥ /setflood <`ɪɴᴛ`/'ᴏɴ'/'ᴏғғ'>*:* `ᴍᴇɴɢᴀᴋᴛɪꜰᴋᴀɴ ᴀᴛᴀᴜ ᴍᴇɴᴏɴᴀᴋᴛɪꜰᴋᴀɴ ꜰʟᴏᴏᴅ`
   ᴄᴏɴᴛᴏʜ *:* `/setflood 5`
     
➥ /setfloodmode <ʙᴀɴ/ᴋɪᴄᴋ/ᴍᴜᴛᴇ/ᴛʙᴀɴ/ᴛᴍᴜᴛᴇ> <ᴠᴀʟᴜᴇ>*:* `ᴛɪɴᴅᴀᴋᴀɴ ʏᴀɴɢ ʜᴀʀᴜs ᴅɪʟᴀᴋᴜᴋᴀɴ ᴋᴇᴛɪᴋᴀ ᴘᴇɴɢɢᴜɴᴀ ᴛᴇʟᴀʜ ᴍᴇʟᴀᴍᴘᴀᴜɪ ʙᴀᴛᴀs ʙᴀɴᴊɪʀ. ʙᴀɴ/ᴋɪᴄᴋ/ᴍᴜᴛᴇ/ᴛᴍᴜᴛᴇ/ᴛʙᴀɴ`

 • *ɴᴏᴛᴇ:*
 
 `• ɴɪʟᴀɪ ʜᴀʀᴜs ᴅɪɪsɪ ᴜɴᴛᴜᴋ ᴛʙᴀɴ ᴅᴀɴ ᴛᴍᴜᴛᴇ!!`
 sᴇᴘᴇʀᴛɪ:
 `5ᴍ` = 5 ᴍɪɴᴜᴛᴇs
 `6ʜ` = 6 ʜᴏᴜʀs
 `3ᴅ` = 3 ᴅᴀʏs
 `1ᴡ` = 1 ᴡᴇᴇᴋ
 
 """

__mod_name__ = "𝙰ɴᴛɪ-ғʟᴏᴏᴅ"

FLOOD_BAN_HANDLER = MessageHandler(
    Filters.all & ~Filters.status_update & Filters.chat_type.groups,
    check_flood,
    run_async=True,
)
SET_FLOOD_HANDLER = CommandHandler(
    "setflood", set_flood, pass_args=True, run_async=True
)  # , filters=Filters.chat_type.groups)
SET_FLOOD_MODE_HANDLER = CommandHandler(
    "setfloodmode", set_flood_mode, pass_args=True, run_async=True
)  # , filters=Filters.chat_type.groups)
FLOOD_HANDLER = CommandHandler(
    "flood", flood, run_async=True
)  # , filters=Filters.chat_type.groups)

dispatcher.add_handler(FLOOD_BAN_HANDLER, FLOOD_GROUP)
dispatcher.add_handler(SET_FLOOD_HANDLER)
dispatcher.add_handler(SET_FLOOD_MODE_HANDLER)
dispatcher.add_handler(FLOOD_HANDLER)
