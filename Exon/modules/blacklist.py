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
import re

from telegram import ChatPermissions, ParseMode
from telegram.error import BadRequest
from telegram.ext import CommandHandler, Filters, MessageHandler
from telegram.utils.helpers import mention_html

import Exon.modules.sql.blacklist_sql as sql
from Exon import LOGGER, dispatcher
from Exon.modules.connection import connected
from Exon.modules.disable import DisableAbleCommandHandler
from Exon.modules.helper_funcs.alternate import send_message, typing_action
from Exon.modules.helper_funcs.chat_status import user_admin, user_not_admin
from Exon.modules.helper_funcs.extraction import extract_text
from Exon.modules.helper_funcs.misc import split_message
from Exon.modules.helper_funcs.string_handling import extract_time
from Exon.modules.log_channel import loggable
from Exon.modules.sql.approve_sql import is_approved
from Exon.modules.warns import warn

BLACKLIST_GROUP = 11


@user_admin
@typing_action
def blacklist(update, context):
    chat = update.effective_chat
    user = update.effective_user
    args = context.args

    if conn := connected(context.bot, update, chat, user.id, need_admin=False):
        chat_id = conn
        chat_name = dispatcher.bot.getChat(conn).title
    else:
        if chat.type == "private":
            return
        chat_id = update.effective_chat.id
        chat_name = chat.title

    filter_list = f"ᴄᴜʀʀᴇɴᴛ ʙʟᴀᴄᴋʟɪsᴛᴇᴅ ᴡᴏʀᴅs ɪɴ <b>{chat_name}</b>:\n"

    all_blacklisted = sql.get_chat_blacklist(chat_id)

    if len(args) > 0 and args[0].lower() == "copy":
        for trigger in all_blacklisted:
            filter_list += f"<code>{html.escape(trigger)}</code>\n"
    else:
        for trigger in all_blacklisted:
            filter_list += f" - <code>{html.escape(trigger)}</code>\n"

    # for trigger in all_blacklisted:
    #     filter_list += " - <code>{}</code>\n".format(html.escape(trigger))

    split_text = split_message(filter_list)
    for text in split_text:
        if (
            filter_list
            == f"ᴄᴜʀʀᴇɴᴛ ʙʟᴀᴄᴋʟɪsᴛᴇᴅ ᴡᴏʀᴅs ɪɴ <b>{html.escape(chat_name)}</b>:\n"
        ):
            send_message(
                update.effective_message,
                f"ɴᴏ ʙʟᴀᴄᴋʟɪsᴛᴇᴅ ᴡᴏʀᴅs ɪɴ <b>{html.escape(chat_name)}</b>!",
                parse_mode=ParseMode.HTML,
            )

            return
        send_message(update.effective_message, text, parse_mode=ParseMode.HTML)


@user_admin
@typing_action
def add_blacklist(update, context):
    msg = update.effective_message
    chat = update.effective_chat
    user = update.effective_user
    words = msg.text.split(None, 1)

    if conn := connected(context.bot, update, chat, user.id):
        chat_id = conn
        chat_name = dispatcher.bot.getChat(conn).title
    else:
        chat_id = update.effective_chat.id
        if chat.type == "private":
            return
        chat_name = chat.title

    if len(words) > 1:
        text = words[1]
        to_blacklist = list(
            {trigger.strip() for trigger in text.split("\n") if trigger.strip()}
        )
        for trigger in to_blacklist:
            sql.add_to_blacklist(chat_id, trigger.lower())

        if len(to_blacklist) == 1:
            send_message(
                update.effective_message,
                f"ᴍᴇɴᴀᴍʙᴀʜᴋᴀɴ ʙʟᴀᴄᴋʟɪsᴛ <code>{html.escape(to_blacklist[0])}</code> ᴅᴀʟᴀᴍ ᴏʙʀᴏʟᴀɴ : <b>{html.escape(chat_name)}</b>!",
                parse_mode=ParseMode.HTML,
            )

        else:
            send_message(
                update.effective_message,
                f"ᴍᴇɴᴀᴍʙᴀʜᴋᴀɴ ʙʟᴀᴄᴋʟɪsᴛ ᴛʀɪɢɢᴇʀ: <code>{len(to_blacklist)}</code> ᴅᴀʟᴀᴍ <b>{html.escape(chat_name)}</b>!",
                parse_mode=ParseMode.HTML,
            )

    else:
        send_message(
            update.effective_message,
            "ʙᴇʀɪ ᴛᴀʜᴜ sᴀʏᴀ ᴋᴀᴛᴀ-ᴋᴀᴛᴀ ᴍᴀɴᴀ ʏᴀɴɢ ɪɴɢɪɴ ᴀɴᴅᴀ ᴛᴀᴍʙᴀʜᴋᴀɴ ᴅᴀʟᴀᴍ ᴅᴀꜰᴛᴀʀ ʜɪᴛᴀᴍ.",
        )


