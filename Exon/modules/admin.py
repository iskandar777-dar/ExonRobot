import html
import os
from typing import Optional

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ParseMode, Update
from telegram.error import BadRequest
from telegram.ext import CallbackContext, CallbackQueryHandler, CommandHandler, Filters
from telegram.utils.helpers import mention_html

from Exon import DRAGONS, LOGGER, dispatcher
from Exon.modules.disable import DisableAbleCommandHandler
from Exon.modules.helper_funcs.alternate import send_message
from Exon.modules.helper_funcs.chat_status import (
    ADMIN_CACHE,
    bot_admin,
    can_pin,
    can_promote,
    connection_status,
    is_user_admin,
    user_admin,
    user_can_promote,
)
from Exon.modules.helper_funcs.extraction import extract_user, extract_user_and_text
from Exon.modules.log_channel import loggable


def user_can_changeinfo(chat, user_admin, id):
    pass


@bot_admin
@user_admin
def set_sticker(update: Update, context: CallbackContext):
    msg = update.effective_message
    chat = update.effective_chat
    user = update.effective_user

    if user_can_changeinfo(chat, user, context.bot.id) is False:
        return msg.reply_text("ᴀɴᴅᴀ ᴋᴇʜɪʟᴀɴɢᴀɴ ʜᴀᴋ ᴜɴᴛᴜᴋ ᴍᴇɴɢᴜʙᴀʜ ɪɴꜰᴏ ᴏʙʀᴏʟᴀɴ!")

    if msg.reply_to_message:
        if not msg.reply_to_message.sticker:
            return msg.reply_text(
                "ᴀɴᴅᴀ ᴘᴇʀʟᴜ ᴍᴇᴍʙᴀʟᴀs ʙᴇʙᴇʀᴀᴘᴀ sᴛɪᴋᴇʀ ᴜɴᴛᴜᴋ ᴍᴇɴɢᴀᴛᴜʀ sᴇᴛ sᴛɪᴋᴇʀ ᴏʙʀᴏʟᴀɴ!"
            )
        stkr = msg.reply_to_message.sticker.set_name
        try:
            context.bot.set_chat_sticker_set(chat.id, stkr)
            msg.reply_text(f"ʙᴇʀʜᴀsɪʟ ᴍᴇɴɢᴀᴛᴜʀ sᴛɪᴋᴇʀ ɢʀᴜᴘ ʙᴀʀᴜ ᴅɪ {chat.title}!")
        except BadRequest as excp:
            if excp.message == "Participants_too_few":
                return msg.reply_text(
                    "ᴍᴀᴀꜰ, ᴋᴀʀᴇɴᴀ ᴘᴇᴍʙᴀᴛᴀsᴀɴ ᴛᴇʟᴇɢʀᴀᴍ, ᴏʙʀᴏʟᴀɴ ʜᴀʀᴜs ᴍᴇᴍɪʟɪᴋɪ ᴍɪɴɪᴍᴀʟ 100 ᴀɴɢɢᴏᴛᴀ sᴇʙᴇʟᴜᴍ ᴍᴇʀᴇᴋᴀ ᴅᴀᴘᴀᴛ ᴍᴇᴍɪʟɪᴋɪ sᴛɪᴋᴇʀ ɢʀᴜᴘ!"
                )
            msg.reply_text(f"ᴋᴇsᴀʟᴀʜᴀɴ! {excp.message}.")
    else:
        msg.reply_text("ᴀɴᴅᴀ ᴘᴇʀʟᴜ ᴍᴇᴍʙᴀʟᴀs ʙᴇʙᴇʀᴀᴘᴀ sᴛɪᴋᴇʀ ᴜɴᴛᴜᴋ ᴍᴇɴɢᴀᴛᴜʀ sᴇᴛ sᴛɪᴋᴇʀ ᴏʙʀᴏʟᴀɴ!")


@bot_admin
@user_admin
def setchatpic(update: Update, context: CallbackContext):
    chat = update.effective_chat
    msg = update.effective_message
    user = update.effective_user

    if user_can_changeinfo(chat, user, context.bot.id) is False:
        msg.reply_text("ᴀɴᴅᴀ ᴋᴇʜɪʟᴀɴɢᴀɴ ʜᴀᴋ ᴜɴᴛᴜᴋ ᴍᴇɴɢᴜʙᴀʜ ɪɴꜰᴏ ɢʀᴜᴘ!")
        return

    if msg.reply_to_message:
        if msg.reply_to_message.photo:
            pic_id = msg.reply_to_message.photo[-1].file_id
        elif msg.reply_to_message.document:
            pic_id = msg.reply_to_message.document.file_id
        else:
            msg.reply_text("ᴀɴᴅᴀ ʜᴀɴʏᴀ ᴅᴀᴘᴀᴛ ᴍᴇɴɢᴀᴛᴜʀ ʙᴇʙᴇʀᴀᴘᴀ ꜰᴏᴛᴏ sᴇʙᴀɢᴀɪ ɢᴀᴍʙᴀʀ ᴏʙʀᴏʟᴀɴ!")
            return
        dlmsg = msg.reply_text("ᴛᴜɴɢɢᴜ sᴇʙᴇɴᴛᴀʀ...")
        tpic = context.bot.get_file(pic_id)
        tpic.download("gpic.png")
        try:
            with open("gpic.png", "rb") as chatp:
                context.bot.set_chat_photo(int(chat.id), photo=chatp)
                msg.reply_text("ʙᴇʀʜᴀsɪʟ ᴍᴇɴɢᴀᴛᴜʀ ᴄʜᴀᴛᴘɪᴄ ʙᴀʀᴜ!")
        except BadRequest as excp:
            msg.reply_text(f"Error! {excp.message}")
        finally:
            dlmsg.delete()
            if os.path.isfile("gpic.png"):
                os.remove("gpic.png")
    else:
        msg.reply_text("ʙᴀʟᴀs ᴋᴇ ʙᴇʙᴇʀᴀᴘᴀ ꜰᴏᴛᴏ ᴀᴛᴀᴜ ꜰɪʟᴇ ᴜɴᴛᴜᴋ ᴍᴇɴɢᴀᴛᴜʀ ɢᴀᴍʙᴀʀ ᴏʙʀᴏʟᴀɴ ʙᴀʀᴜ!")


@bot_admin
@user_admin
def rmchatpic(update: Update, context: CallbackContext):
    chat = update.effective_chat
    msg = update.effective_message
    user = update.effective_user

    if user_can_changeinfo(chat, user, context.bot.id) is False:
        msg.reply_text("ᴀɴᴅᴀ ᴛɪᴅᴀᴋ ᴍᴇᴍɪʟɪᴋɪ ᴄᴜᴋᴜᴘ ʜᴀᴋ ᴜɴᴛᴜᴋ ᴍᴇɴɢʜᴀᴘᴜs ꜰᴏᴛᴏ ɢʀᴜᴘ")
        return
    try:
        context.bot.delete_chat_photo(int(chat.id))
        msg.reply_text("ʙᴇʀʜᴀsɪʟ ᴍᴇɴɢʜᴀᴘᴜs ꜰᴏᴛᴏ ᴘʀᴏꜰɪʟ ᴏʙʀᴏʟᴀɴ!")
    except BadRequest as excp:
        msg.reply_text(f"ᴋᴇsᴀʟᴀʜᴀɴ! {excp.message}.")
        return


