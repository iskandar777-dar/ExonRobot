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

from telegram import ParseMode, Update
from telegram.ext import CallbackContext, CommandHandler, Filters, MessageHandler

from Exon import ALLOW_EXCL, BOT_NAME, CustomCommandHandler, dispatcher
from Exon.modules.disable import DisableAbleCommandHandler
from Exon.modules.helper_funcs.chat_status import (
    bot_can_delete,
    connection_status,
    dev_plus,
    user_admin,
)
from Exon.modules.sql import cleaner_sql as sql

CMD_STARTERS = ("/", "!") if ALLOW_EXCL else "/"
BLUE_TEXT_CLEAN_GROUP = 13
CommandHandlerList = (CommandHandler, CustomCommandHandler, DisableAbleCommandHandler)
command_list = [
    "cleanblue",
    "ignoreblue",
    "unignoreblue",
    "listblue",
    "ungignoreblue",
    "gignoreblue",
    "start",
    "help",
    "settings",
    "donate",
    "stalk",
    "aka",
    "leaderboard",
]

for handler_list in dispatcher.handlers:
    for handler in dispatcher.handlers[handler_list]:
        if any(isinstance(handler, cmd_handler) for cmd_handler in CommandHandlerList):
            command_list += handler.command


def clean_blue_text_must_click(update: Update, context: CallbackContext):
    bot = context.bot
    chat = update.effective_chat
    message = update.effective_message
    if chat.get_member(bot.id).can_delete_messages and sql.is_enabled(chat.id):
        fst_word = message.text.strip().split(None, 1)[0]

        if len(fst_word) > 1 and any(
            fst_word.startswith(start) for start in CMD_STARTERS
        ):

            command = fst_word[1:].split("@")
            chat = update.effective_chat

            if ignored := sql.is_command_ignored(chat.id, command[0]):
                return

            if command[0] not in command_list:
                message.delete()


@connection_status
@bot_can_delete
@user_admin
def set_blue_text_must_click(update: Update, context: CallbackContext):
    chat = update.effective_chat
    message = update.effective_message
    bot, args = context.bot, context.args
    if len(args) >= 1:
        val = args[0].lower()
        if val in ("off", "no"):
            sql.set_cleanbt(chat.id, False)
            reply = f"ʙʟᴜᴇᴛᴇxᴛ ᴄʟᴇᴀɴɪɴɢ ᴅɪɴᴏɴᴀᴋᴛɪꜰᴋᴀɴ ᴜɴᴛᴜᴋ <b>{html.escape(chat.title)}</b>"

            message.reply_text(reply, parse_mode=ParseMode.HTML)

        elif val in ("yes", "on"):
            sql.set_cleanbt(chat.id, True)
            reply = f"ʙʟᴜᴇᴛᴇxᴛ ᴄʟᴇᴀɴɪɴɢ ᴅɪᴀᴋᴛɪꜰᴋᴀɴ ᴜɴᴛᴜᴋ <b>{html.escape(chat.title)}</b>"

            message.reply_text(reply, parse_mode=ParseMode.HTML)

        else:
            reply = "ɴɪʟᴀɪ sᴀʟᴀʜ, ʜᴀɴʏᴀ ᴍᴇɴᴇʀɪᴍᴀ ᴘᴇʀɪɴᴛᴀʜ 'yes', 'on', \  'no', 'off'"
            message.reply_text(reply)
    else:
        clean_status = sql.is_enabled(chat.id)
        clean_status = "Enabled" if clean_status else "Disabled"
        reply = f"ʙʟᴜᴇᴛᴇxᴛ ᴄʟᴇᴀɴɪɴɢ ᴜɴᴛᴜᴋ <b>{html.escape(chat.title)}</b> : <b>{clean_status}</b>"

        message.reply_text(reply, parse_mode=ParseMode.HTML)