@user_admin
@typing_action
def unblacklist(update, context):
    msg = update.effective_message
    chat = update.effective_chat
    user = update.effective_user
    words = msg.text.split(None, 1)

    if conn := connected(context.bot, update, chat, user.id):
        chat_id = conn
        chat_name = dispatcher.bot.getChat(conn).title
    else:
        chat_id = update.effective_chat.id
        if chat.type == "private":
            return
        chat_name = chat.title

    if len(words) > 1:
        text = words[1]
        to_unblacklist = list(
            {trigger.strip() for trigger in text.split("\n") if trigger.strip()}
        )
        successful = 0
        for trigger in to_unblacklist:
            success = sql.rm_from_blacklist(chat_id, trigger.lower())
            if success:
                successful += 1

        if len(to_unblacklist) == 1:
            if successful:
                send_message(
                    update.effective_message,
                    f"ᴍᴇɴɢʜᴀᴘᴜs <code>{html.escape(to_unblacklist[0])}</code> ᴅᴀʀɪ ʙʟᴀᴄᴋʟɪsᴛ ᴅɪ <b>{html.escape(chat_name)}</b>!",
                    parse_mode=ParseMode.HTML,
                )

            else:
                send_message(
                    update.effective_message, "ɪɴɪ ʙᴜᴋᴀɴ ᴀ ʙʟᴀᴄᴋʟɪsᴛ ᴛʀɪɢɢᴇʀ!"
                )

        elif successful == len(to_unblacklist):
            send_message(
                update.effective_message,
                f"ᴍᴇɴɢʜᴀᴘᴜs <code>{successful}</code> ᴅᴀʀɪ ʙʟᴀᴄᴋʟɪsᴛ ᴅɪ <b>{html.escape(chat_name)}</b>!",
                parse_mode=ParseMode.HTML,
            )

        elif not successful:
            send_message(
                update.effective_message,
                "ᴛɪᴅᴀᴋ ᴀᴅᴀ sᴀʟᴀʜ sᴀᴛᴜ ᴘᴜɴ ᴛʀɪɢɢᴇʀs ᴊᴀᴅɪ ᴛɪᴅᴀᴋ ʙɪsᴀ ᴍᴇɴɢʜᴀᴘᴜs.".format(
                    successful, len(to_unblacklist) - successful
                ),
                parse_mode=ParseMode.HTML,
            )

        else:
            send_message(
                update.effective_message,
                f"ᴍᴇɴɢʜᴀᴘᴜs <code>{successful}</code> ᴅᴀʀɪ ʙʟᴀᴄᴋʟɪsᴛ ᴅɪ. {len(to_unblacklist) - successful} ᴛɪᴅᴀᴋ ᴀᴅᴀ, ᴊᴀᴅɪ ᴛɪᴅᴀᴋ ᴅɪʜᴀᴘᴜs.",
                parse_mode=ParseMode.HTML,
            )

    else:
        send_message(
            update.effective_message,
            "ʙᴇʀɪ ᴛᴀʜᴜ sᴀʏᴀ ᴋᴀᴛᴀ-ᴋᴀᴛᴀ ᴍᴀɴᴀ ʏᴀɴɢ ɪɴɢɪɴ ᴀɴᴅᴀ ʜᴀᴘᴜsᴋᴀɴ ᴅᴀʟᴀᴍ ᴅᴀꜰᴛᴀʀ ʜɪᴛᴀᴍ!",
        )