@bot_admin
@user_admin
def set_desc(update: Update, context: CallbackContext):
    msg = update.effective_message
    chat = update.effective_chat
    user = update.effective_user

    if user_can_changeinfo(chat, user, context.bot.id) is False:
        return msg.reply_text("ᴀɴᴅᴀ ᴋᴇʜɪʟᴀɴɢᴀɴ ʜᴀᴋ ᴜɴᴛᴜᴋ ᴍᴇɴɢᴜʙᴀʜ ɪɴꜰᴏ ᴏʙʀᴏʟᴀɴ!")

    tesc = msg.text.split(None, 1)
    if len(tesc) >= 2:
        desc = tesc[1]
    else:
        return msg.reply_text("ᴍᴇɴʏᴇᴛᴇʟ ᴅᴇsᴋʀɪᴘsɪ ᴋᴏsᴏɴɢ ᴛɪᴅᴀᴋ ᴀᴋᴀɴ ᴍᴇɴɢʜᴀsɪʟᴋᴀɴ ᴀᴘᴀ-ᴀᴘᴀ!")
    try:
        if len(desc) > 255:
            return msg.reply_text("ᴅᴇsᴋʀɪᴘsɪ ʜᴀʀᴜs ᴋᴜʀᴀɴɢ ᴅᴀʀɪ 255 ᴋᴀʀᴀᴋᴛᴇʀ!")
        context.bot.set_chat_description(chat.id, desc)
        msg.reply_text(f"ʙᴇʀʜᴀsɪʟ ᴍᴇᴍᴘᴇʀʙᴀʀᴜɪ ᴅᴇsᴋʀɪᴘsɪ ᴏʙʀᴏʟᴀɴ ᴅɪ {chat.title}!")
    except BadRequest as excp:
        msg.reply_text(f"ᴋᴇsᴀʟᴀʜᴀɴ! {excp.message}.")


@bot_admin
@user_admin
def setchat_title(update: Update, context: CallbackContext):
    chat = update.effective_chat
    msg = update.effective_message
    user = update.effective_user
    args = context.args

    if user_can_changeinfo(chat, user, context.bot.id) is False:
        msg.reply_text("ᴀɴᴅᴀ ᴛɪᴅᴀᴋ ᴍᴇᴍɪʟɪᴋɪ ᴄᴜᴋᴜᴘ ʜᴀᴋ ᴜɴᴛᴜᴋ ᴍᴇɴɢᴜʙᴀʜ ɪɴꜰᴏ ᴏʙʀᴏʟᴀɴ!")
        return

    title = " ".join(args)
    if not title:
        msg.reply_text("ᴍᴀsᴜᴋᴋᴀɴ ʙᴇʙᴇʀᴀᴘᴀ ᴛᴇᴋs ᴜɴᴛᴜᴋ ᴍᴇɴᴇᴛᴀᴘᴋᴀɴ ᴊᴜᴅᴜʟ ʙᴀʀᴜ ᴅɪ ᴏʙʀᴏʟᴀɴ ᴀɴᴅᴀ!")
        return

    try:
        context.bot.set_chat_title(int(chat.id), title)
        msg.reply_text(
            f"ʙᴇʀʜᴀsɪʟ ᴍᴇɴɢᴀᴛᴜʀ <b>{title}</b> sᴇʙᴀɢᴀɪ ᴊᴜᴅᴜʟ ᴏʙʀᴏʟᴀɴ ʙᴀʀᴜ!",
            parse_mode=ParseMode.HTML,
        )
    except BadRequest as excp:
        msg.reply_text(f"ᴋᴇsᴀʟᴀʜᴀɴ! {excp.message}.")
        return


@connection_status
@bot_admin
@can_promote
@user_admin
@loggable
def promote(update: Update, context: CallbackContext) -> str:
    bot = context.bot
    args = context.args

    message = update.effective_message
    chat = update.effective_chat
    user = update.effective_user

    promoter = chat.get_member(user.id)

    if (
        not (promoter.can_promote_members or promoter.status == "creator")
        and user.id not in DRAGONS
    ):
        message.reply_text("ᴀɴᴅᴀ ᴛɪᴅᴀᴋ ᴍᴇᴍɪʟɪᴋɪ ʜᴀᴋ ʏᴀɴɢ ᴅɪᴘᴇʀʟᴜᴋᴀɴ ᴜɴᴛᴜᴋ ᴍᴇʟᴀᴋᴜᴋᴀɴ ɪᴛᴜ!")
        return

    user_id = extract_user(message, args)

    if not user_id:
        message.reply_text(
            "ᴀɴᴅᴀ sᴇᴘᴇʀᴛɪɴʏᴀ ᴛɪᴅᴀᴋ ᴍᴇʀᴜᴊᴜᴋ ᴋᴇ ᴘᴇɴɢɢᴜɴᴀ ᴀᴛᴀᴜ ɪᴅ ʏᴀɴɢ ᴅɪᴛᴇɴᴛᴜᴋᴀɴ sᴀʟᴀʜ..",
        )
        return

    try:
        user_member = chat.get_member(user_id)
    except:
        return

    if user_member.status in ("administrator", "creator"):
        message.reply_text("ʙᴀɢᴀɪᴍᴀɴᴀ sᴀʏᴀ ʙᴇʀᴍᴀᴋsᴜᴅ ᴍᴇᴍᴘʀᴏᴍᴏsɪᴋᴀɴ sᴇsᴇᴏʀᴀɴɢ ʏᴀɴɢ sᴜᴅᴀʜ ᴍᴇɴᴊᴀᴅɪ ᴀᴅᴍɪɴ?")
        return

    if user_id == bot.id:
        message.reply_text("sᴀʏᴀ ᴛɪᴅᴀᴋ ʙɪsᴀ ᴍᴇᴍᴘʀᴏᴍᴏsɪᴋᴀɴ ᴅɪʀɪ sᴀʏᴀ sᴇɴᴅɪʀɪ! ᴅᴀᴘᴀᴛᴋᴀɴ ᴀᴅᴍɪɴ ᴜɴᴛᴜᴋ ᴍᴇʟᴀᴋᴜᴋᴀɴɴʏᴀ ᴜɴᴛᴜᴋ sᴀʏᴀ.")
        return

    # set same perms as bot - bot can't assign higher perms than itself!
    bot_member = chat.get_member(bot.id)

    try:
        bot.promoteChatMember(
            chat.id,
            user_id,
            # can_change_info=bot_member.can_change_info,
            can_post_messages=bot_member.can_post_messages,
            can_edit_messages=bot_member.can_edit_messages,
            can_delete_messages=bot_member.can_delete_messages,
            can_invite_users=bot_member.can_invite_users,
            # can_promote_members=bot_member.can_promote_members,
            can_restrict_members=bot_member.can_restrict_members,
            can_pin_messages=bot_member.can_pin_messages,
        )
    except BadRequest as err:
        if err.message == "User_not_mutual_contact":
            message.reply_text("sᴀʏᴀ ᴛɪᴅᴀᴋ ᴅᴀᴘᴀᴛ ᴍᴇᴍᴘʀᴏᴍᴏsɪᴋᴀɴ sᴇsᴇᴏʀᴀɴɢ ʏᴀɴɢ ᴛɪᴅᴀᴋ ᴀᴅᴀ ᴅᴀʟᴀᴍ ɢʀᴜᴘ.")
        else:
            message.reply_text("ᴛᴇʀᴊᴀᴅɪ ᴋᴇsᴀʟᴀʜᴀɴ sᴀᴀᴛ ᴍᴇᴍᴘʀᴏᴍᴏsɪᴋᴀɴ.")
        return

    bot.sendMessage(
        chat.id,
        f"ʙᴇʀʜᴀsɪʟ ᴅɪᴘʀᴏᴍᴏsɪᴋᴀɴ <b>{user_member.user.first_name or user_id}</b> (<code>{user_id}</code>) in {chat.title}",
        parse_mode=ParseMode.HTML,
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        text="🔽 Demote",
                        callback_data=f"admin_demote_{user_member.user.id}",
                    ),
                    InlineKeyboardButton(
                        text="🔄 AdminCache",
                        callback_data=f"admin_refresh_{user_member.user.id}",
                    ),
                ],
            ],
        ),
    )
    log_message = (
        f"<b>{html.escape(chat.title)}:</b>\n"
        f"#PROMOTED\n"
        f"<b>Admin:</b> {mention_html(user.id, user.first_name)}\n"
        f"<b>User:</b> {mention_html(user_member.user.id, user_member.user.first_name)}"
    )

    return log_message


