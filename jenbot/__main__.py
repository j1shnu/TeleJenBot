from pyrogram import idle
from asyncio import get_event_loop

from jenbot.bot import JenkinsBot


async def main():
    await JenkinsBot.start()
    await idle()


if __name__ == "__main__":
    loop = get_event_loop()
    loop.run_until_complete(main())
