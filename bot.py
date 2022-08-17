
import asyncio
import shlex
import os
from sys import stderr, stdout
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup


api_id = int(os.environ.get('API_ID', None))
api_hash = os.environ.get('API_HASH', None)
bot_token = os.environ.get('BOT_TOKEN', None)

app = Client(
    "Download:4u",
    api_id=api_id,
    api_hash=api_hash,
    bot_token=bot_token
)

if not os.path.isdir('DOWNLOADS'):
    os.makedirs('DOWNLOADS')

# Download Function
async def command_run(cmd: str):
    args = shlex.split(cmd)
    print(args)
    process = await asyncio.create_subprocess_exec(
        *args, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
    )
    stdout, stderr = await process.communicate()
    return (
        stdout.decode("utf-8", "replace").strip(),
        stderr.decode("utf-8", "replace").strip(),
        process.returncode,
        process.pid,
    )

@app.on_message(filters.private & filters.command(['start']))
async def start_handler(c:Client, m:Message):
    await m.reply_text(f"Welcome{m.from_user.mention}", quote=True)

@app.on_message(filters.private & filters.text)
async def text_handler(c:Client, m:Message):
    download_u = m.text
    if download_u:
        print(download_u)
        download_location = 'DOWNLOADS' + '/' + '_test.mp3'
        cmd = f"youtube-dl --extract-audio --audio-format mp3 {download_u} -o {download_location}"
        await command_run(cmd)
        await c.send_audio(m.chat.id, download_location)
print("Start")
app.run()
