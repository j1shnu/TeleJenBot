from pyrogram import filters, emoji
from pyrogram.types import (
    Message,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)

from jenbot.bot import JenkinsBot, JenkinsData, Common, delete_msg
from jenbot.helpers.details import get_jobs, get_version, get_running_builds
from jenbot.helpers.message_template import Template


@JenkinsBot.on_message(filters.command("start"))
async def start_msg_handler(c: JenkinsBot, m: Message):
    await m.reply_text(
        text=f"Hello there! I'm **{Common.jenkins_name}**'s Jenkins BOT{emoji.ROBOT}."
        + f"\nConnected Jenkins version is `{get_version()}`"
    )


@JenkinsBot.on_message(filters.command("getid"))
async def get_id(c: JenkinsBot, m: Message):
    msg = f"Current Chat ID :  `{m.chat.id}`"
    if m.reply_to_message:
        msg = f"User ID id : `{m.reply_to_message.from_user.id}`"
    await m.reply_text(text=msg)


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
        return await delete_msg(msg, 5)


@JenkinsBot.on_message(filters.command("showbuild"))
async def show_available_jobs(c: JenkinsBot, m: Message):
    chat_info = [m.chat.id, m.chat.title or m.chat.username]
    if (
        chat_info[0] not in JenkinsData.authorized_chats
        and JenkinsData.admin not in chat_info
    ):
        return
    msg = await m.reply_text(
        f"Getting Available Running Builds..{emoji.MAGNIFYING_GLASS_TILTED_LEFT}"
    )
    try:
        builds = get_running_builds()
        if not builds:
            await msg.edit_text("No Builds are Running Now.")
        else:
            msg_text = f"Hi {m.from_user.mention}, Here are the current running Builds."
            build_text = Template.generate_builds_template(builds)
            await msg.edit_text(f"{msg_text}\n\n{build_text}")
            return await delete_msg(msg, 20)

    except Exception as e:
        await msg.edit_text(
            f"Error Fetching Current Builds..{emoji.DOUBLE_EXCLAMATION_MARK}, Try Again."
        )
    return await delete_msg(msg, 10)