@user_admin
def add_bluetext_ignore(update: Update, context: CallbackContext):
    message = update.effective_message
    chat = update.effective_chat
    args = context.args
    if len(args) >= 1:
        val = args[0].lower()
        if added := sql.chat_ignore_command(chat.id, val):
            reply = f"<b>{args[0]}</b> ᴅɪᴛᴀᴍʙᴀʜᴋᴀɴ ᴋᴇ ʙʟᴜᴇᴛᴇxᴛ ᴄʟᴇᴀɴᴇʀ ɪɢɴᴏʀᴇ ʟɪsᴛ."
        else:
            reply = "ᴄᴏᴍᴍᴀɴᴅ ᴅɪᴀʙᴀɪᴋᴀɴ."
        message.reply_text(reply, parse_mode=ParseMode.HTML)

    else:
        reply = "ᴛɪᴅᴀᴋ ᴀᴅᴀ ᴘᴇʀɪɴᴛᴀʜ ʏᴀɴɢ ᴅɪsᴇᴅɪᴀᴋᴀɴ ᴜɴᴛᴜᴋ ᴅɪᴀʙᴀɪᴋᴀɴ."
        message.reply_text(reply)


@user_admin
def remove_bluetext_ignore(update: Update, context: CallbackContext):
    message = update.effective_message
    chat = update.effective_chat
    args = context.args
    if len(args) >= 1:
        val = args[0].lower()
        if removed := sql.chat_unignore_command(chat.id, val):
            reply = (
                f"<b>{args[0]}</b> ᴅɪʜᴀᴘᴜsᴋᴀɴ ᴅᴀʀɪ ʙʟᴜᴇᴛᴇxᴛ ᴄʟᴇᴀɴᴇʀ ɪɢɴᴏʀᴇ ʟɪsᴛ."
            )
        else:
            reply = "ᴘᴇʀɪɴᴛᴀʜ ᴛɪᴅᴀᴋ ᴅɪᴀʙᴀɪᴋᴀɴ sᴀᴀᴛ ɪɴɪ."
        message.reply_text(reply, parse_mode=ParseMode.HTML)

    else:
        reply = "ᴛɪᴅᴀᴋ ᴀᴅᴀ ᴘᴇʀɪɴᴛᴀʜ ʏᴀɴɢ ᴅɪsᴇᴅɪᴀᴋᴀɴ ᴜɴᴛᴜᴋ ᴅɪᴀʙᴀɪᴋᴀɴ."
        message.reply_text(reply)


@user_admin
def add_bluetext_ignore_global(update: Update, context: CallbackContext):
    message = update.effective_message
    args = context.args
    if len(args) >= 1:
        val = args[0].lower()
        if added := sql.global_ignore_command(val):
            reply = f"<b>{args[0]}</b> ʙᴇʀʜᴀsɪʟ ᴅɪᴛᴀᴍʙᴀʜᴋᴀɴ ᴋᴇ ɢʟᴏʙᴀʟ ʙʟᴜᴇᴛᴇxᴛ ᴄʟᴇᴀɴᴇʀ ɪɢɴᴏʀᴇ ʟɪsᴛ."

        else:
            reply = "ᴄᴏᴍᴍᴀɴᴅ ᴅɪᴀʙᴀɪᴋᴀɴ."
        message.reply_text(reply, parse_mode=ParseMode.HTML)

    else:
        reply = "ᴛɪᴅᴀᴋ ᴀᴅᴀ ᴘᴇʀɪɴᴛᴀʜ ʏᴀɴɢ ᴅɪsᴇᴅɪᴀᴋᴀɴ ᴜɴᴛᴜᴋ ᴅɪᴀʙᴀɪᴋᴀɴ."
        message.reply_text(reply)


