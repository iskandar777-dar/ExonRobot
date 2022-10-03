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

from telegram import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    ParseMode,
    TelegramError,
    Update,
)
from telegram.error import BadRequest
from telegram.ext import CallbackContext, CallbackQueryHandler, CommandHandler, Filters
from telegram.utils.helpers import mention_html

from Exon import (
    DEMONS,
    DEV_USERS,
    DRAGONS,
    LOGGER,
    OWNER_ID,
    TIGERS,
    WOLVES,
    dispatcher,
)
from Exon.modules.disable import DisableAbleCommandHandler
from Exon.modules.helper_funcs.chat_status import (
    bot_admin,
    can_delete,
    can_restrict,
    connection_status,
    dev_plus,
    is_user_admin,
    is_user_ban_protected,
    is_user_in_chat,
    user_admin,
    user_admin_no_reply,
    user_can_ban,
)
from Exon.modules.helper_funcs.extraction import extract_user_and_text
from Exon.modules.helper_funcs.filters import CustomFilters
from Exon.modules.helper_funcs.string_handling import extract_time
from Exon.modules.log_channel import gloggable, loggable


@connection_status
@bot_admin
@can_restrict
@user_admin
@user_can_ban
@loggable
def ban(update: Update, context: CallbackContext) -> str:
    chat = update.effective_chat
    user = update.effective_user
    message = update.effective_message
    log_message = ""
    bot = context.bot
    args = context.args
    reason = ""
    if message.reply_to_message and message.reply_to_message.sender_chat:
        if r := bot.ban_chat_sender_chat(
            chat_id=chat.id,
            sender_chat_id=message.reply_to_message.sender_chat.id,
        ):
            message.reply_text(
                f"ᴄʜᴀɴɴᴇʟ {html.escape(message.reply_to_message.sender_chat.title)} ʙᴇʀʜᴀsɪʟ ʙᴀɴɴᴇᴅ ᴅᴀʀɪ {html.escape(chat.title)}",
                parse_mode="html",
            )

        else:
            message.reply_text("ɢᴀɢᴀʟ ʙᴀɴɴᴇᴅ ᴄʜᴀɴɴᴇʟ")
        return
    user_id, reason = extract_user_and_text(message, args)
    if not user_id:
        message.reply_text("⚠️ ᴘᴇɴɢɢᴜɴᴀ ᴛɪᴅᴀᴋ ᴅɪᴛᴇᴍᴜᴋᴀɴ.")
        return log_message
    try:
        member = chat.get_member(user_id)
    except BadRequest as excp:
        if excp.message != "ᴘᴇɴɢɢᴜɴᴀ ᴛɪᴅᴀᴋ ᴅɪᴛᴇᴍᴜᴋᴀɴ":
            raise
        message.reply_text("sᴇᴘᴇʀᴛɪɴʏᴀ ᴛɪᴅᴀᴋ ᴅᴀᴘᴀᴛ ᴍᴇɴᴇᴍᴜᴋᴀɴ ᴏʀᴀɴɢ ɪɴɪ.")
        return log_message
    if user_id == bot.id:
        message.reply_text("ᴏʜ ʏᴀ, ʙᴀɴ sᴇɴᴅɪʀɪ, ɴᴏᴏʙ ᴋᴀᴍᴜ!")
        return log_message
    if is_user_ban_protected(chat, user_id, member) and user not in DEV_USERS:
        if user_id == OWNER_ID:
            message.reply_text("ᴍᴇɴᴄᴏʙᴀ ᴍᴇɴᴇᴍᴘᴀᴛᴋᴀɴ sᴀʏᴀ ᴍᴇʟᴀᴡᴀɴ ᴛᴜᴀɴ sᴀʏᴀ ʜᴀʜ?")
        elif user_id in DEV_USERS:
            message.reply_text("sᴀʏᴀ ᴛɪᴅᴀᴋ ʙɪsᴀ ʙᴇʀᴛɪɴᴅᴀᴋ ᴍᴇʟᴀᴡᴀɴ ᴋᴇʟᴜᴀʀɢᴀ ᴋᴀᴍɪ.")
        elif user_id in DRAGONS:
            message.reply_text(
                "ᴍᴇʟᴀᴡᴀɴ sᴀʜᴀʙᴀᴛ ᴋɪᴛᴀ ᴅɪ sɪɴɪ ᴀᴋᴀɴ ᴍᴇᴍʙᴀʜᴀʏᴀᴋᴀɴ ɴʏᴀᴡᴀ ᴘᴇɴɢɢᴜɴᴀ."
            )
        elif user_id in DEMONS:
            message.reply_text("ᴍᴇᴍʙᴀᴡᴀ ᴘᴇsᴀɴᴀɴ ᴅᴀʀɪ ᴛᴜᴀɴᴋᴜ ᴜɴᴛᴜᴋ ᴍᴇʟᴀᴡᴀɴ ᴛᴇᴍᴀɴ-ᴛᴇᴍᴀɴ ᴋɪᴛᴀ.")
        elif user_id in TIGERS:
            message.reply_text("ᴍᴇᴍʙᴀᴡᴀ ᴘᴇsᴀɴᴀɴ ᴅᴀʀɪ ᴛᴜᴀɴᴋᴜ ᴜɴᴛᴜᴋ ᴍᴇʟᴀᴡᴀɴ ᴛᴇᴍᴀɴ-ᴛᴇᴍᴀɴ ᴋɪᴛᴀ")
        elif user_id in WOLVES:
            message.reply_text("ᴍᴇɴʏᴀʟᴀᴋᴀɴ ᴀᴋsᴇs ᴍᴇᴍʙᴜᴀᴛ ᴍᴇʀᴇᴋᴀ ᴋᴇʙᴀʟ!")
        else:
            message.reply_text("⚠️ ᴛɪᴅᴀᴋ ʙɪsᴀ ʙᴀɴɴᴇᴅ ᴀᴅᴍɪɴ.")
        return log_message
    if message.text.startswith("/s"):
        silent = True
        if not can_delete(chat, context.bot.id):
            return ""
    else:
        silent = False
    log = (
        f"<b>{html.escape(chat.title)}:</b>\n"
        f"#{'S' if silent else ''}ʙᴀɴɴᴇᴅ\n"
        f"<b>ᴀᴅᴍɪɴ:</b> {mention_html(user.id, html.escape(user.first_name))}\n"
        f"<b>ᴜsᴇʀ:</b> {mention_html(member.user.id, html.escape(member.user.first_name))}"
    )
    if reason:
        log += f"<b>ᴀʟᴀsᴀɴ:</b> {reason}"
    try:
        chat.ban_member(user_id)
        if silent:
            if message.reply_to_message:
                message.reply_to_message.delete()
            message.delete()
            return log
        # bot.send_sticker(chat.id, BAN_STICKER)  # banhammer marie sticker
        reply = (
            f"<code>❕</code><b>Ban Event</b>\n\n"
            f"<b>• ᴜsᴇʀ:</b> {mention_html(member.user.id, html.escape(member.user.first_name))}\n"
            f"<b>• ᴜsᴇʀ 𝙸𝙳:</b> <code>{member.user.id}</code>\n"
            f"<b>• ʙᴀɴɴᴇᴅ ʙʏ:</b> {mention_html(user.id, html.escape(user.first_name))}"
        )
        if reason:
            reply += f"\n<b>• ᴀʟᴀsᴀɴ:</b> {html.escape(reason)}"
        bot.sendMessage(
            chat.id,
            reply,
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            text="ᴜɴʙᴀɴ ❗", callback_data=f"unbanb_unban={user_id}"
                        ),
                        InlineKeyboardButton(
                            text="ᴅᴇʟᴇᴛᴇ ❗", callback_data="unbanb_del"
                        ),
                    ]
                ]
            ),
            parse_mode=ParseMode.HTML,
        )
        return log
    except BadRequest as excp:
        if excp.message == "ʙᴀʟᴀsᴀɴ ᴘᴇsᴀɴ ᴛɪᴅᴀᴋ ᴅɪᴛᴇᴍᴜᴋᴀɴ":
            # Do not reply
            if silent:
                return log
            message.reply_text("ʙᴀɴɴᴇᴅ ❗!", quote=False)
            return log
        else:
            LOGGER.warning(update)
            LOGGER.exception(
                "ᴋᴇsᴀʟᴀʜᴀɴ ʙᴀɴɴɪɴɢ ᴘᴇɴɢɢᴜɴᴀ %s ᴅᴀʟᴀᴍ ɢʀᴜᴘ %s (%s) ᴋᴀʀᴇɴᴀ %s",
                user_id,
                chat.title,
                chat.id,
                excp.message,
            )
            message.reply_text("ᴜʜᴍ...ɪɴɪ ᴛɪᴅᴀᴋ ʙᴇᴋᴇʀᴊᴀ...")
    return log_message


