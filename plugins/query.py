import shutil
import time
from pyrogram import Client
from pyrogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup, InputMediaPhoto
from config import Config, Txt
from helper.database import db
import random
import psutil
from helper.utils import humanbytes


@Client.on_callback_query()
async def cb_handler(client, query: CallbackQuery):
    data = query.data
    user_id = query.from_user.id
    if data == "start":
        await query.message.edit_media(
            InputMediaPhoto(
                random.choice(Config.PICS),
                Txt.START_TXT.format(query.from_user.mention),

            ),

            reply_markup=InlineKeyboardMarkup([[
                InlineKeyboardButton(
                    "⛅ Uᴩᴅᴀᴛᴇꜱ", url=f"https://t.me/{Config.UPDATES}"),
                InlineKeyboardButton(
                    "Sᴜᴩᴩᴏʀᴛ ⛈️", url=f"https://t.me/{Config.SUPPORT}")
            ], [
                InlineKeyboardButton('❄️ Δʙᴏᴜᴛ', callback_data='about'),
                InlineKeyboardButton('Hᴇʟᴩ ❗', callback_data='help')
            ]])
        )
    elif data == "help":

        await query.message.edit_media(
            InputMediaPhoto(
                random.choice(Config.PICS),
                Txt.HELP_TXT

            ),

            reply_markup=InlineKeyboardMarkup([[
                InlineKeyboardButton("ᴋᴇʏᴡᴏʀᴅꜱ", callback_data="list_keys")
            ], [                      
                InlineKeyboardButton("ᐊ ʙᴀᴄᴋ", callback_data="start"),
                InlineKeyboardButton("✘ ᴄʟᴏsᴇ", callback_data="close")
                
            ]])
        )

   

    elif data == "about":
        await query.message.edit_media(
            InputMediaPhoto(
                random.choice(Config.PICS),
                Txt.ABOUT_TXT.format(client.mention),

            ),

            reply_markup=InlineKeyboardMarkup([[
                InlineKeyboardButton("ᐊ ʙᴀᴄᴋ", callback_data="start"),
                InlineKeyboardButton("✘ ᴄʟᴏsᴇ", callback_data="close")
                
            ]])
        )

    elif data == 'stats':
        buttons = [[InlineKeyboardButton(
            '• ʙᴀᴄᴋ', callback_data='start'), InlineKeyboardButton('⟲ ʀᴇʟᴏᴀᴅ', callback_data='stats')]]
        reply_markup = InlineKeyboardMarkup(buttons)
        currentTime = time.strftime("%Hh%Mm%Ss", time.gmtime(
            time.time() - Config.BOT_UPTIME))
        total, used, free = shutil.disk_usage(".")
        total = humanbytes(total)
        used = humanbytes(used)
        free = humanbytes(free)
        cpu_usage = psutil.cpu_percent()
        ram_usage = psutil.virtual_memory().percent
        disk_usage = psutil.disk_usage('/').percent
        await query.message.edit_media(
            InputMediaPhoto(
                random.choice(Config.PICS),
                Txt.STATS_TXT.format(
                    currentTime, total, used, disk_usage, free, cpu_usage, ram_usage)
            ),
            reply_markup=reply_markup
        )

    elif data == "list_keys":
        cursor = db.usrs.find({"user_id": user_id})
        user_data = await cursor.to_list(length=100)

        if not user_data:
            return await query.message.edit("😕 You have no saved keywords.")

        buttons = [
            [InlineKeyboardButton(text=item['keyword'], callback_data=f"showkey_{item['keyword']}")]
            for item in user_data
        ]
        
        await query.message.edit_media(
            InputMediaPhoto(
                random.choice(Config.PICS),
                "📌 Your Saved Keywords:",
            reply_markup=InlineKeyboardMarkup(buttons)
        )
    
    
    elif data.startswith("showkey_"):
        keyword = data.split("showkey_")[1]
        entry = await db.usrs.find_one({"user_id": user_id, "keyword": keyword})

        if not entry:
            return await query.message.edit("❌ Keyword data not found.")

        msg = (
            f"🔑 **Keyword**: `{entry['keyword']}`\n"
            f"📝 **Rename Format**: `{entry.get('rename_format', 'N/A')}`\n"
            f"🖼 **Thumbnail**: `{entry.get('thumbnail', 'N/A')}`\n"
            f"📤 **Dump Channel ID**: `{entry.get('dump', 'N/A')}`\n"
            f"📺 **Channel Title**: `{entry.get('channel_title', 'N/A')}`"
        )

        buttons = [[
            InlineKeyboardButton("🗑 Delete", callback_data=f"delkey_{keyword}"),
            InlineKeyboardButton("🔙 Back", callback_data="list_keys")
        ]]
        await query.message.edit(msg, reply_markup=InlineKeyboardMarkup(buttons))

    elif data.startswith("delkey_"):
        keyword = data.split("delkey_")[1]
        result = await db.usrs.delete_one({"user_id": user_id, "keyword": keyword})

        if result.deleted_count:
            await query.answer("✅ Deleted")
            await query.message.edit(f"🗑 Deleted keyword `{keyword}`.", reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🔙 Back", callback_data="list_keys")]
            ]))
        else:
            await query.answer("❌ Not found or already deleted")

    
    elif data == 'userbot':
        userBot = await db.get_user_bot(query.from_user.id)

        text = f"Name: {userBot['name']}\nUserName: @{userBot['username']}\n UserId: {userBot['user_id']}"

        await query.message.edit(text=text, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton('❌ ʀᴇᴍᴏᴠᴇ ❌', callback_data='rmuserbot')], [InlineKeyboardButton('✘ ᴄʟᴏsᴇ ✘', callback_data='close')]]))

    elif data == 'rmuserbot':
        try:
            await db.remove_user_bot(query.from_user.id)
            await query.message.edit(text='**User Bot Removed Successfully ✅**', reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton('✘ ᴄʟᴏsᴇ ✘', callback_data='close')]]))
        except:
            await query.answer(f'Hey {query.from_user.first_name}\n\n You have already deleted the user')

    elif data == "close":
        try:
            await query.message.delete()
            await query.message.reply_to_message.delete()
            await query.message.continue_propagation()
        except:
            await query.message.delete()
            await query.message.continue_propagation()