@loggable
@user_admin
@typing_action
def blacklist_mode(update, context):
    chat = update.effective_chat
    user = update.effective_user
    msg = update.effective_message
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
                "ᴘᴇʀɪɴᴛᴀʜ ɪɴɪ ʜᴀɴʏᴀ ʙɪsᴀ ᴅɪɢᴜɴᴀᴋᴀɴ ᴅɪɢʀᴜᴘ ʙᴜᴋᴀɴ ᴅɪ ᴘᴍ",
            )
            return ""
        chat = update.effective_chat
        chat_id = update.effective_chat.id
        chat_name = update.effective_message.chat.title

    if args:
        if args[0].lower() in ("off", "nothing", "no"):
            settypeblacklist = "ᴛɪᴅᴀᴋ ᴍᴇʟᴀᴋᴜᴋᴀɴ ᴀᴘᴀᴘᴜɴ"
            sql.set_blacklist_strength(chat_id, 0, "0")
        elif args[0].lower() in ("del", "delete"):
            settypeblacklist = "ᴀᴋᴀɴ ᴍᴇɴɢʜᴀᴘᴜs ᴘᴇsᴀɴ ᴅᴀꜰᴛᴀʀ ʜɪᴛᴀᴍ"
            sql.set_blacklist_strength(chat_id, 1, "0")
        elif args[0].lower() == "warn":
            settypeblacklist = "ᴘᴇʀɪɴɢᴀᴛᴀɴ ᴘᴇɴɢɪʀɪᴍ"
            sql.set_blacklist_strength(chat_id, 2, "0")
        elif args[0].lower() == "mute":
            settypeblacklist = "ʙɪsᴜ ᴘᴇɴɢɪʀɪᴍ"
            sql.set_blacklist_strength(chat_id, 3, "0")
        elif args[0].lower() == "kick":
            settypeblacklist = "ᴛᴇɴᴅᴀɴɢ ᴘᴇɴɢɪʀɪᴍ"
            sql.set_blacklist_strength(chat_id, 4, "0")
        elif args[0].lower() == "ban":
            settypeblacklist = "ᴅɪsᴇɢᴇʟ ᴘᴇɴɢɪʀɪᴍ"
            sql.set_blacklist_strength(chat_id, 5, "0")
        elif args[0].lower() == "tban":
            if len(args) == 1:
                teks = """sᴇᴘᴇʀᴛɪɴʏᴀ ᴀɴᴅᴀ ʟᴇʟᴀʜ ᴜɴᴛᴜᴋ ᴍᴇɴᴇᴛᴀᴘᴋᴀɴ ɴɪʟᴀɪ ᴡᴀᴋᴛᴜ ᴜɴᴛᴜᴋ ᴅᴀꜰᴛᴀʀ ʜɪᴛᴀᴍ ᴛᴇᴛᴀᴘɪ ᴀɴᴅᴀ ᴛɪᴅᴀᴋ ᴍᴇɴᴇɴᴛᴜᴋᴀɴ ᴡᴀᴋᴛᴜ; ᴍᴇɴᴄᴏʙᴀ; , `/blacklistmode tban <timevalue>`.
				
    ᴄᴏɴᴛᴏʜ: 4ᴍ = 4 ᴍɪɴᴜᴛᴇs, 3ʜ = 3 ʜᴏᴜʀs, 6ᴅ = 6 ᴅᴀʏs, 5ᴡ = 5 ᴡᴇᴇᴋs."""
                send_message(update.effective_message, teks, parse_mode="markdown")
                return ""
            restime = extract_time(msg, args[1])
            if not restime:
                teks = """ɴɪʟᴀɪ ᴡᴀᴋᴛᴜ sᴀʟᴀʜ!
    ᴄᴏɴᴛᴏʜ: 4ᴍ = 4 ᴍɪɴᴜᴛᴇs, 3ʜ = 3 ʜᴏᴜʀs, 6ᴅ = 6 ᴅᴀʏs, 5ᴡ = 5 ᴡᴇᴇᴋs."""
                send_message(update.effective_message, teks, parse_mode="markdown")
                return ""
            settypeblacklist = f"ᴜɴᴛᴜᴋ sᴇᴍᴇɴᴛᴀʀᴀ ʙᴀɴ {args[1]}"
            sql.set_blacklist_strength(chat_id, 6, str(args[1]))
        elif args[0].lower() == "tmute":
            if len(args) == 1:
                teks = """sᴇᴘᴇʀᴛɪɴʏᴀ ᴀɴᴅᴀ ʟᴇʟᴀʜ ᴜɴᴛᴜᴋ ᴍᴇɴᴇᴛᴀᴘᴋᴀɴ ɴɪʟᴀɪ ᴡᴀᴋᴛᴜ ᴜɴᴛᴜᴋ ᴅᴀꜰᴛᴀʀ ʜɪᴛᴀᴍ ᴛᴇᴛᴀᴘɪ ᴀɴᴅᴀ ᴛɪᴅᴀᴋ ᴍᴇɴᴇɴᴛᴜᴋᴀɴ ᴡᴀᴋᴛᴜ; ᴍᴇɴᴄᴏʙᴀ;, `/blacklistmode tmute <timevalue>`.
    ᴄᴏɴᴛᴏʜ: 4m = 4 ᴍɪɴᴜᴛᴇs, 3h = 3 ʜᴏᴜʀs, 6d = 6 ᴅᴀʏs, 5w = 5 ᴡᴇᴇᴋs."""
                send_message(update.effective_message, teks, parse_mode="markdown")
                return ""
            restime = extract_time(msg, args[1])
            if not restime:
                teks = """ɴɪʟᴀɪ ᴡᴀᴋᴛᴜ sᴀʟᴀʜ!
    ᴄᴏɴᴛᴏʜ: 4ᴍ = 4 ᴍɪɴᴜᴛᴇs, 3ʜ = 3 ʜᴏᴜʀs, 6ᴅ = 6 ᴅᴀʏs, 5w = 5 ᴡᴇᴇᴋs."""
                send_message(update.effective_message, teks, parse_mode="markdown")
                return ""
            settypeblacklist = f"ᴜɴᴛᴜᴋ sᴇᴍᴇɴᴛᴀʀᴀ ᴍᴜᴛᴇ {args[1]}"
            sql.set_blacklist_strength(chat_id, 7, str(args[1]))
        else:
            send_message(
                update.effective_message,
                "sᴀʏᴀ ʜᴀɴʏᴀ ᴍᴇɴɢᴇʀᴛɪ: off/del/warn/ban/kick/mute/tban/tmute!",
            )
            return ""
        if conn:
            text = f"ᴍᴇɴɢɢᴀɴᴛɪ ᴍᴏᴅᴇ ʙʟᴀᴄᴋʟɪsᴛ: `{settypeblacklist}` in *{chat_name}*!"
        else:
            text = f"ᴍᴇɴɢɢᴀɴᴛɪ ᴍᴏᴅᴇ ʙʟᴀᴄᴋʟɪsᴛ: `{settypeblacklist}`!"
        send_message(update.effective_message, text, parse_mode="markdown")
        return f"<b>{html.escape(chat.title)}:</b>\n<b>ᴀᴅᴍɪɴ:</b> {mention_html(user.id, html.escape(user.first_name))}\nᴍᴇɴɢɢᴀɴᴛɪ ᴍᴏᴅᴇ ʙʟᴀᴄᴋʟɪsᴛ. ᴀᴋᴀɴ {settypeblacklist}."

    getmode, getvalue = sql.get_blacklist_setting(chat.id)
    if getmode == 0:
        settypeblacklist = "ᴅᴏ ɴᴏᴛʜɪɴɢ"
    elif getmode == 1:
        settypeblacklist = "ᴅᴇʟᴇᴛᴇ"
    elif getmode == 2:
        settypeblacklist = "ᴡᴀʀɴ"
    elif getmode == 3:
        settypeblacklist = "ᴍᴜᴛᴇ"
    elif getmode == 4:
        settypeblacklist = "ᴋɪᴄᴋ"
    elif getmode == 5:
        settypeblacklist = "ʙᴀɴ"
    elif getmode == 6:
        settypeblacklist = f"ᴜɴᴛᴜᴋ sᴇᴍᴇɴᴛᴀʀᴀ ʙᴀɴ {getvalue}"
    elif getmode == 7:
        settypeblacklist = f"ᴜɴᴛᴜᴋ sᴇᴍᴇɴᴛᴀʀᴀ ᴍᴜᴛᴇ {getvalue}"
    if conn:
        text = f"sᴀᴀᴛ ɪɴɪ ʙʟᴀᴄᴋʟɪsᴛᴍᴏᴅᴇ: *{settypeblacklist}* ᴅᴀʟᴀᴍ *{chat_name}*."
    else:
        text = f"sᴀᴀᴛ ɪɴɪ ʙʟᴀᴄᴋʟɪsᴛᴍᴏᴅᴇ: *{settypeblacklist}*."
    send_message(update.effective_message, text, parse_mode=ParseMode.MARKDOWN)
    return ""


