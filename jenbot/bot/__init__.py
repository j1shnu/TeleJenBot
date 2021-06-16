from json import loads
from asyncio import sleep
from pyrogram import Client, emoji
from pyrogram.types import Message, CallbackQuery

from jenbot import Common

JenkinsBot = Client(
    session_name=Common().bot_session,
    bot_token=Common().bot_api_key,
    workers=200,
    workdir=Common().work_dir,
    config_file=Common().config_file,
)

Common = Common()


class Data:
    """This is Temporary Data Storing"""

    def __init__(self) -> None:
        self.jobs = None
        self.chat_id = None
        self.job_name = None
        self.job_params = {}
        self.authorized_chats = loads(Common.chats)
        self.password = Common.jenkins_password
        self.admin = Common.admin
        self.sleep_time = 5  # This'll increase by 2 if the current time is gt build eta. This is to avoid FLOOD WAIT.
        self.COLORS = {
            "red": emoji.RED_CIRCLE,
            "notbuilt": emoji.WHITE_CIRCLE,
            "aborted": emoji.BLACK_CIRCLE,
            "blue": emoji.BLUE_CIRCLE,
            "red_anime": f"{emoji.RED_CIRCLE}{emoji.MAN_CONSTRUCTION_WORKER}",
            "blue_anime": f"{emoji.BLUE_CIRCLE}{emoji.MAN_CONSTRUCTION_WORKER}",
        }


JenkinsData = Data()


async def delete_msg(msg: Message, time: int = 0):
    await sleep(time)
    return bool(await msg.delete())


async def alert_and_delete(msg: CallbackQuery, delete: bool = True):
    """This'll alert user and delete the bot message."""
    await msg.answer("Error Fetching Details...! Try Again.", show_alert=True)
    if delete:
        return bool(await msg.message.delete())
    return None