@connection_status
@bot_admin
@can_promote
@user_admin
@loggable
def fullpromote(update: Update, context: CallbackContext) -> str:
    bot = context.bot
    args = context.args

    message = update.effective_message
    chat = update.effective_chat
    user = update.effective_user

    promoter = chat.get_member(user.id)

    if (
        not (promoter.can_promote_members or promoter.status == "creator")
        and user.id not in DRAGONS
    ):
        message.reply_text("ᴀɴᴅᴀ ᴛɪᴅᴀᴋ ᴍᴇᴍɪʟɪᴋɪ ʜᴀᴋ ʏᴀɴɢ ᴅɪᴘᴇʀʟᴜᴋᴀɴ ᴜɴᴛᴜᴋ ᴍᴇʟᴀᴋᴜᴋᴀɴ ɪᴛᴜ!")
        return

    user_id = extract_user(message, args)

    if not user_id:
        message.reply_text(
            "ᴀɴᴅᴀ sᴇᴘᴇʀᴛɪɴʏᴀ ᴛɪᴅᴀᴋ ᴍᴇʀᴜᴊᴜᴋ ᴋᴇ ᴘᴇɴɢɢᴜɴᴀ ᴀᴛᴀᴜ ɪᴅ ʏᴀɴɢ ᴅɪᴛᴇɴᴛᴜᴋᴀɴ sᴀʟᴀʜ..",
        )
        return

    try:
        user_member = chat.get_member(user_id)
    except:
        return

    if user_member.status in ("administrator", "creator"):
        message.reply_text("ʙᴀɢᴀɪᴍᴀɴᴀ sᴀʏᴀ ʙᴇʀᴍᴀᴋsᴜᴅ ᴍᴇᴍᴘʀᴏᴍᴏsɪᴋᴀɴ sᴇsᴇᴏʀᴀɴɢ ʏᴀɴɢ sᴜᴅᴀʜ ᴍᴇɴᴊᴀᴅɪ ᴀᴅᴍɪɴ?")
        return

    if user_id == bot.id:
        message.reply_text("sᴀʏᴀ ᴛɪᴅᴀᴋ ʙɪsᴀ ᴍᴇᴍᴘʀᴏᴍᴏsɪᴋᴀɴ ᴅɪʀɪ sᴀʏᴀ sᴇɴᴅɪʀɪ! ᴅᴀᴘᴀᴛᴋᴀɴ ᴀᴅᴍɪɴ ᴜɴᴛᴜᴋ ᴍᴇʟᴀᴋᴜᴋᴀɴɴʏᴀ ᴜɴᴛᴜᴋ sᴀʏᴀ.")
        return

    # set same perms as bot - bot can't assign higher perms than itself!
    bot_member = chat.get_member(bot.id)

    try:
        bot.promoteChatMember(
            chat.id,
            user_id,
            can_change_info=bot_member.can_change_info,
            can_post_messages=bot_member.can_post_messages,
            can_edit_messages=bot_member.can_edit_messages,
            can_delete_messages=bot_member.can_delete_messages,
            can_invite_users=bot_member.can_invite_users,
            can_promote_members=bot_member.can_promote_members,
            can_restrict_members=bot_member.can_restrict_members,
            can_pin_messages=bot_member.can_pin_messages,
            can_manage_voice_chats=bot_member.can_manage_voice_chats,
        )
    except BadRequest as err:
        if err.message == "User_not_mutual_contact":
            message.reply_text("I can't promote someone who isn't in the group.")
        else:
            message.reply_text("An error occured while promoting.")
        return

    bot.sendMessage(
        chat.id,
        f"Sucessfully promoted <b>{user_member.user.first_name or user_id}</b> (<code>{user_id}</code>) with full rights in {chat.title}!",
        parse_mode=ParseMode.HTML,
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        text="🔽 Demote",
                        callback_data=f"admin_demote_{user_member.user.id}",
                    ),
                    InlineKeyboardButton(
                        text="🔄 AdminCache",
                        callback_data=f"admin_refresh_{user_member.user.id}",
                    ),
                ],
            ],
        ),
    )

    log_message = (
        f"<b>{html.escape(chat.title)}:</b>\n"
        f"#FULLPROMOTED\n"
        f"<b>Admin:</b> {mention_html(user.id, user.first_name)}\n"
        f"<b>User:</b> {mention_html(user_member.user.id, user_member.user.first_name)}"
    )

    return log_message


@connection_status
@bot_admin
@can_promote
@user_admin
@loggable
def lowpromote(update: Update, context: CallbackContext) -> str:
    bot = context.bot
    args = context.args

    message = update.effective_message
    chat = update.effective_chat
    user = update.effective_user

    promoter = chat.get_member(user.id)

    if (
        not (promoter.can_promote_members or promoter.status == "creator")
        and user.id not in DRAGONS
    ):
        message.reply_text("ᴀɴᴅᴀ ᴛɪᴅᴀᴋ ᴍᴇᴍɪʟɪᴋɪ ʜᴀᴋ ʏᴀɴɢ ᴅɪᴘᴇʀʟᴜᴋᴀɴ ᴜɴᴛᴜᴋ ᴍᴇʟᴀᴋᴜᴋᴀɴ ɪᴛᴜ!")
        return

    user_id = extract_user(message, args)

    if not user_id:
        message.reply_text(
            "ᴀɴᴅᴀ sᴇᴘᴇʀᴛɪɴʏᴀ ᴛɪᴅᴀᴋ ᴍᴇʀᴜᴊᴜᴋ ᴋᴇ ᴘᴇɴɢɢᴜɴᴀ ᴀᴛᴀᴜ ɪᴅ ʏᴀɴɢ ᴅɪᴛᴇɴᴛᴜᴋᴀɴ sᴀʟᴀʜ..",
        )
        return

    try:
        user_member = chat.get_member(user_id)
    except:
        return

    if user_member.status in ("administrator", "creator"):
        message.reply_text("ʙᴀɢᴀɪᴍᴀɴᴀ sᴀʏᴀ ʙᴇʀᴍᴀᴋsᴜᴅ ᴍᴇᴍᴘʀᴏᴍᴏsɪᴋᴀɴ sᴇsᴇᴏʀᴀɴɢ ʏᴀɴɢ sᴜᴅᴀʜ ᴍᴇɴᴊᴀᴅɪ ᴀᴅᴍɪɴ?")
        return

    if user_id == bot.id:
        message.reply_text("sᴀʏᴀ ᴛɪᴅᴀᴋ ʙɪsᴀ ᴍᴇᴍᴘʀᴏᴍᴏsɪᴋᴀɴ ᴅɪʀɪ sᴀʏᴀ sᴇɴᴅɪʀɪ! ᴅᴀᴘᴀᴛᴋᴀɴ ᴀᴅᴍɪɴ ᴜɴᴛᴜᴋ ᴍᴇʟᴀᴋᴜᴋᴀɴɴʏᴀ ᴜɴᴛᴜᴋ sᴀʏᴀ.")
        return

    # set same perms as bot - bot can't assign higher perms than itself!
    bot_member = chat.get_member(bot.id)

    try:
        bot.promoteChatMember(
            chat.id,
            user_id,
            can_delete_messages=bot_member.can_delete_messages,
            can_invite_users=bot_member.can_invite_users,
            can_pin_messages=bot_member.can_pin_messages,
        )
    except BadRequest as err:
        if err.message == "User_not_mutual_contact":
            message.reply_text("sᴀʏᴀ ᴛɪᴅᴀᴋ ᴅᴀᴘᴀᴛ ᴍᴇᴍᴘʀᴏᴍᴏsɪᴋᴀɴ sᴇsᴇᴏʀᴀɴɢ ʏᴀɴɢ ᴛɪᴅᴀᴋ ᴀᴅᴀ ᴅᴀʟᴀᴍ ɢʀᴜᴘ.")
        else:
            message.reply_text("ᴛᴇʀᴊᴀᴅɪ ᴋᴇsᴀʟᴀʜᴀɴ sᴀᴀᴛ ᴍᴇᴍᴘʀᴏᴍᴏsɪᴋᴀɴ.")
        return

    bot.sendMessage(
        chat.id,
        f"ʙᴇʀʜᴀsɪʟ ᴅɪᴘʀᴏᴍᴏsɪᴋᴀɴ <b>{user_member.user.first_name or user_id}</b> ᴅᴇɴɢᴀɴ ʜᴀᴋ ʀᴇɴᴅᴀʜ!",
        parse_mode=ParseMode.HTML,
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        text="Demote",
                        callback_data=f"admin_demote_{user_member.user.id}",
                    ),
                    InlineKeyboardButton(
                        text="AdminCache",
                        callback_data=f"admin_refresh_{user_member.user.id}",
                    ),
                ],
            ],
        ),
    )

    log_message = (
        f"<b>{html.escape(chat.title)}:</b>\n"
        f"#LOWPROMOTED\n"
        f"<b>Admin:</b> {mention_html(user.id, user.first_name)}\n"
        f"<b>User:</b> {mention_html(user_member.user.id, user_member.user.first_name)}"
    )

    return log_message

