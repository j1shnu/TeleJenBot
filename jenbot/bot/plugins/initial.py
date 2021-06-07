from asyncio import sleep
from typing import Union
from pyrogram import filters, emoji
from pyrogram.types import (
    Message,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)

from jenbot.bot import JenkinsBot, JenkinsData, Common
from jenbot.helpers.details import get_jobs, get_version


@JenkinsBot.on_message(filters.command("start"))
async def start_msg_handler(c: JenkinsBot, m: Message):
    await m.reply_text(
        text=f"Hello there! I'm **{Common.jenkins_name}**'s Jenkins BOT{emoji.ROBOT}."
        + f"\nMy version is `{get_version()}`"
    )


@JenkinsBot.on_message(filters.command("getid"))
async def get_id(c: JenkinsBot, m: Message):
    await m.reply_text(text=f"Current Chat ID :  `{m.chat.id}`")


@JenkinsBot.on_message(filters.command("jobs"))
async def jobs_msg_handler(c: JenkinsBot, m: Message):
    chat_info = [m.chat.id, m.chat.title or m.chat.username]
    if (
        chat_info[0] not in JenkinsData.authorized_chats
        and JenkinsData.admin not in chat_info
    ):
        return
    msg = await m.reply_text(
        f"Fetching Available Jobs...{emoji.MAGNIFYING_GLASS_TILTED_LEFT}"
    )
    try:
        jobs = get_jobs()
        JenkinsData.jobs = jobs
        jobs = [job["name"] for job in jobs]
        await msg.edit_text(
            "Available Jobs",
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            f"{id + 1}. {job}", callback_data=f"jobs_{id}"
                        )
                    ]
                    for id, job in enumerate(jobs)
                ]
            ),
        )
    except:
        await msg.edit_text(
            f"Hey {m.from_user.mention},\nError Fetching Jobs, try again..!"
        )
        await sleep(5)
        await msg.delete()