@connection_status
@bot_admin
@can_restrict
@user_admin
@user_can_ban
@loggable
def temp_ban(update: Update, context: CallbackContext) -> str:
    chat = update.effective_chat
    user = update.effective_user
    message = update.effective_message
    log_message = ""
    bot, args = context.bot, context.args
    user_id, reason = extract_user_and_text(message, args)
    if not user_id:
        message.reply_text("⚠️ ᴘᴇɴɢɢᴜɴᴀ ᴛɪᴅᴀᴋ ᴅɪᴛᴇᴍᴜᴋᴀɴ.")
        return log_message
    try:
        member = chat.get_member(user_id)
    except BadRequest as excp:
        if excp.message != "ᴘᴇɴɢɢᴜɴᴀ ᴛɪᴅᴀᴋ ᴅɪᴛᴇᴍᴜᴋᴀɴ":
            raise
        message.reply_text("sᴀʏᴀ ᴛɪᴅᴀᴋ ʙɪsᴀ ᴍᴇɴᴇᴍᴜᴋᴀɴ ᴘᴇɴɢɢᴜɴᴀ ɪɴɪ.")
        return log_message
    if user_id == bot.id:
        message.reply_text("sᴀʏᴀ ᴛɪᴅᴀᴋ ᴀᴋᴀɴ ʙᴀɴɴᴇᴅ ᴅɪʀɪ sᴇɴᴅɪʀɪ, ᴀᴘᴀᴋᴀʜ ᴋᴀᴍᴜ ɴᴏᴏʙ ?")
        return log_message
    if is_user_ban_protected(chat, user_id, member):
        message.reply_text("sᴀʏᴀ ᴛɪᴅᴀᴋ ᴍᴇʀᴀsᴀ ᴍᴇɴʏᴜᴋᴀɪ ɪɴɪ.")
        return log_message
    if not reason:
        message.reply_text("ᴀɴᴅᴀ ʙᴇʟᴜᴍ ᴍᴇɴᴇɴᴛᴜᴋᴀɴ ᴡᴀᴋᴛᴜ ᴜɴᴛᴜᴋ ᴍᴇɴᴄᴇᴋᴀʟ ᴘᴇɴɢɢᴜɴᴀ ɪɴɪ!")
        return log_message
    split_reason = reason.split(None, 1)
    time_val = split_reason[0].lower()
    reason = split_reason[1] if len(split_reason) > 1 else ""
    bantime = extract_time(message, time_val)
    if not bantime:
        return log_message
    log = (
        f"<b>{html.escape(chat.title)}:</b>\n"
        "#ᴛᴇᴍᴘ ʙᴀɴɴᴇᴅ\n"
        f"<b>ᴀᴅᴍɪɴ:</b> {mention_html(user.id, html.escape(user.first_name))}\n"
        f"<b>ᴜsᴇʀ:</b> {mention_html(member.user.id, html.escape(member.user.first_name))}\n"
        f"<b>ᴛɪᴍᴇ:</b> {time_val}"
    )
    if reason:
        log += f"\nʀᴇᴀsᴏɴ: {reason}"
    try:
        chat.ban_member(user_id, until_date=bantime)
        # bot.send_sticker(chat.id, BAN_STICKER)  # banhammer marie sticker
        reply_msg = (
            f"<code>❕</code><b>Temporarily Banned</b>\n\n"
            f"<b>• ᴜsᴇʀ:</b> {mention_html(member.user.id, html.escape(member.user.first_name))}\n"
            f"<b>• ᴜsᴇʀ ɪᴅ:</b> <code>{member.user.id}</code>\n"
            f"<b>• ʙᴀɴɴᴇᴅ ғᴏʀ:</b> {time_val}\n"
            f"<b>• ʙᴀɴɴᴇᴅ ʙʏ:</b> {mention_html(user.id, html.escape(user.first_name))}"
        )
        if reason:
            reply_msg += f"\n<b>• ʀᴇᴀsᴏɴ:</b> {html.escape(reason)}"
        bot.sendMessage(
            chat.id,
            reply_msg,
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            text="ᴜɴʙᴀɴ ❗", callback_data=f"unbanb_unban={user_id}"
                        ),
                        InlineKeyboardButton(
                            text="ᴅᴇʟᴇᴛᴇ ❗", callback_data="unbanb_del"
                        ),
                    ]
                ]
            ),
            parse_mode=ParseMode.HTML,
        )
        return log
    except BadRequest as excp:
        if excp.message == "ʙᴀʟᴀsᴀɴ ᴘᴇsᴀɴ ᴛɪᴅᴀᴋ ᴅɪᴛᴇᴍᴜᴋᴀɴ":
            # Do not reply
            message.reply_text(
                f"{mention_html(member.user.id, html.escape(member.user.first_name))} [<code>{member.user.id}</code>] ʙᴀɴɴᴇᴅ ᴜɴᴛᴜᴋ {time_val}.",
                quote=False,
            )
            return log
        else:
            LOGGER.warning(update)
            LOGGER.exception(
                "ᴋᴇsᴀʟᴀʜᴀɴ ʙᴀɴɴɪɴɢ ᴘᴇɴɢɢᴜɴᴀ %s ᴅᴀʟᴀᴍ ɢʀᴏᴜᴘ %s (%s) ᴋᴀʀᴇɴᴀ %s",
                user_id,
                chat.title,
                chat.id,
                excp.message,
            )
            message.reply_text("sɪᴀʟᴀɴ, sᴀʏᴀ ᴛɪᴅᴀᴋ ʙɪsᴀ ʙᴀɴ ᴘᴇɴɢᴜɴᴀ ɪɴɪ.")
    return log_message