disnin ==================================


@connection_status
@bot_admin
@can_promote
@user_admin
@loggable
def demote(update: Update, context: CallbackContext) -> Optional[str]:
    bot = context.bot
    args = context.args

    chat = update.effective_chat
    message = update.effective_message
    user = update.effective_user

    user_id = extract_user(message, args)
    if not user_id:
        message.reply_text(
            "ᴀɴᴅᴀ sᴇᴘᴇʀᴛɪɴʏᴀ ᴛɪᴅᴀᴋ ᴍᴇʀᴜᴊᴜᴋ ᴋᴇ ᴘᴇɴɢɢᴜɴᴀ ᴀᴛᴀᴜ ɪᴅ ʏᴀɴɢ ᴅɪᴛᴇɴᴛᴜᴋᴀɴ ᴛɪᴅᴀᴋ ʙᴇɴᴀʀ.."
        )
        return

    try:
        user_member = chat.get_member(user_id)
    except:
        return

    if user_member.status == "creator":
        message.reply_text("ᴏʀᴀɴɢ ɪɴɪ ᴍᴇɴᴄɪᴘᴛᴀᴋᴀɴ ᴏʙʀᴏʟᴀɴ, ʙᴀɢᴀɪᴍᴀɴᴀ sᴀʏᴀ ᴍᴇɴᴜʀᴜɴᴋᴀɴɴʏᴀ?")
        return

    if user_member.status != "administrator":
        message.reply_text("ᴛɪᴅᴀᴋ ᴅᴀᴘᴀᴛ ᴍᴇɴᴜʀᴜɴᴋᴀɴ ᴀᴘᴀ ʏᴀɴɢ ᴛɪᴅᴀᴋ ᴅɪᴘʀᴏᴍᴏsɪᴋᴀɴ!")
        return

    if user_id == bot.id:
        message.reply_text("sᴀʏᴀ ᴛɪᴅᴀᴋ ʙɪsᴀ ᴍᴇɴᴜʀᴜɴᴋᴀɴ ᴅɪʀɪ sᴀʏᴀ sᴇɴᴅɪʀɪ! ᴅᴀᴘᴀᴛᴋᴀɴ ᴀᴅᴍɪɴ ᴜɴᴛᴜᴋ ᴍᴇʟᴀᴋᴜᴋᴀɴɴʏᴀ ᴜɴᴛᴜᴋ sᴀʏᴀ.")
        return

    try:
        bot.promoteChatMember(
            chat.id,
            user_id,
            can_change_info=False,
            can_post_messages=False,
            can_edit_messages=False,
            can_delete_messages=False,
            can_invite_users=False,
            can_restrict_members=False,
            can_pin_messages=False,
            can_promote_members=False,
            can_manage_voice_chats=False,
        )

        bot.sendMessage(
            chat.id,
            f"<b>{user_member.user.first_name or user_id or None}</b> was demoted by <b>{message.from_user.first_name or None}</b> in <b>{chat.title or None}</b>",
            parse_mode=ParseMode.HTML,
        )

        log_message = (
            f"<b>{html.escape(chat.title)}:</b>\n"
            f"#DEMOTED\n"
            f"<b>Admin:</b> {mention_html(user.id, user.first_name)}\n"
            f"<b>User:</b> {mention_html(user_member.user.id, user_member.user.first_name)}"
        )

        return log_message
    except BadRequest:
        message.reply_text(
            "ᴛɪᴅᴀᴋ ᴅᴀᴘᴀᴛ ᴍᴇɴᴜʀᴜɴᴋᴀɴ. sᴀʏᴀ ᴍᴜɴɢᴋɪɴ ʙᴜᴋᴀɴ ᴀᴅᴍɪɴ, ᴀᴛᴀᴜ sᴛᴀᴛᴜs ᴀᴅᴍɪɴ ᴅɪᴛᴜɴᴊᴜᴋ ᴏʟᴇʜ ᴏʀᴀɴɢ ʟᴀɪɴ"
            " ᴘᴇɴɢɢᴜɴᴀ, ᴊᴀᴅɪ sᴀʏᴀ ᴛɪᴅᴀᴋ ʙɪsᴀ ʙᴇʀᴛɪɴᴅᴀᴋ ᴀᴛᴀs ᴍᴇʀᴇᴋᴀ!"
        )
        return


@user_admin
def refresh_admin(update, _):
    try:
        ADMIN_CACHE.pop(update.effective_chat.id)
    except KeyError:
        pass

    update.effective_message.reply_text("ᴄᴀᴄʜᴇ ᴀᴅᴍɪɴ ᴅɪsᴇɢᴀʀᴋᴀɴ!")


