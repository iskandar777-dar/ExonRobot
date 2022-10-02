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

import time

from telegram import MessageEntity
from telegram.error import BadRequest
from telegram.ext import Filters, MessageHandler

from Exon import REDIS, dispatcher
from Exon.modules.disable import DisableAbleCommandHandler
from Exon.modules.helper_funcs.readable_time import get_readable_time
from Exon.modules.sql.afk_redis import afk_reason, end_afk, is_user_afk, start_afk
from Exon.modules.users import get_user_id

AFK_GROUP = 7
AFK_REPLY_GROUP = 8


def afk(update, context):
    args = update.effective_message.text.split(None, 1)
    user = update.effective_user
    if not user:  # ignore channels
        return

    if user.id == 777000:
        return
    start_afk_time = time.time()
    if len(args) >= 2:
        reason = args[1]
    else:
        reason = "none"
    start_afk(update.effective_user.id, reason)
    REDIS.set(f"afk_time_{update.effective_user.id}", start_afk_time)
    fname = update.effective_user.first_name
    try:
        update.effective_message.reply_text("{} ɪs ɴᴏᴡ ᴀᴡᴀʏ!".format(fname))
    except BadRequest:
        pass


def no_longer_afk(update, context):
    user = update.effective_user
    message = update.effective_message
    if not user:  # ignore channels
        return

    if not is_user_afk(user.id):  # Check if user is afk or not
        return
    end_afk_time = get_readable_time(
        (time.time() - float(REDIS.get(f"afk_time_{user.id}")))
    )
    REDIS.delete(f"afk_time_{user.id}")
    res = end_afk(user.id)
    if res:
        if message.new_chat_members:  # dont say msg
            return
        firstname = update.effective_user.first_name
        try:
            message.reply_text(
                "{} ɪs ʙᴀᴄᴋ ᴏɴʟɪɴᴇ!\n\nʏᴏᴜ ᴡᴇʀᴇ ɢᴏɴᴇ ғᴏʀ {}.".format(
                    firstname, end_afk_time
                )
            )
        except Exception:
            return


def reply_afk(update, context):
    message = update.effective_message
    userc = update.effective_user
    userc_id = userc.id
    if message.entities and message.parse_entities(
        [MessageEntity.TEXT_MENTION, MessageEntity.MENTION]
    ):
        entities = message.parse_entities(
            [MessageEntity.TEXT_MENTION, MessageEntity.MENTION]
        )

        chk_users = []
        for ent in entities:
            if ent.type == MessageEntity.TEXT_MENTION:
                user_id = ent.user.id
                fst_name = ent.user.first_name

                if user_id in chk_users:
                    return
                chk_users.append(user_id)

            elif ent.type == MessageEntity.MENTION:
                user_id = get_user_id(
                    message.text[ent.offset : ent.offset + ent.length]
                )
                if not user_id:
                    # Should never happen, since for a user to become AFK they must have spoken. Maybe changed username?
                    return

                if user_id in chk_users:
                    return
                chk_users.append(user_id)

                try:
                    chat = context.bot.get_chat(user_id)
                except BadRequest:
                    print(
                        "ᴋᴇsᴀʟᴀʜᴀɴ: ᴛɪᴅᴀᴋ ᴅᴀᴘᴀᴛ ᴍᴇɴɢᴀᴍʙɪʟ ɪᴅ ᴘᴇɴɢɢᴜɴᴀ {} ᴜɴᴛᴜᴋ ᴍᴏᴅᴜʟ ᴀꜰᴋ".format(
                            user_id
                        )
                    )
                    return
                fst_name = chat.first_name

            else:
                return

            check_afk(update, context, user_id, fst_name, userc_id)

    elif message.reply_to_message:
        user_id = message.reply_to_message.from_user.id
        fst_name = message.reply_to_message.from_user.first_name
        check_afk(update, context, user_id, fst_name, userc_id)