@connection_status
@bot_admin
@can_restrict
@user_admin_no_reply
@user_can_ban
@loggable
def unbanb_btn(update: Update, context: CallbackContext) -> str:
    bot = context.bot
    query = update.callback_query
    chat = update.effective_chat
    user = update.effective_user
    if query.data != "unbanb_del":
        splitter = query.data.split("=")
        query_match = splitter[0]
        if query_match == "unbanb_unban":
            user_id = splitter[1]
            if not is_user_admin(chat, int(user.id)):
                bot.answer_callback_query(
                    query.id,
                    text="⚠️ ᴀɴᴅᴀ ᴛɪᴅᴀᴋ ᴍᴇᴍɪʟɪᴋɪ ᴄᴜᴋᴜᴘ ʜᴀᴋ ᴜɴᴛᴜᴋ ᴍᴇᴍʙᴜɴʏɪᴋᴀɴ sᴜᴀʀᴀ ᴏʀᴀɴɢ",
                    show_alert=True,
                )
                return ""
            try:
                member = chat.get_member(user_id)
            except BadRequest:
                pass
            chat.unban_member(user_id)
            query.message.edit_text(
                f"{mention_html(member.user.id, html.escape(member.user.first_name))} [<code>{member.user.id}</code>] ᴅɪʙᴇʙᴀsᴋᴀɴ ᴏʟᴇʜ {mention_html(user.id, html.escape(user.first_name))}",
                parse_mode=ParseMode.HTML,
            )
            bot.answer_callback_query(query.id, text="Unbanned!")
            return (
                f"<b>{html.escape(chat.title)}:</b>\n"
                f"#ᴜɴʙᴀɴɴᴇᴅ\n"
                f"<b>ᴀᴅᴍɪɴ:</b> {mention_html(user.id, user.first_name)}\n"
                f"<b>ᴜsᴇʀ:</b> {mention_html(member.user.id, member.user.first_name)}"
            )
    else:
        if not is_user_admin(chat, int(user.id)):
            bot.answer_callback_query(
                query.id,
                text="⚠️ ᴀɴᴅᴀ ᴛɪᴅᴀᴋ ᴍᴇᴍɪʟɪᴋɪ ᴄᴜᴋᴜᴘ ʜᴀᴋ ᴜɴᴛᴜᴋ ᴍᴇɴɢʜᴀᴘᴜs ᴘᴇsᴀɴ.",
                show_alert=True,
            )
            return ""
        query.message.delete()
        bot.answer_callback_query(query.id, text="ᴍᴇɴɢʜᴀᴘᴜs !")
        return ""


