from pyrogram import Client, filters, enums
from helper.database import db
import re
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery, ForceReply
import asyncio
from plugins.features import features_button, extract_episode_number
from pyrogram.errors import UserNotParticipant
from plugins.process import process_key, process_queue

@Client.on_message(filters.command("newformat") & filters.private)
async def set_command(client: Client, message: Message):
    user_id = message.from_user.id
    chat_id = message.chat.id

    try:
        rf_msg = await client.ask(chat_id, "Sᴇɴᴅ ᴛʜᴇ **ʀᴇɴᴀᴍᴇ ꜰᴏʀᴍᴀᴛ**. Uꜱᴇ `Episode` ᴀɴᴅ `Quality` ᴀꜱ ᴩʟᴀᴄᴇʜᴏʟᴅᴇʀꜱ.")
        rename_format = rf_msg.text.strip()

        kw_msg = await client.ask(chat_id, "Sᴇɴᴅ ᴛʜᴇ **ᴋᴇʏᴡᴏʀᴅ** ʏᴏᴜ ᴡᴀɴᴛ ᴛᴏ ᴜꜱᴇ:")
        keyword = kw_msg.text.strip()


        thumb_msg = await client.ask(chat_id, "Sᴇɴᴅ ᴀ **ᴛʜᴜᴍʙɴᴀɪʟ** (ᴀꜱ ᴩʜᴏᴛᴏ).")

        if thumb_msg.text and thumb_msg.text.strip() == "/default":
            await client.send_message(chat_id, "Sᴇᴛᴛɪɴɢ Aꜱ Dᴇꜰᴀᴜʟᴛ....")
            thumbnail_file_id = None

        elif not thumb_msg.photo:
            return await client.send_message(chat_id, "Tʜᴀᴛ ᴡᴀꜱɴ'ᴛ ᴀ ᴩʜᴏᴛᴏ. Pʀᴏᴄᴇꜱꜱ ᴄᴀɴᴄᴇʟʟᴇᴅ....!")
        else:
            thumbnail_file_id = thumb_msg.photo.file_id

        fwd_msg = await client.ask(chat_id, "Nᴏᴡ **ꜰᴏʀᴡᴀʀᴅ ᴀ ᴍᴇꜱꜱᴀɢᴇ ꜰʀᴏᴍ ᴛʜᴇ ᴄʜᴀɴɴᴇʟ** ʏᴏᴜ ᴡᴀɴᴛ ᴛᴏ ꜱᴇᴛ ᴀꜱ ᴅᴜᴍᴩ.\n\nᴏʀ ꜱᴇɴᴅ `/default` ᴛᴏ ᴜꜱᴇ ᴅᴇꜰᴀᴜʟᴛ.")

        if fwd_msg.text and fwd_msg.text.strip() == "/default":
            await client.send_message(chat_id, "Sᴇᴛᴛɪɴɢ ᴀꜱ ᴅᴇꜰᴀᴜʟᴛ...")
            channel = None

        elif not fwd_msg.forward_from_chat:
            return await client.send_message(chat_id, "Nᴏᴛ ꜰᴏʀᴡᴀʀᴅᴇᴅ ꜰʀᴏᴍ ᴀ ᴄʜᴀɴɴᴇʟ. Pʀᴏᴄᴇꜱꜱ ᴄᴀɴᴄᴇʟʟᴇᴅ....!")

        else:
            channel = fwd_msg.forward_from_chat

            try:
                await client.get_chat_member(channel.id, "me")
            except UserNotParticipant:
                await client.send_message(chat_id, "ʏᴏᴜʀ ᴄʜᴀɴɴᴇʟ ʜᴀꜱ ʙᴇᴇɴ ᴀᴅᴅᴇᴅ ꜱᴜᴄᴄᴇꜱꜱꜰᴜʟʟʏ, ʙᴜᴛ ꜰɪʟᴇꜱ ᴡᴏɴᴛ ʙᴇ ꜰᴏʀᴡᴀʀᴅᴇᴅ ᴛʜᴇʀᴇ ᴛɪʟʟ ʏᴏᴜ ᴀᴅᴅ ᴍᴇ \n⚠️ɴᴏᴛᴇ : ɪ'ᴍ ɴᴏᴛ ɪɴ ᴛʜᴀᴛ ᴄʜᴀɴɴᴇʟ. ᴩʟᴇᴀꜱᴇ ᴀᴅᴅ ᴍᴇ.")


        if "." not in rename_format:
            rename_format += ".mkv"
        elif not rename_format.lower().endswith((".mkv", ".mp4", ".avi", ".mov", ".flv", ".webm", ".ts", ".m4v")):
            rename_format += ".mkv"
        await db.usrs.insert_one({
            "user_id": user_id,
            "keyword": keyword,
            "rename_format": rename_format,
            "thumbnail": thumbnail_file_id,
            "dump": channel.id,
            "channel_title": channel.title or "Untitled"
        })

        await client.send_message(chat_id, f"Sᴇᴛᴛɪɴɢꜱ ꜱᴀᴠᴇᴅ ꜱᴜᴄᴄᴇꜱꜱꜰᴜʟʟʏ ᴜɴᴅᴇʀ ᴋᴇʏᴡᴏʀᴅ: `{keyword}`. ✅")
    except Exception as e:
        await client.send_message(chat_id, f"❌ Error: {e}")