def findall(p, s):
    i = s.find(p)
    while i != -1:
        yield i
        i = s.find(p, i + 1)


@user_not_admin
def del_blacklist(update, context):
    chat = update.effective_chat
    message = update.effective_message
    user = update.effective_user
    bot = context.bot
    to_match = extract_text(message)

    if not to_match:
        return

    if is_approved(chat.id, user.id):
        return

    getmode, value = sql.get_blacklist_setting(chat.id)

    chat_filters = sql.get_chat_blacklist(chat.id)
    for trigger in chat_filters:
        pattern = r"( |^|[^\w])" + re.escape(trigger) + r"( |$|[^\w])"
        if re.search(pattern, to_match, flags=re.IGNORECASE):
            try:
                if getmode == 0:
                    return
                if getmode == 1:
                    message.delete()
                elif getmode == 2:
                    message.delete()
                    warn(
                        update.effective_user,
                        chat,
                        f"ᴍᴇɴɢɢᴜɴᴀᴋᴀɴ ʙʟᴀᴄᴋʟɪsᴛᴇᴅ ᴛʀɪɢɢᴇʀ: {trigger}",
                        message,
                        update.effective_user,
                    )

                    return
                elif getmode == 3:
                    message.delete()
                    bot.restrict_chat_member(
                        chat.id,
                        update.effective_user.id,
                        permissions=ChatPermissions(can_send_messages=False),
                    )
                    bot.sendMessage(
                        chat.id,
                        f"ᴍᴜᴛᴇᴅ {user.first_name} ᴍᴇɴɢɢᴜɴᴀᴋᴀɴ ʙʟᴀᴄᴋʟɪsᴛᴇᴅ : {trigger}!",
                    )
                    return
                elif getmode == 4:
                    message.delete()
                    if res := chat.unban_member(update.effective_user.id):
                        bot.sendMessage(
                            chat.id,
                            f"ᴋɪᴄᴋᴇᴅ {user.first_name} ᴍᴇɴɢɢᴜɴᴀᴋᴀɴ ʙʟᴀᴄᴋʟɪsᴛᴇᴅ : {trigger}!",
                        )
                    return
                elif getmode == 5:
                    message.delete()
                    chat.ban_member(user.id)
                    bot.sendMessage(
                        chat.id,
                        f"ʙᴀɴɴᴇᴅ {user.first_name} ᴍᴇɴɢɢᴜɴᴀᴋᴀɴ ʙʟᴀᴄᴋʟɪsᴛᴇᴅ : {trigger}",
                    )
                    return
                elif getmode == 6:
                    message.delete()
                    bantime = extract_time(message, value)
                    chat.ban_member(user.id, until_date=bantime)
                    bot.sendMessage(
                        chat.id,
                        f"ʙᴀɴɴᴇᴅ {user.first_name} ᴜɴᴛɪʟ '{value}' ᴍᴇɴɢɢᴜɴᴀᴋᴀɴ ʙʟᴀᴄᴋʟɪsᴛᴇᴅ : {trigger}!",
                    )
                    return
                elif getmode == 7:
                    message.delete()
                    mutetime = extract_time(message, value)
                    bot.restrict_chat_member(
                        chat.id,
                        user.id,
                        until_date=mutetime,
                        permissions=ChatPermissions(can_send_messages=False),
                    )
                    bot.sendMessage(
                        chat.id,
                        f"ᴍᴜᴛᴇᴅ {user.first_name} ᴜɴᴛɪʟ '{value}' ᴍᴇɴɢɢᴜɴᴀᴋᴀɴ Blacklisted : {trigger}!",
                    )
                    return
            except BadRequest as excp:
                if excp.message != "ᴘᴇsᴀɴ ᴜɴᴛᴜᴋ ᴅɪʜᴀᴘᴜs ᴛɪᴅᴀᴋ ᴅɪᴛᴇᴍᴜᴋᴀɴ":
                    LOGGER.exception("ᴋᴇsᴀʟᴀʜᴀɴ sᴀᴀᴛ ᴍᴇɴɢʜᴀᴘᴜs ᴘᴇsᴀɴ ʙʟᴀᴄᴋʟɪsᴛ.")
            break