@connection_status
@bot_admin
@can_restrict
@user_admin
@user_can_ban
@loggable
def punch(update: Update, context: CallbackContext) -> str:
    chat = update.effective_chat
    user = update.effective_user
    message = update.effective_message
    log_message = ""
    bot, args = context.bot, context.args
    user_id, reason = extract_user_and_text(message, args)
    if not user_id:
        message.reply_text("⚠️ ᴘᴇɴɢɢᴜɴᴀ ᴛɪᴅᴀᴋ ᴅɪᴛᴇᴍᴜᴋᴀɴ")
        return log_message
    try:
        member = chat.get_member(user_id)
    except BadRequest as excp:
        if excp.message != "ᴘᴇɴɢɢᴜɴᴀ ᴛɪᴅᴀᴋ ᴅɪᴛᴇᴍᴜᴋᴀɴ":
            raise
        message.reply_text("⚠️ sᴀʏᴀ ᴛɪᴅᴀᴋ ʙɪsᴀ ᴍᴇɴᴇᴍᴜᴋᴀɴ ᴘᴇɴɢɢᴜɴᴀ ɪɴɪ.")
        return log_message
    if user_id == bot.id:
        message.reply_text("ʏᴇᴀʜʜʜ sᴀʏᴀ ᴛɪᴅᴀᴋ ᴀᴋᴀɴ ᴍᴇʟᴀᴋᴜᴋᴀɴ ɪᴛᴜ.")
        return log_message
    if is_user_ban_protected(chat, user_id):
        message.reply_text("sᴀʏᴀ ʙᴇɴᴀʀ-ʙᴇɴᴀʀ ʙᴇʀʜᴀʀᴀᴘ sᴀʏᴀ ʙɪsᴀ ᴍᴇᴍᴜᴋᴜʟ ᴘᴇɴɢɢᴜɴᴀ ɪɴɪ....")
        return log_message
    if res := chat.unban_member(user_id):
        # bot.send_sticker(chat.id, BAN_STICKER)  # banhammer marie sticker
        bot.sendMessage(
            chat.id,
            f"{mention_html(member.user.id, html.escape(member.user.first_name))} [<code>{member.user.id}</code>] ᴅɪᴛᴇɴᴅᴀɴɢ ᴏʟᴇʜ {mention_html(user.id, html.escape(user.first_name))}",
            parse_mode=ParseMode.HTML,
        )
        log = (
            f"<b>{html.escape(chat.title)}:</b>\n"
            f"#ᴋɪᴄᴋᴇᴅ\n"
            f"<b>ᴀᴅᴍɪɴ:</b> {mention_html(user.id, html.escape(user.first_name))}\n"
            f"<b>ᴜsᴇʀ:</b> {mention_html(member.user.id, html.escape(member.user.first_name))}"
        )
        if reason:
            log += f"\n<b>ʀᴇᴀsᴏɴ:</b> {reason}"
        return log
    else:
        message.reply_text("⚠️ sɪᴀʟᴀɴ, sᴀʏᴀ ᴛɪᴅᴀᴋ ʙɪsᴀ ᴍᴇᴜᴋᴜʟ ᴘᴇɴɢɢᴜɴᴀ ɪɴɪ.")
    return log_message