@Client.on_callback_query(filters.regex('^allinone'))
async def hale_filters(bot: Client, query: CallbackQuery):
    user_id = query.from_user.id
    parts = query.data.split('_')
    type = parts[1]
    batch_no = int(parts[2]) if len(parts) > 2 else "1"
    file = parts[3] if len(parts) > 3 else "d"
    get_meta = await db.get_metadata(user_id)
    if type == 'metadata':
        if get_meta:
            await db.set_metadata(user_id, False)
            await bot.send_message(user_id, "Set To False")
        else:
            await db.set_metadata(user_id, True)
            await bot.send_message(user_id, "Set To True")
        ge_meta = await db.get_metadata(user_id)
        button = [[
                InlineKeyboardButton('ᴍᴇᴛᴀᴅᴀᴛᴀ', callback_data='allinone_curiousity'),
                InlineKeyboardButton('✅' if ge_meta else '❌', callback_data='allinone_metadata_{batch_no}_{file}')
            ],[
                InlineKeyboardButton("File Type", callback_data="allinone_curiousity"),
                InlineKeyboardButton("Document" if file == "d" else "Video", callback_data=f"allinone_video_{batch_no}" if file == "d" else f"allinone_docum_{batch_no}")
            ],[
                InlineKeyboardButton("Confirm", callback_data=f"renme_{batch_no}_v")
        ]]
        await query.message.edit_reply_markup(reply_markup=InlineKeyboardMarkup(button))


    elif type == 'docum':
        button = [[
                InlineKeyboardButton('ᴍᴇᴛᴀᴅᴀᴛᴀ', callback_data='allinone_curiousity'),
                InlineKeyboardButton('✅' if get_meta else '❌', callback_data=f'allinone_metadata_{batch_no}_d')
            ],[
                InlineKeyboardButton("File Type", callback_data="allinone_curiosity"),
                InlineKeyboardButton("Document", callback_data=f"allinone_video_{batch_no}")
            ],[
                InlineKeyboardButton("Confirm", callback_data=f"renme_{batch_no}_d")
        ]]
        await query.message.edit_reply_markup(reply_markup=InlineKeyboardMarkup(button))

    elif type == 'video':
        button = [[
                InlineKeyboardButton('ᴍᴇᴛᴀᴅᴀᴛᴀ', callback_data='allinone_curiousity'),
                InlineKeyboardButton('✅' if get_meta else '❌', callback_data=f'allinone_metadata_{batch_no}_v')
            ],[
                InlineKeyboardButton("File Type", callback_data="allinone_curiousity"),
                InlineKeyboardButton("Video", callback_data=f"allinone_docum_{batch_no}")
            ],[
                InlineKeyboardButton("Confirm", callback_data=f"renme_{batch_no}_v")
        ]]
        await query.message.edit_reply_markup(reply_markup=InlineKeyboardMarkup(button))

    elif type == 'del':
        await db.delete_batch(user_id, batch_no)
        await bot.send_message(user_id, "Deleted!")

    elif type == 'curiousity':
        await query.answer(text="The Other Button..!", show_alert=True)


    


@Client.on_message(filters.private & filters.command('del_dump'))
async def delete_dump(client, message):

    SyD = await message.reply_text("Please Wait ...", reply_to_message_id=message.id)
    dump = await db.get_dump(message.from_user.id)
    if not dump:
        return await SyD.edit("__**😔 ʏᴏᴜ ᴅᴏɴ'ᴛ ʜᴀᴠᴇ ᴀɴʏ ᴅᴜᴍᴩ ᴄʜᴀɴɴᴇʟ**__")
    await db.set_dump(message.from_user.id, message.from_user.id)
    await SyD.edit("__**❌️ ᴅᴜᴍᴩ ᴅᴇʟᴇᴛᴇᴅ**__")


