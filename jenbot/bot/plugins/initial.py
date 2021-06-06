import asyncio
from pyrogram import filters, emoji
from pyrogram.types import (
    Message,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    CallbackQuery,
)

from jenbot.bot import JenkinsBot, JenkinsData, Common
from jenbot.helpers.details import get_jobs, get_version


@JenkinsBot.on_message(filters.command("start", prefixes=["/"]))
async def start_msg_handler(c: JenkinsBot, m: Message):
    await m.reply_text(
        text=f"Hello there! I'm **{Common().jenkins_name}**'s Jenkins BOT{emoji.ROBOT}.\nMy version is `{get_version()}`"
    )


@JenkinsBot.on_message(filters.command("getid", prefixes=["/"]))
async def get_id(c: JenkinsBot, m: Message):
    await m.reply_text(text=f"Your Chat ID :  `{m.chat.id}`")


@JenkinsBot.on_message(
    filters.chat(JenkinsData.authorized_chats) & filters.command("jobs", prefixes=["/"])
)
async def jobs_msg_handler(c: JenkinsBot, m: Message):
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
        asyncio.sleep(5)
        await msg.delete()


@JenkinsBot.on_message(filters.command("test", prefixes=["/"]))
async def CallbackupAlertTest(c: JenkinsBot, m: Message):
    markup = [[InlineKeyboardButton("Test", callback_data="testtest")]]
    await m.reply_text("test test", reply_markup=InlineKeyboardMarkup(markup))
    await m.delete()


@JenkinsBot.on_callback_query(filters.regex("^testtest$"))
async def test_handler(c: JenkinsBot, m: CallbackQuery):
    await m.answer(text="Holaaaaaaaa", show_alert=True)
    # await m.