@bot_admin
@can_restrict
def punchme(update: Update, context: CallbackContext):
    user_id = update.effective_message.from_user.id
    if is_user_admin(update.effective_chat, user_id):
        update.effective_message.reply_text("ᴀᴋᴜ ʙᴇʀʜᴀʀᴀᴘ ᴀᴋᴜ ʙɪsᴀ... ᴛᴀᴘɪ ᴋᴀᴍᴜ ᴀᴅᴍɪɴ.")
        return
    if res := update.effective_chat.unban_member(user_id):
        update.effective_message.reply_text(
            "ᴍᴇᴍᴜᴋᴜʟ ᴋᴀᴍᴜ ᴋᴇʟᴜᴀʀ ɢʀᴜᴘ !!",
        )
    else:
        update.effective_message.reply_text("ʜᴜʜ? ᴀᴋᴜ ᴛɪᴅᴀᴋ ʙɪsᴀ :/")


@connection_status
@bot_admin
@can_restrict
@user_admin
@user_can_ban
@loggable
def unban(update: Update, context: CallbackContext) -> Optional[str]:
    message = update.effective_message
    user = update.effective_user
    chat = update.effective_chat
    log_message = ""
    bot, args = context.bot, context.args
    if message.reply_to_message and message.reply_to_message.sender_chat:
        if r := bot.unban_chat_sender_chat(
            chat_id=chat.id,
            sender_chat_id=message.reply_to_message.sender_chat.id,
        ):
            message.reply_text(
                f"ᴄʜᴀɴɴᴇʟ {html.escape(message.reply_to_message.sender_chat.title)} ʙᴇʀʜᴀsɪʟ ᴍᴇᴍʙᴇʙᴀsᴋᴀɴ ᴅᴀʀɪ {html.escape(chat.title)}",
                parse_mode="html",
            )

        else:
            message.reply_text("ɢᴀɢᴀʟ ᴜɴᴛᴜᴋ ʙᴀɴ ᴄʜᴀɴɴᴇʟ")
        return
    user_id, reason = extract_user_and_text(message, args)
    if not user_id:
        message.reply_text("⚠️ ᴘᴇɴɢɢᴜɴᴀ ᴛɪᴅᴀᴋ ᴅɪᴛᴇᴍᴜᴋᴀɴ.")
        return log_message
    try:
        member = chat.get_member(user_id)
    except BadRequest as excp:
        if excp.message != "ᴘᴇɴɢɢᴜɴᴀ ᴛɪᴅᴀᴋ ᴅɪᴛᴇᴍᴜᴋᴀɴ":
            raise
        message.reply_text("sᴀʏᴀ ᴛɪᴅᴀᴋ ʙɪsᴀ ᴍᴇɴᴇᴍᴜᴋᴀɴ ᴘᴇɴɢɢᴜɴᴀ ɪɴɪ.")
        return log_message
    if user_id == bot.id:
        message.reply_text("ʙᴀɢᴀɪᴍᴀɴᴀ sᴀʏᴀ ᴀᴋᴀɴ ᴍᴇᴍʙᴀᴛᴀʟᴋᴀɴ ʟᴀʀᴀɴɢᴀɴ sᴀʏᴀ ᴊɪᴋᴀ sᴀʏᴀ ᴛɪᴅᴀᴋ ᴀᴅᴀ ᴅɪ sɪɴɪ...?")
        return log_message
    if is_user_in_chat(chat, user_id):
        message.reply_text("⚠️ ᴘᴇɴɢɢᴜɴᴀ ᴛɪᴅᴀᴋ ᴅɪᴛᴇᴍᴜᴋᴀɴ.")
        return log_message
    chat.unban_member(user_id)
    message.reply_text(
        f"{mention_html(member.user.id, html.escape(member.user.first_name))} [<code>{member.user.id}</code>] ᴛᴇʟᴀʜ ᴅɪʙᴇʙᴀsᴋᴀɴ ᴏʟᴇʜ {mention_html(user.id, user.first_name)}",
        parse_mode=ParseMode.HTML,
    )
    log = (
        f"<b>{html.escape(chat.title)}:</b>\n"
        f"#ᴜɴʙᴀɴɴᴇᴅ\n"
        f"<b>ᴀᴅᴍɪɴ:</b> {mention_html(user.id, html.escape(user.first_name))}\n"
        f"<b>ᴜsᴇʀ:</b> {mention_html(member.user.id, html.escape(member.user.first_name))}"
    )
    if reason:
        log += f"\n<b>ᴀʟᴀsᴀɴ:</b> {reason}"
    return log