def __import_data__(chat_id, data):
    # set chat blacklist
    blacklist = data.get("blacklist", {})
    for trigger in blacklist:
        sql.add_to_blacklist(chat_id, trigger)


def __migrate__(old_chat_id, new_chat_id):
    sql.migrate_chat(old_chat_id, new_chat_id)


def __chat_settings__(chat_id, user_id):
    blacklisted = sql.num_blacklist_chat_filters(chat_id)
    return f"ᴛʜᴇʀᴇ ᴀʀᴇ {blacklisted} ʙʟᴀᴄᴋʟɪsᴛᴇᴅ ᴡᴏʀᴅs."


def __stats__():
    return f"⍟ {sql.num_blacklist_filters()} ʙʟᴀᴄᴋʟɪsᴛ ᴛʀɪɢɢᴇʀs, ʟɪɴᴛᴀs {sql.num_blacklist_filter_chats()} ᴏʙʀᴏʟᴀɴ."


__mod_name__ = "𝙱ʟᴀᴄᴋʟɪsᴛs"

__help__ = """

*ᴅᴀꜰᴛᴀʀ ʜɪᴛᴀᴍ ᴅɪɢᴜɴᴀᴋᴀɴ ᴜɴᴛᴜᴋ ᴍᴇɴɢʜᴇɴᴛɪᴋᴀɴ ᴘᴇᴍɪᴄᴜ ᴛᴇʀᴛᴇɴᴛᴜ ᴀɢᴀʀ ᴛɪᴅᴀᴋ ᴅɪᴜᴄᴀᴘᴋᴀɴ ᴅᴀʟᴀᴍ ɢʀᴜᴘ. sᴇᴛɪᴀᴘ ᴋᴀʟɪ ᴏs ᴘᴇᴍɪᴄᴜ ᴅɪsᴇʙᴜᴛᴋᴀɴ, ᴘᴇsᴀɴ ᴀᴋᴀɴ sᴇɢᴇʀᴀ ᴅɪʜᴀᴘᴜs. ᴋᴏᴍʙᴏ ʏᴀɴɢ ʙᴀɢᴜs ᴛᴇʀᴋᴀᴅᴀɴɢ ᴍᴇᴍᴀsᴀɴɢᴋᴀɴ ɪɴɪ ᴅᴇɴɢᴀɴ ꜰɪʟᴛᴇʀ ᴘᴇʀɪɴɢᴀᴛᴀɴ!*

*ɴᴏᴛᴇ*: `ʙʟᴀᴄᴋʟɪsᴛs ᴅᴏ ɴᴏᴛ ᴀғғᴇᴄᴛ ɢʀᴏᴜᴘ ᴀᴅᴍɪɴs.`

✪ /blacklist*:* `ᴠɪᴇᴡ ᴛʜᴇ ᴄᴜʀʀᴇɴᴛ ʙʟᴀᴄᴋʟɪsᴛᴇᴅ ᴡᴏʀᴅs.`

*ᴀᴅᴍɪɴ ᴏɴʟʏ:*
✪ /addblacklist <ᴛʀɪɢɢᴇʀs>*:* `ᴀᴅᴅ ᴀ ᴛʀɪɢɢᴇʀ ᴛᴏ ᴛʜᴇ ʙʟᴀᴄᴋʟɪsᴛ. ᴇᴀᴄʜ ʟɪɴᴇ is ᴄᴏɴsɪᴅᴇʀᴇᴅ ᴏɴᴇ ᴛʀɪɢɢᴇʀ, sᴏ ᴜsɪɴɢ ᴅɪғғᴇʀᴇɴᴛ ʟɪɴᴇs ᴡɪʟʟ ᴀʟʟᴏᴡ ʏᴏᴜ ᴛᴏ ᴀᴅᴅ ᴍᴜʟᴛɪᴘʟᴇ ᴛʀɪɢɢᴇʀs.`

✪ /unblacklist <ᴛʀɪɢɢᴇʀs>*:* `ʀᴇᴍᴏᴠᴇ ᴛʀɪɢɢᴇʀs ғʀᴏᴍ ᴛʜᴇ ʙʟᴀᴄᴋʟɪsᴛ. sᴀᴍᴇ ɴᴇᴡʟɪɴᴇ ʟᴏɢɪᴄ ᴀᴘᴘʟɪᴇs ʜᴇʀᴇ, sᴏ ʏᴏᴜ ᴄᴀɴ ʀᴇᴍᴏᴠᴇ ᴍᴜʟᴛɪᴘʟᴇ ᴛʀɪɢɢᴇʀs ᴀᴛ ᴏɴᴄᴇ.`

✪ /blacklistmode <off/del/warn/ban/kick/mute/tban/tmute>*:* `ᴀᴄᴛɪᴏɴ ᴛᴏ ᴘᴇʀғᴏʀᴍ ᴡʜᴇɴ sᴏᴍᴇᴏɴᴇ sᴇɴᴅs ʙʟᴀᴄᴋʟɪsᴛᴇᴅ ᴡᴏʀᴅs.`

`ʀʙʟᴀᴄᴋʟɪsᴛ sᴛɪᴄᴋᴇʀ ɪs ᴜsᴇᴅ ᴛᴏ sᴛᴏᴘ ᴄᴇʀᴛᴀɪɴ sᴛɪᴄᴋᴇʀs. ᴡʜᴇɴᴇᴠᴇʀ a sᴛɪᴄᴋᴇʀ ɪs sᴇɴᴛ, ᴛʜᴇ ᴍᴇssᴀɢᴇ ᴡɪʟʟ ʙᴇ ᴅᴇʟᴇᴛᴇᴅ ɪᴍᴍᴇᴅɪᴀᴛᴇʟʏ.`

*ɴᴏᴛᴇ:* `ʙʟᴀᴄᴋʟɪsᴛ sᴛɪᴄᴋᴇʀs ᴅᴏ ɴᴏᴛ ᴀғғᴇᴄᴛ ᴛʜᴇ ɢʀᴏᴜᴘ ᴀᴅᴍɪɴ`

✪ /blsticker*:* `ꜱᴇᴇ ᴄᴜʀʀᴇɴᴛ ʙʟᴀᴄᴋʟɪꜱᴛᴇᴅ ꜱᴛɪᴄᴋᴇʀ`


✪ /addblsticker <sticker link>*:* `ᴀᴅᴅ ᴛʜᴇ ꜱᴛɪᴄᴋᴇʀ ᴛʀɪɢɢᴇʀ ᴛᴏ ᴛʜᴇ ʙʟᴀᴄᴋ ʟɪꜱᴛ. ᴄᴀɴ ʙᴇ ᴀᴅᴅᴇᴅ ᴠɪᴀ ʀᴇᴘʟʏ ꜱᴛɪᴄᴋᴇʀ`

✪ /unblsticker <sticker link>*:* `ʀᴇᴍᴏᴠᴇ ᴛʀɪɢɢᴇʀꜱ ғʀᴏᴍ ʙʟᴀᴄᴋʟɪꜱᴛ. ᴛʜᴇ ꜱᴀᴍᴇ ɴᴇᴡʟɪɴᴇ ʟᴏɢɪᴄ ᴀᴘᴘʟɪᴇꜱ ʜᴇʀᴇ, ꜱᴏ ʏᴏᴜ ᴄᴀɴ ᴅᴇʟᴇᴛᴇ ᴍᴜʟᴛɪᴘʟᴇ ᴛʀɪɢɢᴇʀꜱ ᴀᴛ ᴏɴᴄᴇ`

✪ /rmblsticker <sticker link>*:* `ꜱᴀᴍᴇ ᴀꜱ ᴀʙᴏᴠᴇ`

✪ /blstickermode <delete/ban/tban/mute/tmute>*:* `ꜱᴇᴛꜱ ᴜᴘ ᴀ ᴅᴇғᴀᴜʟᴛ ᴀᴄᴛɪᴏɴ ᴏɴ ᴡʜᴀᴛ ᴛᴏ ᴅᴏ ɪғ ᴜꜱᴇʀꜱ ᴜꜱᴇ ʙʟᴀᴄᴋʟɪꜱᴛᴇᴅ ꜱᴛɪᴄᴋᴇʀꜱ`

ɴᴏᴛᴇ:
✪ <sticker link> `ᴄᴀɴ ʙᴇ` `https://t.me/addstickers/<sticker>` `ᴏʀ ᴊᴜꜱᴛ` `<sticker>` `ᴏʀ ʀᴇᴘʟʏ ᴛᴏ ᴛʜᴇ ꜱᴛɪᴄᴋᴇʀ ᴍᴇꜱꜱᴀɢᴇ`

"""

