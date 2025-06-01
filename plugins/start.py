import random
import logging
from pyrogram import Client, filters, enums
from pyrogram.enums import ParseMode
from pyrogram.errors import FloodWait, ChatAdminRequired
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, InputMediaPhoto, CallbackQuery, Message
from helper.database import db
from config import Config, Txt
import humanize
from time import sleep

logger = logging.getLogger(__name__)

@Client.on_message(filters.private & filters.command("start"))
async def start(client, message):

    if message.from_user.id in Config.BANNED_USERS:
        await message.reply_text("Sorry, You are banned.")
        return

    user = message.from_user
    await db.add_user(client, message)
    button = InlineKeyboardMarkup([[
        InlineKeyboardButton(
            '⛅ Uᴘᴅᴀᴛᴇꜱ', url=f'https://t.me/{Config.UPDATES}'),
        InlineKeyboardButton(
            ' Sᴜᴘᴘᴏʀᴛ 🌨️', url=f'https://t.me/{Config.SUPPORT}')
    ], [
        InlineKeyboardButton('❄️ Δʙᴏᴜᴛ', callback_data='about'),
        InlineKeyboardButton(' Hᴇʟᴩ ❗', callback_data='help')
    ], [InlineKeyboardButton('⚙️ sᴛΔᴛs ⚙️', callback_data='stats')]])
    if Config.PICS:
        await message.reply_photo(random.choice(Config.PICS), caption=Txt.START_TXT.format(user.mention), reply_markup=button)
    else:
        await message.reply_text(text=Txt.START_TXT.format(user.mention), reply_markup=button, disable_web_page_preview=True)
        
@Client.on_message(filters.command("del") & filters.private)
async def delete_keyword(client: Client, message: Message):
    user_id = message.from_user.id
    parts = message.text.split(maxsplit=1)

    if len(parts) != 2:
        return await message.reply("❌ Please specify the keyword to delete.\nUsage: `/del your_keyword`", quote=True)

    keyword = parts[1].strip().lower()
    result = await db.usrs.delete_one({"user_id": user_id, "keyword": keyword})

    if result.deleted_count:
        await message.reply(f"✅ Keyword `{keyword}` has been deleted.")
    else:
        await message.reply(f"⚠️ No keyword found as `{keyword}`.")

@Client.on_message(filters.command("clearmydata") & filters.private)
async def clear_all_user_data(client: Client, message: Message):
    user_id = message.from_user.id
    result = await db.usrs.delete_many({"user_id": user_id})

    if result.deleted_count:
        await message.reply(f"🗑️ Deleted all `{result.deleted_count}` saved keyword(s).")
    else:
        await message.reply("⚠️ No saved data found to delete.")