@connection_status
@bot_admin
@can_restrict
@gloggable
def selfunban(update: Update, context: CallbackContext) -> str:
    message = update.effective_message
    user = update.effective_user
    bot, args = context.bot, context.args
    if user.id not in DRAGONS or user.id not in TIGERS:
        return
    try:
        chat_id = int(args[0])
    except:
        message.reply_text("ʙᴇʀɪᴋᴀɴ ᴄʜᴀᴛ ɪᴅ ʏᴀɴɢ ʙᴇɴᴀʀ.")
        return
    chat = bot.getChat(chat_id)
    try:
        member = chat.get_member(user.id)
    except BadRequest as excp:
        if excp.message == "ᴘᴇɴɢɢᴜɴᴀ ᴛɪᴅᴀᴋ ᴅɪᴛᴇᴍᴜᴋᴀɴ":
            message.reply_text("sᴀʏᴀ ᴛɪᴅᴀᴋ ʙɪsᴀ ᴍᴇɴᴇᴍᴜᴋᴀɴ ᴘᴇɴɢɢᴜɴᴀ ɪɴɪ.")
            return
        else:
            raise
    if is_user_in_chat(chat, user.id):
        message.reply_text("ʙᴜᴋᴀɴ ᴋᴀᴜ sᴜᴅᴀʜ ʙᴇʀᴀᴅᴀ ᴅɪɢʀᴜᴘ ɪɴɪ??")
        return
    chat.unban_member(user.id)
    message.reply_text(f"ʏᴇᴘ, sᴀʏᴀ ᴛᴇʟᴀʜ ᴍᴇᴍʙᴀᴛᴀʟᴋᴀɴ ᴘᴇᴍʙʟᴏᴋɪʀᴀɴ ᴘᴇɴɢɢᴜɴᴀ.")
    log = (
        f"<b>{html.escape(chat.title)}:</b>\n"
        f"#ᴜɴʙᴀɴɴᴇᴅ\n"
        f"<b>ᴜsᴇʀ:</b> {mention_html(member.user.id, html.escape(member.user.first_name))}"
    )
    return log