@Client.on_message(filters.private & filters.command('see_dump'))
async def see_dump(client, message):

    SyD = await message.reply_text("Please Wait ...", reply_to_message_id=message.id)
    dump = await db.get_dump(message.from_user.id)
    if dump:
        await SyD.edit(f"**ʏᴏᴜʀ ᴅᴜᴍʙ ᴄʜᴀɴɴᴇʟ:-**\n\n`{dump}`")
    else:
        await SyD.edit("__**😔 ʏᴏᴜ ᴅᴏɴ'ᴛ ʜᴀᴠᴇ ᴀɴʏ ᴅᴜᴍʙ ᴄʜᴀɴɴᴇʟ**__")

@Client.on_message(filters.private & filters.command('set_dump'))
async def add_dump(client, message):

    if len(message.command) == 1:
        return await message.reply_text("**__Give The Dump Channel_\n\nExᴀᴍᴩʟᴇ:- `/set_dump -100XXXXXXX`**")
    dump = message.text.split(" ", 1)[1]
    SyD = await message.reply_text("Please Wait ...", reply_to_message_id=message.id)
    await db.set_dump(message.from_user.id, dump)
    await SyD.edit("__**✅ ꜱᴀᴠᴇᴅ**__")


@Client.on_message(filters.command("batch") & filters.private)
async def start_batch(client, message):
    user_id = message.from_user.id
    last = await db.batches.find({"user_id": user_id}).sort("batch_no", -1).to_list(1)
    batch_no = last[0]["batch_no"] + 1 if last else 1
    await db.set_active_batch(user_id, batch_no)
    await message.reply_text(f"Batch #{batch_no} started.\nSend files now. Type /endbatch to finish.")


@Client.on_message(filters.command("endbatch") & filters.private)
async def end_batch(client, message):
    user_id = message.from_user.id
    batch_no = await db.get_active_batch(user_id)
    if not batch_no:
        return await message.reply_text("No active batch.")

    await db.clear_active_batch(user_id)
    files_cursor = await db.get_batch_files(user_id, batch_no)
    files = await files_cursor.to_list(length=None)

    if not files:
        return await message.reply_text("No files found in this batch.")

    dump = await db.get_dump(user_id)

    text = f"Received {len(files)} files in Batch #{batch_no}\n"
    if len(files) > 15:
        for f in files:
            part = f["file_name"]
            epp = extract_episode_number(part)
            episode = next((x for x in part.split() if "720" in x or "1080" in x or "480" in x), "File")
            text += f"- {episode} E{epp}\n"
    else:
        text += "\n".join(f"- {f['file_name']}" for f in files)

    text += f"\n Current Dump Channel : {dump} \n If You Want To Change Thumbnail, Send Picture Then And Dump Channel By /set_dump ."
    get_meta = await db.get_metadata(user_id)
    button = [[
            InlineKeyboardButton('ᴍᴇᴛᴀᴅᴀᴛᴀ', callback_data='allinone_curiousity'),
            InlineKeyboardButton('✅' if get_meta else '❌', callback_data=f'allinone_metadata_{batch_no}_d')
        ],[
            InlineKeyboardButton("File Type", callback_data="allinone_curiousity"),
            InlineKeyboardButton("Document", callback_data=f"allinone_video_{batch_no}")
        ],[
            InlineKeyboardButton("Confirm", callback_data=f"renme_{batch_no}_d")
    ]]
    await message.reply_text(text, reply_markup=InlineKeyboardMarkup(button))


@Client.on_message(filters.command("process") & filters.private)
async def end_btch(client, message):
    user_id = message.from_user.id
    parts = message.text.split(maxsplit=2)

    if len(parts) != 2:
        return await message.reply_text(
            "**Usage:** `/process <batch_no>`\n\n"
            "Example: `/process 12`",
            parse_mode=enums.ParseMode.MARKDOWN
        )

    
    batch_no = int(parts[1])
    files_cursor = await db.get_batch_files(user_id, batch_no)
    files = await files_cursor.to_list(length=None)

    if not files:
        return await message.reply_text("No files found in this batch.")

    dump = await db.get_dump(user_id)


    text = f"Received {len(files)} files in Batch #{batch_no}\n"
    if len(files) > 15:
        for f in files:
            part = f["file_nme"]
            epp = extract_episode_number(part)
            episode = next((x for x in part.split() if "720" in x or "1080" in x or "480" in x), "File")
            text += f"- {episode} E{epp}\n"
    else:
        text += "\n".join(f"- {f['file_name']}" for f in files)

    text += f"\n\nCurrent Dump Channel : {dump} \n\nIf You Want To Change Thumbnail, Send Picture Then And Dump Channel By /set_dump ."
    get_meta = await db.get_metadata(user_id)
    button = [[
            InlineKeyboardButton('ᴍᴇᴛᴀᴅᴀᴛᴀ', callback_data='allinone_curiousity'),
            InlineKeyboardButton('✅' if get_meta else '❌', callback_data=f'allinone_metadata_{batch_no}')
        ],[
            InlineKeyboardButton("File Type", callback_data="allinone_curiousity"),
            InlineKeyboardButton("Document", callback_data=f"allinone_video_{batch_no}")
        ],[
            InlineKeyboardButton("Confirm", callback_data=f"renme_{batch_no}_d")
    ]]
    await message.reply_text(text, reply_markup=InlineKeyboardMarkup(button))