@connection_status
@bot_admin
@can_promote
@user_admin
def set_title(update: Update, context: CallbackContext):
    bot = context.bot
    args = context.args

    chat = update.effective_chat
    message = update.effective_message

    user_id, title = extract_user_and_text(message, args)
    try:
        user_member = chat.get_member(user_id)
    except:
        return

    if not user_id:
        message.reply_text(
            "ᴀɴᴅᴀ sᴇᴘᴇʀᴛɪɴʏᴀ ᴛɪᴅᴀᴋ ᴍᴇʀᴜᴊᴜᴋ ᴋᴇ ᴘᴇɴɢɢᴜɴᴀ ᴀᴛᴀᴜ ɪᴅ ʏᴀɴɢ ᴅɪᴛᴇɴᴛᴜᴋᴀɴ ᴛɪᴅᴀᴋ ʙᴇɴᴀʀ..",
        )
        return

    if user_member.status == "creator":
        message.reply_text(
            "ᴏʀᴀɴɢ ɪɴɪ ᴍᴇɴᴄɪᴘᴛᴀᴋᴀɴ ᴏʙʀᴏʟᴀɴ, ʙᴀɢᴀɪᴍᴀɴᴀ sᴀʏᴀ ʙɪsᴀ ᴍᴇɴɢᴀᴛᴜʀ ᴊᴜᴅᴜʟ ᴋʜᴜsᴜs ᴜɴᴛᴜᴋɴʏᴀ?",
        )
        return

    if user_member.status != "administrator":
        message.reply_text(
            "ᴛɪᴅᴀᴋ ᴅᴀᴘᴀᴛ ᴍᴇɴʏᴇᴛᴇʟ ᴊᴜᴅᴜʟ ᴜɴᴛᴜᴋ ɴᴏɴ-ᴀᴅᴍɪɴ!\nᴘʀᴏᴍᴏsɪᴋᴀɴ ᴍᴇʀᴇᴋᴀ ᴛᴇʀʟᴇʙɪʜ ᴅᴀʜᴜʟᴜ ᴜɴᴛᴜᴋ ᴍᴇɴʏᴇᴛᴇʟ ᴊᴜᴅᴜʟ ᴋʜᴜsᴜs!",
        )
        return

    if user_id == bot.id:
        message.reply_text(
            "sᴀʏᴀ ᴛɪᴅᴀᴋ ᴅᴀᴘᴀᴛ ᴍᴇɴᴇᴛᴀᴘᴋᴀɴ ᴊᴜᴅᴜʟ sᴀʏᴀ sᴇɴᴅɪʀɪ! ᴅᴀᴘᴀᴛᴋᴀɴ ᴏʀᴀɴɢ ʏᴀɴɢ ᴍᴇɴᴊᴀᴅɪᴋᴀɴ sᴀʏᴀ ᴀᴅᴍɪɴ ᴜɴᴛᴜᴋ ᴍᴇʟᴀᴋᴜᴋᴀɴɴʏᴀ ᴜɴᴛᴜᴋ sᴀʏᴀ.",
        )
        return

    if not title:
        message.reply_text("ᴍᴇɴɢᴀᴛᴜʀ ᴊᴜᴅᴜʟ ᴋᴏsᴏɴɢ ᴛɪᴅᴀᴋ ᴍᴇʟᴀᴋᴜᴋᴀɴ ᴀᴘᴀ-ᴀᴘᴀ!")
        return

    if len(title) > 16:
        message.reply_text(
            "ᴘᴀɴᴊᴀɴɢ ᴊᴜᴅᴜʟ ʟᴇʙɪʜ ᴅᴀʀɪ 16 ᴋᴀʀᴀᴋᴛᴇʀ.\nᴍᴇᴍᴏᴛᴏɴɢɴʏᴀ ᴍᴇɴᴊᴀᴅɪ 16 ᴋᴀʀᴀᴋᴛᴇʀ.",
        )

    try:
        bot.setChatAdministratorCustomTitle(chat.id, user_id, title)
    except BadRequest:
        message.reply_text(
            "ᴇɪᴛʜᴇʀ ᴛʜᴇʏ ᴀʀᴇɴ'ᴛ ᴘʀᴏᴍᴏᴛᴇᴅ ʙʏ ᴍᴇ ᴏʀ ʏᴏᴜ sᴇᴛ ᴀ ᴛɪᴛʟᴇ ᴛᴇxᴛ ᴛʜᴀᴛ ɪs ɪᴍᴘᴏssɪʙʟᴇ ᴛᴏ sᴇᴛ."
        )
        return

    bot.sendMessage(
        chat.id,
        f"ʙᴇʀʜᴀsɪʟ ᴍᴇɴᴇᴛᴀᴘᴋᴀɴ ᴊᴜᴅᴜʟ ᴜɴᴛᴜᴋ <code>{user_member.user.first_name or user_id}</code> "
        f"to <code>{html.escape(title[:16])}</code>!",
        parse_mode=ParseMode.HTML,
    )


@bot_admin
@can_pin
@user_admin
@loggable
def pin(update: Update, context: CallbackContext) -> str:
    bot = context.bot
    args = context.args

    user = update.effective_user
    chat = update.effective_chat

    is_group = chat.type not in ("private", "channel")
    prev_message = update.effective_message.reply_to_message

    is_silent = True
    if len(args) >= 1:
        is_silent = args[0].lower() in ("notify", "loud", "violent")

    if prev_message and is_group:
        try:
            bot.pinChatMessage(
                chat.id,
                prev_message.message_id,
                disable_notification=is_silent,
            )
        except BadRequest as excp:
            if excp.message != "Chat_not_modified":
                raise
        log_message = (
            f"<b>{html.escape(chat.title)}:</b>\n"
            f"#PINNED\n"
            f"<b>Admin:</b> {mention_html(user.id, html.escape(user.first_name))}"
        )

        return log_message


@bot_admin
@can_pin
@user_admin
@loggable
def unpin(update: Update, context: CallbackContext) -> str:
    bot = context.bot
    chat = update.effective_chat
    user = update.effective_user

    try:
        bot.unpinChatMessage(chat.id)
    except BadRequest as excp:
        if excp.message == "Chat_not_modified":
            pass
        else:
            raise

    log_message = (
        f"<b>{html.escape(chat.title)}:</b>\n"
        f"#UNPINNED\n"
        f"<b>Admin:</b> {mention_html(user.id, html.escape(user.first_name))}"
    )

    return log_message


@bot_admin
def pinned(update: Update, context: CallbackContext) -> str:
    bot = context.bot
    msg = update.effective_message
    msg_id = (
        update.effective_message.reply_to_message.message_id
        if update.effective_message.reply_to_message
        else update.effective_message.message_id
    )

    chat = bot.getChat(chat_id=msg.chat.id)
    if chat.pinned_message:
        pinned_id = chat.pinned_message.message_id
        if msg.chat.username:
            link_chat_id = msg.chat.username
            message_link = f"https://t.me/{link_chat_id}/{pinned_id}"
        elif (str(msg.chat.id)).startswith("-100"):
            link_chat_id = (str(msg.chat.id)).replace("-100", "")
            message_link = f"https://t.me/c/{link_chat_id}/{pinned_id}"

        msg.reply_text(
            f"Pinned on {html.escape(chat.title)}.",
            reply_to_message_id=msg_id,
            parse_mode=ParseMode.HTML,
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            text="Pinned Message",
                            url=f"https://t.me/{link_chat_id}/{pinned_id}",
                        )
                    ]
                ]
            ),
        )

    else:
        msg.reply_text(
            f"There is no pinned message in <b>{html.escape(chat.title)}!</b>",
            parse_mode=ParseMode.HTML,
        )


@bot_admin
@user_admin
@connection_status
def invite(update: Update, context: CallbackContext):
    bot = context.bot
    chat = update.effective_chat

    if chat.username:
        update.effective_message.reply_text(f"https://t.me/{chat.username}")
    elif chat.type in [chat.SUPERGROUP, chat.CHANNEL]:
        bot_member = chat.get_member(bot.id)
        if bot_member.can_invite_users:
            invitelink = bot.exportChatInviteLink(chat.id)
            update.effective_message.reply_text(invitelink)
        else:
            update.effective_message.reply_text(
                "sᴀʏᴀ ᴛɪᴅᴀᴋ ᴍᴇᴍɪʟɪᴋɪ ᴀᴋsᴇs ᴋᴇ ᴛᴀᴜᴛᴀɴ ᴜɴᴅᴀɴɢᴀɴ, ᴄᴏʙᴀ ᴜʙᴀʜ ɪᴢɪɴ sᴀʏᴀ!",
            )
    else:
        update.effective_message.reply_text(
            "sᴀʏᴀ ʜᴀɴʏᴀ ʙɪsᴀ ᴍᴇᴍʙᴇʀɪ ᴀɴᴅᴀ ᴛᴀᴜᴛᴀɴ ᴜɴᴅᴀɴɢᴀɴ ᴜɴᴛᴜᴋ ɢʀᴜᴘ ᴅᴀɴ sᴀʟᴜʀᴀɴ sᴜᴘᴇʀ, ᴍᴀᴀꜰ!",
        )