@dev_plus
def remove_bluetext_ignore_global(update: Update, context: CallbackContext):
    message = update.effective_message
    args = context.args
    if len(args) >= 1:
        val = args[0].lower()
        if removed := sql.global_unignore_command(val):
            reply = f"<b>{args[0]}</b> ʙᴇʀʜᴀsɪʟ ᴅɪᴛᴀᴍʙᴀʜᴋᴀɴ ᴋᴇ ɢʟᴏʙᴀʟ ʙʟᴜᴇᴛᴇxᴛ ᴄʟᴇᴀɴᴇʀ ɪɢɴᴏʀᴇ ʟɪsᴛ."

        else:
            reply = "ᴘᴇʀɪɴᴛᴀʜ ᴛɪᴅᴀᴋ ᴅɪᴀʙᴀɪᴋᴀɴ sᴀᴀᴛ ɪɴɪ."
        message.reply_text(reply, parse_mode=ParseMode.HTML)

    else:
        reply = "ᴛɪᴅᴀᴋ ᴀᴅᴀ ᴘᴇʀɪɴᴛᴀʜ ʏᴀɴɢ ᴅɪsᴇᴅɪᴀᴋᴀɴ ᴜɴᴛᴜᴋ ᴅɪᴀʙᴀɪᴋᴀɴ."
        message.reply_text(reply)


@dev_plus
def bluetext_ignore_list(update: Update, context: CallbackContext):

    message = update.effective_message
    chat = update.effective_chat

    global_ignored_list, local_ignore_list = sql.get_all_ignored(chat.id)
    text = ""

    if global_ignored_list:
        text = "ᴘᴇʀɪɴᴛᴀʜ ʙᴇʀɪᴋᴜᴛ sᴀᴀᴛ ɪɴɪ ᴅɪᴀʙᴀɪᴋᴀɴ sᴇᴄᴀʀᴀ ɢʟᴏʙᴀʟ ᴅᴀʀɪ ʙʟᴜᴇᴛᴇxᴛ ᴄʟᴇᴀɴɪɴɢ :\n"

        for x in global_ignored_list:
            text += f" - <code>{x}</code>\n"

    if local_ignore_list:
        text += "\nᴘᴇʀɪɴᴛᴀʜ ʙᴇʀɪᴋᴜᴛ sᴀᴀᴛ ɪɴɪ ᴅɪᴀʙᴀɪᴋᴀɴ sᴇᴄᴀʀᴀ ʟᴏᴋᴀʟ ᴅᴀʀɪ ʙʟᴜᴇᴛᴇxᴛ ᴄʟᴇᴀɴɪɴɢ :\n"

        for x in local_ignore_list:
            text += f" - <code>{x}</code>\n"

    if text == "":
        text = "ᴛɪᴅᴀᴋ ᴀᴅᴀ ᴘᴇʀɪɴᴛᴀʜ ʏᴀɴɢ sᴀᴀᴛ ɪɴɪ ᴅɪᴀʙᴀɪᴋᴀɴ ᴅᴀʀɪ ʙʟᴜᴇᴛᴇxᴛ ᴄʟᴇᴀɴɪɴɢ."
        message.reply_text(text)
        return

    message.reply_text(text, parse_mode=ParseMode.HTML)
    return


SET_CLEAN_BLUE_TEXT_HANDLER = CommandHandler(
    "cleanblue", set_blue_text_must_click, run_async=True
)
ADD_CLEAN_BLUE_TEXT_HANDLER = CommandHandler(
    "ignoreblue", add_bluetext_ignore, run_async=True
)
REMOVE_CLEAN_BLUE_TEXT_HANDLER = CommandHandler(
    "unignoreblue", remove_bluetext_ignore, run_async=True
)
ADD_CLEAN_BLUE_TEXT_GLOBAL_HANDLER = CommandHandler(
    "gignoreblue",
    add_bluetext_ignore_global,
    run_async=True,
)
REMOVE_CLEAN_BLUE_TEXT_GLOBAL_HANDLER = CommandHandler(
    "ungignoreblue",
    remove_bluetext_ignore_global,
    run_async=True,
)
LIST_CLEAN_BLUE_TEXT_HANDLER = CommandHandler(
    "listblue", bluetext_ignore_list, run_async=True
)
CLEAN_BLUE_TEXT_HANDLER = MessageHandler(
    Filters.command & Filters.chat_type.groups,
    clean_blue_text_must_click,
    run_async=True,
)

