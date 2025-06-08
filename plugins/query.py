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
                InlineKeyboardButton("ʜᴏᴡ ᴛᴏ ʀᴇɴᴀᴍᴇ ꜰɪʟᴇꜱ", callback_data="how")
            ], [
                InlineKeyboardButton("ᴛʜᴜᴍʙɴᴀɪʟ", callback_data="pic"),
                InlineKeyboardButton("ᴄᴀᴩᴛɪᴏɴ", callback_data="cap")
            ], [
                InlineKeyboardButton("ꜱᴜꜰꜰɪx ᴀɴᴅ ᴩʀᴇꜰɪx", callback_data="sufpre")
            ], [
                InlineKeyboardButton("ᴅᴜᴍᴩ ᴄʜᴀɴɴᴇʟ", callback_data="dump")
            ], [
                InlineKeyboardButton("ᴍᴇᴛᴀᴅᴀᴛᴀ", callback_data="meta")
            ], [
                InlineKeyboardButton("ᴋᴇʏᴡᴏʀᴅꜱ", callback_data="list_keys")
            ], [                      
                InlineKeyboardButton("ᐊ ʙᴀᴄᴋ", callback_data="start"),
                InlineKeyboardButton("✘ ᴄʟᴏsᴇ", callback_data="close")
                
            ]])
        )


    

    elif data == "newformat":
        user_id = query.from_user.id

        await query.message.edit(
            "Sᴇɴᴅ ᴛʜᴇ **ʀᴇɴᴀᴍᴇ ꜰᴏʀᴍᴀᴛ**. Uꜱᴇ `Episode` ᴀɴᴅ `Quality` ᴀꜱ ᴩʟᴀᴄᴇʜᴏʟᴅᴇʀꜱ.\n\nSᴇɴᴅ /cancel ᴛᴏ ᴄᴀɴᴄᴇʟ."
        )
        rf_msg = await client.listen(user_id)
        if rf_msg.text and rf_msg.text.strip().lower() == "/cancel":
            return await client.send_message(user_id, "❌ Cᴀɴᴄᴇʟʟᴇᴅ.")
        rename_format = rf_msg.text.strip()

        await client.send_message(
            user_id,
            "Sᴇɴᴅ ᴛʜᴇ **ᴋᴇʏᴡᴏʀᴅ** ʏᴏᴜ ᴡᴀɴᴛ ᴛᴏ ᴜꜱᴇ:\n\nSᴇɴᴅ /cancel ᴛᴏ ᴄᴀɴᴄᴇʟ."
        )
        kw_msg = await client.listen(user_id)
        if kw_msg.text and kw_msg.text.strip().lower() == "/cancel":
            return await client.send_message(user_id, "❌ Cᴀɴᴄᴇʟʟᴇᴅ.")
        keyword = kw_msg.text.strip()
        
        await client.send_message(
            user_id,
            "Sᴇɴᴅ ᴀ **ᴛʜᴜᴍʙɴᴀɪʟ** (ᴀꜱ ᴩʜᴏᴛᴏ).\nSᴇɴᴅ /default ᴛᴏ ᴜꜱᴇ ᴅᴇꜰᴀᴜʟᴛ ᴛʜᴜᴍʙ, /cancel ᴛᴏ ᴄᴀɴᴄᴇʟ."
        )
        thumb_msg = await client.listen(user_id)

        if thumb_msg.text and thumb_msg.text.strip().lower() == "/default":
            await client.send_message(user_id, "Sᴇᴛᴛɪɴɢ ᴅᴇꜰᴀᴜʟᴛ ᴛʜᴜᴍʙɴᴀɪʟ...")
            thumbnail_file_id = None
        elif not thumb_msg.photo:
            return await client.send_message(user_id, "Tʜᴀᴛ ᴡᴀꜱɴ'ᴛ ᴀ ᴩʜᴏᴛᴏ. Pʀᴏᴄᴇꜱꜱ ᴄᴀɴᴄᴇʟʟᴇᴅ....!")
        else:
            thumbnail_file_id = thumb_msg.photo.file_id

        await client.send_message(
            user_id,
            "Nᴏᴡ **ꜰᴏʀᴡᴀʀᴅ ᴍᴜʟᴛɪᴘʟᴇ ᴍᴇꜱꜱᴀɢᴇꜱ ꜰʀᴏᴍ ᴛʜᴇ ᴄʜᴀɴɴᴇʟꜱ** ʏᴏᴜ ᴡᴀɴᴛ ᴛᴏ ꜱᴇᴛ ᴀꜱ ᴅᴜᴍᴩ.\n"
            "Sᴇɴᴅ /done ᴡʜᴇɴ ꜰɪɴɪꜱʜᴇᴅ, /default ᴛᴏ ᴜꜱᴇ ᴅᴇꜰᴀᴜʟᴛ (ɴᴏ ᴅᴜᴍᴘ), /cancel ᴛᴏ ᴄᴀɴᴄᴇʟ."
        )

        dump_channels: list[str] = []
        channel_titles: list[str] = []

        while True:
            fwd_msg = await client.listen(user_id)

            if fwd_msg.text and fwd_msg.text.lower() in {"/done", "/default", "/cancel"}:
                choice = fwd_msg.text.lower()
                if choice == "/cancel":
                    return await client.send_message(user_id, "❌ Cᴀɴᴄᴇʟʟᴇᴅ.")
                if choice == "/default":
                    dump_channels.clear()          # keep empty (no dump)
                break

            if not fwd_msg.forward_from_chat:
                await client.send_message(user_id, "❌ Nᴏᴛ ꜰᴏʀᴡᴀʀᴅᴇᴅ ꜰʀᴏᴍ ᴀ ᴄʜᴀɴɴᴇʟ. Tʀʏ ᴀɢᴀɪɴ.")
                continue

            channel = fwd_msg.forward_from_chat
            try:
                await client.get_chat_member(channel.id, "me")
            except UserNotParticipant:
                await client.send_message(
                    user_id,
                    f"⚠️ ɴᴏᴛ ɪɴ {channel.title}. Aᴅᴅ ᴍᴇ ᴀɴᴅ ꜱᴇɴᴅ ᴀɢᴀɪɴ."
                )
                continue

            if str(channel.id) not in dump_channels:
                dump_channels.append(str(channel.id))
                channel_titles.append(channel.title or "Untitled")

        if "." not in rename_format:
            rename_format += ".mkv"
        elif not rename_format.lower().endswith(
            (".mkv", ".mp4", ".avi", ".mov", ".flv", ".webm", ".ts", ".m4v")
        ):
            rename_format += ".mkv"


        await db.usrs.insert_one({
            "user_id": user_id,
            "keyword": keyword,
            "rename_format": rename_format,
            "thumbnail": thumbnail_file_id,
            "dump": "".join(dump_channels),        # saved without spaces
            "channel_titles": channel_titles
        })

        await client.send_message(
            user_id,
            f"Sᴇᴛᴛɪɴɢꜱ ꜱᴀᴠᴇᴅ ꜱᴜᴄᴄᴇꜱꜱꜰᴜʟʟʏ ᴜɴᴅᴇʀ ᴋᴇʏᴡᴏʀᴅ: `{keyword}`. ✅"
        )

    elif data == "delete_all_keywords":
        buttons = [
            [
                InlineKeyboardButton("ᴄᴏɴꜰɪʀᴍ ✓", callback_data="delete_all_keywords_confirm"),
                InlineKeyboardButton("ᴄᴀɴᴄᴇʟ ✘", callback_data="cancel_delete_all")
            ]
        ]
        await query.message.edit_text(
            "⚠️ Are you sure you want to DELETE **ALL** your keywords? This action cannot be undone.",
            reply_markup=InlineKeyboardMarkup(buttons)
        )

    elif data == "delete_all_keywords_confirm":
        result = await db.usrs.delete_many({"user_id": user_id})
        await query.answer(f"✅ Deleted all your keywords ({result.deleted_count}).", show_alert=True)
        await query.message.delete()
        
    elif data == "cancel_delete_all":
        await query.answer("❎ Cancelled deleting all keywords.", show_alert=True)
        await query.message.delete()

    elif data == "meta":
        await query.message.edit_media(
            InputMediaPhoto(
                random.choice(Config.PICS),
                Txt.META_TXT,
            ),

            reply_markup=InlineKeyboardMarkup([[
                InlineKeyboardButton("ᐊ ʙᴀᴄᴋ", callback_data="help"),
                InlineKeyboardButton("ᴄʟᴏsᴇ ✘", callback_data="close")
                
            ]])
        )
    elif data == "dump":
        await query.message.edit_media(
            InputMediaPhoto(
                random.choice(Config.PICS),
                Txt.DUMP_TXT,
            ),

            reply_markup=InlineKeyboardMarkup([[
                InlineKeyboardButton("ᐊ ʙᴀᴄᴋ", callback_data="help"),
                InlineKeyboardButton("ᴄʟᴏsᴇ ✘", callback_data="close")
                
            ]])
        )
    
    elif data == "cap":
        await query.message.edit_media(
            InputMediaPhoto(
                random.choice(Config.PICS),
                Txt.CAP_TXT,
            ),

            reply_markup=InlineKeyboardMarkup([[
                InlineKeyboardButton("ᐊ ʙᴀᴄᴋ", callback_data="help"),
                InlineKeyboardButton("ᴄʟᴏsᴇ ✘", callback_data="close")
                
            ]])
        )
    elif data == "how":
        await query.message.edit_media(
            InputMediaPhoto(
                random.choice(Config.PICS),
                Txt.HOW_TXT,
            ),

            reply_markup=InlineKeyboardMarkup([[
                InlineKeyboardButton("ᐊ ʙᴀᴄᴋ", callback_data="help"),
                InlineKeyboardButton("ᴄʟᴏsᴇ ✘", callback_data="close")
                
            ]])
        )
    elif data == "sufpre":
        await query.message.edit_media(
            InputMediaPhoto(
                random.choice(Config.PICS),
                Txt.SUFPRE_TXT,
            ),

            reply_markup=InlineKeyboardMarkup([[
                InlineKeyboardButton("ᐊ ʙᴀᴄᴋ", callback_data="help"),
                InlineKeyboardButton("ᴄʟᴏsᴇ ✘", callback_data="close")
                
            ]])
        )
    elif data == "pic":
        await query.message.edit_media(
            InputMediaPhoto(
                random.choice(Config.PICS),
                Txt.PIC_TXT,
            ),

            reply_markup=InlineKeyboardMarkup([[
                InlineKeyboardButton("ᐊ ʙᴀᴄᴋ", callback_data="help"),
                InlineKeyboardButton("ᴄʟᴏsᴇ ✘", callback_data="close")
                
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
            return await query.message.edit("😕 Yᴏᴜ ʜᴀᴠᴇ ɴᴏ ꜱᴀᴠᴇᴅ ᴋᴇʏᴡᴏʀᴅꜱ.", reply_markup=InlineKeyboardMarkup([[
                InlineKeyboardButton("ᴀᴅᴅ ᴋᴇʏᴡᴏʀᴅ", callback_data="newformat")
            ], [
                InlineKeyboardButton("ᐊ ʙᴀᴄᴋ", callback_data="help"),
                InlineKeyboardButton("✘ ᴄʟᴏsᴇ", callback_data="close")
                
            ]]))

        buttons = [
            [InlineKeyboardButton(text=item['keyword'], callback_data=f"showkey_{item['keyword']}")]
            for item in user_data
        ]
        buttons.append([InlineKeyboardButton("ᴀᴅᴅ ᴋᴇʏᴡᴏʀᴅ", callback_data="newformat")])
        buttons.append([InlineKeyboardButton("ᐊ ʙᴀᴄᴋ", callback_data="help"),
                       InlineKeyboardButton("ᴅᴇʟᴇᴛᴇ ᴀʟʟ", callback_data="delete_all_keywords")])
        await query.message.edit_media(
            InputMediaPhoto(
                random.choice(Config.PICS),
                "• Yᴏᴜʀ Sᴀᴠᴇᴅ Kᴇʏᴡᴏʀᴅꜱ:",
            ),
            reply_markup=InlineKeyboardMarkup(buttons)
        )
    
    
    elif data.startswith("showkey_"):
        keyword = data.split("showkey_")[1]
        entry = await db.usrs.find_one({"user_id": user_id, "keyword": keyword})

        if not entry:
            return await query.message.edit("❌ Keyword data not found.")

        msg = (
            f"• **Kᴇʏᴡᴏʀᴅ**: `{entry['keyword']}`\n"
            f"• **Rᴇɴᴀᴍᴇ Fᴏʀᴍᴀᴛ**: `{entry.get('rename_format', 'N/A')}`\n"
            f"• **Tʜᴜᴍʙɴᴀɪʟ**: `{entry.get('thumbnail', 'N/A')}`\n"
            f"• **Dᴜᴍᴩ Cʜᴀɴɴᴇʟ Iᴅ**: `{entry.get('dump', 'N/A')}`\n"
            f"• **Dᴜᴍᴩ Tɪᴛʟᴇ**: `{entry.get('channel_title', 'N/A')}`"
        )

        buttons = [[
            InlineKeyboardButton("ᴅᴇʟᴇᴛᴇ", callback_data=f"delkey_{keyword}"),
            InlineKeyboardButton("ᐊ ʙᴀᴄᴋ", callback_data="list_keys")
        ]]
        await query.message.edit(msg, reply_markup=InlineKeyboardMarkup(buttons))

    elif data.startswith("delkey_"):
        keyword = data.split("delkey_")[1]
        result = await db.usrs.delete_one({"user_id": user_id, "keyword": keyword})

        if result.deleted_count:
            await query.answer("✅ Deleted")
            await query.message.edit(f"ᴅᴇʟᴇᴛᴇᴅ ᴛʜᴇ ᴋᴇʏᴡᴏʀᴅ: `{keyword}`.", reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("ᐊ ʙᴀᴄᴋ", callback_data="list_keys")]
            ]))
        else:
            await query.answer("❌ Nᴏᴛ ꜰᴏᴜɴᴅ ᴏʀ ᴀʟʀᴇᴀᴅʏ ᴅᴇʟᴇᴛᴇᴅ")

    
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
