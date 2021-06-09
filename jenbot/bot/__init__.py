from json import loads
from asyncio import sleep
from pyrogram import Client, emoji
from pyrogram.types import Message

from jenbot.common import Common

JenkinsBot = Client(
    session_name=Common().bot_session,
    bot_token=Common().bot_api_key,
    workers=200,
    workdir=Common().work_dir,
    config_file=Common().config_file,
)

Common = Common()


class Data:
    """ This is Temporary Data Storing """

    def __init__(self) -> None:
        self.jobs = None
        self.chat_id = None
        self.job_name = None
        self.job_params = {}
        self.authorized_chats = loads(Common.chats)
        self.password = Common.jenkins_password
        self.admin = Common.admin
        self.sleep_time = 5  # This'll increase by 2 if the current time is gt eta. This is to avoid FLOOD WAIT.
        self.COLORS = {
            "red": emoji.RED_CIRCLE,
            "notbuilt": emoji.WHITE_CIRCLE,
            "aborted": emoji.BLACK_CIRCLE,
            "blue": emoji.BLUE_CIRCLE,
        }


JenkinsData = Data()


async def delete_msg(msg: Message, time: int):
    await sleep(time)
    return bool(await msg.delete())