def check_afk(update, context, user_id, fst_name, userc_id):
    if is_user_afk(user_id):
        reason = afk_reason(user_id)
        since_afk = get_readable_time(
            (time.time() - float(REDIS.get(f"afk_time_{user_id}")))
        )
        if reason == "none":
            if int(userc_id) == int(user_id):
                return
            res = "{} ᴀꜰᴋ.\n\n ᴛᴇʀᴀᴋʜɪʀ ᴛᴇʀʟɪʜᴀᴛ {} ʏᴀɴɢ ʟᴀʟᴜ.".format(fst_name, since_afk)
            update.effective_message.reply_text(res)
        else:
            if int(userc_id) == int(user_id):
                return
            res = "{} ᴀꜰᴋ.\nᴀʟᴀsᴀɴ: {}\n\nᴛᴇʀᴀᴋʜɪʀ ᴛᴇʀʟɪʜᴀᴛ {} ʏᴀɴɢ ʟᴀʟᴜ.".format(
                fst_name, reason, since_afk
            )
            update.effective_message.reply_text(res)


def __user_info__(user_id):
    is_afk = is_user_afk(user_id)
    text = ""
    if is_afk:
        since_afk = get_readable_time(
            (time.time() - float(REDIS.get(f"afk_time_{user_id}")))
        )
        text = "<i>ᴘᴇɴɢɢᴜɴᴀ ɪɴɪ sᴇᴅᴀɴɢ ᴀꜰᴋ (ᴊᴀᴜʜ ᴅᴀʀɪ ᴋᴇʏʙᴏᴀʀᴅ).</i>"
        text += f"\n<i>sᴇᴊᴀᴋ: {since_afk}</i>"

    else:
        text = "<i>ᴘᴇɴɢɢᴜɴᴀ sᴀᴀᴛ ɪɴɪ ᴛɪᴅᴀᴋ ᴀꜰᴋ (ᴊᴀᴜʜ ᴅᴀʀɪ ᴋᴇʏʙᴏᴀʀᴅ).</i>"
    return text


def __gdpr__(user_id):
    end_afk(user_id)


__mod_name__ = "𝙰ғᴋ"

__help__ = """
✪ /afk <ᴀʟᴀsᴀɴ> *:* `ᴛᴀɴᴅᴀɪ ᴅɪʀɪ ᴀɴᴅᴀ sᴇʙᴀɢᴀɪ ᴀꜰᴋ (ᴊᴀᴜʜ ᴅᴀʀɪ ᴋᴇʏʙᴏᴀʀᴅ) ᴋᴇᴛɪᴋᴀ ᴅɪᴛᴀɴᴅᴀɪ sᴇʙᴀɢᴀɪ ᴀꜰᴋ, sᴇᴛɪᴀᴘ ᴍᴇɴᴛᴏɴ ᴀᴋᴀɴ ᴅɪʙᴀʟᴀs ᴅᴇɴɢᴀɴ ᴘᴇsᴀɴ ᴜɴᴛᴜᴋ ᴍᴇɴɢᴀᴛᴀᴋᴀɴ ʙᴀʜᴡᴀ ᴀɴᴅᴀ ᴛɪᴅᴀᴋ ᴛᴇʀsᴇᴅɪᴀ!`
     
*ᴍᴏʀᴇ ᴛʏᴘᴇ*
✪ byy|brb|bye  <ᴀʟᴀsᴀɴ>  *:* `sᴀᴍᴀ sᴇᴘᴇʀᴛɪ ᴀꜰᴋ`
"""


AFK_HANDLER = DisableAbleCommandHandler("afk", afk)
AFK_REGEX_HANDLER = MessageHandler(Filters.regex("(?i)brb|(?i)bye|(?i)byy"), afk)
NO_AFK_HANDLER = MessageHandler(Filters.all & Filters.group, no_longer_afk)
AFK_REPLY_HANDLER = MessageHandler(Filters.all & Filters.group, reply_afk)

dispatcher.add_handler(AFK_HANDLER, AFK_GROUP)
dispatcher.add_handler(AFK_REGEX_HANDLER, AFK_GROUP)
dispatcher.add_handler(NO_AFK_HANDLER, AFK_GROUP)
dispatcher.add_handler(AFK_REPLY_HANDLER, AFK_REPLY_GROUP)