@connection_status
def adminlist(update, context):
    chat = update.effective_chat  ## type: Optional[Chat] -> unused variable
    user = update.effective_user  # type: Optional[User]
    args = context.args  # -> unused variable
    bot = context.bot

    if update.effective_message.chat.type == "private":
        send_message(update.effective_message, "ᴘᴇʀɪɴᴛᴀʜ ɪɴɪ ʜᴀɴʏᴀ ʙᴇʀꜰᴜɴɢsɪ ᴅɪ ɢʀᴜᴘ.")
        return

    update.effective_chat
    chat_id = update.effective_chat.id
    chat_name = update.effective_message.chat.title  # -> unused variable

    try:
        msg = update.effective_message.reply_text(
            "ᴍᴇɴɢᴀᴍʙɪʟ ᴀᴅᴍɪɴ ɢʀᴜᴘ...",
            parse_mode=ParseMode.HTML,
        )
    except BadRequest:
        msg = update.effective_message.reply_text(
            "ᴍᴇɴɢᴀᴍʙɪʟ ᴀᴅᴍɪɴ ɢʀᴜᴘ...",
            quote=False,
            parse_mode=ParseMode.HTML,
        )

    administrators = bot.getChatAdministrators(chat_id)
    text = f"ᴀᴅᴍɪɴ ᴅɪ <b>{html.escape(update.effective_chat.title)}</b>:"

    for admin in administrators:
        user = admin.user
        status = admin.status
        custom_title = admin.custom_title

        if user.first_name == "":
            name = "☠ ᴀᴋᴜɴ ʏᴀɴɢ ᴅɪʜᴀᴘᴜs"
        else:
            name = "{}".format(
                mention_html(
                    user.id,
                    html.escape(f"{user.first_name} " + ((user.last_name or ""))),
                )
            )

            ##if user.is_bot:
            # bot_admin_list.append(name)
            # administrators.remove(admin)
            # continue

        #   continue

        # if user.username:
        #    name = escape_markdown("@" + user.username)
        if status == "creator":
            text += "\n\n 🌐 ᴄʀᴇᴀᴛᴏʀ:"
            text += f" {name}\n"

            if custom_title:
                text += f"<code> ┗━ {html.escape(custom_title)}</code>\n"

    text += "\n 🎖 ᴀᴅᴍɪɴɪsᴛʀᴀᴛᴏʀs"

    custom_admin_list = {}
    normal_admin_list = []

    for admin in administrators:
        user = admin.user
        status = admin.status
        custom_title = admin.custom_title

        if user.first_name == "":
            name = "☠ ᴀᴋᴜɴ ʏᴀɴɢ ᴅɪʜᴀᴘᴜs"
        else:
            name = "{}".format(
                mention_html(
                    user.id,
                    html.escape(f"{user.first_name} " + ((user.last_name or ""))),
                )
            )

        if status == "administrator":
            if custom_title:
                try:
                    custom_admin_list[custom_title].append(name)
                except KeyError:
                    custom_admin_list[custom_title] = [name]
            else:
                normal_admin_list.append(name)

    for admin in normal_admin_list:
        text += f"\n<code> • </code>{admin}"

    for admin_group in custom_admin_list.copy():
        if len(custom_admin_list[admin_group]) == 1:
            text += f"\n<code> • </code>{custom_admin_list[admin_group][0]} | <code>{html.escape(admin_group)}</code>"

            custom_admin_list.pop(admin_group)

    text += "\n"
    for admin_group, value in custom_admin_list.items():
        text += f"\n🚨 <code>{admin_group}</code>"
        for admin in value:
            text += f"\n<code> • </code>{admin}"
        text += "\n"

        # text += "\n🤖 Bots:"
        # for each_bot in bot_admin_list:
        # text += "\n<code> • </code>{}".format(each_bot)

    try:
        msg.edit_text(text, parse_mode=ParseMode.HTML)
    except BadRequest:  # if original message is deleted
        return


# if user.is_bot:

# bot_admin_list.append(name)

#  administrators.remove(admin)

# text += "Bottos:"

# for each_bot in bot_admin_list:


@user_admin
@user_can_promote
def promote_button(update: Update, context: CallbackContext):
    query = update.callback_query
    user = update.effective_user
    chat = update.effective_chat
    bot = context.bot

    mode = query.data.split("_")[1]
    try:
        if is_user_admin(chat, user.id):
            if mode == "demote":
                user_id = query.data.split("_")[2]
                user_member = chat.get_member(user_id)
                bot.promoteChatMember(
                    chat.id,
                    user_id,
                    can_change_info=False,
                    can_post_messages=False,
                    can_edit_messages=False,
                    can_delete_messages=False,
                    can_invite_users=False,
                    can_restrict_members=False,
                    can_pin_messages=False,
                    can_promote_members=False,
                    # can_manage_voice_chats=False
                )
                query.message.delete()
                bot.answer_callback_query(
                    query.id,
                    f"ʙᴇʀʜᴀsɪʟ ᴅɪᴛᴜʀᴜɴᴋᴀɴ {user_member.user.first_name or user_id}",
                    show_alert=True,
                )
            elif mode == "refresh":
                try:
                    ADMIN_CACHE.pop(update.effective_chat.id)
                except KeyError:
                    pass
                bot.answer_callback_query(query.id, "ᴄᴀᴄʜᴇ ᴀᴅᴍɪɴ ᴅɪsᴇɢᴀʀᴋᴀɴ!")
    except BadRequest as excp:
        if excp.message not in [
            "Message is not mod",
            "User_id_invalid",
            "Message Deleted",
        ]:
            LOGGER.exception("ᴘᴇɴɢᴇᴄᴜᴀʟɪᴀɴ ᴅᴀʟᴀᴍ ᴛᴏᴍʙᴏʟ ᴘʀᴏᴍᴏsɪ. %s", str(query.data))


