from time import sleep
from math import floor
from pyrogram import filters, emoji
from asyncio import sleep as aiosleep
from pyrogram.types import CallbackQuery
from pyrogram.errors import FloodWait, BadRequest

from jenbot.bot import JenkinsData, JenkinsBot
from jenbot.helpers import build, message_template
from jenbot.helpers.details import get_job_details, get_param_names


@JenkinsBot.on_callback_query(filters.regex("^start_build$"))
async def start_buid(c: JenkinsBot, m: CallbackQuery):
    job_name = JenkinsData.job_name
    job_params = JenkinsData.job_params
    job_details = get_job_details(jobName=job_name)
    if not job_details:
        return bool(
            await m.answer("Error Fetching Details...! Try Again.", show_alert=True)
        )
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
        await m.answer(
            "Error Fetching Details To Start The Build. Try Again..!", show_alert=True
        )
        return bool(await m.message.delete())
    build_text = f"**BUILD Started.** - [Console Log]({build_info['url']}/console)"
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
                await m.message.edit(
                    text=f"{msg_text}{build_text}\n{progressbar} {percentage}%{infoTxt}"
                )
                await aiosleep(JenkinsData.sleep_time)
            except FloodWait as e:
                sleep(e.x)
            except BadRequest as e:
                pass
        percentage_old = percentage
    else:
        build_finished = build.is_finished(job_name, build_info["build_num"])
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
        await aiosleep(2)
        await m.message.delete()