@bot_admin
@can_restrict
@loggable
def banme(update: Update, context: CallbackContext):
    user_id = update.effective_message.from_user.id
    chat = update.effective_chat
    user = update.effective_user
    if is_user_admin(update.effective_chat, user_id):
        update.effective_message.reply_text("⚠️ sᴀʏᴀ ᴛɪᴅᴀᴋ ʙɪsᴀ ʙᴀɴɴᴇᴅ ᴀᴅᴍɪɴ.")
        return
    if res := update.effective_chat.ban_member(user_id):
        update.effective_message.reply_text("ʏᴇs, ᴋᴀᴍᴜ ʙᴇɴᴀʀ!")
        return f"<b>{html.escape(chat.title)}:</b>\n#ʙᴀɴᴍᴇ\n<b>ᴜsᴇʀ:</b> {mention_html(user.id, user.first_name)}\n<b>ɪᴅ:</b> <code>{user_id}</code>"

    else:
        update.effective_message.reply_text("Huh? sᴀʏᴀ ᴛɪᴅᴀᴋ ʙɪsᴀ :/")


@dev_plus
def abishnoi(update: Update, context: CallbackContext):
    args = context.args
    bot = context.bot
    try:
        chat_id = str(args[0])
        del args[0]
    except TypeError:
        update.effective_message.reply_text("ᴛᴏʟᴏɴɢ ʙᴇʀɪ sᴀʏᴀ ᴏʙʀᴏʟᴀɴ ᴜɴᴛᴜᴋ ᴅɪɢᴀᴜɴɢᴋᴀɴ!")
    to_send = " ".join(args)
    if len(to_send) >= 2:
        try:
            bot.sendMessage(int(chat_id), to_send)
        except TelegramError:
            LOGGER.warning("ᴛɪᴅᴀᴋ ʙɪsᴀ ᴋɪʀɪᴍ ᴋᴇ ɢʀᴜᴘ %s", chat_id)
            update.effective_message.reply_text(
                "ᴛɪᴅᴀᴋ ʙɪsᴀ ᴍᴇɴɢɪʀɪᴍ ᴘᴇsᴀɴ. ᴍᴜɴɢᴋɪɴ sᴀʏᴀ ʙᴜᴋᴀɴ ʙᴀɢɪᴀɴ ᴅᴀʀɪ ɢʀᴜᴘ ɪᴛᴜ?"
            )


__help__ = """
*ᴜsᴇʀ ᴄᴏᴍᴍᴀɴᴅs:*

• /kickme*:* `ᴍᴇɴᴇɴᴅᴀɴɢ ᴘᴇɴɢɢᴜɴᴀ ʏᴀɴɢ ᴍᴇɴɢᴇʟᴜᴀʀᴋᴀɴ ᴘᴇʀɪɴᴛᴀʜ `

• /banme*:* `ᴍᴇᴍ-ʙᴀɴɴᴇᴅ ᴘᴇɴɢɢᴜɴᴀ ʏᴀɴɢ ᴍᴇɴɢᴇʟᴜᴀʀᴋᴀɴ ᴘᴇʀɪɴᴛᴀʜ `

*ᴀᴅᴍɪɴs ᴏɴʟʏ:*

• /ban <userhandle>*:*` ʙᴀɴ ᴘᴇɴɢɢᴜɴᴀ ( ᴅᴀʀɪ ᴘᴇʀɪɴᴛᴀʜ ᴀᴛᴀᴜ ʙᴀʟᴀsᴀɴ ᴘᴇsᴀɴ ) `
)
• /sban <ᴜsᴇʀʜᴀɴᴅʟᴇ>*:* `ᴅɪᴀᴍ-ᴅɪᴀᴍ ʙᴀɴ ᴘᴇɴɢɢᴜɴᴀ. ᴍᴇɴɢʜᴀᴘᴜs ᴘᴇʀɪɴᴛᴀʜ, ᴍᴇɴɢʜᴀᴘᴜs ʙᴀʟᴀsᴀɴ ᴘᴇsᴀɴ ᴅᴀɴ ᴛɪᴅᴀᴋ ᴍᴇᴍʙᴀʟᴀs. ( ᴅᴀʀɪ ᴘᴇʀɪɴᴛᴀʜ ᴀᴛᴀᴜ ʙᴀʟᴀsᴀɴ ᴘᴇsᴀɴ )`

• /tban <ᴜsᴇʀʜᴀɴᴅʟᴇ> x(m/h/d)*:* `ʙᴀɴ ᴘᴇɴɢɢᴜɴᴀ ᴜɴᴛᴜᴋ x ᴡᴀᴋᴛᴜ. ( ᴅᴀʀɪ ᴘᴇʀɪɴᴛᴀʜ ᴀᴛᴀᴜ ʙᴀʟᴀsᴀɴ ᴘᴇsᴀɴ ). ᴍ = ᴍɪɴᴜᴛᴇs, h = ʜᴏᴜʀs, d = ᴅᴀʏs.`

• /unban <userhandle>*:* `ᴍᴇᴍʙᴇʙᴀsᴋᴀɴ ᴘᴇɴɢɢᴜɴᴀ. ( ᴅᴀʀɪ ᴘᴇʀɪɴᴛᴀʜ ᴀᴛᴀᴜ ʙᴀʟᴀsᴀɴ ᴘᴇsᴀɴ )`

• /kick <userhandle>*:* `ᴍᴇɴᴇɴᴅᴀɴɢ ᴘᴇɴɢɢᴜɴᴀ, ( ᴅᴀʀɪ ᴘᴇʀɪɴᴛᴀʜ ᴀᴛᴀᴜ ʙᴀʟᴀsᴀɴ ᴘᴇsᴀɴ )`

• /mute <userhandle>*:* `ᴍᴇᴍʙɪsᴜᴋᴀɴ ᴘᴇɴɢɢᴜɴᴀ. ( ᴅᴀʀɪ ᴘᴇʀɪɴᴛᴀʜ ᴀᴛᴀᴜ ʙᴀʟᴀsᴀɴ ᴘᴇsᴀɴ )`

• /tmute <userhandle> x(m/h/d)*:* `ᴍᴇᴍʙɪsᴜᴋᴀɴ ᴘᴇɴɢɢᴜɴᴀ ᴜɴᴛᴜᴋ x ᴡᴀᴋᴛᴜ. ( ᴅᴀʀɪ ᴘᴇʀɪɴᴛᴀʜ ᴀᴛᴀᴜ ʙᴀʟᴀsᴀɴ ᴘᴇsᴀɴ ). ᴍ = ᴍɪɴᴜᴛᴇs, h = ʜᴏᴜʀs, d = ᴅᴀʏs `
.
• /unmute <userhandle>*:* `ᴍᴇᴍʙᴜɴʏɪᴋᴀɴ ᴘᴇɴɢɢᴜɴᴀ `
.
• /zombies*:* `ᴍᴇɴᴄᴀʀɪ ᴀᴋᴜɴ ᴛᴇʀʜᴀᴘᴜs `

• /zombies clean*:* `ᴍᴇᴍʙᴜᴀɴɢ ᴀᴋᴜɴ ᴛᴇʀʜᴀᴘᴜs `
.
• /abishnoi <chatid> <ᴍsɢ>*:* ` ᴍᴇᴍʙᴜᴀᴛ sᴀʏᴀ ᴍᴇɴɢɪʀɪᴍ ᴘᴇsᴀɴ ᴋᴇ ᴏʙʀᴏʟᴀɴ ᴛᴇʀᴛᴇɴᴛᴜ `.
"""