__help__ = """
ᴅɪ sɪɴɪ ᴀᴅᴀʟᴀʜ ʙᴀɴᴛᴜᴀɴ ᴜɴᴛᴜᴋ ᴍᴏᴅᴜʟ *ᴀᴅᴍɪɴ* :

*ᴀᴅᴍɪɴ ᴘᴇʀɪɴᴛᴀʜ*:

✥ ᴘɪɴs ❉

 • /pin: `ᴅɪᴀᴍ-ᴅɪᴀᴍ ᴍᴇɴʏᴇᴍᴀᴛᴋᴀɴ ᴘᴇsᴀɴ ʏᴀɴɢ ᴅɪʙᴀʟᴀs ` 

 • /unpin: `ᴍᴇʟᴇᴘᴀs ᴘɪɴ ᴘᴇsᴀɴ ʏᴀɴɢ sᴀᴀᴛ ɪɴɪ ᴅɪsᴇᴍᴀᴛᴋᴀɴ `

 • /pinned: `ᴜɴᴛᴜᴋ ᴍᴇɴᴅᴀᴘᴀᴛᴋᴀɴ ᴘᴇsᴀɴ ʏᴀɴɢ ᴅɪsᴇᴍᴀᴛᴋᴀɴ sᴀᴀᴛ ɪɴɪ `

 • /unpinall: `ᴜɴᴛᴜᴋ ᴍᴇʟᴇᴘᴀs ᴘɪɴ sᴇᴍᴜᴀ ᴘᴇsᴀɴ ᴅᴀʟᴀᴍ ᴏʙʀᴏʟᴀɴ `
 

❉ ᴘʀᴏᴍᴏᴛᴇ ᴀɴᴅ ᴛɪᴛʟᴇs ❉:

 • /promote: `ᴍᴇᴍᴘʀᴏᴍᴏsɪᴋᴀɴ ᴘᴇɴɢɢᴜɴᴀ ʏᴀɴɢ ᴅɪʙᴀʟᴀs (ᴅᴀᴘᴀᴛ ᴅɪɢᴜɴᴀᴋᴀɴ sᴇʙᴀɢᴀɪ ᴘʀᴏᴍᴏsɪ ᴘᴇɴᴜʜ ᴀᴛᴀᴜ ᴘʀᴏᴍᴏsɪ ʀᴇɴᴅᴀʜ)`

 • /demote: `ᴍᴇɴᴜʀᴜɴᴋᴀɴ ᴘᴇɴɢɢᴜɴᴀ ʏᴀɴɢ ᴅɪʙᴀʟᴀs `

 • /title <ᴛɪᴛʟᴇ ᴅɪsɪɴɪ>: `ᴍᴇɴᴇᴛᴀᴘᴋᴀɴ ᴊᴜᴅᴜʟ ᴋʜᴜsᴜs ᴜɴᴛᴜᴋ ᴀᴅᴍɪɴ ʏᴀɴɢ ᴅɪᴘʀᴏᴍᴏsɪᴋᴀɴ ʙᴏᴛ `

 • /admincache:  `ᴘᴀᴋsᴀ ᴍᴇɴʏᴇɢᴀʀᴋᴀɴ ᴅᴀꜰᴛᴀʀ ᴀᴅᴍɪɴ`

❉ ᴏᴛʜᴇʀs :❉

 • /setgtitle <ᴛɪᴛʟᴇ ʙᴀʀᴜ>: `ᴍᴇɴɢᴀᴛᴜʀ ᴊᴜᴅᴜʟ ᴏʙʀᴏʟᴀɴ`
 
 • /setdesc <ᴋᴇᴛᴇʀᴀɴɢᴀɴ>: `ᴍᴇɴɢᴀᴛᴜʀ ᴅᴇsᴋʀɪᴘsɪ ᴏʙʀᴏʟᴀɴ`
 
 • /setsticker <ᴍᴇᴍʙᴀʟᴀs sᴛɪᴋᴇʀ>: ` sᴇᴛ ᴘᴀᴋᴇᴛ sᴛɪᴋᴇʀ ᴅᴀʟᴀᴍ sᴜᴘᴇʀɢʀᴜᴘ`
 
 • /setgpic <ᴍᴇᴍʙᴀʟᴀs ɢᴀᴍʙᴀʀ>: `sᴇᴛ ꜰᴏᴛᴏ ᴘʀᴏꜰɪʟ ɢʀᴜᴘ `
 
 • /delgpic: `ᴍᴇɴɢʜᴀᴘᴜs ꜰᴏᴛᴏ ᴘʀᴏꜰɪʟ ɢʀᴜᴘ `
 
 • /admins: `ᴍᴇɴᴜɴᴊᴜᴋᴋᴀɴ ᴅᴀꜰᴛᴀʀ ᴀᴅᴍɪɴ ᴅɪ ᴏʙʀᴏʟᴀɴ`
 
 • /invitelink: `ᴍᴇɴᴅᴀᴘᴀᴛ ᴛᴀᴜᴛᴀɴ ᴜɴᴅᴀɴɢᴀɴ ᴅᴀʀɪ ᴏʙʀᴏʟᴀɴ ɪᴛᴜ `

*ᴍᴏᴅᴇʀᴀᴛɪᴏɴ*:

❉ ʟᴀʀᴀɴɢᴀɴ ᴅᴀɴ ᴛᴇɴᴅᴀɴɢᴀɴ: ❉

 • /ban <userhandle>: `ᴍᴇʟᴀʀᴀɴɢ ᴘᴇɴɢɢᴜɴᴀ (ᴠɪᴀ ʜᴀɴᴅʟᴇ, ᴏʀ ʀᴇᴘʟʏ`)

 • /sban <userhandle>: `ᴅɪᴀᴍ-ᴅɪᴀᴍ ᴍᴇʟᴀʀᴀɴɢ ᴘᴇɴɢɢᴜɴᴀ ʟᴀʟᴜ ᴍᴇɴɢʜᴀᴘᴜs ᴘᴇʀɪɴᴛᴀʜ + ᴍᴇᴍʙᴀʟᴀs ᴘᴇsᴀɴ ᴅᴀɴ ᴛɪᴅᴀᴋ ᴍᴇᴍʙᴀʟᴀs (ᴠɪᴀ ʜᴀɴᴅʟᴇ, ᴏʀ ʀᴇᴘʟʏ)`

 • /dban <messagereplied>: `ᴅɪᴀᴍ-ᴅɪᴀᴍ ᴍᴇʟᴀʀᴀɴɢ ᴘᴇɴɢɢᴜɴᴀ ᴅᴀɴ ᴍᴇɴɢʜᴀᴘᴜs ᴛᴀʀɢᴇᴛ ʏᴀɴɢ ᴍᴇᴍʙᴀʟᴀs ᴘᴇsᴀɴ

 • /tban <userhandle> x(m/h/d): `ᴍᴇʟᴀʀᴀɴɢ ᴘᴇɴɢɢᴜɴᴀ ᴜɴᴛᴜᴋ x ᴡᴀᴋᴛᴜ, (ᴠɪᴀ ʜᴀɴᴅʟᴇ, ᴏʀ ʀᴇᴘʟʏ) ᴍ = ᴍɪɴᴜᴛᴇs, ʜ = ʜᴏᴜʀs, ᴅ = ᴅᴀʏs

 • /unban <userhandle>: `ᴍᴇᴍʙᴀᴛᴀʟᴋᴀɴ ᴘᴇᴍʙʟᴏᴋɪʀᴀɴ ᴘᴇɴɢɢᴜɴᴀ (ᴠɪᴀ ʜᴀɴᴅʟᴇ, ᴏʀ ʀᴇᴘʟʏ)`

 • /punch or kick <userhandle>: `ᴍᴇɴɪɴᴊᴜ ᴘᴇɴɢɢᴜɴᴀ ᴋᴇʟᴜᴀʀ ᴅᴀʀɪ ɢʀᴜᴘ (ᴠɪᴀ ʜᴀɴᴅʟᴇ, ᴏʀ ʀᴇᴘʟʏ)`

❉ ᴍᴜᴛɪɴɢ: ❉

 • /mute <userhandle>: `ᴍᴇᴍʙᴜɴɢᴋᴀᴍ ᴘᴇɴɢɢᴜɴᴀ ᴊᴜɢᴀ ᴅᴀᴘᴀᴛ ᴅɪɢᴜɴᴀᴋᴀɴ sᴇʙᴀɢᴀɪ ʙᴀʟᴀsᴀɴ, ᴍᴇɴᴏɴᴀᴋᴛɪꜰᴋᴀɴ ᴘᴇɴɢɢᴜɴᴀ ʏᴀɴɢ ᴅɪʙᴀʟᴀs`

 • /tmute <userhandle> x(m/h/d): 'ᴍᴇᴍʙᴜɴɢᴋᴀᴍ ᴘᴇɴɢɢᴜɴᴀ ᴜɴᴛᴜᴋ x ᴡᴀᴋᴛᴜ, (ᴠɪᴀ ʜᴀɴᴅʟᴇ, ᴏʀ ʀᴇᴘʟʏ). ᴍ = minutes, ʜ = ʜᴏᴜʀs, ᴅ = ᴅᴀʏs'

 • /unmute <userhandle>: `ᴍᴇᴍʙᴜɴʏɪᴋᴀɴ sᴜᴀʀᴀ ᴘᴇɴɢɢᴜɴᴀ ᴊᴜɢᴀ ᴅᴀᴘᴀᴛ ᴅɪɢᴜɴᴀᴋᴀɴ sᴇʙᴀɢᴀɪ ʙᴀʟᴀsᴀɴ ᴜɴᴛᴜᴋ ᴍᴇɴᴏɴᴀᴋᴛɪꜰᴋᴀɴ ᴘᴇɴɢɢᴜɴᴀ ʏᴀɴɢ ᴅɪʙᴀʟᴀs `

*ʟᴏɢɢɪɴɢ*:

 • /logchannel: ᴅᴀᴘᴀᴛᴋᴀɴ ɪɴꜰᴏ sᴀʟᴜʀᴀɴ ʟᴏɢ

 • /setlog: ᴀᴛᴜʀ sᴀʟᴜʀᴀɴ ʟᴏɢ

 • /unsetlog: ʜᴀᴘᴜs sᴀʟᴜʀᴀɴ ʟᴏɢ

✥ ʜᴏᴡ ᴛᴏ sᴇᴛᴜᴘ:

 • ᴛᴀᴍʙᴀʜᴋᴀɴ sᴀʟᴜʀᴀɴ ʙᴏᴛ ᴅᴇɴɢᴀɴ ɪᴢɪɴ ᴀᴅᴍɪɴ

 • ᴋɪʀɪᴍ /sᴇᴛʟᴏɢ ᴘᴇʀɪɴᴛᴀʜ ᴅɪ sᴀʟᴜʀᴀɴ

 • ғᴏʀᴡᴀʀᴅ ᴛʜᴀᴛ ᴄʜᴀɴɴᴇʟ ᴍᴇssᴀɢᴇ ᴛᴏ ᴛʜᴇ ɢʀᴏᴜᴘ ʏᴏᴜ ᴡᴀɴᴛ ᴛᴏ sᴇᴛᴜᴘ ʟᴏɢɢɪɴɢ ғᴏʀ, ᴛʜᴇ sᴀᴍᴇ ᴄʜᴀɴɴᴇʟ ᴍᴇssᴀɢᴇ ᴄᴀɴ ʙᴇ ғᴏʀᴡᴀʀᴅᴇᴅ ᴛᴏ ᴍᴜʟᴛɪᴘʟᴇ ɢʀᴏᴜᴘs ᴀᴛ ᴏɴᴄᴇ ᴀs ᴡᴇʟʟ

✥ ʀᴜʟᴇs:

 • /rules: `ɢᴇᴛ ᴛʜᴇ ʀᴜʟᴇs ғᴏʀ ᴛʜɪs ᴄʜᴀᴛ`
 
 • /setrules <ʏᴏᴜʀ ʀᴜʟᴇs ʜᴇʀᴇ>: `sᴇᴛ ᴛʜᴇ ʀᴜʟᴇs ғᴏʀ ᴛʜɪs ᴄʜᴀᴛ`
 
 • /clearrules: `ᴄʟᴇᴀʀ ᴛʜᴇ ʀᴜʟᴇs ғᴏʀ ᴛʜɪs ᴄʜᴀᴛ `
 
"""
SET_DESC_HANDLER = CommandHandler(
    "setdesc", set_desc, filters=Filters.chat_type.groups, run_async=True
)
SET_STICKER_HANDLER = CommandHandler(
    "setsticker", set_sticker, filters=Filters.chat_type.groups, run_async=True
)
SETCHATPIC_HANDLER = CommandHandler(
    "setgpic", setchatpic, filters=Filters.chat_type.groups, run_async=True
)
RMCHATPIC_HANDLER = CommandHandler(
    "delgpic", rmchatpic, filters=Filters.chat_type.groups, run_async=True
)
SETCHAT_TITLE_HANDLER = CommandHandler(
    "setgtitle", setchat_title, filters=Filters.chat_type.groups, run_async=True
)

