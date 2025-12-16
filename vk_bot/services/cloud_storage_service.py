from io import BytesIO
from typing import BinaryIO

import aiohttp


async def upload_audio_file(binary: bytes):
    file_binary: BinaryIO = BytesIO(binary)

    upload_url = "https://ideasformuseums.com/tgbot/upload-audio/"
    async with aiohttp.ClientSession() as session:
        form = aiohttp.FormData()
        form.add_field(
            name="audio_file",
            value=file_binary,
            filename="voice.ogg",
            content_type="audio/ogg"
        )
        async with session.post(upload_url, data=form) as resp:
            upload_response = await resp.json(content_type="text/html")

            if "filename" in upload_response:
                return "https://ideasformuseums.com/tgbot/get-audio/?filename=" + upload_response["filename"]

            raise Exception(f"Error downloading audio: {upload_response}")