@Client.on_message(filters.private & (filters.document | filters.video))
async def handle_sedia(client: Client, message: Message):
    user_id = message.from_user.id
    media = message.document or message.video
    filename = (media.file_name or "").lower()
    batch_no = await db.get_active_batch(user_id)

    if not batch_no:
        keyword_entries = await db.usrs.find({"user_id": user_id}).to_list(length=100)
        
        if not keyword_entries:
            return await process_queue(client, message)

        matched_keywords = [entry["keyword"] for entry in keyword_entries if entry.get("keyword", "").lower() in filename]

        if len(matched_keywords) > 1:
            return await message.reply(
                f"❌ Multiple keywords matched in filename: `{', '.join(matched_keywords)}`\nPlease delete unnecessary keywords using `/del <keyword>` or `/clearmydata`.",
                quote=True
            )

        if len(matched_keywords) == 1:
            keyword = matched_keywords[0].lower()
            await message.reply_text("🆗 Keyword match found. Proceeding with keyword.")
            await process_key(client, message, keyword)
            return

        return await process_queue(client, message)
    

    
@Client.on_message(filters.private & filters.command('set_prefix'))
async def add_caption(client, message):

    if len(message.command) == 1:
        return await message.reply_text("**__Give The Prefix__\n\nExᴀᴍᴩʟᴇ:- `/set_prefix @username`**")
    prefix = message.text.split(" ", 1)[1]
    SnowDev = await message.reply_text("Please Wait ...", reply_to_message_id=message.id)
    await db.set_prefix(message.from_user.id, prefix)
    await SnowDev.edit("__**✅ ᴘʀᴇꜰɪx ꜱᴀᴠᴇᴅ**__")


@Client.on_message(filters.private & filters.command('del_prefix'))
async def delete_prefix(client, message):

    SnowDev = await message.reply_text("Please Wait ...", reply_to_message_id=message.id)
    prefix = await db.get_prefix(message.from_user.id)
    if not prefix:
        return await SnowDev.edit("__**😔 ʏᴏᴜ ᴅᴏɴ'ᴛ ʜᴀᴠᴇ ᴀɴʏ ᴘʀᴇꜰɪx**__")
    await db.set_prefix(message.from_user.id, None)
    await SnowDev.edit("__**❌️ ᴘʀᴇꜰɪx ᴅᴇʟᴇᴛᴇᴅ**__")


@Client.on_message(filters.private & filters.command('see_prefix'))
async def see_caption(client, message):

    SnowDev = await message.reply_text("Please Wait ...", reply_to_message_id=message.id)
    prefix = await db.get_prefix(message.from_user.id)
    if prefix:
        await SnowDev.edit(f"**ʏᴏᴜʀ ᴘʀᴇꜰɪx:-**\n\n`{prefix}`")
    else:
        await SnowDev.edit("__**😔 ʏᴏᴜ ᴅᴏɴ'ᴛ ʜᴀᴠᴇ ᴀɴʏ ᴘʀᴇꜰɪx**__")


# SUFFIX
@Client.on_message(filters.private & filters.command('set_suffix'))
async def add_csuffix(client, message):

    if len(message.command) == 1:
        return await message.reply_text("**__Give The Suffix__\n\nExᴀᴍᴩʟᴇ:- `/set_suffix @username`**")
    suffix = message.text.split(" ", 1)[1]
    SnowDev = await message.reply_text("Please Wait ...", reply_to_message_id=message.id)
    await db.set_suffix(message.from_user.id, suffix)
    await SnowDev.edit("__**✅ ꜱᴜꜰꜰɪx ꜱᴀᴠᴇᴅ**__")


