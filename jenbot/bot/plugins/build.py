from math import floor
from pyrogram import filters, emoji
from asyncio import sleep as aiosleep
from contextlib import suppress as ignored
from pyrogram.errors import FloodWait, BadRequest, MessageNotModified
from pyrogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup

from jenbot import logging
from jenbot.helpers import build, message_template
from jenbot.helpers.details import get_job_details, get_param_names
from jenbot.bot import JenkinsData, JenkinsBot, delete_msg, alert_and_delete


@JenkinsBot.on_callback_query(filters.regex("^start_build$"))
async def confirm_build(c: JenkinsBot, m: CallbackQuery):
    if not JenkinsData.jobs:
        return await alert_and_delete(m)
    job_name, job_params = JenkinsData.job_name, JenkinsData.job_params
    job_details = get_job_details(jobName=job_name)
    if not job_details:
        return await alert_and_delete(m, delete=False)
    params = get_param_names(job_details["property"]) if job_details["property"] else []
    msg_text = message_template.Template.MESSAGE.format(
        job_name=job_name,
        jobURL=job_details["url"],
        color=JenkinsData.COLORS[job_details["color"]],
        lastBuildURL=job_details["lastBuild"]["url"] or None,
        description=job_details["description"] or None,
        paramNum=len(params),
    )
    msg_params = message_template.Template.generate_param_template(
        param_data=job_params
    )
    msg_text = f"{msg_text}{msg_params}\n**Do You Want To Continue With The Build?**"
    markup = [
        [
            InlineKeyboardButton(
                f"YES {emoji.CHECK_MARK_BUTTON}", callback_data="build_confirmed"
            ),
            InlineKeyboardButton(f"NO {emoji.CROSS_MARK}", callback_data="back2params"),
        ],
    ]
    await m.message.edit(text=msg_text, reply_markup=InlineKeyboardMarkup(markup))


@JenkinsBot.on_callback_query(filters.regex("^build_confirmed$"))
async def start_buid(c: JenkinsBot, m: CallbackQuery):
    if not JenkinsData.jobs:
        return await alert_and_delete(m)
    job_name = JenkinsData.job_name
    job_params = JenkinsData.job_params
    job_details = get_job_details(jobName=job_name)
    if not job_details:
        return await alert_and_delete(m, delete=False)
    params = get_param_names(job_details["property"]) if job_details["property"] else []
    msg_text = message_template.Template.MESSAGE.format(
        job_name=job_name,
        jobURL=job_details["url"],
        color=JenkinsData.COLORS[job_details["color"]],
        lastBuildURL=job_details["lastBuild"]["url"] or None,
        description=job_details["description"] or None,
        paramNum=len(params),
    )
    msg_params = message_template.Template.generate_param_template(
        param_data=job_params
    )
    msg_text = f"{msg_text}{msg_params}"
    await m.message.edit("Starting **BUILD**....")
    build_info = build.start_build(job_name, job_params)
    if not build_info:
        return await alert_and_delete(m)
    build_text = f"**BUILD Started.** - [Console Log]({build_info['url']}/console)"
    logging.info(
        f"{job_name}(Number: {build_info['build_num']}) "
        + f"build started by {m.from_user.username}({m.from_user.id})."
    )
    await m.message.edit(text=f"{msg_text}{build_text}")
    await aiosleep(3)
    percentage_old = 0
    while not build.is_finished(job_name, build_info["build_num"]):
        progressbar = "{}{}"
        eta = build.get_eta(job_name, build_info["build_num"])
        percentage = build.get_percentage(build_info["start_time"], eta)
        if percentage != percentage_old:
            progressbar = progressbar.format(
                "".join(("█" for _ in range(floor(percentage / 5)))),
                "".join(("░" for _ in range(20 - floor(percentage / 5)))),
            )
            try:
                infoTxt = "\n__(Progress bar may not be 100% accurate.)__"
                final_msg = (
                    f"{msg_text}{build_text}\n{progressbar} {percentage}%{infoTxt}"
                )
                # https://t.me/pyrogramchat/326148
                with ignored(MessageNotModified):
                    await m.message.edit(
                        text=f"{msg_text}{build_text}\n{progressbar} {percentage}%{infoTxt}"
                    )
                await aiosleep(JenkinsData.sleep_time)
            except FloodWait as e:
                logging.warning(f"Flood wait, Sleeping for {e.x} seconds.")
                aiosleep(e.x)
            except (BadRequest) as e:
                logging.error(e)
                pass
        percentage_old = percentage
    else:
        build_finished = build.is_finished(job_name, build_info["build_num"])
        logging.info(f"{job_name} build status : {build_finished}")
        if build_finished == "SUCCESS":
            msg_text = msg_text + f"**BUILD COMPLETED** {emoji.CHECK_MARK_BUTTON}"
        elif build_finished == "FAILURE":
            msg_text = msg_text + f"**BUILD FAILED** {emoji.CROSS_MARK}"
        elif build_finished == "ABORTED":
            msg_text = msg_text + f"**BUILD ABORTED** {emoji.CROSS_MARK}"
        else:
            msg_text = (
                msg_text + f"**BUILD FAILED**, Unknown Error..! {emoji.CROSS_MARK}"
            )
        final_msg = (
            "Hey {user}, Checkout the Build Result.\n\n"
            + "{msg_text}\n"
            + "[Console Log Link]({url}/console)\n\n"
        )
        await c.send_message(
            chat_id=m.message.chat.id,
            text=final_msg.format(
                user=m.from_user.mention,
                msg_text=msg_text,
                url=build_info["url"],
                smile=emoji.SMILING_FACE,
            ),
            disable_web_page_preview=True,
        )
        return await delete_msg(m.message, 1)
