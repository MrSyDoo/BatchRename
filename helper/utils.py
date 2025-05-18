import math
import time
import logging
from datetime import datetime
from pytz import timezone
from config import Config, Txt
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from pyrogram import Client
import re, aiohttp, os

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


async def metadata_text(metadata_code):
    author = None
    title = None
    video_title = None
    audio_title = None
    subtitle_title = None

    flags = [i.strip() for i in metadata_code.strip().split('--') if i.strip()]
    for f in flags:
        if f.startswith("change-author"):
            author = f[len("change-author"):].strip()
        elif f.startswith("change-title"):
            title = f[len("change-title"):].strip()
        elif f.startswith("change-video-title"):
            video_title = f[len("change-video-title"):].strip()
        elif f.startswith("change-audio-title"):
            audio_title = f[len("change-audio-title"):].strip()
        elif f.startswith("change-subtitle-title"):
            subtitle_title = f[len("change-subtitle-title"):].strip()

    return author, title, video_title, audio_title, subtitle_title

async def download_image(url, save_path):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            if resp.status == 200:
                with open(save_path, 'wb') as f:
                    f.write(await resp.read())
                return save_path
            else:
                raise Exception(f"Failed to download image, status code: {resp.status}")


    
async def start_clone_bot(UsrBot, data=None):
    await UsrBot.start()
    return UsrBot


def client(data):
    return Client("USERBOT", Config.API_ID, Config.API_HASH, session_string=data)

async def remove_path(*paths):
    for path in paths:
        if path and os.path.lexists(path):
            os.remove(path)


async def progress_for_pyrogram(current, total, ud_type, message, start):
    now = time.time()
    diff = now - start

    if round(diff % 5.00) == 0 or current == total:
        percentage = current * 100 / total
        speed = current / diff
        elapsed_time, time_to_completion, estimated_total_time = calculate_times(
            diff, current, total, speed
        )

        progress = generate_progress_bar(percentage)
        tmp = progress + Txt.PROGRESS_BAR.format(
            round(percentage, 2),
            humanbytes(current),
            humanbytes(total),
            humanbytes(speed),
            estimated_total_time if estimated_total_time != "" else "0 s",
        )

        try:
            await message.edit(text=f"{ud_type}\n\n{tmp}")
        except:
            pass


def generate_progress_bar(percentage):
    return (
        "".join(["⬢" for _ in range(math.floor(percentage / 5))])
        + "".join(["⬡" for _ in range(20 - math.floor(percentage / 5))])
    )


def calculate_times(diff, current, total, speed):
    elapsed_time = TimeFormatter(milliseconds=round(diff) * 1000)
    time_to_completion = TimeFormatter(round((total - current) / speed) * 1000)
    estimated_total_time = elapsed_time + time_to_completion
    return elapsed_time, time_to_completion, estimated_total_time


def humanbytes(size):
    if not size:
        return ""
    power = 2 ** 10
    n = 0
    Dic_powerN = {0: " ", 1: "K", 2: "M", 3: "G", 4: "T"}
    while size > power:
        size /= power
        n += 1
    return f"{round(size, 2)} {Dic_powerN[n]}ʙ"


def TimeFormatter(milliseconds: int) -> str:
    seconds, milliseconds = divmod(int(milliseconds), 1000)
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    days, hours = divmod(hours, 24)
    tmp = (
        (f"{days}ᴅ, ") if days else ""
    ) + (
        (f"{hours}ʜ, ") if hours else ""
    ) + (
        (f"{minutes}ᴍ, ") if minutes else ""
    ) + (
        (f"{seconds}ꜱ, ") if seconds else ""
    ) + (
        (f"{milliseconds}ᴍꜱ, ") if milliseconds else ""
    )
    return tmp[:-2]


def convert(seconds):
    seconds = seconds % (24 * 3600)
    hour = seconds // 3600
    seconds %= 3600
    minutes = seconds // 60
    seconds %= 60
    return "%d:%02d:%02d" % (hour, minutes, seconds)


async def send_log(b, u):
    if Config.LOG_CHANNEL is not None:
        curr = datetime.now(timezone("Asia/Kolkata"))
        date = curr.strftime("%d %B, %Y")
        time_str = curr.strftime("%I:%M:%S %p")
        await b.send_message(
            Config.LOG_CHANNEL,
            f"**--Nᴇᴡ Uꜱᴇʀ Sᴛᴀʀᴛᴇᴅ Tʜᴇ Bᴏᴛ--**\n\n"
            f"Uꜱᴇʀ: {u.mention}\nIᴅ: `{u.id}`\nUɴ: @{u.username}\n\n"
            f"Dᴀᴛᴇ: {date}\nTɪᴍᴇ: {time_str}\n\nBy: {b.mention}",
        )

def add_prefix_suffix(input_string, prefix='', suffix=''):
    pattern = r'(?P<filename>.*?)(\.\w+)?$'
    match = re.search(pattern, input_string)
    if match:
        filename = match.group('filename')
        extension = match.group(2) or ''
        if prefix == None:
            if suffix == None:
                return f"{filename}{extension}"
            return f"{filename} {suffix}{extension}"
        elif suffix == None:
            if prefix == None:
               return f"{filename}{extension}"
            return f"{prefix}{filename}{extension}"
        else:
            return f"{prefix}{filename} {suffix}{extension}"


    else:
        return input_string
