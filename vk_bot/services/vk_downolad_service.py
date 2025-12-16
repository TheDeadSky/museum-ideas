import aiohttp


async def download_voice_audio(url: str):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                return await response.read()

            raise Exception(f"Error downloading audio: status: {response.status} | response: {await response.text()}")