__mod_name__ = "𝙱ᴀɴs"

BAN_HANDLER = CommandHandler(["ban", "sban"], ban, run_async=True)
TEMPBAN_HANDLER = CommandHandler(["tban"], temp_ban, run_async=True)
KICK_HANDLER = CommandHandler(["kick", "punch"], punch, run_async=True)
UNBAN_HANDLER = CommandHandler("unban", unban, run_async=True)
##ROAR_HANDLER = CommandHandler("roar", selfunban, run_async=True)
UNBAN_BUTTON_HANDLER = CallbackQueryHandler(unbanb_btn, pattern=r"unbanb_")
KICKME_HANDLER = DisableAbleCommandHandler(
    ["kickme", "punchme"], punchme, filters=Filters.chat_type.groups, run_async=True
)
ABISHNOI_HANDLER = CommandHandler(
    "abishnoi",
    abishnoi,
    pass_args=True,
    filters=CustomFilters.sudo_filter,
    run_async=True,
)
BANME_HANDLER = CommandHandler("banme", banme, run_async=True)

dispatcher.add_handler(BAN_HANDLER)
dispatcher.add_handler(TEMPBAN_HANDLER)
dispatcher.add_handler(KICK_HANDLER)
dispatcher.add_handler(UNBAN_HANDLER)
# dispatcher.add_handler(ROAR_HANDLER)
dispatcher.add_handler(KICKME_HANDLER)
dispatcher.add_handler(UNBAN_BUTTON_HANDLER)
dispatcher.add_handler(ABISHNOI_HANDLER)
dispatcher.add_handler(BANME_HANDLER)

__handlers__ = [
    BAN_HANDLER,
    TEMPBAN_HANDLER,
    KICK_HANDLER,
    UNBAN_HANDLER,
    # ROAR_HANDLER,
    KICKME_HANDLER,
    UNBAN_BUTTON_HANDLER,
    ABISHNOI_HANDLER,
    BANME_HANDLER,
]
