import asyncio
from subprocess import call
from pyrogram import Client, filters
import os
import subprocess
from pyrogram.types import InlineKeyboardButton, Message, InlineKeyboardMarkup
from subprocess import call, check_output
from hachoir.metadata import extractMetadata
from hachoir.parser import createParser

app = Client(
    "Download:4u",
    api_id=4730697,
    api_hash="5b451ec5950aae4b8e914359c7975dca",
    bot_token="5518721863:AAHG0rvEPF8z8gjz2X8pL8jc_fDYL4F0cL8"
)

if not os.path.isdir('DOWNLOADS'):
    os.makedirs('DOWNLOADS')


def get_duration(filepath):
    metadata = extractMetadata(createParser(filepath))
    if metadata.has("duration"):
        return metadata.get('duration').seconds
    else:
      	return 0

def get_width_height(filepath):
    metadata = extractMetadata(createParser(filepath))
    if metadata.has("width") and metadata.has("height"):
        return metadata.get("width"), metadata.get("height")
    else:
      	return 1280, 720



@app.on_message(filters.private & filters.command(['start', 'help']))
async def start_handler(c:Client, m:Message):
    await m.reply_text(
        text=f"**Hi {m.from_user.mention} Welcome**",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(text='help', callback_data='help'),
                    InlineKeyboardButton(text='Settings', callback_data='settings')
                ]
            ]
        ),
        quote=True
    )

@app.on_message(filters.text & filters.private)
async def download_handler(c:Client, m:Message):
    m_data = m.text
    if 'aplusewings' in m_data:
        msg = await m.reply_text('**Valid Link**')

        if '|' in m_data:
            url_parts = m_data.split('|')
            download_link = url_parts[0]
            custom_file_name = url_parts[1]

        else:
            download_link = m_data
            custom_file_name = 'AJ_VIDEO'

        download_location = 'DOWNLOADS' + '/' + str(custom_file_name) + '.mp4'
        await msg.edit('**Download Strated!**')

        print('Download Process!')

        command_to_exec = [
                "youtube-dl",
                "-c",
                "-f",
                "0",
                "--hls-prefer-ffmpeg",
                download_link,
                "-o",
                download_location,
                "--no-warnings"
            ]
        process = await asyncio.create_subprocess_exec(
            *command_to_exec,
            # stdout must a pipe to be accessible as process.stdout
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        # Wait for the subprocess to finish
        stdout, stderr = await process.communicate()
        e_response = stderr.decode().strip()
        t_response = stdout.decode().strip()

        print('Gettings Duration and width and height..')
        try:
            width, height = get_width_height(download_location)
            duration = get_duration(download_location)
            if download_location:
               await m.reply_video(
                    download_location,
                    quote=True,
                    supports_streaming=True,
                    duration=duration,
                    width=width,
                    height=height
                )
        except Exception as e:
            await msg.edit(f"**{e}**")
    else:
        await m.reply_text('**Link not valid**')

print('Bot Starting!')
app.run()