BLACKLIST_HANDLER = DisableAbleCommandHandler(
    "blacklist", blacklist, pass_args=True, admin_ok=True, run_async=True
)
ADD_BLACKLIST_HANDLER = CommandHandler("addblacklist", add_blacklist, run_async=True)
UNBLACKLIST_HANDLER = CommandHandler("unblacklist", unblacklist, run_async=True)
BLACKLISTMODE_HANDLER = CommandHandler(
    "blacklistmode", blacklist_mode, pass_args=True, run_async=True
)
BLACKLIST_DEL_HANDLER = MessageHandler(
    (Filters.text | Filters.command | Filters.sticker | Filters.photo)
    & Filters.chat_type.groups,
    del_blacklist,
    allow_edit=True,
    run_async=True,
)

dispatcher.add_handler(BLACKLIST_HANDLER)
dispatcher.add_handler(ADD_BLACKLIST_HANDLER)
dispatcher.add_handler(UNBLACKLIST_HANDLER)
dispatcher.add_handler(BLACKLISTMODE_HANDLER)
dispatcher.add_handler(BLACKLIST_DEL_HANDLER, group=BLACKLIST_GROUP)

__handlers__ = [
    BLACKLIST_HANDLER,
    ADD_BLACKLIST_HANDLER,
    UNBLACKLIST_HANDLER,
    BLACKLISTMODE_HANDLER,
    (BLACKLIST_DEL_HANDLER, BLACKLIST_GROUP),
]