ADMINLIST_HANDLER = DisableAbleCommandHandler("admins", adminlist, run_async=True)

PIN_HANDLER = CommandHandler(
    "pin", pin, filters=Filters.chat_type.groups, run_async=True
)
UNPIN_HANDLER = CommandHandler(
    "unpin", unpin, filters=Filters.chat_type.groups, run_async=True
)
PINNED_HANDLER = CommandHandler(
    "pinned", pinned, filters=Filters.chat_type.groups, run_async=True
)

INVITE_HANDLER = DisableAbleCommandHandler("invitelink", invite, run_async=True)

PROMOTE_HANDLER = DisableAbleCommandHandler("promote", promote, run_async=True)
FULLPROMOTE_HANDLER = DisableAbleCommandHandler(
    "fullpromote", fullpromote, run_async=True
)
LOWPROMOTE_HANDLER = DisableAbleCommandHandler("lowpromote", lowpromote, run_async=True)
DEMOTE_HANDLER = DisableAbleCommandHandler("demote", demote, run_async=True)
PROMOTE_CALLBACK_HANDLER = CallbackQueryHandler(
    promote_button, pattern=r"admin_", run_async=True
)


SET_TITLE_HANDLER = CommandHandler("title", set_title, run_async=True)
ADMIN_REFRESH_HANDLER = CommandHandler(
    "admincache", refresh_admin, filters=Filters.chat_type.groups, run_async=True
)

dispatcher.add_handler(SET_DESC_HANDLER)
dispatcher.add_handler(SET_STICKER_HANDLER)
dispatcher.add_handler(SETCHATPIC_HANDLER)
dispatcher.add_handler(RMCHATPIC_HANDLER)
dispatcher.add_handler(SETCHAT_TITLE_HANDLER)
dispatcher.add_handler(ADMINLIST_HANDLER)
dispatcher.add_handler(PIN_HANDLER)
dispatcher.add_handler(UNPIN_HANDLER)
dispatcher.add_handler(PINNED_HANDLER)
dispatcher.add_handler(INVITE_HANDLER)
dispatcher.add_handler(PROMOTE_HANDLER)
dispatcher.add_handler(FULLPROMOTE_HANDLER)
dispatcher.add_handler(PROMOTE_CALLBACK_HANDLER)
dispatcher.add_handler(LOWPROMOTE_HANDLER)
dispatcher.add_handler(DEMOTE_HANDLER)
dispatcher.add_handler(SET_TITLE_HANDLER)
dispatcher.add_handler(ADMIN_REFRESH_HANDLER)

__mod_name__ = "𝙰ᴅᴍɪɴs"
__command_list__ = [
    "setdesc" "setsticker" "setgpic" "delgpic" "setgtitle" "adminlist",
    "admins",
    "invitelink",
    "promote",
    "fullpromote",
    "lowpromote",
    "demote",
    "admincache",
]
__handlers__ = [
    SET_DESC_HANDLER,
    SET_STICKER_HANDLER,
    SETCHATPIC_HANDLER,
    RMCHATPIC_HANDLER,
    SETCHAT_TITLE_HANDLER,
    ADMINLIST_HANDLER,
    PIN_HANDLER,
    UNPIN_HANDLER,
    PINNED_HANDLER,
    PROMOTE_CALLBACK_HANDLER,
    INVITE_HANDLER,
    PROMOTE_HANDLER,
    FULLPROMOTE_HANDLER,
    LOWPROMOTE_HANDLER,
    DEMOTE_HANDLER,
    SET_TITLE_HANDLER,
    ADMIN_REFRESH_HANDLER,
]