@Client.on_message(filters.private & filters.command('del_suffix'))
async def delete_suffix(client, message):

    SnowDev = await message.reply_text("Please Wait ...", reply_to_message_id=message.id)
    suffix = await db.get_suffix(message.from_user.id)
    if not suffix:
        return await SnowDev.edit("__**😔 ʏᴏᴜ ᴅᴏɴ'ᴛ ʜᴀᴠᴇ ᴀɴʏ ꜱᴜꜰꜰɪx**__")
    await db.set_suffix(message.from_user.id, None)
    await SnowDev.edit("__**❌️ ꜱᴜꜰꜰɪx ᴅᴇʟᴇᴛᴇᴅ**__")


@Client.on_message(filters.private & filters.command('see_suffix'))
async def see_csuffix(client, message):

    SnowDev = await message.reply_text("Please Wait ...", reply_to_message_id=message.id)
    suffix = await db.get_suffix(message.from_user.id)
    if suffix:
        await SnowDev.edit(f"**ʏᴏᴜʀ ꜱᴜꜰꜰɪx:-**\n\n`{suffix}`")
    else:
        await SnowDev.edit("__**😔 ʏᴏᴜ ᴅᴏɴ'ᴛ ʜᴀᴠᴇ ᴀɴʏ ꜱᴜꜰꜰɪx**__")

@Client.on_message(filters.private & filters.command('set_rep'))
async def add_rep(client, message):
    if len(message.command) < 3:
        return await message.reply_text("**__Give The Prefix__\n\nExᴀᴍᴩʟᴇ:- `/set_prefix @username`**")
    txt = message.text.split(" ", 2)
    Sydd = txt[1]
    Syddd = txt[2] if txt[2] else ''
    SyD = await message.reply_text("Please Wait ...", reply_to_message_id=message.id)
    await db.set_rep(message.from_user.id, Sydd, Syddd)
    await SyD.edit("__**ꜱᴀᴠᴇᴅ !**__")


@Client.on_message(filters.private & filters.command('del_rep'))
async def delete_rep(client, message):
    SyD = await message.reply_text("Please Wait ...", reply_to_message_id=message.id)
    dump = await db.get_rep(message.from_user.id)
    if not dump:
        return await SyD.edit("__**😔 ʏᴏᴜ ᴅᴏɴ'ᴛ ʜᴀᴠᴇ ᴀɴʏ ᴘʀᴇꜰɪx**__")
    await db.set_rep(message.from_user.id, None, None)
    await SyD.edit("__**❌️ ᴘʀᴇꜰɪx ᴅᴇʟᴇᴛᴇᴅ**__")

@Client.on_message(filters.private & filters.command('set_swap'))
async def add_swapc(client, message):
    if len(message.command) < 2:
        return await message.reply_text("Usage: `/set_swap old:new [old2:new2 ...]`", parse_mode=enums.ParseMode.MARKDOWN)

    try:
        swap_text = message.text.split(None, 1)[1]
        pairs = swap_text.split()

        saved = []
        failed = []

        for pair in pairs:
            if ':' not in pair:
                failed.append(f"`{pair}` (missing `:`)")
                continue
            old, new = pair.split(":", 1)
            await db.add_swap(message.from_user.id, old, new)
            saved.append(f"`{old}` => `{new}`")

        response = ""
        if saved:
            response += "✅ Saved Swaps:\n" + "\n".join(saved)
        if failed:
            response += "\n\n❌ Failed:\n" + "\n".join(failed)

        await message.reply(response, parse_mode=enums.ParseMode.MARKDOWN)
    except Exception as e:
        await message.reply(f"❌ Failed to process swaps.\n\nError: `{e}`", parse_mode=enums.ParseMode.MARKDOWN)

@Client.on_message(filters.command("del_swap") & filters.private)
async def delete_swap_cmd(_, message):
    if len(message.command) < 2:
        return await message.reply_text("Usage: `/del_swap key`", parse_mode=enums.ParseMode.MARKDOWN)
    
    key = message.command[1]
    await db.delete_swap(message.from_user.id, key)
    await message.reply_text(f"✅ Swap with key `{key}` deleted.", parse_mode=enums.ParseMode.MARKDOWN)

@Client.on_message(filters.command("swaps") & filters.private)
async def list_swaps(_, message):
    swaps = await db.get_swaps(message.from_user.id)
    if not swaps:
        return await message.reply_text("❌ No swaps set yet.")
    
    text = "**🔁 Your Current Swaps:**\n\n"
    text += "\n".join([f"`{k}` → `{v}`" for k, v in swaps.items()])
    await message.reply_text(text, parse_mode=enums.ParseMode.MARKDOWN)


