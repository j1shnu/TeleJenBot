import asyncio
from pyrogram import idle

from jenbot.bot import JenkinsBot


async def main():
    await JenkinsBot.start()
    await idle()


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())