dispatcher.add_handler(SET_CLEAN_BLUE_TEXT_HANDLER)
dispatcher.add_handler(ADD_CLEAN_BLUE_TEXT_HANDLER)
dispatcher.add_handler(REMOVE_CLEAN_BLUE_TEXT_HANDLER)
dispatcher.add_handler(ADD_CLEAN_BLUE_TEXT_GLOBAL_HANDLER)
dispatcher.add_handler(REMOVE_CLEAN_BLUE_TEXT_GLOBAL_HANDLER)
dispatcher.add_handler(LIST_CLEAN_BLUE_TEXT_HANDLER)
dispatcher.add_handler(CLEAN_BLUE_TEXT_HANDLER, BLUE_TEXT_CLEAN_GROUP)

__mod_name__ = "𝙲ʟᴇᴀɴɪɴɢ"
__handlers__ = [
    SET_CLEAN_BLUE_TEXT_HANDLER,
    ADD_CLEAN_BLUE_TEXT_HANDLER,
    REMOVE_CLEAN_BLUE_TEXT_HANDLER,
    ADD_CLEAN_BLUE_TEXT_GLOBAL_HANDLER,
    REMOVE_CLEAN_BLUE_TEXT_GLOBAL_HANDLER,
    LIST_CLEAN_BLUE_TEXT_HANDLER,
    (CLEAN_BLUE_TEXT_HANDLER, BLUE_TEXT_CLEAN_GROUP),
]

__help__ = f"""
ʙʟᴜᴇ ᴛᴇxᴛ ᴄʟᴇᴀɴᴇʀ ᴍᴇɴɢʜᴀᴘᴜs sᴇᴍᴜᴀ ᴘᴇʀɪɴᴛᴀʜ ʏᴀɴɢ ᴅɪʙᴜᴀᴛ-ʙᴜᴀᴛ ʏᴀɴɢ ᴅɪᴋɪʀɪᴍ ᴏʀᴀɴɢ ᴅᴀʟᴀᴍ ᴏʙʀᴏʟᴀɴ ᴀɴᴅᴀ.

• /cleanblue <on/off/yes/no>*:* `ᴍᴇᴍʙᴇʀsɪʜᴋᴀɴ ᴘᴇʀɪɴᴛᴀʜ sᴇᴛᴇʟᴀʜ ᴅɪᴋɪʀɪᴍ`

• /ignoreblue <word>*:* `ᴍᴇɴᴄᴇɢᴀʜ ᴏᴛᴏᴍᴀᴛɪs ᴍᴇᴍʙᴇʀsɪʜᴋᴀɴ ᴘᴇʀɪɴᴛᴀʜ \`

• /unignoreblue <word>*:* `ᴍᴇɴɢʜᴀᴘᴜs ᴍᴇɴᴄᴇɢᴀʜ ᴏᴛᴏᴍᴀᴛɪs ᴍᴇᴍʙᴇʀsɪʜᴋᴀɴ ᴘᴇʀɪɴᴛᴀʜ `

• /listblue*:* `ᴅᴀꜰᴛᴀʀ ᴘᴇʀɪɴᴛᴀʜ ʏᴀɴɢ sᴀᴀᴛ ɪɴɪ ᴍᴀsᴜᴋ ᴅᴀꜰᴛᴀʀ ᴘᴜᴛɪʜ `
 
*ʜᴀɴʏᴀ sᴜᴅᴏ:*
 
• /gignoreblue <word>*:* `ᴅɪᴀʙᴀɪᴋᴀɴ sᴇᴄᴀʀᴀ ɢʟᴏʙᴀʟ ʙʟᴜᴇᴛᴇxᴛ ᴄʟᴇᴀɴɪɴɢ ᴅᴀʀɪ ᴋᴀᴛᴀ ʏᴀɴɢ ᴅɪsɪᴍᴘᴀɴ ᴅɪ sᴇʟᴜʀᴜʜ` {BOT_NAME}.

• /ungignoreblue <word>*:* `ʜᴀᴘᴜs ᴘᴇʀɪɴᴛᴀʜ ᴛᴇʀsᴇʙᴜᴛ ᴅᴀʀɪ ɢʟᴏʙᴀʟ ᴄʟᴇᴀɴɪɴɢ ʟɪsᴛ `
"""
